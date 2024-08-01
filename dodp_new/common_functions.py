# -*- coding: utf-8 -*-

import re
from typing import Optional


def method_not_override(method_name: str) -> str:
    return f'Метод {method_name} не переопределен'


def get_normalized(text: Optional[str]) -> Optional[str]:
    return re.sub(r'\n|\s{2,}|\t', '', text) if text else None
