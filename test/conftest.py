from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest


import json
import os
import sys


sys.path.append("../")
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from hashing import Hasher
from database import get_db,engine
from models import Base, Users
from config import setting
from schemas import Createuser

SQLALCHEMY_DATABASE_URL='sqlite:///test.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close() 
    
    app.dependency_overrides[get_db]=override_get_db
    client=TestClient(app)
    yield client 

# @pytest.fixture
# def token_header(client : TestClient):
#     test_email="sheersh@gkmit.co"
#     test_pass="sheersh"
#     db=TestingSessionLocal()
#     user=db.query(Users).filter(Users.email==test_email).first()
#     if user is None:
#         user=Users(email=test_email, password=test_pass)
#         db.add(user)
#         db.commit()
#         db.refresh(user)
#     data={"username" : test_email, "password" : test_pass}
#     response=client.post("/login/token" , data = data)
#     token=response.json()["access_token"]
#     return {"Authorization" : f"Bearer {token}"}

@pytest.fixture
def token_headers(client: TestClient):
    test_email = setting.TEST_EMAIL
    test_password = setting.TEST_PASS
    data = {"username": test_email, "password": test_password}
    response = client.post("/login/token", data=data)
    token = response.json()["access_token"]
    print(token)
    return {"Authorization": f"Bearer {token}"}