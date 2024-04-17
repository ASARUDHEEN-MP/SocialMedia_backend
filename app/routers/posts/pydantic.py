from typing import Optional
from pydantic import BaseModel
from datetime import datetime



class create_post(BaseModel):
    content:str
    image:str
    location:Optional[str]=None


class postrespponse(create_post):
    id:int
    author_id:int
    likes_count:int
    created_dt:datetime
    
    # telling the pydantic to intract with orm
    class Config:
        orm_mode = True

