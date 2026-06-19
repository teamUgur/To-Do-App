from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

URL_SQLALCHEMY_DB = "sqlite:///./tets.db"

engine = create_engine(
    URL_SQLALCHEMY_DB, connect_args={"check_same_thread": False}
)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()