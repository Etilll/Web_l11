from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Depends, Query
from ..database import get_db
from ..models.book import Contact
from ..schemas import ResponseContact
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date, timedelta

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.get("/by_id/{contact_id}", response_model=ResponseContact) #, dependencies=[Depends(get_token_header)]
async def get_contact(contact_id: Annotated[int, Path(title="The id of contact to find")], db: Session=Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        return contact
    raise HTTPException(status_code=404, detail="contact not found")

@router.get("/", response_model=list[ResponseContact])
async def all_contacts(db: Session=Depends(get_db), 
                    id: Annotated[int | None, Query(alias="id", example="id=42")]=None,
                    name: Annotated[str | None, Query(alias="name", example="name=Jone")]=None, 
                    surname: Annotated[str | None, Query(alias="surname", example="surname=Jenkins")]=None, 
                    mail: Annotated[str | None, Query(alias="mail", example="mail=123@gmail.com")]=None, 
                    phone: Annotated[str | None, Query(alias="phone", example="phone=380731290102")]=None):
    result = []
    if id or name or surname or mail or phone:
        finames = 'id name surname mail phone'.split()
        fivals = [id, name, surname, mail, phone]
        result = db.query(Contact)
        for filtname, filtval in zip(finames, fivals):
            if filtval is not None:
                d = {filtname: filtval}
                result = result.filter_by(**d)
        return result.all()
    else:
        result = db.query(Contact).all()
    if result == []:
        raise HTTPException(status_code=404, detail="No match was found, or the database is empty!")
    else:
        return result


@router.post("/")
async def add_contact(contact: ResponseContact, db: Session = Depends(get_db)):
    try:
        contact = Contact(**contact.model_dump())
        db.add(contact)
        db.commit()
        db.refresh(contact)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail="Object with this id already exists in the system!")
    return contact

@router.delete("/{contact_id}")
async def del_contact(contact_id: Annotated[int, Path(title="The id of a contact to delete")], db: Session = Depends(get_db)):
    contact = db.get_one(Contact, contact_id)
    db.delete(contact)
    db.commit()
    return {"Successfull":f"contact with id {contact_id} deleted!"}

@router.put("/{contact_id}")
async def del_contact(contact_id: Annotated[int, Path(title="The id of a contact to delete")], db: Session = Depends(get_db), 
                    id: Annotated[int | None, Query(alias="id", example="id=42")]=None,
                    name: Annotated[str | None, Query(alias="name", example="name=Jone")]=None, 
                    surname: Annotated[str | None, Query(alias="surname", example="surname=Jenkins")]=None, 
                    mail: Annotated[str | None, Query(alias="mail", example="mail=123@gmail.com")]=None, 
                    phone: Annotated[str | None, Query(alias="phone", example="phone=380731290102")]=None,): 
    contact = db.get_one(Contact, contact_id)
    if id:
        contact.id = id
    if name:
        contact.name = name
    if surname:
        contact.surname = surname
    if mail:
        contact.mail = mail
    if phone:
        contact.phone = phone
    db.add(contact)
    db.commit()
    return {"Successfull":f"contact with id {contact_id} edited!"}

@router.get("/bdays")
async def calc_birthdays(db: Session = Depends(get_db)):
    contacts = db.query(Contact).all()
    days_ahead = (datetime(date.today().year,date.today().month,date.today().day) + timedelta(days=7)).date()

    upcoming_birthdays = []
    for contact in contacts:
        BD_DAY = contact.birthday
        if BD_DAY != None:
            TODAY = date.today()
            if (BD_DAY.month < TODAY.month) or ((BD_DAY.month == TODAY.month) and (BD_DAY.day < TODAY.day)):
                BD_DAY = BD_DAY.replace(year = TODAY.year + 1)
            else:
                BD_DAY = BD_DAY.replace(year = TODAY.year)

            if BD_DAY <= days_ahead:
                upcoming_birthdays.append(contact)
           
    return upcoming_birthdays
