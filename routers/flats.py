from fastapi import APIRouter, Depends , HTTPException,status
from database import get_db
from typing import List
from schemas import Createflat,Showflat
from models import Flats , Users
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from routers.login import oauth2_scheme
from jose import jwt
from config import setting

router=APIRouter()


# @router.post("/items",tags=["Items"], response_model=Showitem)
# def create_items(item: CreateItem , db: Session= Depends(get_db),token:str=Depends(oauth2_scheme)):
 
#     try:
#         payload=jwt.decode(token, 'SHEERSH', algorithms=['HS256'])
#         username=payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials1")
#         user=db.query(Users).filter(Users.email==username).first()
#         if user is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials2")
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials3")
#     date=datetime.now().date()
#     owner_id=user.id
#     item=Items(**item.dict(),date_posted=date, owner_id=owner_id) 
#     db.add(item)
#     db.commit()
#     db.refresh(item)
#     return item

def get_user_from_token(db, token):
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, setting.ALGORITHM)
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate Credentials",
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate Credetials",
        )
    user = db.query(Users).filter(Users.email == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    if user.email=="sheersh@gkmit.co":
        return user
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the owner (unauthorized)",
        )


@router.post("/flat", tags=["Flats"], response_model=Showflat)
def create_flat(
    flat: Createflat, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    user = get_user_from_token(db , token)
    owner_id=user.email
    flat = Flats(**flat.dict(), date_posted=datetime.now().date(), owner_id=owner_id)
    db.add(flat)
    db.commit()
    db.refresh(flat)
    return flat

@router.put("/flats/{id}",tags=["Flats"] )
def update_flat(id: int , obj: Createflat , db: Session= Depends(get_db),token:str=Depends(oauth2_scheme)):
    user = get_user_from_token(db, token)
    existing_flat = db.query(Flats).filter(Flats.id == id)
    if existing_flat.first() is None:
        return {"message": f"No Details found for Flat ID {id}"}
    if existing_flat.first().owner_id == user.id:
        # ref.update(jsonable_encoder(obj))
        existing_flat.update(obj.__dict__)
        db.commit()
        return {"message" : "Flat detail updated successfully"}
    else:
        return {"message": "You are not authorized"}

# @router.delete("/items/{id}",tags=["Items"] )
# def delete_items(id: int , db: Session= Depends(get_db)):
#     ref=db.query(Items).filter(Items.id==id)
#     if not ref.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Item with id {id} not exist")
#     ref.delete()
#     db.commit()
#     return {"message" : "Item deleted successfully"}

@router.delete("/flat/delete/{id}", tags=["Flats"])
def delete_flat_by_id(
    id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    user = get_user_from_token(db, token)
    existing_flat = db.query(Flats).filter(Flats.id == id)
    if not existing_flat.first():
        return {"message": f"No Details found for Flat ID {id}"}
    if existing_flat.first().owner_id == user.email:
        existing_flat.delete()
        db.commit()
        return {"message": f"Flat ID {id} has been successfully deleted"}
    else:
        return {"message": "You are not authorizedx"}


@router.get("/flats/all",tags=["Flats"], response_model=List[Showflat])
def read_flats(db: Session= Depends(get_db)):
    flats=db.query(Flats).all()
    return flats

@router.get("/flats/{id}",tags=["Flats"], response_model=Showflat)
def read_flat(id: int, db: Session= Depends(get_db)):
    flat=db.query(Flats).filter(Flats.id==id).first()
    if not flat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Flat with id {id} not exist")
    return flat

