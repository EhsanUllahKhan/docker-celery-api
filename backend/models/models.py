from sqlalchemy import Column, Integer, String

from ..database import Base


class Command(Base):
    __tablename__ = "command"

    c_id = Column(Integer, primary_key=True, index=True)
    command = Column(String(length=50))
    result = Column(String(length=5000))
