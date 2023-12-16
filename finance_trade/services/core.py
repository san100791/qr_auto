import logging
import threading
from contextlib import contextmanager

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from finance_trade.config import make_config
from finance_trade.models import (
    User,
    UserSerssion,
)

logger = logging.getLogger(__name__)


def create_app_engine(dsn: str, app_name: str, engine_opts: dict = None) -> Engine:
    options = " ".join([f"-c application_name={app_name}", "-c statement_timeout=50000"])
    opts = {"pool_pre_ping": True, "echo_pool": True, "pool_recycle": 1200, **(engine_opts or {})}
    engine = create_engine(dsn, connect_args={"options": options}, **opts)
    return engine


class Core:
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    def __new__(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                cls.__singleton_instance = object.__new__(cls)
        return cls.__singleton_instance

    def __getattr__(self, item):
        if not self.__singleton_instance:
            raise Exception("core is not initialized")
        return getattr(self.__singleton_instance, item)

    @classmethod
    def instance(cls) -> "Core":
        return cls.__singleton_instance

    def __init__(self):
        self.config = make_config()
        self.db_engine = create_app_engine(
            self.config.app_db.dsn,
            self.config.app_name,
            self.config.app_db.engine_opts,
        )
        self.db_session = scoped_session(
            sessionmaker(
                binds={
                    User: self.db_engine,
                    UserSerssion: self.db_engine,
                }
            )
        )

    @contextmanager
    def session(self):
        s = self.db_session()
        try:
            yield s
            s.commit()
        except Exception:  # noqa: B902
            s.rollback()
            raise
        finally:
            s.close()


class DatabaseServiceMixin:
    @property
    def session(self):
        return core.db_session()

    @property
    def config(self):
        return core.config


class CoreWrapper:
    def __getattr__(self, attr):
        g = Core.instance()  # key spot
        if not g:
            raise ValueError("Core is not initialized")
        return getattr(Core.instance(), attr)


core = CoreWrapper()
