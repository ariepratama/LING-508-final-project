import logging
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List

from datasets import load_dataset
from sqlalchemy import MetaData, Table, Column, Integer, DateTime, Text
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

from app.models import Document, RawDocument


class DocumentRepository(ABC):
    @abstractmethod
    def retrieve(self, date: datetime) -> List[Document]:
        pass

    @abstractmethod
    def store(self, date: datetime, doc: Document) -> None:
        pass


class WebDocumentRepositoryImpl(DocumentRepository):
    """Retrieve document from the web. the text itself may contain html tags
    """
    # limiting the news dataset only for demonstration purpose
    limit = 1000

    def retrieve(self, date: datetime) -> List[RawDocument]:
        # chose validation dataset so that it will be lighter to be loaded
        multi_news_dataset = load_dataset("multi_news", split="validation")
        raw_documents = []

        for text in multi_news_dataset["document"][:self.limit]:
            raw_documents.append(RawDocument(date=date, text=text))

        return raw_documents

    def store(self, date: datetime, doc: Document) -> None:
        raise Exception("Cannot do store using WebDocumentRepositoryImpl")


class SQLDocumentRepositoryImpl(DocumentRepository):
    INSTANCES = {}

    @staticmethod
    def instance(host: str = "localhost", database: str = "ling_508", engine: str = "mysql",
                 user: str = None, password: str = None):
        """ initiate and return singleton instance of SQLDocumentRepositoryImpl. Prefer to use this static method
        compared to initiating by yourselves.

        :param engine:
        :param host:
        :type database:
        :return:
        """
        if engine in SQLDocumentRepositoryImpl.INSTANCES:
            return SQLDocumentRepositoryImpl.INSTANCES[engine]
        repository = SQLDocumentRepositoryImpl()
        conn_str = f"{engine}://{host}/{database}"
        if user is not None and password is not None:
            conn_str = f"{engine}://{user}:{password}@{host}/{database}"
        repository.db_init(conn_str)
        return repository

    db_engine = None
    db_conn = None
    metadata = MetaData()
    documents = Table("documents", metadata,
                      Column("id", Integer(), primary_key=True, autoincrement="ignore_fk"),
                      Column("date", DateTime(), index=True),
                      Column("text", Text()))

    def db_init(self, connection_str):
        """ initiate db connection. This method must be called after constructing this object

        :param connection_str:
        :return:
        """
        self.db_engine = create_engine(connection_str)
        self.metadata.create_all(self.db_engine)
        self.db_conn = self.db_engine.connect()

    def retrieve(self, date: datetime) -> List[Document]:
        """ retrieve

        :param date:
        :return:
        """
        date = date.date()
        query = self.documents.select().where(
            self.documents.c.date >= date,
            self.documents.c.date <= date + timedelta(days=1)
        )
        results = self.db_conn.execute(query).fetchall()
        results = [
            Document(**row) for row in results
        ]
        return results

    def store(self, date: datetime, doc: Document) -> None:
        """ Insert single document into persistence

        :param date:
        :param doc:
        :return:
        """
        transaction = self.db_conn.begin()

        try:
            query = self.documents.insert().values(
                date=doc.date,
                text=doc.text
            )
            self.db_conn.execute(query)
            transaction.commit()
        except IntegrityError as ie:
            transaction.rollback()
            logging.warning(f"failed to execute transaction, rolling back {ie}")

    def truncate(self) -> None:
        """ delete all data in the db without deleting the table, use this only for testing purpose

        :return:
        """
        transaction = self.db_conn.begin()
        try:
            query = self.documents.delete()
            self.db_conn.execute(query)
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            logging.warning(f"failed to truncate documents table, rolling back {e}")
