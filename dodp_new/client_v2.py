import re

from .client import DODPClient
from .general import DODPVersion
from .request_body_v2 import LOGON_v2


class DODPClientV2(DODPClient):
    def __init__(self, url: str):
        self._version = DODPVersion.V201
        super().__init__(url)

    def login(self, username: str, password: str) -> bool:
        self._logger.debug(f'Calling login with {username}:{password}')
        self._headers.update({'SOAPAction': '/logOn'})
        body = LOGON_v2(username, password)
        response_data = self._send(body)
        if response_data is None:
            return False
        can_side_back_match = re.search(r'<supportsServerSideBack>true<', response_data, re.DOTALL)
        if can_side_back_match:
            self._supportsServerSideBack = True
        can_search_match = re.search(r'<supportsSearch>true<', response_data, re.DOTALL)
        if can_search_match:
            self._supportsSearch = True
        success_login_match = re.search(r'<ns1:logOnResult>true<', response_data, re.DOTALL)
        return True if success_login_match else False
