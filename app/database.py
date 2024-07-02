from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlalchemy_db_connect = "postgresql://postgres:Asarudheen12@database-2.crio86ka6p83.ap-southeast-2.rds.amazonaws.com:5432/socialmedia"

engine=create_engine(sqlalchemy_db_connect)

session=sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base=declarative_base()


def getdb():
   
    db=session()
    try:
        yield db
    finally:
        db.close()
