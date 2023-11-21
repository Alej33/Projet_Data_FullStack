from fastapi import FastAPI, Response, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from sqlalchemy.orm import Session
from .database import engine, session, get_db
from . import models
import os
from dotenv import load_dotenv


load_dotenv("creds.env")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Book(BaseModel):
    title : str
    genre : str 
    availability : bool = True
    desired_genre : str
    description : str
    country : str
    city : str


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

# select all rows in our db
@app.get("/books")
def get_posts():
    cursor.execute("SELECT * FROM Books")
    posts = cursor.fetchall()
    return {"message": posts}


# insert a post into our database
@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_post(post : Book):
    cursor.execute(""" INSERT INTO Books (title, genre, availability, description, desired_genre, country, city) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING * """,
                    (post.title, post.genre, post.availability, post.description, post.desired_genre, post.country, post.city))
    
    created_post = cursor.fetchone()
    conn.commit()
    return {"message":created_post}


# fetch one instance with id 
@app.get("/books/{id}")
def get_post(id : int):
    cursor.execute(""" SELECT * FROM Books WHERE id = %s """, str(id))
    post = cursor.fetchone()
    if not post : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='book not found :()')
    return {f"book with id : {id}": post}   


# delete a post with id 
@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    cursor.execute(""" DELETE FROM Books where id = %s RETURNING * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='book to delete not found :()')
    return {"deleted book": deleted_post}

# update a postx with id : 
@app.put("/books/{id}")
def update_post(id : int, post: Book):
    cursor.execute(""" UPDATE Books SET title = %s, genre = %s, availability = %s, description = %s, desired_genre = %s WHERE id = %s RETURNING *""", 
                   (post.title, post.genre, post.availability, post.description, post.desired_genre, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='book to update not found :()')

    return {f"updated book with id {id}" : updated_post}


# test the orm method : 
@app.get("/sqlalchemy")
def get_posts(db : Session = Depends(get_db)):
    return {"status":"success"}





