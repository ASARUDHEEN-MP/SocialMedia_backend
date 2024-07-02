from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from ...database import Base


post_hashtags = Table(
    "post_hashtags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("hashtag_id", Integer, ForeignKey("hashtags.id")),
)




class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    image = Column(String)  # url to the image
    location = Column(String)
    created_dt = Column(DateTime, default=datetime.utcnow())
    likes_count = Column(Integer, default=0)

    author_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"))
    author = relationship("oauth.models.User", back_populates="posts")
    hastag=relationship("Hashtag",secondary=post_hashtags,back_populates="posts")


   

    


class Hashtag(Base):
    __tablename__ = "hashtags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    posts=relationship("Post",secondary=post_hashtags,back_populates="hastag")

   