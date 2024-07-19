from enum import StrEnum


BASE_HEADERS = {
    'Content-Type': 'text/xml; charset=utf-8',
    'Accept': 'text/xml'
}

CLIENT_TIMEOUT = 5
"""Максимальное время ожидания ответа от сервера"""


class DODPVersion(StrEnum):
    V1 = 'v1'
    V201 = 'v2.0.1'
    V202 = 'v2.0.2'
