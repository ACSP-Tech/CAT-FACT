from .general import StrictBaseModel as BaseModel
from pydantic import EmailStr
import datetime

class MeUser(BaseModel):
    email: EmailStr
    name: str
    stack: str

class MeOut(BaseModel):
    status: str
    user: MeUser
    timestamp: datetime
    fact: str