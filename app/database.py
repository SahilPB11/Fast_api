from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

password = "Sahilgarg@1"
encoded_password = quote_plus(password)
SQLALCHAMY_DATABASE_URL = f"postgresql://postgres:{encoded_password}@localhost/fastapi"

engine = create_engine(SQLALCHAMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
