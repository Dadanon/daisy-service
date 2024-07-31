from .request_body_v2 import LOGON_v2, GETCR_BODY_V2
from .client import *


class DODPClientV2(DODPClient):
    def __init__(self, url: str):
        self._version = DODPVersion.V201
        super().__init__(url)

    # INFO: public methods

    def login(self, username: str, password: str) -> bool:
        self._logger.debug(f'Calling login with {username}:{password}')
        self._update_soap_action(SOAPAction.LOGON)
        body = LOGON_v2(username, password)
        response_data = self._send(body)
        if response_data is None:
            return False
        service_attributes_match = re.search(r'<ns1:serviceAttributes>(.*?)</ns1:serviceAttributes>', response_data, re.DOTALL)
        if service_attributes_match is None:
            return False
        service_attributes = service_attributes_match.group(1)
        can_side_back_match = re.search(r'<supportsServerSideBack>true<', service_attributes, re.DOTALL)
        if can_side_back_match:
            self._supportsServerSideBack = True
        can_search_match = re.search(r'<supportsSearch>true<', service_attributes, re.DOTALL)
        if can_search_match:
            self._supportsSearch = True
        return True

    def get_book_content(self, book_id: str) -> Optional[BookContent]:
        body = GETCR_BODY_V2 % (book_id, 'STREAM')
        return self._get_book_content(book_id, body)
