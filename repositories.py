from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from models import Document, RawDocument


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


class MysqlDocumentRepositoryImpl(DocumentRepository):

    def retrieve(self, date: datetime) -> List[Document]:
        pass

    def store(self, date: datetime, doc: Document) -> None:
        pass
