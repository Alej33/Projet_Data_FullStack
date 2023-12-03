from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Request
from typing import Optional, List
from dotenv import load_dotenv
import os

load_dotenv(".env")


# structure of the url : postgresql://<username>:<password>/<ip-adress/hostname>/<database-name>
port, server_name = 5432 , 'postgres' 

SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ.get('USER')}:{os.environ.get('PASSWORD')}@localhost:{port}/{server_name}"

#print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(url = SQLALCHEMY_DATABASE_URL)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
