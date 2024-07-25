from enum import StrEnum
from typing import List, Optional

BASE_HEADERS = {
    'Content-Type': 'text/xml; charset=utf-8',
    'Accept': 'text/xml'
}

CLIENT_TIMEOUT = 5
"""Максимальное время ожидания ответа от сервера"""


class SOAPAction(StrEnum):
    LOGOFF = '/logOff'
    USER_RESPONSES = '/userResponses'
    GET_CONTENT_LIST = '/getContentList'
    GET_SERVICE_ATTRIBUTES = '/getServiceAttributes'
    SET_READING_SYSTEM_ATTRIBUTES = '/setReadingSystemAttributes'
    LOGON = '/logOn'
    GET_CONTENT_RESOURCES = '/getContentResources'


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


class InputType(StrEnum):
    """
    Класс, показывающий возможные модели ввода - цифры, цифры и числа, аудио
    """
    TEXT_NUMERIC = 'TEXT_NUMERIC'
    TEXT_ALPHANUMERIC = 'TEXT_ALPHANUMERIC'
    AUDIO = 'AUDIO'


class Label:
    """
    Функциональное наименование
    """
    text: str
    audio_path: Optional[str]

    def __init__(self, text: str, audio_path: Optional[str] = None):
        self.text = text
        self.audio_path = audio_path

    def to_dict(self):
        return {
            'text': self.text,
            'audio_path': self.audio_path
        }


class InputQuestion:
    """
    Класс, являющийся конечной точкой для userResponses.
    Имеет уникальный id и текст описания вопроса (находится в теге label)
    """
    id: str
    label: Label
    input_types: List[InputType]

    def __init__(self, id: str, label: Label, input_types: List[InputType]):
        self.id = id
        self.label = label
        self.input_types = input_types

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label.to_dict(),
            'input_types': [input_type.value for input_type in self.input_types]
        }


class Choice:
    """
    Класс, предоставляющий выбор для multipleChoiceQuestion.
    Имеет уникальный id и текст описания выбора (находится в теге label -> text).
    Также необходимо указывать родительский id для получения ответа
    """
    parent_id: str
    id: str
    label: Label

    def __init__(self, parent_id: str, id: str, label: Label):
        self.parent_id = parent_id
        self.id = id
        self.label = label

    def to_dict(self):
        return {
            'parent_id': self.parent_id,
            'id': self.id,
            'label': self.label.to_dict()
        }


class MultipleChoiceQuestion:
    """
    Класс, предоставляющий пользователю возможность выбора между
    различными опциями. Имеет уникальный id, являющийся parent_id
    для его choices и текст заголовка. Пример:
    Заголовок: что вы хотите выбрать?
    Choices: [первое, второе]
    """
    id: str
    label: Label
    choices: List[Choice]

    def __init__(self, id: str, label: Label, choices: List[Choice]):
        self.id = id
        self.label = label
        self.choices = choices

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label.to_dict(),
            'choices': [choice.to_dict() for choice in self.choices]
        }


class Questions:
    """
    Общий класс ответа на userResponses. Может содержать один/несколько
    inputQuestion и/или один/несколько multipleChoiceQuestion или
    идентификатор контент листа (contentListRef) или label (простой текст)
    """
    content_list_ref: Optional[str]
    label: Optional[Label]
    input_questions: List[InputQuestion]
    multiple_choice_questions: List[MultipleChoiceQuestion]

    def __init__(self, content_list_ref: Optional[str] = None, label: Optional[Label] = None, input_questions: List[InputQuestion] = [], multiple_choice_questions: List[MultipleChoiceQuestion] = []):
        self.content_list_ref = content_list_ref
        self.label = label
        self.input_questions = input_questions
        self.multiple_choice_questions = multiple_choice_questions

    def to_dict(self):
        return {
            'content_list_ref': self.content_list_ref,
            'label': self.label.to_dict() if self.label else None,
            'input_questions': [input_question.to_dict() for input_question in self.input_questions],
            'multiple_choice_questions': [multiple_choice_question.to_dict() for multiple_choice_question in self.multiple_choice_questions]
        }
