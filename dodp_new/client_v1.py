import re
from typing import Optional, Self

from .general import DODPVersion, BookContent, LGKContent, LKFContent
from .client import DODPClient
from .request_body_v1 import LOGON, SETRSA, GETSA, GETCR


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
            return False
        result_match = re.search(r'<ns1:setReadingSystemAttributesResult>(.*?)<', response_data)
        if not result_match:
            return False
        return result_match.group(1) == 'true'

    # INFO: public methods

    def login(self, username: str, password: str) -> bool:
        """
        1. Логинимся
        2. В случае успеха получаем список возможностей сервера
        3. В случае успеха устанавливаем его в параметры класса
        4. Отправляем список возможностей устройства на сервер
        5. Возвращаем True в случае успеха
        """
        self._logger.debug(f'Calling login with {username}:{password}')
        self._headers.update({'SOAPAction': '/logOn'})
        body = LOGON % (username, password)
        response_data = self._send(body)
        if response_data is None:
            return False
        success_login_match = re.search(r'<ns1:logOnResult>true<', response_data, re.DOTALL)
        if not success_login_match:
            return False
        self._logger.debug('Login successful')
        service_attrs = self.__get_service_attributes()
        if service_attrs is None:
            return False
        self._logger.debug('Service attributes are fetched successfully')
        can_side_back_match = re.search(r'<ns1:supportsServerSideBack>true<', service_attrs, re.DOTALL)
        if can_side_back_match:
            self._supportsServerSideBack = True
        can_search_match = re.search(r'<ns1:supportsSearch>true<', service_attrs, re.DOTALL)
        if can_search_match:
            self._supportsSearch = True
        can_set_rsa = self.__set_reading_system_attributes()
        if can_set_rsa is not None:
            self._logger.debug('Login successful')
            return True

    def get_book_content(self, book_id: str) -> Optional[BookContent]:
        self._logger.debug(f'Calling get_book_content with {book_id}')
        self._headers.update({'SOAPAction': '/getContentResources'})
        body = GETCR % book_id
        response_data = self._send(body)
        if response_data is None:
            return None
        book_content: BookContent = BookContent()
        lgk_match = re.search(r'<ns1:resource .*?mimeType="application/lgk".*?/>', response_data, re.DOTALL)
        if not lgk_match:
            self._logger.error(f'LGK block not found in book content resources with id: {book_id}')
        lgk_uri = re.search(r'uri="(.*?)"', lgk_match.group(0)).group(1)
        lgk_size = float(re.search(r'size="(.*?)"', lgk_match.group(0)).group(1))
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
