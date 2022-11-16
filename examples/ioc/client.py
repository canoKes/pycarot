from dataclasses import dataclass

from data_access import IRepository


@dataclass
class Service:
    repository: IRepository

    def get_message(self) -> None:
        data = self.repository.get_data()
        print(f">> message: {' '.join(data)}")


@dataclass
class Client:
    service: Service

    def do_action(self):
        self.service.get_message()
