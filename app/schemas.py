from pydantic import BaseModel, Field
from datetime import date

class ResponseContact(BaseModel):
    name:str = Field(title="Name of a person in question", min_length=1, max_length=20)
    surname:str = Field(title="Surname of a person in question", min_length=1, max_length=35)
    mail:str = Field(title="Email of a person in question", min_length=1, max_length=50, pattern="\S{3,}@[a-zA-Z]{2,}\.[a-zA-Z]{2,}")
    phone:str = Field(title="Phone of a person in question", min_length=10, max_length=12, pattern="\d{10}")
    birthday:date = Field(title="B-day of a person in question")

    class Config:
        from_attributes = True
