from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from .db import Base, engine

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    mail = Column(String)
    phone = Column(String)
    birthday = Column(Date)
    owner = relationship("User", back_populates="contacts")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    contacts = relationship("Contact", back_populates="owner")

Base.metadata.create_all(bind=engine)
