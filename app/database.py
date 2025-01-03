# from typing import Annotated

# from fastapi import Depends, FastAPI, HTTPException, Query
# from sqlmodel import Field, Session, SQLModel, create_engine, select

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import supabase
from supabase import create_client, Client
import time 
from .config import * 

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# run raw sql 
# while True:
#     try:
#         supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Database connection failed:", error)
#         time.sleep(3)