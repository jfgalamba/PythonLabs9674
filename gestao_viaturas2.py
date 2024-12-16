"""
Programa para gestão do catálogo de viaturas. Este programa permitirá:
    - Listar o catálogo
    - Pesquisar por alguns campos 
    - Eliminar um registo do catálogo
    - Guardar o catálogo em ficheiro

o Construtor alternativo Viatura, CSV

o Métodos __str__, __repr__

o Property ano da matricula

o VehicleCollection com I/O (mas utilizar dicionário)
"""

from datetime import date
import re
from typing import TextIO


CSV_DELIM = '|'


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

    @classmethod
    def from_csv(cls, csv: str, csv_delim = CSV_DELIM) -> 'Viatura':
        attrs = csv.split(csv_delim)
        return cls(
            matricula = attrs[0],
            marca = attrs[1],
            modelo = attrs[2],
            data = attrs[3],
        )
    #:

    @property
    def ano(self) -> int:
        return self.data.year
    #:

    def __str__(self):
        return f'Viatura[matricula: {self.matricula} | {self.marca} {self.modelo}]'
    #:

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f"{cls_name}('{self.matricula}', '{self.marca}', '{self.modelo}', '{self.data.isoformat}')"
    #:
#:

def valida_matricula(matricula: str) -> bool:
    return bool(re.fullmatch(r'[0-9]{2}-[A-Z]{2}-[0-9]{2}', matricula))
#:

def valida_matricula2(matricula: str) -> bool:
    """
    Uma ou mais palavras alfanuméricas
    """
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

def valida_modelo(modelo):
    return valida_marca(modelo)
#:

class InvalidAttr(ValueError):
    """
    Invalid Attribute.
    """
#:

class VehicleCollection:
    def __init__(self):
        self._vehicles: dict[str, Viatura] = {}
    #:

    @classmethod
    def from_csv(cls, csv_path: str) -> 'VehicleCollection':
        vehicles = VehicleCollection()
        with open(csv_path, 'rt') as file:
            for line in relevant_lines(file):
                vehicles.append(Viatura.from_csv(line))
        return vehicles
    #:

    def append(self, viat: Viatura):
        if self.search_by_id(viat.matricula):
            raise DuplicateValue(f'Viatura com matricula {viat.matricula} já adicionada')
        self._vehicles[viat.matricula] = viat
    # :

    def search_by_id(self, matricula: str) -> Viatura | None:
        return self._vehicles.get(matricula)
    #:

    def _dump(self):
        for viat in self._vehicles.values():
            print(viat)
    #:
#:

def relevant_lines(file: TextIO):
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        if line[:2] in ('##', '//'):
            continue
        yield line
#:

class DuplicateValue(Exception):
    """
    If there is a duplicate product in a ProductCollection.
    """
#:

def main():
    try:
        viaturas = VehicleCollection.from_csv('viaturas.csv')
    except InvalidAttr as ex:
        print("Erro ao carregar viaturas")
        print(ex)
    else:
        viaturas._dump()
#:

if __name__ == '__main__':
    main()
