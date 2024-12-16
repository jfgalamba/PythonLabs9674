"""
Primeiro exemplo. Utiliza pedidos GET.

Executar:
    $ fastapi dev hello_fastapi.py

DESCONTINUADO
    Executar:
        $ uvicorn hello_fastapi:app --reload
"""

from fastapi import FastAPI


app = FastAPI()


# Por omissão FastAPI gera JSON

@app.get('/')
async def index():
    return {'msg': 'Hello from FastAPI'}
#:

@app.get('/computeitem/{value}')
async def compute_item(value: int, param1: str | None = None, param2: str | None = None):
    return {'2 x value': 2 * value, 'text': f'{param1}/{param2}'}
#: