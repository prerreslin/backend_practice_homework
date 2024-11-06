from pydantic import BaseModel
from typing import List, Optional

class BookModel(BaseModel):
    id: int
    title: str
    author: str
    year: Optional[int] = None
    quantity: Optional[int] = None