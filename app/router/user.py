from fastapi import HTTPException, Response, status, Depends, APIRouter
from .. import models, schema, utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def createuser(user: schema.UserCreate, db: Session = Depends(get_db)):
    # hash the password
    hashed_password = utils.hash(user.password)
    print(hashed_password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/getUser/{id}", response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} was not found",
        )
    return user
