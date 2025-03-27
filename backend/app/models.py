# app/models.py
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database connection details
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://myuser:mypassword@mysql:3306/tododb")

# Database connection and ORM setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# To-Do Model
class TodoItem(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String(150), index=True)
    completed = Column(Boolean, default=False)

# Create the tables if they don't exist
Base.metadata.create_all(bind=engine)
