import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Text, List, Tuple

import stanza
from bs4 import BeautifulSoup

from models.models import Document, RawDocument, NERSpan
from repositories.repositories import WebDocumentRepositoryImpl, SQLDocumentRepositoryImpl, SQLNERSpanRepository


def process(is_test: bool):
    scrapper_service = ScrapyScrapperService.instance(is_test=is_test)
    ne_service = StanzaNERExtractionService.instance(is_test=is_test)

    logging.debug("extracting document from the web....")
    raw_docs: List[RawDocument] = scrapper_service.extract(date=datetime.now())

    if is_test:
        raw_docs = raw_docs[:2]

    for raw_doc in raw_docs:
        doc = scrapper_service.clean_html(raw_doc)
        logging.debug(f"storing document to persistence {raw_doc}")
        scrapper_service.store_document(doc)

        logging.debug(f"extracting ner from document={raw_doc}")
        raw_ne_spans: List[Tuple[int, int, Text]] = ne_service.extract(doc)
        ner_spans: List[NERSpan] = [
            NERSpan.of(start_span=start_span, end_span=end_span, document_id=doc.id, ner_tag=ner_tag)
            for (start_span, end_span, ner_tag)
            in raw_ne_spans
        ]
        logging.debug(f"storing ner_spans={ner_spans}")
        ne_service.store(ner_spans)


def teardown_process():
    """ clean up the process remnants after test

    :return:
    """
    scrapper_service = ScrapyScrapperService.instance(is_test=True)
    ne_service = StanzaNERExtractionService.instance(is_test=True)
    scrapper_service.empty_db()
    ne_service.empty_db()


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
    INSTANCE = None

    @staticmethod
    def instance(is_test=False):
        if not ScrapyScrapperService.INSTANCE:
            ScrapyScrapperService.INSTANCE = ScrapyScrapperService(is_test=is_test)

        return ScrapyScrapperService.INSTANCE

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
        raw_document.text = soup.getText()
        return raw_document

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

    @abstractmethod
    def store(self, ner_spans: List[NERSpan]) -> None:
        pass


class StanzaNERExtractionService(NERExtractionService):
    """ NER extraction by using Stanford's stanza model
    """

    INSTANCE = None

    @staticmethod
    def instance(lang="en", is_test=False):
        if not StanzaNERExtractionService.INSTANCE:
            StanzaNERExtractionService.INSTANCE = StanzaNERExtractionService(lang=lang, is_test=is_test)

        return StanzaNERExtractionService.INSTANCE

    def __init__(self, lang="en", is_test=False):
        self.NLP = stanza.Pipeline(lang=lang, processors="tokenize,ner")
        if is_test:
            self.ne_repo = SQLNERSpanRepository.instance(
                host="",
                database="ling_508.db",
                engine="sqlite"
            )
            return

        self.ne_repo = SQLNERSpanRepository.instance(
            host="localhost",
            database="ling_508",
            engine="mysql+pymysql",
            user="root",
            password="root"
        )

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

    def store(self, ner_spans: List[NERSpan]) -> None:
        """ Store all the ner_spans into persistence

        :param ner_spans:
        :return:
        """
        for ner_span in ner_spans:
            self.ne_repo.store(ner_span)

    def empty_db(self) -> None:
        """ Only used at tests, empty the db after running integration tests
        :return:
        """
        self.ne_repo.truncate()


class WebService(ABC):

    @abstractmethod
    def retrieve_related_ner_categories(self, search_term: str) -> List[str]:
        pass

    @abstractmethod
    def retrieve_related_documents(self, search_term: str) -> List[Document]:
        pass


class WebServiceImpl(WebService):
    INSTANCE = None

    @staticmethod
    def instance(is_test=False):
        if not WebServiceImpl.INSTANCE:
            WebServiceImpl.INSTANCE = WebServiceImpl(is_test=is_test)

        return WebServiceImpl.INSTANCE

    def __init__(self, is_test=False):
        if is_test:
            self.db_document_repository = SQLDocumentRepositoryImpl.instance(
                host="",
                database="ling_508.db",
                engine="sqlite"
            )
            self.ner_repository = SQLNERSpanRepository.instance(
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
        self.ner_repository = SQLNERSpanRepository.instance(
            host="localhost",
            database="ling_508",
            engine="mysql+pymysql",
            user="root",
            password="root"
        )

    def retrieve_related_ner_categories(self, search_term: str) -> List[str]:
        return self.ner_repository.find_related_ner_categories(search_term)

    def retrieve_related_documents(self, search_term: Text) -> List[Document]:
        doc_ids = self.ner_repository.find_document_ids_by_ner_category(search_term)
        docs = self.db_document_repository.find_by_ids(doc_ids)
        return docs
