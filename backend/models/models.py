from sqlalchemy import Column, Integer, String

from ..database import Base


class Command(Base):
    __tablename__ = "command"

    c_id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String(length=30))
    username = Column(String(length=50))
    port = Column(Integer)
    command = Column(String)
    task_id=Column(String)
    result = Column(String, nullable=True)
    exception = Column(String, nullable=True)

