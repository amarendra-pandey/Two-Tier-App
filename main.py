from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from database import SessionLocal,get_db
from models import TaskDB,UserDB
from sqlalchemy.orm import Session
from schemas import User,Task,Updt_Task,TaskResponse,Token, GoalRequest
from auth import hash_password,verify_password, create_token,verify_token
from ai import suggest_task
# from typing import List

app = FastAPI()

oauth2scheme = OAuth2PasswordBearer(tokenUrl="login")

# tasks = []

def get_current_user(token :str = Depends(oauth2scheme)):
    return verify_token(token)

@app.get("/")
def read_root():
    return {"msg" : "Hello Amarendra"}


# @app.get("/tasks")
# def get_task(db:Session = Depends(get_db)):
#     # db = SessionLocal()
#     tasks = db.query(TaskDB).all()
#     # db.close()
#     return tasks

# @app.get("/tasks/{id}")
# def read_task(id:int):
#     return {"id":id}

@app.post("/tasks")
def create_task(
    task: Task, 
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
    ):
    # db = SessionLocal()

    db_user = db.query(UserDB).filter(UserDB.username == user).first()

    db_task = TaskDB(id=task.id, title=task.title, user_id = db_user.id)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # db.close()

    return {"msg":"Task Added","Task": db_task}

# def add_task(task:Task):
#     tasks.append(task)
#     print(tasks)
#     return {"msg":"Task Added","Task":task}

@app.put("/tasks/{id}")
def updt_task_put(
    id:int, 
    updt_task:Task,
    db:Session = Depends(get_db),
    user:str = Depends(get_current_user)):

    db_user = db.query(UserDB).filter(UserDB.username == user).first()

    task = db.query(TaskDB).filter(
        TaskDB.id == id,
        TaskDB.user_id == db_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updt_task.title

    db.commit();
    db.refresh(task)

    return {"msg":"updated", "task": task}

    





    # for i in range(len(tasks)):
    #     if tasks[i].id == id:
    #         tasks[i]=updt_task
    #         return {"msg":"updated","task":tasks[i]}
    # return {"error":"Task not found"}

@app.patch("/tasks/{id}")
def updt_task(
    id:int, 
    updt_task:Updt_Task,
    db:Session = Depends(get_db),
    user:str = Depends(get_current_user)
    ):

    db_user = db.query(UserDB).filter(UserDB.username == user).first()

    task = db.query(TaskDB).filter(
        TaskDB.id == id,
        TaskDB.user_id == db_user.id
    ).first()

    if not task:
        return {"error":"Task not found"}

    task.title = updt_task.title

    db.commit();
    db.refresh(task)

    return {"msg":"updated", "task title": task.title}


    # for task in tasks:
    #     if task.id == id:
    #         task.title=updt_task.title
    #         return {"msg":"updated","task":task}
    # return {"error":"Task not found"}

@app.post("/signup")
def signup(user:User, db:Session = Depends(get_db)):
    existing_user = db.query(UserDB).filter(UserDB.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(user.password)

    db_user = UserDB(username=user.username, password = hashed)
    db.add(db_user)
    db.commit()

    return {"msg":"User Created"}

# @app.post("/login")
# def login(user:User, db:Session = Depends(get_db)):
#     db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
#     print("###")
#     print(db_user)

#     if not db_user or not verify_password(user.password, db_user.password):
#         return {"error": "Invalid Credentials"}

#     token = create_token({"sub":user.username})

#     return {"access token": token}

# ------------------------auth for fetching /tasks so that not anyone can access it------------------------------------


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    skip: int =0,
    limit: int = 10,
    title: str = None,
    db:Session = Depends(get_db),
    user: str= Depends(get_current_user)
):
    db_user = db.query(UserDB).filter(UserDB.username == user).first()

    query = db.query(TaskDB).filter(TaskDB.user_id == db_user.id)

    if title:
        query = query.filter(TaskDB.title.contains(title))

    return query.offset(skip).limit(limit).all()

@app.post("/login", response_model = Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == form_data.username).first()

    print(db_user)

    if not db_user or not verify_password(form_data.password,db_user.password):
        return {"error":"Invalid Credentials"}
    
    token =create_token({"sub":form_data.username})

    return {"access_token": token, "token_type":"bearer"}

@app.delete("/tasks/{id}")
def delete_task(
    id: int,
    db:Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    db_user = db.query(UserDB).filter(UserDB.username == user).first()

    task = db.query(TaskDB).filter(
        TaskDB.id == id,
        TaskDB.user_id == db_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail= "Task not found")

    db.delete(task)
    db.commit()

    return {"msg":"Task deleted"}

@app.post("/tasks/suggest", response_model=list[TaskResponse])
def suggest_and_store(
    data: GoalRequest,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
    ):
    
    db_user = db.query(UserDB).filter(UserDB.username == user).first()

    existing_task = db.query(TaskDB).filter(
        TaskDB.goal == data.goal,
        TaskDB.user_id == db_user.id
        ).all()
    
    if existing_task:
        print("CACHE HIT")
        return existing_task

    suggestions = suggest_task(data.goal)

    saved_task = []

    for title in suggestions:
        task = TaskDB(title=title,
                    user_id = db_user.id,
                    goal = data.goal)

        db.add(task)
        saved_task.append(task)

    
    db.commit()
    
    for task in saved_task:
        db.refresh(task)

    return saved_task