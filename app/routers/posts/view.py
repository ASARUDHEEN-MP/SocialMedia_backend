from fastapi import HTTPException,Depends,APIRouter,status
from sqlalchemy.orm import Session
from . import pydantic,service
from ...database import getdb
from ..authtocken import current_user

# create the root for cretaing the post
postrouter=APIRouter()


# create the function for the post
# dependencies can be injected into route functions (depends) 
@postrouter.post("/createpost",status_code=status.HTTP_201_CREATED)
async def createpost(posts:pydantic.create_post,db:Session=Depends(getdb),current_user:str=Depends(current_user)):
    user=current_user
    # create post
    posts= await service.createpost(db,posts,user.id)
    if not posts:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Post not created")
    
    return {"message":"succefully created the post"}



# create the function of retriving the current user post
@postrouter.get("/posts",response_model=list[pydantic.postrespponse])
async def get_posts(db:Session=Depends(getdb),current_user:str=Depends(current_user)):
    post_user=await service.post_list(db,current_user.id)
    return post_user

   
