from .request_body_v1 import LOGON_BODY_V1, SETRSA_BODY, GETSA_BODY, GETCR_BODY_V1
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
        response = self._send(GETSA_BODY)
        return response

    def __set_reading_system_attributes(self) -> bool:
        """
        Отправить на сервер список возможностей устройства
        """
        self._logger.debug('Calling __set_reading_system_attributes')
        self._update_soap_action(SOAPAction.SET_READING_SYSTEM_ATTRIBUTES)
        response_data = self._send(SETRSA_BODY)
        if response_data is None:
            return False
        set_rsa_tag: TagInfo = get_tag_info_by_params('setReadingSystemAttributesResult', response_data)
        if not set_rsa_tag:
            return False
        return set_rsa_tag.content == 'true'

    # INFO: public methods

    def login(self, username: str, password: str) -> bool:
        """
        1. Логинимся
        2. В случае успеха получаем список возможностей сервера
        3. В случае успеха устанавливаем его в параметры класса
        4. Отправляем список возможностей устройства на сервер
        5. Возвращаем True в случае успеха
        """
        request_body = LOGON_BODY_V1 % (username, password)
        response_data = self._get_response_data(request_body, 'login', SOAPAction.LOGON, username=username, password=password)
        if response_data is None:
            return False
        logonresult_tag: TagInfo = get_tag_info_by_params('logOnResult', response_data)
        if not logonresult_tag:
            self._logger.error('No logonresult tag in response data')
            return False
        service_attrs = self.__get_service_attributes()
        if service_attrs is None:
            self._logger.error('No service attributes tag in response data')
            return False
        self._logger.debug('Service attributes are fetched successfully')
        can_side_back_tag: TagInfo = get_tag_info_by_params('supportsServerSideBack', service_attrs)
        if can_side_back_tag:
            self._supportsServerSideBack = can_side_back_tag.content == 'true'
        supports_search_tag: TagInfo = get_tag_info_by_params('supportsSearch', service_attrs)
        if supports_search_tag:
            self._supportsSearch = supports_search_tag.content == 'true'
        can_set_rsa = self.__set_reading_system_attributes()
        if can_set_rsa is not None:
            self._logger.debug(f'Login with version: {self._version} succeeded')
            return True

    def get_book_content(self, book_id: str) -> Optional[BookContent]:
        body = GETCR_BODY_V1 % book_id
        return self._get_book_content(book_id, body)
