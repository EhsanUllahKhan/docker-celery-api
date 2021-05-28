from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connectionstring for db
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://ehsan:ehsan@192.168.0.108/ehsan"
SQLALCHEMY_DATABASE_URL='mysql+pymysql://ehsan:ehsan@db:3306/vmi_db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(engine)