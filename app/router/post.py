from typing import List
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from .. import models, schema, outh2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schema.PostResponse])
async def login(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts;")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schema.PostResponse,
)
def create_post(
    post: schema.PostCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(outh2.get_current_user),
):
    # cursor.execute(
    #     "INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    print(user_id)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get(
    "/{id}",
    response_model=schema.PostResponse,
)
def getpost(id: int, res: Response, db: Session = Depends(get_db), user_id: int = Depends(outh2.get_current_user)):
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
    return post


@router.delete("/{id}")
def delete_Post(
    id: int,
    response: Response,
    db: Session = Depends(get_db),
    user_id: int = Depends(outh2.get_current_user),
):
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


@router.put("/{id}", response_model=schema.PostResponse)
def update_Post(
    id: int,
    post: schema.PostCreate,
    response: Response,
    db: Session = Depends(get_db),
    user_id: int = Depends(outh2.get_current_user),
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
        post_query.update(post.model_dump(), synchronize_session=False)  # type: ignore
        db.commit()
        return post_query.first()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
