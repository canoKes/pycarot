from dataclasses import dataclass, field
from typing import Any


@dataclass
class Entry:
    """Base class of all entry types."""

    implementation: type
    service: type = None

    def __post_init__(self) -> None:
        if not isinstance(self.implementation, type):
            raise ValueError("implementation has to be a type")
        if self.service is None:
            self.service = self.implementation
        if not isinstance(self.service, type):
            raise ValueError("service has to be a type")

    @property
    def key(self) -> str:
        return self.service.__name__


@dataclass
class InstanceEntry(Entry):
    """Returns a preconstructed instance."""

    arguments: tuple = field(default_factory=tuple)
    keywords: dict[str, Any] = field(default_factory=dict)


@dataclass
class SingletonEntry(Entry):
    """A singlton entry. Returns always the same instance of an object."""

    instance: object = None
