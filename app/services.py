from abc import ABC, abstractmethod
from datetime import datetime
from typing import Text, List, Tuple

import stanza
from bs4 import BeautifulSoup

from app.models import Document, RawDocument
from app.repositories import WebDocumentRepositoryImpl, SQLDocumentRepositoryImpl


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

    def __init__(self, is_test=False):
        self.web_document_repository = WebDocumentRepositoryImpl()
        if is_test:
            self.db_document_repository = SQLDocumentRepositoryImpl.instance(
                host="",
                database="ling_508.db",
                engine="sqlite"
            )
            return

        self.db_document_repository = SQLDocumentRepositoryImpl.instance(
            host="localhost",
            database="ling_508",
            engine="mysql+pymysql",
            user="root",
            password="root"
        )

    def extract(self, date: datetime) -> List[RawDocument]:
        return self.web_document_repository.retrieve(date=date)

    def clean_html(self, raw_document: RawDocument) -> Document:
        soup = BeautifulSoup(raw_document.text, "html.parser")
        return soup.getText()

    def store_document(self, document: Document) -> None:
        self.db_document_repository.store(document.date, document)

    def empty_db(self) -> None:
        """ Only used at tests, empty the db after running integration tests
        :return:
        """
        self.db_document_repository.truncate()


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

    INSTANCE = None

    @staticmethod
    def instance():
        if not StanzaNERExtractionService.INSTANCE:
            StanzaNERExtractionService.INSTANCE = StanzaNERExtractionService()

        return StanzaNERExtractionService.INSTANCE

    def __init__(self, lang="en"):
        self.NLP = stanza.Pipeline(lang=lang, processors="tokenize,ner")

    def extract(self, doc: Document) -> List[Tuple[int, int, Text]]:
        parsed_doc = self.NLP(doc.text)
        results: List[Tuple[int, int, Text]] = []
        for sentence in parsed_doc.sentences:
            for token in sentence.tokens:
                if token.ner != "O":
                    results.append((
                        token.start_char,
                        token.end_char,
                        token.ner
                    ))
        return results


class WebService(ABC):
    @abstractmethod
    def retrieve_related_documents(self, search_term: Text) -> List[Document]:
        pass


class WebServiceImpl(WebService):
    def __init__(self):
        pass

    def retrieve_related_documents(self, search_term: Text) -> List[Document]:
        return []
