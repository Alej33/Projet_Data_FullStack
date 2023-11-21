from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# structure of the url : postgresql://<username>:<password>/<ip-adress/hostname>/<database-name>

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Youyoude12@localhost/fastapi"

engine = create_engine(url = SQLALCHEMY_DATABASE_URL)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()