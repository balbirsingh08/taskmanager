from fastapi import FastAPI, Depends, HTTPException
from typing import List

import models, schemas, crud, auth
from database import engine, Base, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User Endpoints
@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.require_admin)):
    return crud.create_user(db, user)

@app.get("/users/", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(get_db), current_admin: models.User = Depends(auth.require_admin)):
    return crud.get_users(db)

# Task Endpoints
@app.post("/tasks/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.create_task(db, task, current_user.id)

@app.get("/tasks/", response_model=List[schemas.TaskOut])
def list_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.get_tasks(db, skip, limit)

@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    updated = crud.update_task(db, task_id, task, current_user.id)
    if not updated:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    return updated

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    deleted = crud.delete_task(db, task_id, current_user.id, current_user.role == "admin")
    if not deleted:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    return {"detail": "Task deleted"}
# Add this endpoint temporarily (remove after creating admin)
@app.post("/register/", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.create_user(db, user)