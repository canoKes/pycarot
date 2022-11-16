from client import Client, Service
from data_access import DbConfiguration, DbConnector, IRepository, Repository

from pycarot import ioc


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
