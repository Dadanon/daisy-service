from enum import StrEnum
from typing import List, Optional, Dict

from dodp_new.common_functions import get_normalized

BASE_HEADERS = {
    'Content-Type': 'text/xml; charset=utf-8',
    'Accept': 'text/xml'
}

CLIENT_TIMEOUT = 5
"""Максимальное время ожидания ответа от сервера"""


class TagInfo:
    """Основной класс, хранящий информацию о тегах"""
    name: str  # Название тега
    params: Dict[str, str]  # Словарь с параметрами тега
    __content: Optional[str]  # Содержимое тега, может хранить в себе другие нераспаршенные теги

    def __init__(self, name: str, params: Dict[str, str] = {}, content: Optional[str] = None):
        self.name = name
        self.params = params
        self.__content = get_normalized(content)

    def to_dict(self):
        return {
            'name': self.name,
            'params': self.params,
            'content': self.content
        }

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = get_normalized(content)


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


class AudioContent:
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


class LGKContent(AudioContent):
    pass


class LKFContent(AudioContent):
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


class Label:
    """
    Функциональное наименование
    """
    text: str
    audio: Optional[AudioContent]

    def __init__(self, text: str, audio: Optional[AudioContent] = None):
        self.text = text
        self.audio = audio

    def to_dict(self):
        return {
            'text': self.text,
            'audio': self.audio.to_dict() if self.audio else None
        }


class InputQuestion:
    """
    Класс, являющийся конечной точкой для userResponses.
    Имеет уникальный id и текст описания вопроса (находится в теге label)
    """
    id: str
    label: Label
    input_types: List[str]

    def __init__(self, id: str, label: Label, input_types: List[str]):
        self.id = id
        self.label = label
        self.input_types = input_types

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label.to_dict(),
            'input_types': self.input_types
        }


class Choice:
    """
    Класс, предоставляющий выбор для multipleChoiceQuestion.
    Имеет уникальный id и текст описания выбора (находится в теге label -> text).
    Родительский id для получения ответа - это id MultipleChoiceQuestion, в котором
    находится данный объект Choice
    """
    id: str
    label: Label

    def __init__(self, id: str, label: Label):
        self.id = id
        self.label = label

    def to_dict(self):
        return {
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

    def __init__(self):
        self.content_list_ref = None
        self.label = None
        self.input_questions = []
        self.multiple_choice_questions = []

    def to_dict(self):
        return {
            'content_list_ref': self.content_list_ref,
            'label': self.label.to_dict() if self.label else None,
            'input_questions': [input_question.to_dict() for input_question in self.input_questions],
            'multiple_choice_questions': [multiple_choice_question.to_dict() for multiple_choice_question in self.multiple_choice_questions]
        }


class BookListed:
    id: str
    label: Label

    def __init__(self, id: str, label: Label):
        self.id = id
        self.label = label

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label.to_dict()
        }


class BookList:
    total: int
    label: Label
    books: List[BookListed]

    def __init__(self, total: int, label: Label):
        self.total = total
        self.label = label
        self.books = []

    def to_dict(self):
        return {
            'total': self.total,
            'label': self.label.to_dict(),
            'books': [book.to_dict() for book in self.books]
        }


# class InnerOperation(StrEnum):
#     """Внутренний класс для соотнесения всех возможных операций
#     с соответствующим телом запроса в зависимости от версии"""
#     LOGOFF = LOGOFF_BODY
#     SEARCH = SEARCH_BODY
#     GET_CONTENT_LIST_ID = GET_CONTENT_LIST_ID_BODY
#     GET_BOOKS_LIST = GET_BOOKS_LIST_BODY
#
#     LOGON_V1 = LOGON_BODY_V1
#     GET_SERVICE_ATTRIBUTES = GETSA_BODY
#     SET_READING_SYSTEM_ATTRIBUTES = SETRSA_BODY
#     GET_CONTENT_RESOURCES_V1 = GETCR_BODY_V1
#
#     LOGON_V2 = LOGON_BODY_V2
#     GET_CONTENT_RESOURCES_V2 = GETCR_BODY_V2
#
#
# class Operation(IntEnum):
#     """Публичные операции, вызываемые пользователем"""
#     LOGOFF = 0
#     LOGON = 1
#
#
#
# BODY_DICT = {
#
# }
# """Общий словарь, соотносит"""
