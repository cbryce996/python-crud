from sqlalchemy import Column, Integer, String
from database.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    password = Column(String)
    full_name = Column(String)
    address = Column(String)
    phone_number = Column(String)
