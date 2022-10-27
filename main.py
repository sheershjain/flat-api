from fastapi import FastAPI
from config import setting
from database import engine
from models import Base
from routers import flats, users, login
from webapps.routers import flats as web_items, user , auth
from fastapi.staticfiles import StaticFiles
# We are using Alembic migrations
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=setting.title,
    description=setting.description,
    version=setting.version,
    terms_of_service=setting.terms_of_service,
    contact=setting.contact,
    license_info=setting.license_info,
    openapi_tags=setting.tags_metadata
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(flats.router)
app.include_router(login.router)
app.include_router(web_items.router)
app.include_router(user.router)
app.include_router(auth.router)
