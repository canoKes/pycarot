from dataclasses import dataclass
from pycarot import Event, EventManager

class Event1(Event):
    pass

@dataclass
class Event2(Event):
    field1: str

class Subscriber1:

    def __init__(self, events: EventManager) -> None:
        events.register_for(self, Event1)

    def on_event1(self, event, sender) -> None:
        print(event)

class Subscriber2:

    def __init__(self, events: EventManager) -> None:
        events.register_for(self, Event1)
        events.register_for(self, Event2)

    def on_event1(self, event, sender) -> None:
        print(event)

    def on_event2(self, event, sender) -> None:
        print(event)


def main() -> None:
    manager = EventManager()
    sub1 = Subscriber1(manager)
    sub1 = Subscriber2(manager)
    manager.publish(None, Event1())
    manager.publish(None, Event2("Test Event"))

if __name__ == "__main__":
    main()