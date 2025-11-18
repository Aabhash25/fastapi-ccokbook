# FASTAPI Learning Notes

## Table of Contents

- [First Steps With FAST API](#first-steps-with-fast-api)

## First Steps With FAST API

FastAPI is a modern, fast web framework for building APIs with Python based on standard Python type hints.

Key features that define FastAPI are the following:

- **Speed:** It’s one of the fastest frameworks for building APIs in Python, thanks to its underlying Starlette framework for web parts and Pydantic for data handling.
- **Ease of use:** FastAPI is designed to be easy to use, with intuitive coding that accelerates your development time.
- **Automatic documentation using Swagger:** With FastAPI, the API documentation is generated automatically, a feature that is both a time-saver and a boon for developers.

### Applying Asynchronous Programming

Asynchronous Programming helps our application to handle more request simultaneously. It is a style of concurrent programming in which tasks are executed without blocking the execution of other tasks,improving the overall performance of our application. We use async await to leverage asynchronous programming.

```python
@app.get("/")
async def read_root():
    return{"Hello":"World"}
```

### Exploring Routers and Endpoints

#### Endpoints

Endpoints are the points in which api interaction happen. In fast api, an end point is created by decorating a function with an HTTP method such as @app.get('/')

```python
from fastapi import FASTAPI
app= FASTAPI()

@app.get("/")
async def read_root():
return{"message":"this is test message"}

```

In this snippet we define an endpoint for the root url. When a get request is made to this url, the read_root function is invoked, returning a json response

#### Routers

When we need to handle multiple endpoints that are in different files, we can benefit from using routers. Router assist us i grouping our endpoints into differnet modules.

```python
from fastapi import FASTAPI
router = APIRouter()

@router.get("/items/{items_id}")
async def read_items(item_id: int):
    return {"item_id":item_id}
```

We can now reuse it and attach the route to the FAST api server in main.py

```python
import router_example
app = FASTAPI()
app.include_router(router_example.router)

@app.get("/")
async def read_root("/"):
    return {"Hello":"World"}

```

#### Running Your FAST API Server

Run the server using `uvicorn main:app --reload`

### Exploring automatic documentation

We can access the automatic docs at http://127.0.0.1:8000/docs for Swagger UI and http://127.0.0.1:8000/redoc for Redoc.

### Working with path and query parameters

Parameters allow nyouar api to accept input from users, making your endpoints dynamic and responsive.

#### Path Parameter

Path parameters are parts of the URL that are expected to change. For instance, in an endpoint such
as /books/{book_id}, book_id is a path parameter. FastAPI allows you to capture these
parameters effortlessly and use them in your function.

```python
@app.get("/author/{author_id}")
async def read_author(author_id: int):
    return{
        "author_id": author_id,
        "name": "Ernest Hemingway"
    }
```

Here {author_id} is a path parameter

#### Query Parameter

Query parameters are used to refine or customize the response of an API endpoint.
They can be included in the URL after a question mark (? ). For instance, /
books?genre=fiction&year=2010 might return only books that fall under the fiction
genre released in 2010.

```python
@app.get("/books")
async def read_books(year: int = None):
    if year:
        return {"year": year, "books": ["Book1", "Book 2"]}
    return {"books": ["All Books"]}
```

Here, year is an optional query parameter. By assigning None as a default value, we make it optional.
If a year is specified, the endpoint returns books from that year; otherwise, it returns all books.

When we dont provide the query parameter,http://127.0.0.1:8000/books -> it returns All Books
if we provide the path parameter, http://127.0.0.1:8000/books?year=2003 -> it returns specific books

### Defining and using Request and Response models

FASTAPI uses pydantic models to define the structure of request data and response data.These models ensure your api is validated,clean and well documented automatically.
Pydantic models are a powerful feature for data validation and conversion. They allow you to define
the structure, type, and constraints of the data your application handles, both for incoming requests
and outgoing responses.

#### Creating the model

```python
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    year:int
```

Here , Book is a pydantic bace model class with three typed fields.

#### Defining the request body

```python
In fast api , pydantic models are not just for validation. They also serve as the request body.
from models import Book


@app.post("/book")
async def create_book(book: Book):
    return book
```

In this endpoint, when a user sends a POST request to the /book endpoint with JSON data, FastAPI
automatically parses and validates it against the Book model. If the data is invalid, the user gets an
automatic error response.

#### Validating request data

Pydantic offers advanced validation features. For instance, you can add regex validations, default
values, and more:

```python
from pydantic import BaseModel, Field
class Book(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=50)
    year: int = Field(..., gt=1900, lt=2100)
```

#### Managing Respnse Formats

astAPI allows you to define response models explicitly, ensuring that the data returned by your
API matches a specific schema. This can be particularly useful for filtering out sensitive data or
restructuring the response.

```python
from pydantic import BaseModel


class BookResponse(BaseModel):
    title: str
    author: str


@app.get("/allbooks")
async def read_all_books() -> list[BookResponse]:
    return [
        {"id": 1, "title": "1984", "author": "Mr X"},
        {
            "id": 1,
            "title": "The Great Gatsby",
            "author": "F.Scott Fitzgerald",
        },
    ]
```

Here, the -> list[BookResponse] function type hint tells FastAPI to use the BookResponse
model for responses, ensuring that only the title and author fields are included in the response JSON.
Alternatively, you can specify the response type in the endpoint decorator’s arguments as follows:

```python
@app.get("/allbooks", response_model= list[BookResponse])
async def read_all_books() -> Any:
# rest of the endpoint content
```

#### Handling Errors and Exceptions

FastAPI provides built-in support for handling exceptions and errors.
When an error occurs, FastAPI returns a JSON response containing details about the error, which is
very useful for debugging. However, there are situations where you might want to customize these
error responses for better user experience or security

We can create a custom error handler that catches a specific type of error and returns a custom response. For instance, if a requested resource is not found, we might want to return a more friendly error message.

```python
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code, content={"message": "Oops, Somehting went wrong"}
    )
```

In this example, the http_exception_handler function will be used to handle HTTPException
errors. Whenever an HTTPException error is raised anywhere in your application, FastAPI will
use this handler to return a custom response.

In some cases we might want to customize the response for validation errors.

```python
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
```

This custom handler will catch any RequestValidationError error and return a plain text
response with the details of the error
