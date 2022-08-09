import datetime
import unittest
from datetime import datetime

from models.models import Document, NERSpan
from repositories.repositories import SQLDocumentRepositoryImpl, WebDocumentRepositoryImpl, SQLNERSpanRepository


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


class SQLLiteNERSpanRepositoryImplTest(unittest.TestCase):
    doc_repo = SQLDocumentRepositoryImpl.instance(engine="sqlite", host="", database="ling_508.db")
    repo = SQLNERSpanRepository.instance(engine="sqlite", host="", database="ling_508.db")

    def test_store(self):
        doc = Document(date=datetime.now(), text="Miley Cirus is here")
        self.doc_repo.store(doc.date, doc)

        ner_span1 = NERSpan.of(document_id=doc.id, start_span=0, end_span=4, ner_tag="B-PERSON")
        self.repo.store(ner_span1)

    def test_find_by_ner_category(self):
        doc = Document(date=datetime.now(), text="Miley Cirus is here")
        self.doc_repo.store(doc.date, doc)

        ner_span1 = NERSpan.of(document_id=doc.id, start_span=0, end_span=4, ner_tag="B-PERSON")
        self.repo.store(ner_span1)

        ner_span2 = NERSpan.of(document_id=doc.id, start_span=5, end_span=10, ner_tag="E-PERSON")
        self.repo.store(ner_span2)

        ner_spans = self.repo.find_by_ner_category("PERSON")
        self.assertEqual(2, len(ner_spans))
        self.assertEqual(ner_span1.start_span, ner_spans[0].start_span)
        self.assertEqual(ner_span2.end_span, ner_spans[1].end_span)

    def tearDown(self) -> None:
        self.doc_repo.truncate()
        self.repo.truncate()


if __name__ == '__main__':
    unittest.main()
