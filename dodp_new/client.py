import logging
import re
from typing import Optional

import requests
from logging import Logger
from http import HTTPStatus
from .general import DODPVersion, BASE_HEADERS, CLIENT_TIMEOUT
from .exceptions import *
from .messages import method_not_override
from .request_body import LOGOFF


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
        self._headers.update({'SOAPAction': '/logOff'})
        response_data = self._send(LOGOFF)
        if response_data is None:
            return False
        result_match = re.search(r'<ns1:logOffResult>(.*?)<', response_data, re.DOTALL)
        if result_match is None:
            return False
        return result_match.group(1) == 'true'

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
