"""
Manages a contact "list". 
"""

from datetime import datetime
import json
from typing import Iterable

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field


app = FastAPI()

"""
    2. Fazer "hello_fastapi3.py" com:
        2.1 Lista de contactos em memória e inicializar com 3 contactos

        2.2 Operações para:
            . obter um contacto pelo email_addr
            . alterar um contacto localizado pelo email_addr (PUT)
            - acrescentar novo contacto (POST)

        2.3 Redefinir 2.1 para ler contactos a partir de ficheiro JSON
"""

class Contact(BaseModel):
    id: int                = Field(gt = 10_000, lt = 99_999, frozen = True)
    name: str              = Field(min_length = 1, frozen = True)
    email_addr: EmailStr   = Field(pattern = r'.+@mail\.com')
    last_changed: datetime  = datetime.now()
    available: bool | None = None
#:


# contacts = [
#     Contact(
#         id=12345,
#         name='Alberto',
#         email_addr='alb@mail.com',
#         available=False,
#     ),
#     Contact(
#         id=12346,
#         name='Armando',
#         email_addr='arm@mail.com',
#         available=True,
#     ),
#     Contact(
#         id=12347,
#         name='Arnaldo',
#         email_addr='arn@mail.com',
#         available=True,
#     ),
# ]

def save_contacts(file_path: str, contacts: Iterable[Contact]):
    with open(file_path, 'wt') as file:
        data = [contact.model_dump() for contact in contacts]
        json.dump(data, file, default=str)
#:

def load_contacts(file_path: str):
    with open(file_path, 'rt') as file:
        data = json.load(file)
        return [Contact(**obj) for obj in data]
#:

# save_contacts("contacts.json", contacts)
contacts = load_contacts("contacts.json")

def find_contact_by(find_fn) -> tuple[int, Contact | None]:
    for i, contact in enumerate(contacts):
        if find_fn(contact):
            return i, contact
    return -1, None
#:

def find_contact_by_id(contact_id: int) -> tuple[int, Contact | None]:
    return find_contact_by(lambda contact: contact.id == contact_id)
#:

def update_contact_from(contact: Contact, new_contact_info: Contact):
    contact.email_addr = new_contact_info.email_addr
    contact.available = new_contact_info.available
    contact.last_changed = datetime.now()
#:

@app.get('/')
async def index():
    return {"msg": "Retrieve contact information APP"}
#:

@app.get('/contact')
async def get_contacts():
    return contacts
#:

@app.get('/contact/{contact_id}')
async def get_contact_by_id(contact_id: int):
    _, contact = find_contact_by_id(contact_id)
    return contact
#:

@app.get('/contact/email/{email_addr}')
async def get_contact_by_email(email_addr: str):
    _, contact = find_contact_by(lambda contact: contact.email_addr == email_addr)
    if not contact:
        return {'error': f'Email address {email_addr} not found'}
    return contact
#:

@app.put('/contact/{contact_id}')
async def update_contact_by_id(contact_id: int, contact: Contact):
    i, existing_contact = find_contact_by_id(contact_id)
    if not existing_contact:
        return {'error': 'Contact with ID {contact_id} not found'}
    update_contact_from(contacts[i], contact)
#:

@app.post('/contact/email')
async def new_contact(new_contact: Contact):
    def same_id_or_email(existing_contact: Contact):
        return (
               new_contact.id == existing_contact.id 
            or new_contact.email_addr == existing_contact.email_addr
        )
    _, contact = find_contact_by(same_id_or_email)
    if contact:
        return {'error': f'Contact id/email_addr is not unique.'}
    contacts.append(new_contact)
#:

@app.put('/contact/email/{email_addr}')
async def update_contact_by_email(email_addr: str, new_info: Contact):
    _, contact = find_contact_by(lambda contact: contact.email_addr == email_addr)
    if not contact:
        return {'error': f'Email address {email_addr} not found'}
    update_contact_from(contact, new_info)
#:

class NewEmailAddr(BaseModel):
    new_email_addr: EmailStr
#:

@app.put('/contact/new_email_addr/{contact_id}')
async def update_email_by_id(contact_id: int, req: NewEmailAddr):
    _, contact = find_contact_by_id(contact_id)
    if not contact:
        return {'error': 'Contact with ID {contact_id} not found'}
    contact.email_addr = req.new_email_addr
#:

