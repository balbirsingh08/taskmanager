from sqlalchemy.orm import Session
import models, schemas, auth

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(title=task.title, description=task.description, owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Task).offset(skip).limit(limit).all()

def update_task(db: Session, task_id: int, task_data: schemas.TaskCreate, user_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task and task.owner_id == user_id:
        task.title = task_data.title
        task.description = task_data.description
        db.commit()
        db.refresh(task)
        return task
    return None

def delete_task(db: Session, task_id: int, user_id: int, is_admin: bool = False):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return None
    if task.owner_id != user_id and not is_admin:
        return None
    db.delete(task)
    db.commit()
    return task
