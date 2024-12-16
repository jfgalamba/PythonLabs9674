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
    # raise ValueError('Big problema!!!')
    return {'2 x value': 2 * value, 'text': f'{param1}/{param2}'}
#:


"""
Criámos uma api API que:

o Recebe pedidos HTTP nos caminhos / e /computeitem/{value}.
o Ambos os caminhos aceitam pedidos HTTP GET
o O caminho /computeitem/{value} tem um parâmetro de caminho value
  que deve ser um int.
o O caminho /computeitem/{value} tem dois parâmetros de consulta str 
  (query string) opcionais param1 e param2.

Agora aceda a: http://127.0.0.1:8000/docs
Agora aceda a: http://127.0.0.1:8000/redoc
"""

# EXERCÍCIO: 
#       1. Correr no vosso repositório o hello_fastapi1.py
#       2. Testar
#       3. Acrescentar função para receber dois parâmetros x e y e devolver
#          a soma de x com y. A função deve ser acessível por get e o caminho
#          deve começar com "/sum". A função deve-se chamar "sum".
#

@app.get("/sum/{x}/{y}")
async def sum(x: int, y: int):
    return {"x + y": x + y}
#:

