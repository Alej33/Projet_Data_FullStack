from fastapi import FastAPI, Response, HTTPException, status, Depends, Request, responses, Form
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from sqlalchemy.orm import Session
from database import engine, session, get_db, BookCreatePost
from models import Book
import models
import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.responses import RedirectResponse



load_dotenv(".env")

models.Base.metadata.create_all(bind=engine)

TEMPLATES = Jinja2Templates(directory="templates")


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


# get req for showing the add post page 
@app.get("/join-us/add-post")
def form_post(request: Request):
    return TEMPLATES.TemplateResponse('add_post.html', context={'request': request})

# thanks page for submitting a post
@app.get("join-us/Thank_you")
def redirect_post(request: Request):
    return TEMPLATES.TemplateResponse('post_added.html', context={'request': request})


# post req for adding a post
@app.post("/join-us/add-post")
def form_post(request: Request, 
              title: str = Form(...),
              genre: str = Form(...),
              desired_genre : str = Form(...),
              country : str = Form(...),
              city : str = Form(...),
              description: str = Form(...),
              db: Session = Depends(get_db)):

    result = Book(title=title,
                  country=country,
                  city = city,
                  description=description,
                  genre = genre, 
                  desired_genre=desired_genre, 
                  )

    db.add(result)
    db.commit()
    db.refresh(result)
    return TEMPLATES.TemplateResponse('post_added.html', context={'request': request})


# Pgae accueil / display the books
@app.get("/Accueil")
async def get_posts(request:Request):
    cursor.execute("SELECT * FROM Books")
    posts = cursor.fetchall()
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "books": posts},
    )








