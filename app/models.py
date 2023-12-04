from database import Base
from sqlalchemy import Integer, String, Column, Boolean, LargeBinary
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text



class Book(Base) : 
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String, nullable=False)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    description = Column(String, server_default='No description provided for this book')
    availability = Column(Boolean, nullable=False, server_default='TRUE')
    desired_genre = Column(String, server_default='Surprise')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))
    image = Column(String)


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    receiver_email = Column(String, nullable=False)
    sender_email = Column(String, nullable=False)    
    message = Column(String, nullable=False)
    sent_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))


class Utilisateur(Base) :
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True,autoincrement=True, nullable=False) 
    nom = Column(String, nullable=False)
    email = Column(String, nullable=False)
    country = Column(String, nullable=False)
    password_hash = Column(LargeBinary, nullable=False)
    password_salt = Column(LargeBinary, nullable=False)
