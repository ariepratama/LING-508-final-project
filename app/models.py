from datetime import datetime
from typing import Text


class Document:
    """ general document representation
    """

    def __init__(self, date: datetime, text: Text, id: int = None):
        """

        :param date:
        :param text:
        :param id: if None, then it was not persisted from db
        """
        self.id = id
        self.date = date
        self.text = text

    def __str__(self) -> str:
        return f"Document(id={self.id}, date={self.date}, text={self.text})"

    def __repr__(self) -> str:
        return self.__str__()


class RawDocument(Document):
    """ Unprocessed document from the web
    """

    def __init__(self, date: datetime, text: Text):
        super(RawDocument, self).__init__(date, text)


class NERSpan:
    def __init__(self, id: int, start_span: int, end_span: int, document_id: int, ner_tag: str, ner_category: str):
        self.id = id
        self.start_span = start_span
        self.end_span = end_span
        self.document_id = document_id
        self.ner_tag = ner_tag
        self.ner_category = ner_category
