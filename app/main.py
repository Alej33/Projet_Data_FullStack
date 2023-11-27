from fastapi import FastAPI, Response, HTTPException, status, Depends, Request, responses, Form
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from sqlalchemy.orm import Session
from .database import engine, session, get_db, BookCreatePost
from .models import Book
from . import models
import os
from dotenv import load_dotenv
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.responses import RedirectResponse



load_dotenv("creds.env")

models.Base.metadata.create_all(bind=engine)



app = FastAPI()


while True :
    try :
        conn = psycopg2.connect(host ='localhost', dbname='fastapi' ,user = os.environ.get("USER"),
                                password = os.environ.get("PASSWORD"),  cursor_factory=RealDictCursor)
        print('successfully connected to db !!')
        cursor = conn.cursor()
        break

    except Exception as error:  
        print("connection de database failed ! Trying again... ")
        print(f"error : {error}")
        time.sleep(3)


@app.get("/books", response_model=List[Book])
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

@app.post("/join-us/add-post", status_code=status.HTTP_201_CREATED)
def add_book(title: str = Form(...), 
             genre: str = Form(...),
             desired_genre: str = Form(...),
             country: str = Form(...),
             city: str = Form(...),
             description: str = Form(...),
             db: Session = Depends(get_db)):
    # Create a new book instance
    new_book = Book(title=title, genre=genre, desired_genre=desired_genre, 
                    country=country, city=city, description=description)
    # Add to the database
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"message": "Book added successfully", "book": new_book}









