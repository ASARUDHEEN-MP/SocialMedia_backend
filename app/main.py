from fastapi import FastAPI,Request
from app.routers import authenticaters
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,database
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import RedirectResponse

app=FastAPI()

# create database tables based on the model
models.Base.metadata.create_all(bind=database.engine)

# middlware 
@app.middleware("http")
async def enforce_https(request:Request,call_next):
    # if request.method == "POST" and request.url.path != "/login":
        # Print the full URL of the incoming request
        # try:
        #     data = await request.json()
        #     token = data.get("token")
        #     if token:
        #         print("Token found in request body:", token)
        #     else:
        #         print("Token not found in request body")
        # except Exception as e:
        #     print("Error while parsing request body:", e)
    response = await call_next(request)
    return response



# connect the routers to the main file
app.include_router(authenticaters.router)