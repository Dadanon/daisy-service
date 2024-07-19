import re
from typing import Optional

from .general import DODPVersion
from .client import DODPClient
from .request_body_v1 import LOGON, SETRSA, GETSA


class DODPClientV1(DODPClient):
    def __init__(self, url: str):
        self._version = DODPVersion.V1
        super().__init__(url)

    def __get_service_attributes(self) -> Optional[str]:
        """
        Получить список возможностей, предоставляемых
        сервисом электронных библиотек
        """
        self._logger.debug('Calling __get_service_attributes')
        self._headers.update({'SOAPAction': '/getServiceAttributes'})
        response = self._send(GETSA)
        return response

    def __set_reading_system_attributes(self) -> bool:
        """
        Отправить на сервер список возможностей устройства
        """
        self._logger.debug('Calling __set_reading_system_attributes')
        self._headers.update({'SOAPAction': '/setReadingSystemAttributes'})
        response_data = self._send(SETRSA)
        if response_data is None:
            print('aa')
            return False
        result_match = re.search(r'<ns1:setReadingSystemAttributesResult>(.*?)<', response_data)
        if not result_match:
            return False
        result = result_match.group(1)
        return result == 'true'

    def login(self, username: str, password: str) -> bool:
        """
        1. Логинимся
        2. В случае успеха получаем сервисные атрибуты с сервера
        3. В случае успеха устанавливаем их как параметр класса
        4.
        """
        self._logger.debug(f'Login call with {username}:{password}')
        self._headers.update({'SOAPAction': '/logOn'})
        body = LOGON % (username, password)
        response_data = self._send(body)
        if response_data is None:
            return False
        login_result_match = re.search(r'<ns1:logOnResult>(.*?)</ns1:logOnResult>', response_data, re.DOTALL)
        if not login_result_match:
            return False
        login_result = login_result_match.group(1)
        if login_result != 'true':
            return False
        self._logger.debug('Login successful')
        service_attrs = self.__get_service_attributes()
        if service_attrs is None:
            return False
        self._logger.debug('Service attributes are fetched successfully')
        can_side_back_match = re.search(r'<ns1:supportsServerSideBack>(.*?)<', service_attrs, re.DOTALL)
        if can_side_back_match:
            self._supportsServerSideBack = can_side_back_match.group(1) == 'true'
        can_search_match = re.search(r'<ns1:supportsSearch>(.*?)<', service_attrs, re.DOTALL)
        if can_search_match:
            self._supportsSearch = can_search_match.group(1) == 'true'
        return self.__set_reading_system_attributes()
