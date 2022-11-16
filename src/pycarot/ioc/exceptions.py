class TypeExistsException(Exception):
    def __init__(self, key: str) -> None:
        self.message = f"type '{key}' is already registered!"
        super().__init__(self.message)


class TypeNotRegisteredException(Exception):
    def __init__(self, type: type) -> None:
        self.message = f"type '{type.__name__}' is not registered!"
        super().__init__(self.message)
