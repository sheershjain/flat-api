
from enum import unique
from sqlalchemy import Column, Integer, String , ForeignKey, Boolean , Date
from database import Base
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ =  "users"

    id = Column(Integer,primary_key = True)
    email = Column(String,nullable= False,unique=True)
    password = Column(String,nullable= False)
    is_active = Column(Boolean, default=True)
    

class Flats(Base):
    __tablename__ =  "flats"

    id = Column(Integer,primary_key = True,index=True)
    floor_no = Column(Integer)
    rooms = Column(Integer )
    halls = Column(Integer )
    monthly_rent = Column(String,nullable= False)
    date_posted =Column(Date)
    owner_id = Column(String)
    description = Column(String,nullable= False)

    