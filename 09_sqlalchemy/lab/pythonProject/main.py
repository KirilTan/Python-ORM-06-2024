from sqlalchemy import create_engine

DATABASE_URL = 'postgresql+psycopg2://postgres:password@localhost:5432/09_lab'
engine = create_engine(DATABASE_URL)
