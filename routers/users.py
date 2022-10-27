from fastapi import APIRouter, Depends
from schemas import Createuser, Showuser
from database import get_db
from hashing import Hasher
from sqlalchemy.orm import Session
from models import Users
router=APIRouter()


@router.get("/users",tags=["Users"])
def read_users():
    return [{"message": "hello Users"}]

@router.post("/users",tags=["Users"],response_model=Showuser)
def create_users(user: Createuser, db: Session=Depends(get_db)):
    user=Users(email=user.email, password=Hasher.get_password_hash(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user