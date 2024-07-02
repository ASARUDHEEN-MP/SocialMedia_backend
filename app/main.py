from fastapi import FastAPI,Request
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .routers.oauth import models
from . import database,apirouter
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",  # Replace with the actual origin of your frontend
    "http://localhost:5173",
    # Add more origins as needed
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create database tables based on the model
database.Base.metadata.create_all(bind=database.engine)



# connect the routers to the from the file of apirouter 
app.include_router(apirouter.apirouters)

# # middlware 
# @app.middleware("http")
# async def enforce_https(request:Request,call_next):
#     # if request.method == "POST" and request.url.path != "/login":
#         # Print the full URL of the incoming request
#         # try:
#         #     data = await request.json()
#         #     token = data.get("token")
#         #     if token:
#         #         print("Token found in request body:", token)
#         #     else:
#         #         print("Token not found in request body")
#         # except Exception as e:
#         #     print("Error while parsing request body:", e)
#     if "Authorization" in request.headers:
#         auth_header = request.headers["Authorization"]
#         parts = auth_header.split()
        
#     response = await call_next(request)
#     return response
