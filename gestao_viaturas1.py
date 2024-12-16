"""
Programa para gestão do catálogo de viaturas. Este programa permitirá:
    - Listar o catálogo
    - Pesquisar por alguns campos 
    - Eliminar um registo do catálogo
    - Guardar o catálogo em ficheiro

"""

from datetime import date
import re


class Viatura:

    def __init__(
            self,
            matricula: str,  # matricula: DD-LL-DD onde D: Dígito L: Letra
            marca: str,      # marca: deve ter uma ou mais palavras (apenas letras ou dígitos)
            modelo: str,     # modelo: mesmo que a marca
            data: str,       # data: deve vir no formato ISO: 'YYYY-MM-DD'
    ):
        # 1. Validar
        if not valida_matricula(matricula):
            raise InvalidAttr(f'Matrícula inválida: {matricula}')

        if not valida_marca(marca):
            raise InvalidAttr(f'Marca inválida: {marca}')

        if not valida_modelo(modelo):
            raise InvalidAttr(f'Modelo inválido: {modelo}')

        # 2. Definir objecto
        self.matricula = matricula
        self.marca = marca
        self.modelo = modelo
        try:
            self.data = date.fromisoformat(data)
        except ValueError as ex:
            raise InvalidAttr(f'Data inválida: {data}') from ex
    #:
#:

def valida_matricula(matricula: str) -> bool:
    return bool(re.fullmatch(r'[0-9]{2}-[A-Z]{2}-[0-9]{2}', matricula))
#:

def valida_matricula2(matricula: str) -> bool:
    partes = matricula.split('-')
    return (
            len(partes) == 3
        and (partes[0].isdigit() and len(partes[0]) == 2)
        and (partes[1].isalpha() and len(partes[1]) == 2 and partes[1] == partes[1].upper())
        and (partes[2].isdigit() and len(partes[2]) == 2)
    )
#:

def valida_marca(marca: str) -> bool:
    """
    Uma ou mais palavras alfanuméricas
    """
    palavras = marca.split()
    return len(palavras) >= 1 and all(palavra.isalnum() for palavra in palavras)
#:

# def valida_marca(marca: str) -> bool:
#     """
#     Uma ou mais palavras alfanuméricas
#     """
#     palavras = marca.split()
#     for palavra in palavras:
#         if not palavra.isalnum():
#             return False
#     return True
# #:

def valida_modelo(modelo):
    return valida_marca(modelo)
#:

class InvalidAttr(ValueError):
    """
    Invalid Attribute.
    """
#:

"""
EXPRESSÕES LISTA E OUTRAS

nums = [20, -30, 40, 50, 60, -2, -1, 40]
txt = 'Estamos a aprender expressões lista e outras...'

positivos = []
for num in nums:
    if num > 0:
        positivos.append(num)

dobros = []
for num in nums:
    dobros.append(2 * num)

# expressão lista: [EXPRESSAO(VAR) for VAR in ITERÁVEL [if CONDICAO(VAR)]]
positivos = [num for num in nums if num > 0]  # SELECT num FROM nums WHERE num > 0
dobros = [2 * num for num in nums]            # SELECT 2 * num FROM nums
dobro_positivos = [2 * num for num in nums if num > 0] 

vogais        = [ch for ch in txt if ch in 'aeiouAEIOU']
vogais_unicas = {ch for ch in txt if ch in 'aeiouAEIOU'}

todos_divisiveis_por_dez = True
for num in nums:
    if num % 10 != 0:
        todos_divisiveis_por_dez = False
print(f"Todos divisiveis por 10? {todos_divisiveis_por_dez}")

all([True, False, True])

all(num % 10 == 0 for num in nums)
"""