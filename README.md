# FASTAPI Learning Notes

## What is FastAPI?

FastAPI is a modern, fast web framework for building APIs with Python based on standard Python type hints.

Key features that define FastAPI are the following:

- **Speed:** It’s one of the fastest frameworks for building APIs in Python, thanks to its underlying Starlette framework for web parts and Pydantic for data handling.
- **Ease of use:** FastAPI is designed to be easy to use, with intuitive coding that accelerates your development time.
- **Automatic documentation using Swagger:** With FastAPI, the API documentation is generated automatically, a feature that is both a time-saver and a boon for developers.

## Applying Asynchronous Programming

Asynchronous Programming helps our application to handle more request simultaneously. It is a style of concurrent programming in which tasks are executed without blocking the execution of other tasks,improving the overall performance of our application. We use async await to leverage asynchronous programming.

```python
@app.get("/")
async def read_root():
    return{"Hello":"World"}
```

## Exploring Routers and Endpoints

### Endpoints

Endpoints are the points in which api interaction happen. In fast api, an end point is created by decorating a function with an HTTP method such as @app.get('/')

```python
from fastapi import FASTAPI
app= FASTAPI()

@app.get("/")
async def read_root():
return{"message":"this is test message"}

```

In this snippet we define an endpoint for the root url. When a get request is made to this url, the read_root function is invoked, returning a json response

## Routers

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

## Running Your FAST API Server

Run the server using `uvicorn main:app --reload`

## Exploring automatic documentation

We can access the automatic docs at http://127.0.0.1:8000/docs for Swagger UI and http://127.0.0.1:8000/redoc for Redoc.

## Working with path and query parameters

Parameters allow nyouar api to accept input from users, making your endpoints dynamic and responsive.

### Path Parameter

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

### Query Parameter

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
