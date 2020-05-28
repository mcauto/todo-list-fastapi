from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from .config import sqlalchemy_settings

engine = create_engine(
    sqlalchemy_settings.SQLALCHEMY_DATABASE_URL.format(
        MYSQL_USER=sqlalchemy_settings.MYSQL_USER,
        MYSQL_PASSWORD=sqlalchemy_settings.MYSQL_PASSWORD,
        MYSQL_ROOT_PASSWORD=sqlalchemy_settings.MYSQL_ROOT_PASSWORD,
        MYSQL_HOST=sqlalchemy_settings.MYSQL_HOST,
        MYSQL_DATABASE=sqlalchemy_settings.MYSQL_DATABASE,
    ),
    pool_size=sqlalchemy_settings.SQLALCHEMY_POOL_SIZE,
    pool_recycle=sqlalchemy_settings.SQLALCHEMY_POOL_RECYCLE,
    pool_timeout=sqlalchemy_settings.SQLALCHEMY_POOL_TIMEOUT,
    echo=sqlalchemy_settings.SQLALCHEMY_ECHO,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_database_session() -> Generator[Session, None, None]:
    """ sqlalchemy Session generator """
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
