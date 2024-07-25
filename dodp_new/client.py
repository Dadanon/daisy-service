import logging
import re
from typing import Optional, Self, List, Tuple

import requests
from logging import Logger
from http import HTTPStatus
from .general import DODPVersion, BASE_HEADERS, CLIENT_TIMEOUT, BookList, BookListed, BookContent, SOAPAction, \
    LGKContent, LKFContent, Questions
from .exceptions import *
from .messages import method_not_override
from .request_body import *


class DODPClient:
    _headers: dict  # Заголовки, используемые в теле запроса
    _version: DODPVersion  # Версия DODP
    _url: str  # Адрес сервера электронных библиотек
    _search_id: Optional[str]  # Идентификатор для поиска
    _logger: Logger  # Сборщик данных об ошибках
    # Список важных параметров сервера
    _supportsServerSideBack: bool
    _supportsSearch: bool

    def __init__(self, url: str):
        self._headers = BASE_HEADERS
        self._url = url
        self._search_id = None
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

    def _update_soap_action(self, action: SOAPAction):
        self._headers.update({'SOAPAction': action})

    def _get_book_content(self, book_id: str, body: str) -> Optional[BookContent]:
        self._logger.debug(f'Calling get_book_content with {book_id}, daisy version: {self._version}')
        self._update_soap_action(SOAPAction.GET_CONTENT_RESOURCES)
        response_data = self._send(body)
        if response_data is None:
            self._logger.error(f'No response while calling _get_book_content with version {self._version}')
            return None
        book_content: BookContent = BookContent()
        lgk_match = re.search(r'<ns1:resource .*?mimeType="application/lgk".*?/>', response_data, re.DOTALL)
        if not lgk_match:
            self._logger.error(f'LGK block not found in book content resources with id: {book_id}')
        lgk_str = lgk_match.group(0)
        lgk_uri = re.search(r'uri="(.*?)"', lgk_str).group(1)
        lgk_size = float(re.search(r'size="(.*?)"', lgk_str).group(1))
        lgk_content: LGKContent = LGKContent(lgk_uri, lgk_size)
        book_content.lgk_content = lgk_content
        lkf_matches = re.finditer(r'<ns1:resource[^>]*?mimeType="audio/x-lkf"[^>]*?/>', response_data, re.DOTALL)
        for lkf_match in lkf_matches:
            lkf_str = lkf_match.group(0)
            lkf_uri = re.search(r'uri="(.*?)"', lkf_str).group(1)
            lkf_size = float(re.search(r'size="(.*?)"', lkf_str).group(1))
            lkf_content: LKFContent = LKFContent(lkf_uri, lkf_size)
            book_content.lkf_content.append(lkf_content)
        return book_content

    @property
    def version(self):
        return self._version

    def set_search_id(self, search_id: str):
        if not self._search_id:
            self._search_id = search_id

    def login(self, username: str, password: str):
        """
        Подключиться к серверу электронных библиотек со своим аккаунтом.
        Реализация метода отличается в разных версиях протокола
        """
        self._logger.error(method_not_override('login'))
        raise NotOverrideError('login')

    def logoff(self) -> bool:
        """
        Выйти из аккаунта на сервере электронных библиотек
        """
        self._logger.debug('Calling logoff')
        self._update_soap_action(SOAPAction.LOGOFF)
        response_data = self._send(LOGOFF_BODY)
        if response_data is None:
            self._logger.error('Null response on calling logoff')
            return False
        result_match = re.search(r'<ns1:logOffResult>true<', response_data, re.DOTALL)
        if result_match is None:
            self._logger.error('logOffResult is not found in server response or is False')
            return False
        return True

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

    def __get_questions_response(self, response_data: str) -> Optional[Questions]:
        """Ответ на userResponses с id = search может быть в стиле
        inputQuestion или multipleChoiceQuestion или микс с
        inputQuestion и multipleChoiceQuestion.
        По сути возвращается объект Questions, из которого мы получаем всю информацию
        или None, если ен найден тег ns1:questions"""
        questions_body_match = re.search()


    def get_search_id(self) -> Optional[str]:
        """
        Метод, необходимый для получения нужного id при запросах
        """
        self._logger.debug('Calling _search')
        self._update_soap_action(SOAPAction.USER_RESPONSES)
        response_data = self._send(SEARCH_BODY)
        if response_data is None:
            self._logger.error('Null response on calling search')
            return None
        search_id_match = re.search(r'ns1:inputQuestion id="(.*?)">', response_data, re.DOTALL)
        print(response_data)
        if search_id_match is None:
            self._logger.error('inputQuestion id is not found in server response')
            return None
        return search_id_match.group(1)

    def _get_content_list_id(self, text: str) -> Optional[str]:
        """
        Получить идентификатор контент листа
        :param search_id: идентификатор поиска, уникальный для каждой электронной библиотеки
        :param text: текст, являющийся частью названия книги, автора
        :return: content list id as string
        """
        self._logger.debug('Calling _get_content_list_id')
        content_list_id_body = GET_CONTENT_LIST_ID_BODY % (self._search_id, text)
        response_data = self._send(content_list_id_body)
        if response_data is None:
            self._logger.error('Null response on calling _get_content_list_id')
            return None
        content_list_ref_match = re.search(r'<contentListRef>(.*?)</contentListRef>', response_data, re.DOTALL)
        if content_list_ref_match is None:
            self._logger.error('contentListRef is not found in server response')
            return None
        return content_list_ref_match.group(1)

    def _get_book_list(self, content_list_id: str, first_item: int = 0, last_item: int = -1) -> BookList:
        """
        Получить список книг (срез списка от first_item до last_item)
        :param content_list_id: идентификатор контент листа
        :param first_item: индекс первого элемента в подсписке
        :param last_item: индекс последнего элемента в подсписке
        :return: список книг с общим их числом
        """
        book_list = BookList(total=0)
        self._logger.debug('Calling _get_book_list')
        self._update_soap_action(SOAPAction.GET_CONTENT_LIST)
        books_list_body = GET_BOOKS_LIST_BODY % (content_list_id, first_item, last_item)
        response_data = self._send(books_list_body)
        if response_data is None:
            self._logger.error('Null response on calling _get_books_list')
            return book_list
        total_match = re.search(r'<ns1:contentList totalItems="(.*?)"', response_data, re.DOTALL)
        if total_match is None:
            self._logger.error('No total count found in server response')
        else:
            book_list.total = int(total_match.group(1))
        content_items_iter = re.finditer(r'<ns1:contentItem id="(.*?)">.*?<ns1:text>(.*?)<', response_data, re.DOTALL)
        for content_item in content_items_iter:
            book_listed = BookListed(id=content_item.group(1), name=content_item.group(2))
            book_list.books.append(book_listed)
        return book_list

    # INFO: public methods block --------------------------------------------------------------------------------------
    def get_book_list(self, text: str, first_item: int = 0, last_item: int = -1) -> BookList:
        self._logger.debug(f'Public method calling: get_book_list with text: {text}')
        content_list_id = self._get_content_list_id(text)
        if content_list_id is None:
            return []
        book_list = self._get_book_list(content_list_id, first_item, last_item)
        return book_list

    def get_book_content(self, book_id: str):
        self._logger.error(method_not_override('get_book_content'))
        raise NotOverrideError('get_book_content')

    # INFO: end block -------------------------------------------------------------------------------------------------
