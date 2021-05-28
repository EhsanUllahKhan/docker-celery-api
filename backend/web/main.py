import json
from pydantic import BaseModel
from fastapi import FastAPI, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from .worker import celery
from .schemas import VMI
app = FastAPI()
#
from ..database import SessionLocal
from ..models.models import Command


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/")
async def create_item(item: VMI, db: Session=Depends(get_db)):
    task_name = "hello.task"
    task = celery.send_task(task_name, args=[item.host, item.port, item.username, item.command])
    try:
        command = Command(
            command=item.command,
            hostname=item.host,
            port=item.port,
            username=item.username,
            task_id=task.id,
            task_state="Pending",
            result=None,
            exception=None
            )
        added = db.add(command)
        db.commit()
        db.close()
        return dict(id=task.id, url='localhost:5000/check_task/{}'.format(task.id))
    except Exception as ex:
        return dict(error=type(ex).__name__)
    # finally:
    #     db.close()

@app.get("/check_task/{id}")
def check_task(id: str, db: Session=Depends(get_db)):

    task = db.query(Command).filter(Command.task_id == id).first()
    if task is None:
        raise HTTPException(status_code=400, detail="Task not found for given id")
    return {'status_code':200, 'task':task}
