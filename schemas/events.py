from pydantic import Field,BaseModel,validator
from typing import Optional
from datetime import date as dat,timedelta

class EventModel(BaseModel):
    title: str
    description: Optional[str] = None
    date: dat = Field(...,example=dat.today()+timedelta(days=1))
    is_public: bool = Field(default=True)

    @validator("date")
    def data_validate(cls,value):
        if value < dat.today():
            raise ValueError(f"Date {value} cannot be in the past")
        elif value == dat.today():
            return value + timedelta(days=1)
        return value