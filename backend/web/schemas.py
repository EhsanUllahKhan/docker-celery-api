from typing import Optional

from pydantic import BaseModel

class VMI(BaseModel):
    username: str
    host: str
    port: int
    command: str

class Command_schema(BaseModel):
    c_id: int
    command: str
    hostname : str
    username : str
    port : int
    task_id : str
    result : Optional[str] = None
    task_state : str
    exception : Optional[str] = None

    class Config:
        orm_mode = True
