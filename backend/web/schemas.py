from pydantic import BaseModel

class VMI(BaseModel):
    username: str
    host: str
    port: int
    command: str

    class Config:
        schema_extra = {
            "example": {
                "username": "Foo",
                "host": "192.168.10.1",
                "port": '22',
                "command": 'pwd',
            }
        }