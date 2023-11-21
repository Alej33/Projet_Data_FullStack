from .database import Base
from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text



class Book(Base) : 
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    description = Column(String, server_default='No description provided for this book')
    availability = Column(Boolean, nullable=False, server_default='TRUE')
    desired_genre = Column(String, server_default='Surprise')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))

