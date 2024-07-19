from .messages import method_not_override


class NotOverrideError(Exception):
    method_name: str

    def __init__(self, method_name: str):
        self.method_name = method_name

    def __str__(self):
        print(method_not_override(self.method_name))