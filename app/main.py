from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi import Body
from pydantic import BaseModel
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="Sahilgarg@1",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.get("/sqlalchmy")
# def text_post(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}


@app.get("/posts")
async def login(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts;")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"message": "Hell x", "data": posts}


@app.post("/createPost", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     "INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"return": new_post}


@app.get("/post/{id}")
async def getpost(id: int, res: Response, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * from posts WHERE id = %s ", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return {"post_details": post}


@app.delete("/post/{id}")
def delete_Post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is not None:
        post.delete(synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )


@app.put("/post/{id}")
async def update_Post(
    id: int, post: Post, response: Response, db: Session = Depends(get_db)
):
    # cursor.execute(
    #     "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING *",
    #     (post.title, post.content, post.published, id),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    check_post = post_query.first()
    if check_post is not None:
        post_query.update(post.model_dump(), synchronize_session=False)
        db.commit()
        return {"message": "updated successfully", "data": post_query.first()}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
