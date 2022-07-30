import datetime
import unittest
from datetime import datetime

from app.models import Document
from app.repositories import SQLDocumentRepositoryImpl, WebDocumentRepositoryImpl


class WebDocumentRepositoryImplTest(unittest.TestCase):
    repo = WebDocumentRepositoryImpl()

    def test_retrieve(self):
        raw_documents = self.repo.retrieve(date=datetime.now())
        self.assertEqual(self.repo.limit, len(raw_documents))


class SQLLiteDocumentRepositoryImplTest(unittest.TestCase):
    repo = SQLDocumentRepositoryImpl.instance(engine="sqlite", host="", database="ling_508.db")

    def test_retrieve(self):
        text_1 = "document 1"
        text_2 = "document 2"
        doc_1 = Document(date=datetime.now(), text=text_1)
        doc_2 = Document(date=datetime.now(), text=text_2)
        self.repo.store(doc_1.date, doc_1)
        self.repo.store(doc_2.date, doc_2)

        results = self.repo.retrieve(doc_1.date)
        self.assertEqual(2, len(results))
        self.assertTrue(isinstance(results[0], Document))

    def test_store(self):
        doc = Document(date=datetime.now(), text="some random text is here")

        self.repo.store(doc.date, doc)
        results = self.repo.retrieve(doc.date)
        self.assertEqual(1, len(results))

    def tearDown(self) -> None:
        self.repo.truncate()


if __name__ == '__main__':
    unittest.main()
