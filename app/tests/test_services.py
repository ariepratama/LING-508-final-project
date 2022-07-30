import datetime
import unittest
from datetime import datetime
from unittest import mock

from app.models import Document, RawDocument
from app.services import ScrapyScrapperService


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


if __name__ == '__main__':
    unittest.main()
