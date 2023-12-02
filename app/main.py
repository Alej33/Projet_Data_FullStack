from fastapi import FastAPI, Response, HTTPException, status, Depends, Request, responses, Form, UploadFile, File
from pydantic import BaseModel
from typing import Optional
from random import randrange
import base64
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from sqlalchemy.orm import Session
from .database import engine, session, get_db, BookCreatePost
from .models import Book
from . import models
import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.responses import RedirectResponse



load_dotenv(".env")

#print(os.environ.get("USER"), os.environ.get("PASSWORD"))

models.Base.metadata.create_all(bind=engine)

TEMPLATES = Jinja2Templates(directory="templates")


app = FastAPI()


while True :
    try :
        conn = psycopg2.connect(host ='localhost', dbname='postgres' ,user = os.environ.get("USER"),
                                password = os.environ.get("PASSWORD"), port = 5432 ,cursor_factory=RealDictCursor)
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
              image : UploadFile = File(...) ,
              db: Session = Depends(get_db)):

    image_data = base64.b64encode((image.file.read())).decode("utf-8") if image else None
    print(image_data)

    result = Book(title=title,
                  country=country,
                  city = city,
                  description=description,
                  genre = genre, 
                  desired_genre=desired_genre, 
                  image = image_data
                  )

    db.add(result)
    db.commit()
    db.refresh(result)
    return TEMPLATES.TemplateResponse('post_added.html', context={'request': request})


# Let's add the user's page
@app.get("/user")
async def show_user(request:Request):
    cursor.execute("SELECT * FROM Books")
    posts = cursor.fetchall()
    return TEMPLATES.TemplateResponse(
        "user.html",
        {"request": request, "books":posts},
    )


# Displaying results w filters : 
@app.get("/Accueil")
async def filter_results(request:Request, 
                         genre: str = None, 
                         timeAdded : str = None):

    print(genre)

    query = "SELECT * FROM Books WHERE 1=1"

    if genre:
        if genre == 'All':
            query = "SELECT * FROM Books"
        else:  
            query += f" AND genre = '{genre}'" 

    if timeAdded == 'earliest' :
        query += f" ORDER BY created_at ASC"

    elif timeAdded == 'latest': 
        query += f" ORDER BY created_at DESC"

    print(query)

    cursor.execute(query)
    posts = cursor.fetchall()
        
    return TEMPLATES.TemplateResponse(
        "index.html",
        context={"request": request, "books": posts}
    )
