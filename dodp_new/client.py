import logging

import requests
from logging import Logger
from http import HTTPStatus

from .functions import *
from .request_body import *
from .general import *
from .exceptions import *


class DODPClient:
    _headers: dict  # Заголовки, используемые в теле запроса
    _version: DODPVersion  # Версия DODP
    _url: str  # Адрес сервера электронных библиотек
    _logger: Logger  # Сборщик данных об ошибках
    # Список важных параметров сервера
    _supportsServerSideBack: bool
    _supportsSearch: bool

    def __init__(self, url: str):
        self._headers = BASE_HEADERS
        self._url = url
        # Logger settings
        logger_name = f'dodpclient_{self._version}'
        self._logger = Logger(logger_name, logging.DEBUG)
        handler = logging.FileHandler(f"{logger_name}.log", mode='w')
        formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        # Установка важных параметров сервера по умолчанию
        self._supportsServerSideBack = False
        self._supportsSearch = False

    @property
    def version(self):
        return self._version

    def _update_soap_action(self, action: SOAPAction):
        self._headers.update({'SOAPAction': action})

    def _send(self, body: str) -> Optional[str]:
        """
        Общий метод для отправки запроса на сервер электронных
        библиотек (например, av3715.ru).
        :param body: Тело запроса для отправки на сервер
        :return: Строка ответа
        """
        try:
            data = body.encode('utf-8')
            response = requests.post(self._url, data=data, headers=self._headers, timeout=CLIENT_TIMEOUT)
            if response.status_code != HTTPStatus.OK:
                error_message = f'error status code: {response.status_code}, reason: {response.reason}, text: {response.text}'
                self._logger.error(f'Server request error, url: {self._url}, message: {error_message}')
                return None
            cookie = response.headers.get('set-cookie')
            if cookie is not None:
                self._headers.update({'Cookie': cookie})
            return response.text
        except requests.exceptions.Timeout:
            self._logger.error('Automatic timeout interval expired')
        except requests.exceptions.SSLError:
            self._logger.error('Automatic SSL error')

    def _get_response_data(self, body: str, method_name: str, soap_action: SOAPAction, **kwargs) -> Optional[str]:
        log_message = f'Calling {method_name}'
        if kwargs:
            log_message += ' with '
            args_messages = [f'{k}: {v}' for k, v in kwargs.items()]
            log_message += ', '.join(args_messages)
        self._logger.debug(log_message)
        self._update_soap_action(soap_action)
        response_data = self._send(body)
        if response_data is None:
            self._logger.error(f'Null response on calling {method_name} with version {self._version}')
            return None
        # print(f'Response data in _get_response_data:\n{response_data}')
        return response_data

    def _get_book_content(self, book_id: str, body: str) -> Optional[BookContent]:
        response_data = self._get_response_data(body, '_get_book_content', SOAPAction.GET_CONTENT_RESOURCES)
        result = get_book_content_object(book_id, response_data)
        match result:
            case Ok(book_content):
                return book_content
            case Err(error_message):
                self._logger.error(error_message)
                return None

    def login(self, username: str, password: str):
        """
        Подключиться к серверу электронных библиотек со своим аккаунтом.
        Реализация метода отличается в разных версиях протокола
        """
        self._logger.error(method_not_override('login'))
        raise NotOverrideError('login')

    def logoff(self) -> bool:
        """Выйти из аккаунта на сервере электронных библиотек"""
        response_data = self._get_response_data(LOGOFF_BODY, 'logoff', SOAPAction.LOGOFF)
        if response_data is None:
            return False
        log_off_result_tag = get_tag_info_by_params('logOffResult', response_data)
        if not log_off_result_tag:
            self._logger.error('logOffResult is not found in server response')
            return False
        if log_off_result_tag.content != 'true':
            self._logger.error('logOffResult is False')
            return False
        return True

    def get_questions(self, question_id: str, value: str) -> Optional[Questions]:
        request_body = GET_QUESTIONS_BODY % (question_id, value)
        response_data = self._get_response_data(request_body, 'get_questions', SOAPAction.USER_RESPONSES, question_id=question_id, value=value)
        # print(f'Response data:\n{response_data}')
        if response_data is None:
            return None
        questions: Questions = get_questions_object(response_data)
        if not questions:
            self._logger.error('No questions tag found in response while calling get_questions')
            return None

        return questions

    def get_search_questions(self) -> Optional[Questions]:
        """Метод, необходимый для получения объекта Questions при search запросе"""
        response_data = self._get_response_data(SEARCH_BODY, 'get_search_questions', SOAPAction.USER_RESPONSES)
        if response_data is None:
            return None
        questions: Optional[Questions] = get_questions_object(response_data)
        if questions is None:
            self._logger.error('No questions tag found in response while calling get_search_questions')
            return None
        return questions

    def get_content_list(self, content_list_id: str, first_item: int = 0, last_item: int = -1) -> Optional[BookList]:
        request_body = GET_CONTENT_LIST_BODY % (content_list_id, first_item, last_item)
        response_data = self._get_response_data(request_body, 'get_content_list', SOAPAction.GET_CONTENT_LIST, content_list_id=content_list_id, first_item=first_item, last_item=last_item)
        if response_data is None:
            return None
        content_list_tag: TagInfo = get_tag_info_by_params('contentList', response_data)
        if not content_list_tag:
            self._logger.error('No content list tag found in response')
            return None
        cl_total: int = int(content_list_tag.params.get('totalItems'))
        cl_label_tag: TagInfo = get_root_tag_info('label', content_list_tag.content)
        if not cl_label_tag:
            self._logger.error('No label tag found in content list')
            return None
        cl_label: Label = get_label(cl_label_tag)
        if not cl_label:
            self._logger.error('Not all label fields present in content list')
            return None
        book_list: BookList = BookList(total=cl_total, label=cl_label)
        book_tags: List[TagInfo] = get_tag_info_list_by_params('contentItem', content_list_tag.content)
        for book_tag in book_tags:
            book_id: str = book_tag.params.get('id')
            book_label: Label = get_label(book_tag.content)
            if book_label:
                book_listed: BookListed = BookListed(id=book_id, label=book_label)
                book_list.books.append(book_listed)
        return book_list

    def get_book_content(self, book_id: str):
        self._logger.error(method_not_override('get_book_content'))
        raise NotOverrideError('get_book_content')

    # INFO: end block -------------------------------------------------------------------------------------------------
