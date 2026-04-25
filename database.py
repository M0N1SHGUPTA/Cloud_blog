from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

'''
engine connects, session talks, Base
defines tables, get_db gives routes a session and
cleans up after.
'''

#Where the database lives
SQLALCHEMY_DATABASE_URL = "sqlite:///./cloud_blog.db"

#The connection to the database from the app
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False},
)

#This creates database sesison, A session is a open conversation, read, write, and when done we can close it.
SessionLocal = sessionmaker(autocommit = False,
    autoflush = False,
    bind = engine                            
)

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as db:
        yield db

