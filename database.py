import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL')


try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    with engine.connect() as connection:
        print("Connection successful!")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
except Exception as e:
    print(f"Connection failed: {e}")


# engine = create_engine(SQLALCHEMY_DATABASE_URL)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        