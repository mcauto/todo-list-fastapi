from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    pool_size=settings.SQLALCHEMY_POOL_SIZE,
    pool_recycle=settings.SQLALCHEMY_POOL_RECYCLE,
    pool_timeout=settings.SQLALCHEMY_POOL_TIMEOUT,
    echo=settings.SQLALCHEMY_ECHO,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
