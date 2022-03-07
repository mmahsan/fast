from distutils.ccompiler import new_compiler
from enum import auto

from multiprocessing import synchronize
from operator import mod
from os import stat
from pyexpat import model

from sqlite3 import Cursor
from statistics import mode
from xml.dom import IndexSizeErr
from chardet import detect_all
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.param_functions import Body

from typing import Optional, List
from random import randrange
from urllib3 import Retry
import psycopg
from psycopg.rows import dict_row
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from . database import engine, get_db



models.Base.metadata.create_all(bind=engine)

app = FastAPI()



my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == (int(id)):
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/posts", response_model=List[schemas.Post])

def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    
    return posts



@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
 #  new_post = models.Post(title=post.title, content=post.content, published=post.published)
 #  By adding **post.dict() we can shorten writing the whole table statements.
 #  We  unpack the dictionory with ** 
 
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
# title str, content


@app.get("/posts/latest", response_model=schemas.Post)
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail post": post}



@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id== id).first()
 
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail= f"post with id: {id} was not found")
#        response.status_code = status.HTTP_404_NOT_FOUND
#        return {"message": f"post with id: {id} was not found"}

#    return {"post detail": f"Here is post {id}"}
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id== id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post.delete(synchronize_session = False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()



@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #hash the password -- user.password
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
 

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"User with id: {id} does not exist")
       
    
    return user