from . import pydantic
from sqlalchemy.orm import Session
from .models import Post,Hashtag
import re
from sqlalchemy import desc



# create hastags for the posts
async def hastags(db:Session,db_post:pydantic.create_post):
    
    regex = r"#\w+"
    matches=re.findall(regex,db_post.content)
    print(matches)
    for match in matches:
        name=match[1:]
          
        hastags=db.query(Hashtag).filter(Hashtag.name==name).first()
        print(hastags,"kkkkk")
        if not hastags:
               print("heey helloo")
               hastags=Hashtag(name=name)
               db.add(hastags)
               db.commit()
        db_post.hastag.append(hastags)
            




# create the post function 

async   def createpost(db:Session,post:pydantic.create_post,user_id:int):
    db_post=Post(
        content=post.content,
        image=post.image,
        location=post.location,
        author_id=user_id

    )
    # create the hastags
    await hastags(db,db_post)
    db.add(db_post)
    db.commit()
    return db_post




# create the function to retrive the posts created by user from user_id
async def post_list(db:Session,user_id:int):
     posts=(
          db.query(Post).filter(Post.author_id==user_id).order_by(desc(Post.created_dt)).all()
     ) 
     if not posts:
          return {"message":"there is no post left"}
     return posts
