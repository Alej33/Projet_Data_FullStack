from fastapi import FastAPI, Response, HTTPException, status, Depends, Request, responses, Form, UploadFile, File
from pydantic import BaseModel
from typing import Optional
from random import randrange
import base64
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from sqlalchemy.orm import Session
from database import engine, session, get_db
from models import Book,Messages
import models
import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.responses import RedirectResponse
import bcrypt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



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
def form_post(request: Request) :
    return TEMPLATES.TemplateResponse('add_post.html', context={'request': request})

# thanks page for submitting a post
@app.get("join-us/Thank_you")
def redirect_post(request: Request):
    return TEMPLATES.TemplateResponse('post_added.html', context={'request': request})


# post req for adding a post
@app.post("/join-us/add-post")
def form_post(request: Request, 
              email :str = Form(...),
              title: str = Form(...),
              genre: str = Form(...),
              desired_genre : str = Form(...),
              country : str = Form(...),
              city : str = Form(...),
              description: str = Form(...),
              image : UploadFile = File(...) ,
              db: Session = Depends(get_db)):

    image_data = base64.b64encode((image.file.read())).decode("utf-8") if image else None

    result = Book(email= email,
                  title=title,
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


@app.get("/user/{email}")
async def show_user(request: Request, email: str, db: Session = Depends(get_db)):
    # Query user details based on email
    user = db.query(models.Utilisateur).filter(models.Utilisateur.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Query messages for the user
    messages = db.query(Messages).filter(Messages.receiver_email == email).all()

    return TEMPLATES.TemplateResponse(
        "user.html",
        {
            "request": request, 
            "user": user, 
            "messages": messages
        }
    )


# Displaying results w filters : 
@app.get("/")
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



@app.get("/messages")
def get_all_messages(request:Request, db: Session = Depends(get_db)):
    messages = db.query(Messages).all()
    return TEMPLATES.TemplateResponse("messages.html", context={"request": request, "messages": messages})

@app.get("/message_sent")
def notif(request:Request):
    return TEMPLATES.TemplateResponse("message_sent.html", context={"request": request})


@app.get("/login")
async def login(request:Request):
    return TEMPLATES.TemplateResponse(
        "login.html",
        context={"request": request}
    )

@app.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Utilisateur).filter(models.Utilisateur.email == form_data.username).first()
    if not user or not bcrypt.checkpw(form_data.password.encode('utf-8'), user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    response = RedirectResponse(url=f"/user/{user.email}", status_code=303)
    return response

@app.get("/register")
async def login(request:Request):
    return TEMPLATES.TemplateResponse(
        "signup.html",
        context={"request": request}
    )

@app.post("/register")
async def register_user(
    request: Request, 
    email: str = Form(...), 
    password: str = Form(...),
    nom: str = Form(...),
    country: str = Form(...),
    db: Session = Depends(get_db)
):

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    print("test")
    new_user = models.Utilisateur(email=email, nom=nom, country=country, password_hash=hashed_password, password_salt=salt)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/{book_id}")
def send_message(request:Request, book_id: int, email: str = Form(...), message: str = Form(...), db: Session = Depends(get_db)):
    # Get the book's email and other details from the database
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Create a new message
    new_message = Messages(receiver_email=book.email, sender_email=email, message=message)

    # Add the message to the database
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return TEMPLATES.TemplateResponse('post_added.html', context={"request":request})