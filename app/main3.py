from os import stat
from sqlite3 import Cursor
from xml.dom import IndexSizeErr
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from urllib3 import Retry
import psycopg
from psycopg.rows import dict_row
import time
from sqlalchemy.orm import Session
from . import models
from . database import engine, SessionLocal
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/sqlalchemy")
def test_posts(db:Session = Depends(get_db)):
    return {"Status:" : "success"}




class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:                         #Loop to keep connecting to DB

    try:                            # Try to connect to DB using psycopg package
        conn = psycopg.connect(host='localhost', port=31404, dbname='fastapi', user='postgres', password='Muhammad', row_factory=dict_row)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:      # Output Error on issues connecting to DB
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(3)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == (int(id)):
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/posts")

def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
#   We dont use the below method because it is prone to SQL injection. As some one can put in SQL commands inside the contents directly. Instead we save the values in Variable/place holder 1st then let pyscopg package handle the request.

#    cursor.execute(f"INSERT INTO posts (title, content, published) VALUES({post.title},{post.content},{post.published})")

    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published) )
# SQL RETURNING above will not output . It has to be fetched from as shown below
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}
# title str, content


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail post": post}



@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("SELECT * FROM posts WHERE id = %s ;", [id] )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail= f"post with id: {id} was not found")
#        response.status_code = status.HTTP_404_NOT_FOUND
#        return {"message": f"post with id: {id} was not found"}

#    return {"post detail": f"Here is post {id}"}
    return {"post detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    delete_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""", (post.title, post.content,post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()     
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    return {'data:': updated_post}


while True:                         #Loop to keep connecting to DB

    try:                            # Try to connect to DB using psycopg package
        conn = psycopg.connect(host='localhost', port=31404, dbname='fastapi', user='postgres', password='Muhammad', row_factory=dict_row)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:      # Output Error on issues connecting to DB
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(3)