from typing import Any, Type

from .container import Container, T

_container: Container = None


def set_container(container: Container) -> None:
    global _container
    if not isinstance(container, Container):
        raise Exception("container has to be type of Container")
    _container = container


def register(implementation: type, service: type = None) -> None:
    _container.register(implementation, service)


def register_instance(
    implementation: type, service: type = None, args: tuple = (), kwds: dict[str, Any] = None
) -> None:
    _container.register_instance(implementation, service, args, kwds)


def register_singleton(implementation: type, service: type = None, instance: object = None) -> None:
    _container.register_singleton(implementation, service, instance)


def get(type: Type[T], default: Any = None) -> T:
    instance = _container.get(type)
    if instance is None:
        return default
    return instance
