import threading


class Event:
    """Base class for all custom events"""

    @property
    def name(self) -> str:
        return type(self).__name__

    def __str__(self) -> str:
        attributes = vars(self).items()
        out = self.name
        if attributes:
            out += f" {', '.join([f'{k}({v})' for k, v in attributes])}"
        return out

    def __repr__(self) -> str:
        return str(self)


class EventManager:
    __slots__ = ("_subs", "_entries")

    def __init__(self) -> None:
        self._subs: dict[int, object] = {}
        self._entries: dict[int, list[type]] = {}

    def subscribe(self, subscriber: object) -> None:
        self._subscribe(subscriber)

    def _subscribe(self, subscriber: object) -> int:
        sid = id(subscriber)
        if not sid in self._subs:
            self._subs[sid] = subscriber
        return sid

    def unsubscribe(self, subscriber: object) -> None:
        sid = id(subscriber)
        if not sid in self._subs:
            return
        del self._subs[sid]
        if sid in self._entries:
            del self._entries[sid]

    def register_for(self, subscriber: object, EventType: type) -> None:
        sid = self._subscribe(subscriber)
        if not sid in self._entries:
            self._entries[sid] = []
        self._entries[sid].append(EventType)

    def unregister(self, subscriber: object, EventType: type) -> None:
        sid = id(subscriber)
        if not sid in self._entries:
            return
        if EventType in self._entries[sid]:
            self._entries[sid].remove(EventType)

    def publish(self, sender, event: Event) -> None:
        subs = self._subs.copy()
        for sid in subs:
            if not sid in self._entries:
                continue
            if not type(event) in self._entries[sid]:
                continue
            getattr(subs[sid], f"on_{ event.name.lower() }")(event, sender)

    def publish_async(self, sender, event: Event) -> None:
        threading.Thread(target=self.publish, args=(event, sender), daemon=True).start()
