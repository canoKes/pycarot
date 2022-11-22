import threading
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime


class Event(ABC):
    """Base class for all custom events"""

    def __str__(self) -> str:
        items = [f"{k}={v}" for k, v in vars(self).items() if not k.startswith("__")]
        return f"[{ datetime.now() }] {type(self).__name__} ({ ', '.join(items) })"


SubEntryMap = dict[int, list[type]]


@dataclass
class EventAggregator:
    __subs: dict[int, object] = field(default_factory=dict)
    __entries: SubEntryMap = field(default_factory=dict)

    def subscribe(self, subscriber: object) -> None:
        self.__subscribe(subscriber)

    def __subscribe(self, subscriber: object) -> int:
        sid = id(subscriber)
        if not sid in self.__subs:
            self.__subs[sid] = subscriber
        return sid

    def unsubscribe(self, subscriber: object) -> None:
        sid = id(subscriber)
        if not sid in self.__subs:
            return
        del self.__subs[sid]
        if sid in self.__entries:
            del self.__entries[sid]

    def register_for(self, subscriber: object, EventType: type) -> None:
        sid = self.__subscribe(subscriber)
        if not sid in self.__entries:
            self.__entries[sid] = []
        self.__entries[sid].append(EventType)

    def unregister(self, subscriber: object, EventType: type) -> None:
        sid = id(subscriber)
        if not sid in self.__entries:
            return
        if EventType in self.__entries[sid]:
            self.__entries[sid].remove(EventType)

    def publish(self, sender, event: Event) -> None:
        subs = self.__subs.copy()
        for sid in subs:
            if not sid in self.__entries:
                continue
            if not type(event) in self.__entries[sid]:
                continue
            getattr(subs[sid], f"on_{ type(event).__name__.lower() }")(sender, event)

    def publish_async(self, sender, event: Event) -> None:
        thread = threading.Thread(target=self.publish, args=(sender, event))
        thread.daemon = True
        thread.start()
