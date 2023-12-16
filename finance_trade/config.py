import enum
import logging
import os
import urllib
from dataclasses import dataclass, field
from typing import Any, List, Optional

import sentry_sdk

from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from finance_trade.project import CONVENTION_NAME, NAME


class AppConfig:
    def __init__(self, env) -> None:
        self.env = env
        self.relacetd_hosts = {
            "testnet_binance": "https://testnet.binance.vision/api",
        }
        self.flask_config = {
            'development': {
                'DEBUG': True,
                'ENV': 'development',
                'SECRET_KEY': 'your_secret_key_for_development'
            },
            'production': {
                'DEBUG': False,
                'ENV': 'production',
                'SECRET_KEY': 'your_secret_key_for_production'
            },
            'testing': {
                'TESTING': True,
                'ENV': 'testing',
                'SECRET_KEY': 'your_secret_key_for_testing'
            }
        }
        self.db_config = {
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", "postgres"),
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432"),
            "db_name": os.getenv("DB_NAME", "finance_trade"),
        }        

configuration = AppConfig(env=os.getenv("ENVIRONMENT", "local"))


@dataclass
class DatabaseConfig:
    host: str
    database: str
    user: str
    password: str
    port: int
    data_source_name: str = "postgresql"
    engine_opts: dict = field(default_factory=dict)

    @property
    def dsn(self) -> str:
        port_str = f":{self.port}" if self.port else ""
        return f"{self.data_source_name}://{self.user}:{self.password}@{self.host}{port_str}/{self.database}"

    @classmethod
    def from_dict(
        cls, db_conf: dict, engine_opts: Optional[dict] = None, data_source: str = "postgresql"
    ) -> "DatabaseConfig":
        cfg = cls(
            host=db_conf["host"],
            database=db_conf["name"],
            user=db_conf["user"],
            password=db_conf["password"],
            port=db_conf.get("port"),
            data_source_name=data_source,
            engine_opts=engine_opts or {},
        )
        return cfg


@dataclass
class SentryConfig:
    dsn: str
    traces_sample_rate: float

    @classmethod
    def from_dict(cls, conf: dict) -> "SentryConfig":
        c = cls(dsn=conf["dsn"], traces_sample_rate=conf.get("traces_sample_rate", 0.1))
        return c


@dataclass
class Config:
    env: str
    app_name: str
    convention_app_name: str
    app_db: DatabaseConfig
    sentry: SentryConfig
    redis_uri: str
    related_hosts: dict
    flask_config: dict


def make_config(*, db_engine_opts: Optional[dict] = None) -> Config:

    cfg = Config(
        env=configuration.env,
        app_name=NAME,
        convention_app_name=CONVENTION_NAME,
        app_db=DatabaseConfig.from_dict(configuration["database"], engine_opts=db_engine_opts),
        related_hosts=configuration.related_hosts(),
        sentry=SentryConfig.from_dict(configuration["sentry"]),
        flask_config=configuration.flask_config(),
    )
    return cfg


def init_sentry_flask(sentry_conf: SentryConfig, environment: str = None):
    integrations = [
        FlaskIntegration(),
        SqlalchemyIntegration(),
        LoggingIntegration(level=logging.INFO, event_level=logging.WARNING),
    ]
    init_sentry(sentry_conf, environment.name if environment else "local", integrations=integrations)


def init_sentry(sentry_conf: SentryConfig, environment: str = None, integrations: List[Any] = None):
    if integrations is None:
        integrations = [
            SqlalchemyIntegration(),
            LoggingIntegration(level=logging.INFO, event_level=logging.WARNING),
        ]

    sentry_sdk.init(
        dsn=sentry_conf.dsn,
        traces_sample_rate=sentry_conf.traces_sample_rate,
        environment=environment,
        integrations=integrations,
    )


def get_database_dsn(cluster, db_name):
    config = configuration.db_config()[cluster]
    dsn = "postgresql://{user}:{password}@{host}:{port}/{dbname}".format(
        host=config["host"], port=config["port"], password=config["password"], user=config["user"], dbname=config["db_name"]
    )
    return dsn
