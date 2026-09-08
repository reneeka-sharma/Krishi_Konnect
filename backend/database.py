# SQLite connection and session helper 
"""
This is the descriptuon of what this file does
this file is responsible for :
a. connecting fast api project to the SQLite database
b. creating database sessions
c. providing and closing the database session safely 
"""
import pathlib as Path # helps to find the location of our project in database file
from sqlalchemy import create_engine # creates connection between python and database 
from sqlalchemy.orm import DeclarativeBase, sessionmaker 
"""
DeclarativeBase - used as baseclass
sessionmaker - creates database session we can use to read/write in database 
"""
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # find the main project folder (.parent.parent) 
""" 
example- 
KrishiKonnect/
 ├── backend/
 │   └── database.py   <- __file__ 
 └── krishikonnect.db
then basically PROJECT_ROOT points to KrishiKonnect/

"""
DATABASE_URL = f"sqlite:///{PROJECT_ROOT / 'krishikonnect.db'}"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
) #this creates the connection engine that SQLAlchemy will use to communicate with SQLite
SessionLocal = sessionmaker(
    # changes are not automatially saved
    # we can expiclity use db.commit() when we want to save changes 
    autocommit=False,
    autoflush=False, # will not automatically send pending changes to the database before every query.
    bind=engine #connects these session to our database engine.
) # creates factory for database session 
# whenever we need to intract with database we create a session using db = SessionLocal()

class Base(DeclarativeBase): # base is parent class of all database models
    pass 

def get_db():
    """Provide one database session per request and always close it."""
    db = SessionLocal()
    try:
        yield db
        """ 
        unlike return yield temporarily pause this function and API can use now 
        db.query(parameters),
        db.add(...),
        db.commit(...), etc
        """
    #finally always executes after request is finished
    finally: 
        db.close()


