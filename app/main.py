from fastapi import FastAPI
from app.routers import authenticaters
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app=FastAPI()





app.include_router(authenticaters.router)