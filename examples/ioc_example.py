import traceback
from dataclasses import dataclass
from typing import Any, Protocol

from pycarot import ioc


@dataclass
class DbConfiguration:
    host: str
    user: str
    password: str
    database: str


@dataclass
class DbConnector:
    configuration: DbConfiguration
    name: str = None

    def connect(self) -> None:
        print(">> open db connection (", end="")
        print(", ".join([f"{k}={v}" for k, v in vars(self.configuration).items()]), end="")
        print(")")

    def disconnect(self) -> None:
        print(">> close db connection")

    def __enter__(self) -> None:
        self.connect()

    def __exit__(self, type: type, ex: Exception, trace: traceback) -> None:
        self.disconnect()


class IRepository(Protocol):
    connector: DbConnector

    def get_data(self) -> Any:
        ...


@dataclass
class Repository(IRepository):
    connector: DbConnector

    def get_data(self) -> list[str]:
        with self.connector:
            print(">> get data from repository")
            return ["seems", "working", "!!"]


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


def configure_ioc() -> None:
    container = ioc.Container()
    ioc.set_container(container)

    config = DbConfiguration("localhost", "admin", "", "test_db")
    ioc.register_singleton(DbConfiguration, instance=config)
    ioc.register_instance(DbConnector, kwds={"name": "MYSQL"})
    ioc.register(Repository, IRepository)
    ioc.register(Service)
    ioc.register(Client)


def main() -> None:
    configure_ioc()
    client = ioc.get(Client)
    client.do_action()


if __name__ == "__main__":
    main()
