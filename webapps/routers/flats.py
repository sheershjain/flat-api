from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from models import Flats, Users
from sqlalchemy.orm import Session
from database import get_db
from jose import jwt
from config import setting
from datetime import datetime
from typing import Optional


router = APIRouter(include_in_schema=False)

templates= Jinja2Templates(directory="templates")

@router.get("/", tags=["HomePage"])
def home_page(request: Request, db: Session = Depends(get_db), msg: str = None):
    flats = db.query(Flats).all()
    return templates.TemplateResponse(
        "flat_homepage.html", {"request": request, "flats": flats, "msg": msg}
    )

@router.get("/detail/{id}")
def flat_detail(request: Request, id: int, db: Session = Depends(get_db)):
    flat = db.query(Flats).filter(Flats.id == id).first()
    return templates.TemplateResponse(
        "flat_detail.html", {"request": request, "flat": flat}
    )

@router.get("/create-an-flat")
def create_an_flat(request: Request):
    return templates.TemplateResponse("create_flat.html", {"request": request})

@router.post("/create-an-flat")
async def create_an_flat(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    floor_no = form.get("floor_no")
    rooms = form.get("rooms")
    halls = form.get("halls")
    monthly_rent = form.get("monthly_rent")
    description = form.get("description")
    errors = []
    if not description or len(description) < 10:
        errors.append("Description should be > 10 chars")
    if len(errors) > 0:
        return templates.TemplateResponse(
            "create_flat.html", {"request": request, "errors": errors}
        )
    try:
        token = request.cookies.get("access_token")
        if not token:
            errors.append("Kindly Authenticate first by login")
            return templates.TemplateResponse(
                "create_flat.html", {"request": request, "errors": errors}
            )
        scheme, _, param = token.partition(" ")
        payload = jwt.decode(param, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
        email = payload.get("sub")
        if email is None:
            errors.append("Kindly login first, you are not authenticated")
            return templates.TemplateResponse(
                "create_flat.html", {"request": request, "errors": errors}
            )
        else:
            user = db.query(Users).filter(Users.email == email).first()
            if user is None:
                errors.append("You are not authenticated, Kindly Login")
                return templates.TemplateResponse(
                    "create_flat.html", {"request": request, "errors": errors}
                )
            if user.email=="sheersh@gkmit.co":
                flat = Flats(
                    floor_no = floor_no,
                    rooms = rooms,
                    halls = halls,
                    monthly_rent = monthly_rent,
                    description = description,
                    owner_id = "sheersh@gkmit.co",
                )
                db.add(flat)
                db.commit()
                db.refresh(flat)
                print(flat.id)
                return responses.RedirectResponse(
                    f"/detail/{flat.id}", status_code=status.HTTP_302_FOUND
                )
            else:
                errors.append("You are not the owner, Only owners are allowed to change")
                return templates.TemplateResponse(
                    "create_flat.html", {"request": request, "errors": errors}
                )

    except Exception as e:
        errors.append("Something is wrong !")
        print(e)
        return templates.TemplateResponse(
            "create_flat.html", {"request": request, "errors": errors}
        )

@router.get("/delete-flat")
def show_flats_to_delete(request: Request, db: Session = Depends(get_db)):
    errors = []
    token = request.cookies.get("access_token")
    if token is None:
        errors.append("Kindly Login/Authenticate")
        return templates.TemplateResponse(
            "show_flats_to_delete.html", {"request": request, "errors": errors}
        )
    else:
        try:
            scheme, _, param = token.partition(" ")
            payload = jwt.decode(
                param, setting.SECRET_KEY, algorithms=setting.ALGORITHM
            )
            email = payload.get("sub")
            if email=="sheersh@gkmit.co":
                flats = db.query(Flats).all()
                return templates.TemplateResponse(
                    "show_flats_to_delete.html", {"request": request, "flats": flats}
                )
            else:
                errors.append("Only Owners are allowed to delete flat details")
                return templates.TemplateResponse(
                    "show_flats_to_delete.html", {"request": request, "errors": errors}
                )
        except Exception as e:
            print(e)
            errors.append("Something is wrong!!, May be you are not Authenticated")
            return templates.TemplateResponse(
                "show_flats_to_delete.html",
                {"request": request, "errors": errors},
            )