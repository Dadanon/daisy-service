from .request_body_v1 import LOGON, SETRSA, GETSA, GETCR
from .client import *


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
        self._update_soap_action(SOAPAction.GET_SERVICE_ATTRIBUTES)
        response = self._send(GETSA)
        return response

    def __set_reading_system_attributes(self) -> bool:
        """
        Отправить на сервер список возможностей устройства
        """
        self._logger.debug('Calling __set_reading_system_attributes')
        self._update_soap_action(SOAPAction.SET_READING_SYSTEM_ATTRIBUTES)
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
        self._update_soap_action(SOAPAction.LOGON)
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
        body = GETCR % book_id
        return self._get_book_content(book_id, body)
