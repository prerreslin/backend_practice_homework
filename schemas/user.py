from pydantic import BaseModel,Field,constr,EmailStr,validator
import re

class UserModel(BaseModel):
    first_name: constr(min_length=2, pattern="^[A-Za-z]+$") = Field("")
    last_name: constr(min_length=2, pattern="^[A-Za-z]+$") = Field("")
    email: EmailStr
    password: str = Field("")
    phone_number: constr(pattern=r"^\+?1?\d{9,15}$") = Field("")
    has_permission:bool

    @validator('password')
    def validate_password(cls, value):
        if (len(value) < 8 or
            not re.search(r"[A-Z]", value) or
            not re.search(r"[!@#$%^&*(),.?\":{}|<>_]", value)):
            raise ValueError("Password must be at least 8 characters long, containing an uppercase letter and a special character.")
        return value