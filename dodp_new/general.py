from enum import StrEnum
from typing import List, Optional

BASE_HEADERS = {
    'Content-Type': 'text/xml; charset=utf-8',
    'Accept': 'text/xml'
}

CLIENT_TIMEOUT = 5
"""Максимальное время ожидания ответа от сервера"""


class DODPVersion(StrEnum):
    V1 = 'v1'
    V201 = 'v2.0.1'
    V202 = 'v2.0.2'


LOGIN_DICT = {
    'manufacturer': 'Антон Свистов (a.svistov@ia-group.ru)',
    'model_py': 'daisy_py',
    'model_go': 'daisy_go',
    'serial': '040923',
    'version': '2023.09.04'
}


class BookListed:
    id: str
    name: str

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class BookList:
    total: int
    books: List[BookListed]

    def __init__(self, total: int):
        self.total = total
        self.books = []

    def to_dict(self):
        return {
            'total': self.total,
            'books': [book.to_dict() for book in self.books]
        }


class UrlContent:
    uri: str
    size: float

    def __init__(self, uri: str, size: float):
        self.uri = uri
        self.size = size

    def to_dict(self):
        return {
            'uri': self.uri,
            'size': self.size
        }


class LGKContent(UrlContent):
    pass


class LKFContent(UrlContent):
    pass


class BookContent:
    lgk_content: Optional[LGKContent]
    lkf_content: List[LKFContent]

    def __init__(self):
        self.lgk_content = None
        self.lkf_content = []

    def to_dict(self):
        return {
            'lgk_content': self.lgk_content.to_dict() if self.lgk_content else None,
            'lkf_content': [content.to_dict() for content in self.lkf_content]
        }
