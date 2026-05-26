from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import declarative_base
from database import engine

Base = declarative_base()

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer,primary_key=True, index=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    goal = Column(String)

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)