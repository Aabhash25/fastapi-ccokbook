# FASTAPI Learning Notes

## What is FastAPI?

FastAPI is a modern, fast web framework for building APIs with Python based on standard Python type hints.

Key features that define FastAPI are the following:

- **Speed:** It’s one of the fastest frameworks for building APIs in Python, thanks to its underlying Starlette framework for web parts and Pydantic for data handling.
- **Ease of use:** FastAPI is designed to be easy to use, with intuitive coding that accelerates your development time.
- **Automatic documentation using Swagger:** With FastAPI, the API documentation is generated automatically, a feature that is both a time-saver and a boon for developers.

## Applying Asynchronous Programming

Asynchronous Programming helps our application to handle more request simultaneously. It is a style of concurrent programming in which tasks are executed without blocking the execution of other tasks,improving the overall performance of our application. We use async await to leverage asynchronous programming.

````python
@app.get("/")
async def read_root():
    return{"Hello":"World"}

## Exploring Routers and Endpoints
### Endpoints
Endpoints are the points in which api interaction happen. In fast api, an end point is created by decorating a function with an HTTP method such as @app.get('/')

```python
from fastapi import FASTAPI
app= FASTAPI()
```

@app.get("/")
async def read_root():
    return{"message":"this is test message"}

In this snippet we define an endpoint for the root url. When a get request is made to this url, the read_root function is invoked, returning a json response
````
