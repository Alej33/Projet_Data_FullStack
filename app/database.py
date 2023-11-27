from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Request
from typing import Optional, List
from dotenv import load_dotenv
import os

load_dotenv(".env")


# structure of the url : postgresql://<username>:<password>/<ip-adress/hostname>/<database-name>
port, server_name = 5433, 'postgres_books' 

SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ.get('USER')}:{os.environ.get('PASSWORD')}@localhost:{port}/{server_name}"

engine = create_engine(url = SQLALCHEMY_DATABASE_URL)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


class BookCreatePost:
    def __init__(self, request: Request):
        self.request: Request = request
        self.title : Optional[str] = None
        self.genre : Optional[str] = None
        self.availability : Optional[bool] = None
        self.desired_genre : Optional[str] = None
        self.description : Optional[str] = None
        self.country : Optional[str] = None
        self.city : Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.title = form.get("title")
        self.genre = form.get("genre")
        self.availability = form.get("availability")
        self.desired_genre = form.get("desired_genre")
        self.description = form.get("description")
        self.country = form.get("company")
        self.city = form.get("city")
