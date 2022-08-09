from typing import Text


class SearchNamedEntityRequest:
    """
        class to search NER documents.
    """

    def __init__(self, search_term: Text):
        self.search_term = search_term
