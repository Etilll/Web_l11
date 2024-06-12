from sqlalchemy import Column, Integer, String, Date

from ..database import Base, engine

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    mail = Column(String)
    phone = Column(String)
    birthday = Column(Date)

Base.metadata.create_all(bind=engine)
