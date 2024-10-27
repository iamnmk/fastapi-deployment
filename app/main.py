from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime

app = FastAPI(title="BookStore API", 
             description="A simple API to demonstrate FastAPI deployment",
             version="1.0.0")

class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    price: float
    published_date: str

# Simulate a database with a list
books_db = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "price": 9.99,
        "published_date": "1925-04-10"
    },
    {
        "id": 2,
        "title": "1984",
        "author": "George Orwell",
        "price": 12.99,
        "published_date": "1949-06-08"
    }
]

@app.get("/")
async def root():
    return {
        "message": "Welcome to BookStore API",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "BookStore API",
        "dependencies": {
            "database": "connected",
            "api": "running"
        }
    }

@app.get("/books", response_model=List[Book])
async def get_books():
    return books_db

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    book = next((book for book in books_db if book["id"] == book_id), None)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=Book)
async def create_book(book: Book):
    new_book = book.dict()
    new_book["id"] = max(book["id"] for book in books_db) + 1
    books_db.append(new_book)
    return new_book

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)