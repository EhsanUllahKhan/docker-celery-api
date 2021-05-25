from pydantic import BaseModel

class VMI(BaseModel):
    username: str
    host: str
    port: int
    command: str

class Command_schema(BaseModel):
    c_id: int
    command: str
    result: str

    class Config:
        orm_mode = True
