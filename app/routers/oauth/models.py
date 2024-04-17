from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Date,Enum
from ...database import Base
from datetime import datetime
from ..posts.models import Post
from . import enum
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"


    id=Column(Integer,primary_key=True)
    username=Column(String,unique=True,nullable=True)
    email=Column(String,unique=True,index=True,nullable=True)
    hashed_password = Column(String)
    is_active=Column(Boolean, default=True)
    role = Column(String)

    dob=Column(Date)
    gender=Column(Enum(enum.Gender))
    profile_pic=Column(String)

    posts=relationship(Post,back_populates="author")

  



