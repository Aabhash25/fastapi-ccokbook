from fastapi import FastAPI

app = FastAPI()

# @app.get("/books/{book_id}")
# async def read_book(
#     book_id: int,
# ):  # Here we are using type hint and automatic data validation
#     return {"book_id": book_id, "title": "The Great Gatsby", "author": "Random Author"}

# @app.get("/author/{author_id}")
# async def read_author(author_id: int):
#     return {"author_id": author_id, "name": "Ernest Hemingway"}

# @app.get("/books")
# async def read_books(
#     year: int = None,
# ):  # Here, year is an optional query parameter. By assigning none as default value we make it optional.
#     if year:
#         return {"year": year, "books": ["Book1", "Book 2"]}
#     return {"books": ["All Books"]}

from models import Book


@app.post("/book")
async def create_book(book: Book):
    return book


# from pydantic import BaseModel

# class BookResponse(BaseModel):
#     title: str
#     author: str
#     id: int

# @app.get("/allbooks")
# async def read_all_books() -> list[BookResponse]:
#     return [
#         {"id": 1, "title": "1984", "author": "Mr X"},
#         {
#             "id": 1,
#             "title": "The Great Gatsby",
#             "author": "F.Scott Fitzgerald",
#         },
#     ]

# from fastapi import FastAPI, HTTPException
# from starlette.responses import JSONResponse

# app = FastAPI()


# @app.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=exc.status_code, content={"message": "Oops, Somehting went wrong"}
#     )


# @app.get("/error_endpoint")
# async def raise_exception():
#     raise HTTPException(status_code=400)

import json

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return PlainTextResponse(
        "This is a plain text response:" f"\n{json.dumps(exc.errors(),indent=2)}",
        status_code=status.HTTP_400_BAD_REQUEST,
    )
