from typing import Optional

from dodp_new.general import Questions, BookList


def login(username: str, password: str) -> bool:
    """����� � ������� � ������� � �������"""
    ...


def logoff() -> bool:
    """����� �� ��������"""
    ...


def get_search_questions() -> Optional[Questions]:
    """�������� �������� ������"""
    ...


def get_questions(question_id: str, value: str) -> Optional[Questions]:
    """������� ����� � �������� ��� ���� �������� ������"""
    ...


def get_book_list(self, text: str, first_item: int = 0, last_item: int = -1) -> BookList:
    """�������� ������ ����"""
    ...