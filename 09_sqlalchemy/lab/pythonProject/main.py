from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = 'postgresql+psycopg2://postgres:password@localhost:5432/09_lab'
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)