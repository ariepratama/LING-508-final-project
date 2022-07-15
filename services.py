from abc import ABC, abstractmethod
from datetime import datetime
from typing import Text, List, Tuple

from models import Document, RawDocument
from repositories import WebDocumentRepositoryImpl, MysqlDocumentRepositoryImpl


class ScrapperService(ABC):
    """ A service that retrieves raw data from the web, clean it, and store the cleaned data into persistence.
    """

    @abstractmethod
    def extract(self, date: datetime) -> List[RawDocument]:
        """ Extract article data from the web.
        :param date: article date
        :return:
        """
        pass

    @abstractmethod
    def clean_html(self, raw_document: RawDocument) -> Document:
        pass

    @abstractmethod
    def store_document(self, document: Document) -> None:
        pass


class ScrapyScrapperService(ScrapperService):
    """ Scraping by using scrapy library
    """

    def __init__(self):
        self.web_document_repository = WebDocumentRepositoryImpl()
        self.db_document_repository = MysqlDocumentRepositoryImpl()

    def extract(self, date: datetime) -> List[RawDocument]:
        pass

    def clean_html(self, raw_document: RawDocument) -> Document:
        pass

    def store_document(self, document: Document) -> None:
        pass


class NERExtractionService(ABC):
    """ A component that will handle the named entity extraction
    """

    @abstractmethod
    def extract(self, doc: Document) -> List[Tuple[int, int, Text]]:
        """ extract named entities from a document.
        :param doc:
        :return: List of tuple with format: (start_span, end_span, ner_category)
        """
        pass


class StanzaNERExtractionService(NERExtractionService):
    """ NER extraction by using Stanford's stanza model
    """

    def __init__(self):
        pass

    def extract(self, doc: Document) -> List[Tuple[int, int, Text]]:
        pass


class WebService(ABC):
    @abstractmethod
    def retrieve_related_documents(self, search_term: Text) -> List[Document]:
        pass


class WebServiceImpl(WebService):
    def __init__(self):
        pass

    def retrieve_related_documents(self, search_term: Text) -> List[Document]:
        return []
