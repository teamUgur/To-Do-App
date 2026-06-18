from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_SQLALCHEMY_DB = "sqllite:///./test.db"

engine = create_engine(
    URL_SQLALCHEMY_DB, connect_config={"check_same_thread": False}
)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()