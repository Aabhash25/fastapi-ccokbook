# What is FastAPI and what Python feature does it rely heavily on?

# -> Fast Api is a framework that is used to build Restful APIs quickly. Fast Api heavily relies on python type hints/
# Eg - def get_user(user_id: int, active: bool = True)

# How is FastAPI different from Flask or Django REST Framework?

# -> 1. Speed and Performance : built on starlette and Pydantic, designed for high performance async apis.
# 2. Data Validation : uses Pydantic for data validation and serialization.
# 3. Automatic Interactive Documentation : generates interactive API docs using Swagger UI and ReDoc.

# Write a simple FastAPI app with a single GET endpoint /hello returning "Hello FastAPI".

# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/hello")
# async def get_hello():
#     return "Hello Fastapi"

# Create a route /items/{item_id} that accepts an integer item ID and returns it in JSON.
# Add validation so that item_id must be greater than 0.
# from fastapi import FastAPI, Path

# app = FastAPI()


# @app.get("/items/{items_id}")
# async def get_iterm(
#     items_id: int = Path(
#         ..., gt=0, description="The ID of the item to retrieve, must be greater than 0"
#     )
# ):
#     return {"item_id": items_id}

# Create a route /users/{username} where username must be a string with at least 3 characters.

# from fastapi import FastAPI, Path

# app = FastAPI()


# @app.get("/users/{username}")
# async def get_username(
#     username: str = Path(
#         ..., min_length=3, description="The username must be at least 3 characters long"
#     )
# ):
#     return {"username": username}

# Make an endpoint /search that requires a query parameter q and an optional parameter limit (default = 10).

# from fastapi import FastAPI, Query

# app = FastAPI()


# @app.get("/search")
# async def search(
#     q: str = Query(..., description="The search query string"),
#     limit: int = Query(10, description="The number of results to return"),
# ):
#     return {"query": q, "limit": limit}


# Create an endpoint /products that allows a query parameter available: bool and returns a filtered result.

# from fastapi import FastAPI

# app = FastAPI()
# products = [
#     {"id": 1, "name": "Laptop", "available": True},
#     {"id": 2, "name": "Mouse", "available": False},
#     {"id": 3, "name": "Keyboard", "available": True},
# ]


# @app.get("/products")
# async def get_products(available: bool):
#     filtered = [p for p in products if p["available"] == available]
#     return {"products": filtered}

# Add validation to restrict a query parameter price so it cannot be negative.
# from fastapi import FastAPI, Query

# app = FastAPI()


# @app.get("/products_by_price")
# async def get_products(
#     price: float = Query(..., ge=0, description="Price must be non-negative")
# ):
#     return {"price": price}


# Define a User Pydantic model with fields: name(str), age(int), email(str).

# from fastapi import FastAPI
# from pydantic import BaseModel, Field, EmailStr

# app = FastAPI()


# class User(BaseModel):
#     name: str
#     age: int = Field(..., ge=18, description="Age must be at least 18")
#     email: EmailStr


# @app.get("/user")
# async def get_user():
#     user = User(name="John Doe", age=30, email="aabhsash@gmail.com")
#     return user


# @app.post("/user")
# async def create_user(user: User):
#     return user


# Create a Blog model with title, content, and optional tags list. Add an endpoint /blogs/create.

# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List, Optional

# app = FastAPI()


# class Blog(BaseModel):
#     title: str
#     content: str
#     tags: Optional[List[str]] = None  # Optional list of tags


# @app.post("/blogs/create")
# async def create_blog(blog: Blog):
#     return blog


# Create a response model that hides the user email when sending client responses.

# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()


# class User(BaseModel):
#     name: str
#     age: int
#     email: str


# class UserResponse(BaseModel):
#     name: str
#     age: int


# @app.get("/users/{user_id}", response_model=UserResponse)
# async def get_user(user_id: int):
#     user = User(name="John Doe", age=30, email="aabhash25@gmail.com")
#     return user

# Build a /profile endpoint where the request contains full data but response returns only:

# name
# age

# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()


# class Profile(BaseModel):
#     name: str
#     age: int
#     email: str
#     address: str
#     password: str


# class ProfileResponse(BaseModel):
#     name: str
#     age: int


# @app.post("/profile", response_model=ProfileResponse)
# async def create_profile(profile: Profile):
#     return profile

# Create a list response model that returns a list of items, each containing id and title.

# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List

# app = FastAPI()


# class Item(BaseModel):
#     id: int
#     title: str


# items_data = [
#     {"id": 1, "title": "Item One"},
#     {"id": 2, "title": "Item Two"},
#     {"id": 3, "title": "Item Three"},
# ]


# @app.get("/items", response_model=List[Item])
# async def get_items():
#     return items_data


# Write an endpoint that raises an HTTP 404 error when an item is not found.

# from fastapi import FastAPI, HTTPException

# app = FastAPI()

# items = {
#     1: {"name": "Item One", "description": "This is item one"},
#     2: {"name": "Item Two", "description": "This is item two"},
# }


# @app.get("/items/{item_id}")
# def get_item(item_id: int):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return items[item_id]

# Customize an HTTPException response message.

# from fastapi import FastAPI, HTTPException

# app = FastAPI()


# @app.get("/item/{item_id}")
# def get_item(item_id: int):
#     if item_id != 1:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Item with ID {item_id} not found. Please check the ID and try again.",
#             headers={"X-Error": "ItemNotFound"},
#         )
#     return {"item_id": item_id, "name": "Sample Item"}

# Create a global exception handler for generic exceptions returning a custom JSON message.


# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse

# app = FastAPI()


# # Global exception handler
# @app.exception_handler(Exception)
# async def global_exception_handler(request: Request, exc: Exception):
#     return JSONResponse(
#         status_code=500,
#         content={
#             "error": "Internal Server Error",
#             "message": "Something went wrong on the server.",
#             "path": str(request.url),
#         },
#     )


# @app.get("/divide")
# def divide(a: int, b: int):
#     return {"result": a / b}  # dividing by zero triggers the global handler

# Why is return HTTPException(...) wrong? What is the correct way to raise it?

# Fast api expects HTTP exceptions to be raised not returned
# returning it will not trigger the exception hjandler
# The correct way is to use the raise keyword:
# raise HTTPException(status_code=404, detail="Item not found")


# Create a router in a separate Python file named items_router.py.

# Add it to the main FastAPI app using include_router.

# Create two router routes:

# /items (GET) → returns all items

# /items/{id} (GET) → returns one item

# from fastapi import FastAPI
# from items_routers import router as items_router

# app = FastAPI()
# app.include_router(items_router)
