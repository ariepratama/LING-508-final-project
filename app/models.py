from datetime import datetime
from typing import Text


class Document:
    """ general document representation

    """

    def __init__(self, date: datetime, text: Text):
        self.date = None
        self.text = None


class RawDocument(Document):
    """ Unprocessed document from the web
    """

    def __init__(self, date: datetime, text: Text):
        super.__init__(date, text)
