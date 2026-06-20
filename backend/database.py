from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

URL_SQLALCHEMY_DB = "sqlite:///./tets.db"

engine = create_engine(
    URL_SQLALCHEMY_DB, connect_args={"check_same_thread": False}
)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass