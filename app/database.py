from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlalchemy_db_connect = "postgresql://postgres:1234@localhost/fastapi"
engine=create_engine(sqlalchemy_db_connect)

session=sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base=declarative_base()


def getdb():
    db=session()
    try:
        yield db
    finally:
        db.close()
