from ..database.models import Contact
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date, timedelta

async def get_contacts(db,id,name,surname,mail,phone):
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
    return result

async def add_contact(contact, db):
    try:
        contact = Contact(**contact.model_dump())
        db.add(contact)
        db.commit()
        db.refresh(contact)
        return contact
    except IntegrityError as e:
        return e

async def delete_contact(contact_id, db):
    contact = db.get_one(Contact, contact_id)
    if contact:
        db.delete(contact)
        db.commit()
        return {"Successfull":f"contact with id {contact_id} deleted!"}
    else:
        return None

async def put_contact(contact_id,db,id,name,surname,mail,phone): 
    contact = db.get_one(Contact, contact_id)
    if contact:
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
    else:
        return None

async def calculate_birthdays(db):
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
