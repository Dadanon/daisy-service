from typing import Optional

from dodp_new.general import Questions, BookList


def login(username: str, password: str) -> bool:
    """Войти в систему с логином и паролем"""
    ...


def logoff() -> bool:
    """Выйти из аккаунта"""
    ...


def get_search_questions() -> Optional[Questions]:
    """Получить варианты поиска"""
    ...


def get_questions(question_id: str, value: str) -> Optional[Questions]:
    """Сделать выбор и получить для него варианты поиска"""
    ...


def get_book_list(self, text: str, first_item: int = 0, last_item: int = -1) -> BookList:
    """Получить список книг"""
    ...