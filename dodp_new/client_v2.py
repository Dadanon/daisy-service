import re

from .client import DODPClient
from .general import DODPVersion
from .request_body_v2 import LOGON


class DODPClientV2(DODPClient):
    def __init__(self, url: str):
        self._version = DODPVersion.V1
        super().__init__(url)

    def login(self, username: str, password: str) -> bool:
        self._logger.debug(f'Calling login with {username}:{password}')
        self._headers.update({'SOAPAction': '/logOn'})
        body = LOGON % (username, password)
        response_data = self._send(body)
        if response_data is None:
            return False
        can_side_back_match = re.search(r'<supportsServerSideBack>(.*?<)', response_data, re.DOTALL)
        if can_side_back_match:
            self._supportsServerSideBack = can_side_back_match.group(1) == 'true'
        can_search_match = re.search(r'<supportsSearch>(.*?)<', response_data, re.DOTALL)
        if can_search_match:
            self._supportsSearch = can_search_match.group(1) == 'true'
        return True
