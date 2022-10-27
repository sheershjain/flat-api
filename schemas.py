from pydantic import BaseModel, EmailStr
from datetime import date
class Createuser(BaseModel):
    email: EmailStr
    password: str

class Createflat(BaseModel):
    floor_no: int
    rooms : int
    halls : int
    monthly_rent : str
    description : str


class Showuser(BaseModel):
    id : int
    email: EmailStr
    is_active: bool
    
    class Config:
        orm_mode=True

class Showflat(BaseModel):
    id : int
    floor_no: int
    rooms : int
    halls : int
    monthly_rent : str
    date_posted : date
    description : str
        
    class Config:
        orm_mode=True

