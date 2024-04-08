from fastapi import APIRouter,Depends
from  ..database import engine,getdb
from sqlalchemy.orm import Session
from sqlalchemy import  MetaData, Table,select


router=APIRouter()

