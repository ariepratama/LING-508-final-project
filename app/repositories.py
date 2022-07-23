from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from sqlalchemy import MetaData, Table, Column, Integer, DateTime, String
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

from models import Document, RawDocument
import logging


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

    def retrieve(self, date: datetime) -> List[RawDocument]:
        pass

    def store(self, date: datetime, doc: Document) -> None:
        raise Exception("Cannot do store using WebDocumentRepositoryImpl")


class SQLDocumentRepositoryImpl(DocumentRepository):
    INSTANCE = None

    @staticmethod
    def instance(host: str, database: str):
        """ initiate and return singleton instance of MysqlRepository. Prefer to use this static method
        compared to initiating by yourselves

        :param host:
        :type database:
        :return:
        """
        if SQLDocumentRepositoryImpl.INSTANCE is not None:
            return SQLDocumentRepositoryImpl.INSTANCE
        repository = SQLDocumentRepositoryImpl(host=host, database=database)
        return repository

    db_engine = None
    db_conn = None
    metadata = MetaData()
    documents = Table("documents", metadata,
                      Column("id", Integer(), primary_key=True, autoincrement="ignore_fk"),
                      Column("date", DateTime(), index=True),
                      Column("text", String()))

    def db_init(self, connection_str):
        self.db_engine = create_engine(connection_str)
        self.metadata.create_all(self.db_engine)
        self.db_conn = self.db_engine.connect()

    def retrieve(self, date: datetime) -> List[Document]:
        query = self.documents.select([self.documents]).where(self.documents.date == date)
        results = self.db_conn.execute(query).fetchall()
        print(results)
        pass

    def store(self, date: datetime, doc: Document) -> None:
        transaction = self.db_conn.begin()

        try:
            self.documents.insert().values(
                date=doc.date,
                text=doc.text
            )
            transaction.commit()
        except IntegrityError as ie:
            transaction.rollback()
            logging.warning(f"failed to execute transaction, rolling back {ie}")
        pass
