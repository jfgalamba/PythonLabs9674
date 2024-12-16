"""
Manages access to the underlying storage for vehicles. Vehicles are
stored in a CSV file. This modules provides two types to represent 
vehicles in memory:

    - `Vehicle`: a product in memory
    - `VehicleCollection`: manages a collection of vehicles in memory
"""

import datetime
import re
from typing import Iterable, TextIO


CSV_DELIM = '|'





class Vehicle:
    def __init__(
            self,
            license_plate: str,  # matricula: DD-LL-DD onde D: Dígito L: Letra
            make: str,            # marca: deve ter uma ou mais palavras (apenas letras ou dígitos)
            model: str,           # modelo: mesmo que a marca
            date: str,            # data: deve vir no formato ISO: 'YYYY-MM-DD'
    ):
        # 1. Validar
        if not self.validate_license_plate(license_plate):
            raise InvalidAttr(f'Matrícula inválida: {license_plate}')

        if not self.validate_make(make):
            raise InvalidAttr(f'Marca inválida: {make}')

        if not self.validate_model(model):
            raise InvalidAttr(f'Modelo inválido: {model}')

        # 2. Definir objecto
        self.license_plate = license_plate
        self.make = make
        self.model = model
        try:
            self.date = datetime.date.fromisoformat(date)
        except ValueError as ex:
            raise InvalidAttr(f'Data inválida: {date}') from ex
    #:

    @classmethod
    def from_csv(cls, csv: str, csv_delim = CSV_DELIM) -> 'Vehicle':
        attrs = csv.split(csv_delim)
        return cls(
            license_plate = attrs[0],
            make = attrs[1],
            model = attrs[2],
            date = attrs[3],
        )
    #:

    def to_csv(self, csv_delim = CSV_DELIM) -> str:
        return csv_delim.join((
            self.license_plate,
            self.make,
            self.model,
            str(self.date),
        ))
    #:

    @property
    def year(self) -> int:
        return self.date.year
    #:

    def __str__(self):
        return f'Viatura[matricula: {self.license_plate} | {self.make} {self.model}]'
    #:

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f"{cls_name}('{self.license_plate}', '{self.make}', '{self.model}', '{self.date.isoformat}')"
    #:

    @staticmethod
    def validate_license_plate(matricula: str) -> bool:
        return bool(re.fullmatch(r'[0-9]{2}-[A-Z]{2}-[0-9]{2}', matricula))
    #:

    @staticmethod
    def validate_license_plate2(matricula: str) -> bool:
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

    @staticmethod
    def validate_make(make: str) -> bool:
        """
        Uma ou mais palavras alfanuméricas
        """
        palavras = make.split()
        return len(palavras) >= 1 and all(palavra.isalnum() for palavra in palavras)
    #:

    @staticmethod
    def validate_model(model: str) -> bool:
        return Vehicle.validate_make(model)
    #:

    @staticmethod
    def validate_date(date: str) -> bool:
        try:
            datetime.date.fromisoformat(date)
            return True
        except ValueError:
            return False
    #:
#:

class InvalidAttr(ValueError):
    """
    Invalid Attribute.
    """
#:

class VehicleCollection:
    def __init__(self, vehicles: Iterable[Vehicle] = ()):
        self._vehicles: dict[str, Vehicle] = {}
        for vehicle in vehicles:
            self._vehicles[vehicle.license_plate] = vehicle
    #:

    @classmethod
    def from_csv(cls, csv_path: str, csv_delim = CSV_DELIM, encoding = 'UTF-8') -> 'VehicleCollection':
        vehicles = VehicleCollection()
        with open(csv_path, 'rt', encoding = encoding) as file:
            for line in relevant_lines(file):
                vehicles.append(Vehicle.from_csv(line, csv_delim))
        return vehicles
    #:

    def export_to_csv(self, csv_path: str, csv_delim = CSV_DELIM, encoding = 'UTF-8'):
        if len(self._vehicles) == 0:
            raise ValueError("Coleccção vazia")
        with open(csv_path, 'wt', encoding = encoding) as file:
            for vehicle in self._vehicles.values():
                print(vehicle.to_csv(csv_delim), file=file)
    #:

    def append(self, viat: Vehicle):
        if self.search_by_id(viat.license_plate):
            raise DuplicateValue(f'Viatura com matricula {viat.license_plate} já adicionada')
        self._vehicles[viat.license_plate] = viat
    # :

    def search_by_id(self, license_plate: str) -> Vehicle | None:
        return self._vehicles.get(license_plate)
    #:

    def search(self, find_fn):
        for vehicle in self._vehicles.values():
            if find_fn(vehicle):
                yield vehicle
    #:

    def __iter__(self):
        for vehicle in self._vehicles.values():
            yield vehicle
    #:

    def __len__(self) -> int:
        return len(self._vehicles)
    #:

    def remove_by_id(self, license_plate: str) -> Vehicle | None:
        vehicle = self._vehicles.get(license_plate)
        if vehicle:
            del self._vehicles[license_plate]
        return vehicle
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

"""
class A:
    def __init__(self, x: int):
        self.x = x
    #:
    @classmethod
    def from_dobro(cls, dobro_de_x: int):
        return cls(dobro_de_x//2)

class B(A):
    def soma(self, b):
        return self.x  + b
    
obj1 = A(20)
obj2 = A.from_dobro(40)

obj3 = B(100)
obj4 = B.from_dobro(200)

"""
