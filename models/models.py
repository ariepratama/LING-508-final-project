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
    """ Named entity span in a document. It describes which token, denoted by start_span and end_span, will be tagged.
    ner_tag is the full tag of a token, if it is using BIO/IOB format: B-PERSON, ner_category is the actual named entity
    tag, without any prefixes, for example PERSON
    """

    @staticmethod
    def of(start_span: int, end_span: int, document_id: int, ner_tag: str):
        ner_category = ner_tag.split("-")[-1]
        return NERSpan(
            start_span=start_span,
            end_span=end_span,
            document_id=document_id,
            ner_tag=ner_tag,
            ner_category=ner_category
        )

    def __init__(self, start_span: int, end_span: int, document_id: int, ner_tag: str, ner_category: str, id: int = -1):
        self.id = id
        self.start_span = start_span
        self.end_span = end_span
        self.document_id = document_id
        self.ner_tag = ner_tag
        self.ner_category = ner_category

    def __str__(self) -> str:
        return f"NERSpan(id={self.id}, start_span={self.start_span}, end_span={self.end_span}, document_id={self.document_id} , ner_tag={self.ner_tag})"

    def __repr__(self) -> str:
        return self.__str__()
