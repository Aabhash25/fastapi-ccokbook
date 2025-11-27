from sqlalchemy.orm import (
    DeclarativeBase,
)  # helper used to create a declarative base class


class Base(DeclarativeBase):  # base class fo all you sql alchemy orm models
    pass


from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

# Mapped is a generic type used to anbnotate attributes that are mapped to the database
# mapped_column is a helper that creates a sql column mapping (replaces the older Column(...) usage in manny patterns)


class User(Base):  # user is an orm model class
    __tablename__ = "user"  # tells sql alchemy the name of the database table
    id: Mapped[int] = mapped_column(
        primary_key=True
    )  # declareds an id attribute maped to a db colum and typed as int in python,mapped(column) makes this column the tables primary key
    name: Mapped[str]
    email: Mapped[str]


DATABASE_URL = "sqlite:///./test.db"
# This is a SQLAlchemy database URL that tells your FastAPI / Python app to connect to a SQLite database file named test.db.
# Let’s break it down:
# 🔹 sqlite://
# Specifies the database dialect you’re using → SQLite.
# 🔹 Third slash sqlite:///
# For SQLite, three slashes means a relative file path:
# sqlite:///./test.db → file inside current directory
# Equivalent to: "sqlite:///test.db"
# 🔹 ./test.db
# This is the path to the database file, relative to the project folder where you run the app.


from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL
)  # creates a connection engine that sqlalchemy will use to talk to your database

Base.metadata.create_all(
    bind=engine
)  # It creates all database tables defined by your SQLAlchemy models if they don’t already exist.

from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# It creates a factory that gives you new database sessions (connections) whenever your FastAPI app needs to talk to the database
