from os import stat
from sqlite3 import Cursor
from xml.dom import IndexSizeErr
from fastapi import FastAPI, Response, status, HTTPException

from fastapi.param_functions import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

from urllib3 import Retry

import psycopg
from psycopg.rows import dict_row
import time

app = FastAPI()

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
#    print(post)
#    print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict) 
#   my_posts.append(post.dict())
    return {"data": post_dict}
# title str, content


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail post": post}



@app.get("/posts/{id}")
def get_post(id: int, response: Response):
#    print(id)
#    print(type(id))
    post = find_post(id)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail= f"post with id: {id} was not found")
#        response.status_code = status.HTTP_404_NOT_FOUND
#        return {"message": f"post with id: {id} was not found"}

#    return {"post detail": f"Here is post {id}"}
    return {"post detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # delete post
    # find index in the array that has required ID 
    # my_posts.pop(index)
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    my_posts.pop(index)
 #   return {"message": "post was successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    index = find_index_post(id)
     
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data:': post_dict}
