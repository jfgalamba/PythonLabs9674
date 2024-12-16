"""
Manages a contact "list". 
"""

from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr


app = FastAPI()


class Contact(BaseModel):
    id: int
    name: str
    email_addr: EmailStr
    last_changed: datetime = datetime.now()
    available: bool | None = None
#:

the_contact = Contact(
    id=12345,
    name='Alberto',
    email_addr='alb@mail.com',
    available=False,
)


@app.get('/')
async def index():
    return {"msg": "Retrieve contact information APP"}
#:

@app.get('/contact/{id}')
async def get_contact_by_id(contact_id: int):
    if contact_id != the_contact.id:
        return None
    return the_contact
#:

@app.put('/contact/{contact_id}')
async def update_contact(contact_id: int, contact: Contact):
    global the_contact
    if contact_id != the_contact.id:
        return None
    the_contact = contact
    the_contact.last_changed = datetime.now()
#:

"""
EXERCÍCIO: 
    1. Acrescentar put para actualizar email apenas

    2. Fazer "hello_fastapi3.py" com:
        2.1 Lista de contactos em memória e inicializar com 3 contactos

        2.2 Operações para:
            . obter um contacto pelo email_addr
            . alterar um contacto localizado pelo email_addr (PUT)
            - acrescentar novo contacto (POST)

        2.3 Redefinir 2.1 para ler contactos a partir de ficheiro JSON
"""