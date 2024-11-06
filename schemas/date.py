from pydantic import BaseModel,validator,Field
from datetime import date,timedelta

class DateModel(BaseModel):
    data:str = Field(...,example=date.today()+timedelta(days=1))

    @validator("data")
    def data_valid(cls,value):
        parsed_date = date.fromisoformat(value)
        if parsed_date and parsed_date < date.today():
            return None
        elif parsed_date == date.today():
            return parsed_date + timedelta(days=1)
        return parsed_date