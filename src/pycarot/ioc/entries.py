from typing import Any


class Entry:
    """Base class of all entry types."""

    __slots__ = ("implementation", "service")

    @property
    def key(self) -> str:
        return self.service.__name__

    def __init__(self, implementation: type, service: type = None) -> None:
        if not isinstance(implementation, type):
            raise ValueError("implementation has to be a type")
        if service is None:
            service = implementation
        if not isinstance(service, type):
            raise ValueError("service has to be a type")

        self.implementation = implementation
        self.service = service



class InstanceEntry(Entry):
    """Returns a preconstructed instance."""

    __slots__ = ("arguments", "keywords")

    def __init__(self, implementation: type, service: type = None, arguments: tuple[Any] = None, keywords: dict[str, Any] = None) -> None:
        super().__init__(implementation, service)
        self.arguments = arguments if arguments is not None else ()
        self.keywords = keywords if keywords is not None else {}


class SingletonEntry(Entry):
    """A singlton entry. Returns always the same instance of an object."""

    __slots__ = ("instance",)

    def __init__(self, implementation: type, service: type = None, instance: object = None) -> None:
        super().__init__(implementation, service)
        self.instance = instance
