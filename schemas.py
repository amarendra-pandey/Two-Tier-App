from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    id:int
    title:str

class Updt_Task(BaseModel):
    title:Optional[str] = None

class User(BaseModel):
    username: str
    password: str

class TaskResponse(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token:str
    token_type:str

class GoalRequest(BaseModel):
    goal: str