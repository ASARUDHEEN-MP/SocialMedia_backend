from fastapi import APIRouter

from .routers.oauth.view import router
from .routers.posts.view import postrouter


# prefix will allow you to give all the router in v1
apirouters=APIRouter()

#  its the routers of the entire router and it will pass to the main.py file and connect it

apirouters.include_router(router)
apirouters.include_router(postrouter)

