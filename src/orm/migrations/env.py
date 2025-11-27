from logging.config import fileConfig
from urllib.parse import unquote

from pydantic import PostgresDsn
from sqlalchemy import engine_from_config, pool, URL

from alembic import context

import orm
import orm.models
from env_settings import ENV

env = ENV()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def get_sqlalchemy_url(postgres_dsn: PostgresDsn) -> URL:
    host = postgres_dsn.hosts()[0]
    query = dict(postgres_dsn.query_params())
    query["async_fallback"] = "True"
    query.pop("ssl_mode", None)

    username = host["username"]
    password = host["password"]
    host_addr = host["host"]
    path = postgres_dsn.path

    return URL.create(
        drivername=postgres_dsn.scheme,
        username=unquote(username) if username else username,
        password=unquote(password) if password else password,
        host=unquote(host_addr) if host_addr else host_addr,
        port=host["port"],
        database=path.lstrip("/") if path else path,
        query=query
    )


target_metadata = orm.Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=get_sqlalchemy_url(env.POSTGRES_DSN),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=get_sqlalchemy_url(env.POSTGRES_DSN),
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
