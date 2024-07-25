from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from main import engine

# Create a base class for the ORM models
Base = declarative_base()


# Create classes
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)


# Create the table
Base.metadata.create_all(engine)