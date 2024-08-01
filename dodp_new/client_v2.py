from .request_body_v2 import GETCR_BODY_V2, LOGON_BODY_V2
from .client import *


class DODPClientV2(DODPClient):
    def __init__(self, url: str):
        self._version = DODPVersion.V201
        super().__init__(url)

    # INFO: public methods

    def login(self, username: str, password: str) -> bool:
        request_body = LOGON_BODY_V2 % (username, password)
        response_data = self._get_response_data(request_body, 'login', SOAPAction.LOGON, username=username, password=password)
        if response_data is None:
            return False
        service_attributes_tag: TagInfo = get_tag_info_by_params('serviceAttributes', response_data)
        if not service_attributes_tag:
            self._logger.error('No service attributes tag found in response data')
            return False
        supports_server_side_back_tag: TagInfo = get_tag_info_by_params('supportsServerSideBack', service_attributes_tag.content)
        if supports_server_side_back_tag:
            self._supportsServerSideBack = supports_server_side_back_tag.content == 'true'
        supports_search_tag: TagInfo = get_tag_info_by_params('supportsSearch', service_attributes_tag.content)
        if supports_search_tag:
            self._supportsSearch = supports_search_tag.content == 'true'
        self._logger.debug(f'Login with version: {self._version} succeeded')
        return True

    def get_book_content(self, book_id: str) -> Optional[BookContent]:
        body = GETCR_BODY_V2 % (book_id, 'STREAM')
        return self._get_book_content(book_id, body)
