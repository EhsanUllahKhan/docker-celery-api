from sqlalchemy import Column, Integer, String

from ..database import Base


class Command(Base):
    __tablename__ = "command"

    c_id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String(length=30))
    username = Column(String(length=50))
    port = Column(Integer)
    command = Column(String(length=500))
    task_id=Column(String(length=50))
    result = Column(String(length=5000), nullable=True)
    task_state=Column(String(length=50))
    exception = Column(String(length=5000), nullable=True)