import datetime
import unittest
from datetime import datetime
from unittest import mock

from models.models import Document, RawDocument
from services.services import ScrapyScrapperService, process, teardown_process
from services.services import StanzaNERExtractionService


class ScrapyScrapperServiceMysqlTest(unittest.TestCase):
    service = ScrapyScrapperService(is_test=False)

    def test_store(self):
        """ test store documents into mysql
        :return:
        """
        raw_documents = self.service.extract(date=datetime.now())
        for doc in raw_documents[:3]:
            self.service.store_document(doc)

    def tearDown(self) -> None:
        self.service.empty_db()


class ScrapyScrapperServiceTest(unittest.TestCase):
    service = ScrapyScrapperService(is_test=True)

    def test_clean_html(self):
        sample_html = """
        <html>
            <body>
                <p>Bon Jovi</p>
                <p>It's my life!</p>
            </body>
        </html>"""
        expected_text = """Bon Jovi
It's my life!"""
        raw_document = RawDocument(date=datetime.now(), text=sample_html)
        cleaned_text = self.service.clean_html(raw_document)
        self.assertTrue(expected_text, cleaned_text)

    @mock.patch("app.tests.test_services.ScrapyScrapperServiceTest.service.db_document_repository")
    def test_store_document(self, mock_repository):
        """ test store documents into mocked db

        :param mock_repository:
        :return:
        """
        text = "some random text"
        doc = Document(date=datetime.now(), text=text)

        self.service.store_document(doc)
        self.assertTrue(mock_repository.store.called)

    def tearDown(self) -> None:
        self.service.empty_db()


class NERExtractionServiceTest(unittest.TestCase):
    def test_extract(self):
        text = "Barrack Obama and Donald Trump have finally agreed on Equador."
        doc = Document(id=33, date=datetime.now(),
                       text=text)
        ner_tagger_service = StanzaNERExtractionService.instance()
        results = ner_tagger_service.extract(doc)
        self.assertEqual(5, len(results))
        self.assertEqual("Barrack", text[results[0][0]:results[0][1]])
        self.assertEqual("B-PERSON", results[0][2])

        self.assertEqual("Obama", text[results[1][0]:results[1][1]])
        self.assertEqual("E-PERSON", results[1][2])


class ProcessTest(unittest.TestCase):
    def test_process(self):
        process(is_test=True)

    def tearDown(self) -> None:
        teardown_process()


if __name__ == '__main__':
    unittest.main()
