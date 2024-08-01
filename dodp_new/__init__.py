from typing import Optional, Type

from dodp_new.client import DODPClient
from dodp_new.client_v1 import DODPClientV1
from dodp_new.client_v2 import DODPClientV2
from dodp_new.exceptions import GetClientError


def __get_client(client_type: Type[DODPClient], url: str, username: str, password: str) -> Optional[DODPClient]:
    client: client_type = client_type(url)
    can_login = client.login(username, password)
    if can_login:
        questions = client.get_search_questions()
        if questions:
            # print(questions.to_dict())
            return client
    return None


def client_login(url: str, username: str, password: str) -> DODPClient:
    client_v1 = __get_client(DODPClientV1, url, username, password)
    if client_v1:
        return client_v1
    client_v2 = __get_client(DODPClientV2, url, username, password)
    if client_v2:
        return client_v2
    raise GetClientError()


__all__ = [
    'client_login'
]
