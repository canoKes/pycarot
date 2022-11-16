import traceback
from dataclasses import dataclass
from typing import Any, Protocol


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
