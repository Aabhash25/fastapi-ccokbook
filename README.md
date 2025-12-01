# FASTAPI Learning Notes

## Table of Contents

- [First Steps With FAST API](#first-steps-with-fast-api)
- [SQL Alchemy With FAST API GUIDE](#sql-alchemy-with-fast-api-guide)
- [Working With Data](#working-with-data)
- [Building RESTful APIs with FastAPI](#Building-restful-apis-with-fastapi)

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

#### Exploring automatic documentation

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

### FASTAPI APPLICATION (main.py)

#### Step 1: Import Dependencies

```python
from fastapi import Depends,FastAPI,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal,User
```

#### Step 2: Database Dependency Function

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally db.close
```

Creates new database session
Yield the session (gives it to the rout function)
Automatically closes the session when done (even if error occur)

### Dependency Injection

Instead of creating database connections manually in each route:

```python
# ❌ Without dependency injection
@app.get("/users/")
def read_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users
```

We use Depends() to inject it automatically:

```python
# ✅ With dependency injection
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

### CRUD OPERATIONS

#### CREATE- ADD NEW USER

```python
class UserBody(BaseModel):
    name: str
    email: str

@app.post("/user")
def add_new_user(user: UserBody, db: Session = Depends(get_db)):
    # Create ORM object
    new_user = User(name=user.name, email=user.email)

    # Add to session (staged for insertion)
    db.add(new_user)

    # Commit to database (actually inserts)
    db.commit()

    # Refresh to get auto-generated ID
    db.refresh(new_user)

    return new_user
```

#### Read- READ USER

```python
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

#### Read specific user

```python
@app.get("/user")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User Not Found")

    return user
```

#### Update

```python
@app.post("/user/{user_id}")
def update_user(user_id: int, user: UserBody, db: Session = Depends(get_db)):
    # Find existing user
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields
    db_user.name = user.name
    db_user.email = user.email

    # Save changes
    db.commit()

    # Refresh to get latest data
    db.refresh(db_user)

    return db_user
```

#### Delete

```python
@app.delete("/user")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not Found")

    # Delete from database
    db.delete(db_user)
    db.commit()

    return {"details": "User deleted"}
```

## Working With Data

Data handling forms the backbone of any web application which helps in integrating, managing, and optimizing data storage using both SQL and NoSQL databases.

### Setting Up SQL Databases

SQL is the standard language for managing and manipulating relational databases. When combined with Fast A[PI, it unlocks a world of possibliies in data storage and retrieval.
Fast API's compatibility with SQL databases is facilitiated through ORMs . The most popular one is SQLAlchemy
`pip install sqlalchemy`
SQlAlchemy acts ad the bridge between the python code and the database, allowing us to interact with the database using Python classes and objects rather than writing raw SQL queries.
In SQLAlchemy, models are typically6 defined using classes, with each class corresponding to a table in the database, and each attribute of the class corresponding to a coloumn in the table.

1. Create a folder called sql_example and create a file name database.py

```python
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase)
    pass
```

To define a model in SQL Alchemy, you need to create a base class that derives from the Declarative Base Class. This Base class maiontains a catalog of classes and tables you have defined and is central to SQLAlchemy's ORM functionality.

2. Once you have your base class , you can start defininf your models. For instance, if you have a table for users, your model might look something like this

```python
from sqlalchemy.orm import(
    Mapped,
    mapped_coloumn
)
class User(Base):
    __tablename__= "user"
    id: Mapped[int]= mapped_coloumn(
        primary_key=True
    )
    name: Mapped[str]
    email: Mapped[str]
```

In this model, User class corresponds to a table named user in the database, with columns
for id, name, and email. Each class attribute specifies the data type of the column

3. Once your models have been defined, the next step is to connect to the database and create
   these tables. SQLAlchemy uses a connection string to define the details of the database it needs
   to connect to. The format of this connection string varies depending on the database system
   you are using.
   For example, a connection string for a SQLite database might look like this:
   `DATABASE_URL = "SQLITE:///./TEST.DB`
   SQLite is a lightweight, file-based database that doesn’t require a separate server process. It’s
   an excellent choice for development and testing.
4. No further setup is required for SQLite as it will automatically create the test.db database
   file the first time you connect to it.
   You will use the DATABASE_URL connection string to create an Engine object in SQLAlchemy
   that represents the core interface to the database:

```python
from sqlalchemy import create_engine
engine= create_engine(DATABASE_URL)
```

5. With the engine created, you can proceed to create your tables in the database. You can do this
   by passing your base class and the engine to SQLAlchemy’s create_all method

```python
Base.metadata.create_all(bind=engine)
```

Now that you’ve defined all the abstractions of the database in your code, you can proceed with setting
the database connection.

#### Establishing a database connection

The final part of setting up a SQL database setup is establishing a database connection. This connection
allows your application to communicate with the database, executing queries and retrieving data.
Database connections are managed with sessions. A session in SQLAlchemy represents a workspace
for your objects, a place where you can add new records or fetch existing ones. Each session is bound
to a single database connection.
To manage sessions, we need to create a SessionLocal class. This class will be used to create and
manage session objects for the interactions with the database. Here’s how you can create it:

```python
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
```

The sessionmaker function creates a factory for sessions. The autocommit and autoflush
parameters are set to False, meaning you have to manually commit transactions and manage them
when your changes are flushed to the database.
With the SessionLocal class in place, you can create a function that will be used in your FastAPI
route functions to get a new database session. We can create it in the main.py module like so:

```python
from database import SessionLocal
def get_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

In your route functions, you can use this function as a dependency to communicate with
the database.
In FastAPI, this can be done with the Depends class. In the main.py file, you can then add an endpoint:

```python
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from database import SessionLocal
app = FastAPI()
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

This approach ensures that a new session is created for each request and closed when the request is
finished, which is crucial for maintaining the integrity of your database transactions.
You can then run the server with the following command:
`uvicorn main:app --reload`
If you try to call the endpoint GET at localhost:8000/users you will get an empty list since
no users have been added already.

#### Understanding CRUD Operation with SQL Alchemy

After setting up your SQL database with FastAPI, the next crucial step is creating database models. This
process is central to how your application interacts with the database. Database models in SQLAlchemy
are essentially Python classes that represent tables in your SQL database. They provide a high-level,
object-oriented interface to manipulate database records as if they were regular Python objects.

##### Creating a new user

```python
class UserBody(BaseModel):
    name: str
    email: str
@app.post("/user")
def add_new_user(
    user: UserBody,
    db: Session = Depends(get_db)
):
    new_user = User(
        name=user.name,
        email=user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
```

##### Reading a specific user

```python
@app.get("/user")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user
```

##### Updating a user

```python
@app.post("/user/{user_id}")
def update_user(user_id: int, user: UserBody, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user
```

#### Deleting a user

```python
@app.delete("/user")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    db.delete(db_user)
    db.commit()
    return {"details": "User deleted"}
```

## SQL Alchemy With FAST API GUIDE

### Database Configuration(database.py)

#### Step 1: Create Base Class

```python
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
```

DeclarativeBase is the foundation of all ORM models
All your database models will inherit from this Base Class
It provides the machinery to map python classes to database tables

#### Step 2: Define ORM Model

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

```python
class User(Base):
    __tablename__="user"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]
    email:Mapped[str]
```

**tablename** : specifies the actual table name in the database
Mapped[int] : type annotation tellin python/sql alchemy the expected type
mapped_column() : defines column properties
primary_key= True : Maked this colum the priomary key
Mapped[str] : String columns(automatically becomes VARCHAR in SQL)

#### Step 3: Database URL Configuration

```python
DATABASE_URL="sqlite:///./test.db"
```

sqllite : Database type
test.dv - file name

#### Step 4 : Create Database Engine

```python
from sqlalchemy import create_engine
engine=create_engine(DATABASE_URL)
```

creates a connection pool to the database
handle all low level database communication
manages connections efficiently

#### Step 5 : Create Tables

```python
Base.metadata.create_all(bind_engine)
```

Reads all models that inherit from the Base
Creates corresponding tables in the database
Only creates tables that dont exist(safe to run multiple times)

#### Step 6 : Session Factory

```python
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

Creeates a factory for database sessions
Session: a workspace for database operations
autocommit=False : Changes aren't saved untill you call db.commit()
autoflush=Fales : Don't automatically sync changes to database
bind=engine : Connect sessions to our database engine

### Integrating MongoDB for NoSQL data storage

Transitioning from SQL to NoSQL databases opens up a different paradigm in data storage and
management. NoSQL databases, like MongoDB, are known for their flexibility, scalability, and ability
to handle large volumes of unstructured data.

NoSQL databases differ from traditional SQL databases in that they often allow for more dynamic and
flexible data models. MongoDB, for example, stores data in binary JSON (BSON) format, which can
easily accommodate changes in data structure. This is particularly useful in applications that require
rapid development and frequent updates to the database schema.

`pip install pymongo`

1. Create a new project folder called nosql_example. Start by defining connection configuration
   in a database.py file:

```python
from pymongo import MongoClient
client = MongoClient()
database = client.mydatabase
```

Here, mydatabase is the name of your database.

2. Once the connection has been set up, you can define your collections (equivalent to tables
   in SQL databases) and start interacting with them. MongoDB stores data in collections of
   documents, where each document is a JSON-like structure:

```python
user_collection = database["users"]

```

Here, user_collection is a reference to the users collection in your MongoDB database.
Accesses a database named "mydatabase".
If the database does not exist yet, MongoDB will create it automatically when you insert the first document.

3. To test the connection, you can create an endpoint that will retrieve all users that should return
   an empty list in a main.py file:

```python
from database import user_collection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()
class User(BaseModel):
    name: str
    email: str
@app.get("/users")
def read_users() -> list[User]:
    return [user for user in user_collection.find()]
```

4. Now, we can run our mongod instance as
   `$mongod`
   In windows
   `net start MongoDB`

5.Now that the connection has been set up, we are going to create an endpoint to add a user and one to
retrieve a specific user with an ID. We’ll create both endpoints in the main.py module.

#### Creating a new user

To add a new document to a collection, use the insert_one method

class UserResponse(User):
id: str

```python
@app.post("/user")
def create_user(user: User) -> UserResponse:
    result = user_collection.insert_one(user.model_dump(exclude_none=True))
    user_response = UserResponse(id=str(result.inserted_id), **user.model_dump())
    return user_response
```

#### Reading a user

```python
@app.get("/user")
def get_user(user_id: str):
db_user = user_collection.find_one(
{"\_id": ObjectId(user_id) if ObjectId.is_valid(user_id) else None}
)
if db_user is None:
raise HTTPException(status_code=404, detail="User Not Found")
user_response = UserResponse(id=str(db_user["_id"]), \*\*db_user)
return user_response
```

In Mongo, the ID of the document is not stored in plain text, but in a 12-byte object. That’s why we
need to initialize a dedicated bson.ObjectId when querying the database and explicitly decode
to str when returning the value through the response

## Building RESTful APIs with FastAPI

Here, we will build RESTful apis for a task manager application. We will use csv file for database and additionally we will secure api with Oauth2. Furthermore, we willl tackle the important aspect of verisonuing your API over time without breaking existing clients.

In this chapter, we’re going to cover the following recipes:
• Creating CRUD operations
• Creating RESTful endpoints
• Testing your RESTful API
• Handling complex queries and filtering
• Versioning your API
• Securing your API with OAuth2
• Documenting your API with Swagger and Redoc

we will use Pytest for testing

`pip install pytest`

### Creating CRUD Operations

tasks.csv

```python
id,title,description,status
2,Task Two, Desccription Two,Ongoing
3,we,are,weee

```

models.py

```python
from pydantic import BaseModel

class Task(BaseModel):
    title:str
    description:str
    status:str

# his model is used when you create or update a task.

# ➡️ Why no id?
# Because when the user sends data to create a task, the user does not provide the task ID.
# The ID is generated by the database.
class TaskWithId(Task):
    id:int

# This model is used when the API returns data (GET requests, created tasks, updated tasks, etc.).

# ➡️ Why include id?
# Because when the database returns a task record, it always includes an ID.
```

operations.py

```python
import csv
from typing import Optional

from models import Task, TaskWithId

DATABASE_FILENAME = "tasks.csv"

column_fields = ["id", "title", "description", "status"]


def read_all_tasks() -> list[TaskWithId]:  # returns a list TaskwithId objects
    with open(DATABASE_FILENAME) as csvfile:
        reader = csv.DictReader(
            csvfile
        )  # reads a csv where each row becomes a dictionary
        return [
            TaskWithId(**row) for row in reader
        ]  # It reads each line of the CSV and converts it into a Pydantic model, then returns ALL those models as a list.


def read_task(task_id) -> Optional[TaskWithId]:
    with open(DATABASE_FILENAME) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row["id"]) == task_id:
                return TaskWithId(**row)


def get_next_id():
    try:
        with open(DATABASE_FILENAME, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            max_id = max(int(row["id"]) for row in reader)
            return max_id + 1
    except (FileNotFoundError, ValueError):
        return 1


def write_task_into_csv(task: TaskWithId):
    with open(DATABASE_FILENAME, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=column_fields)
        writer.writerow(task.model_dump())


def create_task(task: Task) -> TaskWithId:
    id = get_next_id()
    task_with_id = TaskWithId(id=id, **task.model_dump())
    write_task_into_csv(task_with_id)
    return task_with_id


def modify_task(id: int, task: dict) -> Optional[TaskWithId]:
    updated_task: Optional[TaskWithId] = None
    tasks = read_all_tasks()
    for number, task_ in enumerate(tasks):
        if task_.id == id:
            tasks[number] = updated_task = task_.model_copy(update=task)
    with open(DATABASE_FILENAME, mode="w", newline="") as csvfile:  # rewrite the file
        writer = csv.DictWriter(
            csvfile,
            fieldnames=column_fields,
        )
        writer.writeheader()
        for task in tasks:
            writer.writerow(task.model_dump())
    if updated_task:
        return updated_task


def remove_task(id: int) -> bool:
    deleted_task: Optional[Task] = None
    tasks = read_all_tasks()
    with open(DATABASE_FILENAME, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_fields)
        writer.writeheader()
        for task in tasks:
            if task.id == id:
                deleted_task = task
                writer.writerow(task.model_dump())
            if deleted_task:
                dict_task_without_id = deleted_task.model_dump()
                del dict_task_without_id["id"]
                return Task(**dict_task_without_id)
```

main.py

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import Task, TaskWithId
from operations import read_all_tasks, read_task, create_task, modify_task, remove_task

app = FastAPI()


@app.get("/tasks", response_model=list[TaskWithId])
def get_tasks():
    tasks = read_all_tasks()
    return tasks


@app.get("/task/{task_id}")
def get_task(task_id: int):
    task = read_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/task", response_model=TaskWithId)
def add_task(task: Task):
    return create_task(task)


class UdpdateTask(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None


@app.put("/task/{task_id}", response_model=TaskWithId)
def update_task(task_id: int, task_update: UdpdateTask):
    modified = modify_task(task_id, task_update.model_dump(exclude_unset=True))
    if not modified:
        raise HTTPException(status_code=404, detail="task not found")
    return modified


@app.delete("/task/{task_id}", response_model=Task)
def delete_task(task_id: int):
    removed_task = remove_task(task_id)
    if not removed_task:
        raise HTTPException(status_code=404, detail="task not found")
    return removed_task

```
