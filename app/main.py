from typing import Optional
from fastapi import FastAPI
from fastapi import Body
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .router import user, post, auth

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

    published: bool = True


app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
