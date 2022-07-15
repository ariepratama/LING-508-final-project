from typing import *


class DocumentResponse:
    def __init__(self, doc_id: int, summary_text: Text, text: Text, ner_spans: List[Tuple[int, int, Text]]):
        """ Response for retrieved documents.
        :param doc_id:
        :param summary_text:
        :param text:
        :param ner_spans: in form of (start, end, tag), e.g: (0, 3, "People")
        """
        self.doc_id = 0
        self.summary_text = ""
        self.text = ""
        self.ner_spans = []


class SearchNamedEntityResponse:
    def __init__(self, documents: List[DocumentResponse]):
        self.documents = documents
