from fastapi import HTTPException, Path, status
from typing import List
from schemas import BookModel
from db import Session,Book
from sqlalchemy import select
from main import app

@app.get("/get_books", response_model=List[BookModel])
async def get_books():
    with Session() as session:
        books = session.query(Book).all()
        return books


@app.post("/add_book")
async def add_book(data:BookModel):
    with Session() as session:
        book = Book(
            title=data.title,
            author=data.author,
            year=data.year,
            quantity=data.quantity,
        )
        session.add(book)
        session.commit()
    return {"message": "Book added successfully"}


@app.get("/books/{id}", response_model=BookModel)
async def get_book(id: int = Path(...)):
    with Session() as session:
        book = session.scalar(select(Book).where(Book.id == id))
        if book:
            return book
        raise HTTPException(status_code=404, detail="Book not found")