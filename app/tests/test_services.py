import datetime
import unittest
from datetime import datetime
from unittest import mock

from app.models import Document, RawDocument
from app.services import ScrapyScrapperService

service = ScrapyScrapperService()


class ScrapyScrapperServiceTest(unittest.TestCase):

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
        cleaned_text = service.clean_html(raw_document)
        self.assertTrue(expected_text, cleaned_text)

    @mock.patch("app.tests.test_services.service.db_document_repository")
    def test_store_document(self, mock_repository):
        text = "some random text"
        doc = Document(date=datetime.now(), text=text)

        service.store_document(doc)
        self.assertTrue(mock_repository.store.called)


if __name__ == '__main__':
    unittest.main()
