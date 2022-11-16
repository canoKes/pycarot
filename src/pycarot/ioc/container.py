import inspect
from typing import Any, Type, TypeVar

from .entries import Entry, InstanceEntry, SingletonEntry
from .exceptions import TypeExistsException, TypeNotRegisteredException

T = TypeVar("T")
EntryDict = dict[str, Entry]


class Container:
    _entries: EntryDict = None

    def __init__(self) -> None:
        self.reset()

    def _register(self, entry: Entry) -> None:
        key = entry.key
        if key in self._entries:
            raise TypeExistsException(key)
        self._entries[key] = entry

    def _instantiate(self, entry: Entry, *args, **kwds) -> object:
        arguments = [x for x in args]
        keywords = kwds.copy()
        signature = inspect.signature(entry.implementation)
        for p in signature.parameters.values():
            if p.name == "self" or not self.exists(p.annotation):
                continue

            if p.kind == p.POSITIONAL_ONLY:
                arguments.append(self.get(p.annotation))
            elif p.kind == p.KEYWORD_ONLY or p.kind == p.POSITIONAL_OR_KEYWORD:
                keywords[p.name] = self.get(p.annotation)
        return entry.implementation(*tuple(arguments), **keywords)

    def exists(self, type: type) -> bool:
        entry = self._entries.get(type.__name__, None)
        return True if entry else False

    def reset(self) -> None:
        self._entries = {}

    def get(self, type: Type[T]) -> T:
        entry = self._entries.get(type.__name__, None)
        if entry is None:
            raise TypeNotRegisteredException(type)
        if isinstance(entry, SingletonEntry):
            if not entry.instance:
                entry.instance = self._instantiate(entry)
            return entry.instance
        elif isinstance(entry, InstanceEntry):
            return self._instantiate(entry, *entry.arguments, **entry.keywords)
        elif isinstance(entry, Entry):
            return self._instantiate(entry)

    def register(
        self,
        implementation: type,
        service: type = None,
    ) -> None:
        self._register(Entry(implementation, service))

    def register_instance(
        self,
        implementation: type,
        service: type = None,
        args: tuple = (),
        kwds: dict[str, Any] = None,
    ) -> None:
        if kwds is None:
            kwds = {}
        self._register(InstanceEntry(implementation, service, args, kwds))

    def register_singleton(
        self,
        implementation: type,
        service: type = None,
        instance: object = None,
    ) -> None:
        self._register(SingletonEntry(implementation, service, instance))
