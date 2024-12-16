"""
Manages access to the underlying storage for products. Products are
stored in a CSV file. This modules provides two types to represent 
products in memory:

- `Product`: a product in memory

- `ProductCollection`: manages a collection of products in memory. This
  collection can be loaded/updated from/to a CSV file.

"""

from decimal import Decimal as dec
import re
from typing import Iterable, TextIO


CSV_DELIM = ','
PRODUCT_TYPES = {
    "AL": "Alimentação",
    "DL": "Detergentes p/ Loiça",
    "FRL": "Frutas e Legumes",
}


class Product:
    # id, designacao,tipo/categoria,quantidade,preco unitário
    def __init__(
            self,
            id_: int,        # > 0 e cinco dígitos
            name: str,       # pelo menos 2 palavras com pelo menos 2 cars.
            prod_type: str,  # tipo só pode ser 'AL', 'DL', 'FRL'
            quantity: int,   # >= 0
            price: dec,      # >= 0
    ):
        # 1. Validar parâmetros
        if id_ <= 0 or len(str(id_)) != 5:
            raise InvalidProdAttr(f"{id_=} inválido (deve ser > 0 e ter 5 dígitos)")

        if not Product.validate_name(name):
            raise InvalidProdAttr(f"{name=} inválido")

        if prod_type not in PRODUCT_TYPES:
            raise InvalidProdAttr(f"{prod_type=}: tipo não reconhecido.")

        if quantity < 0:
            raise InvalidProdAttr(f"{quantity=} inválida (deve ser >= 0)")

        if price < 0:
            raise InvalidProdAttr(f"{price=} inválido (deve ser >= 0)")

        # 2. Inicializar/definir o objecto
        self.id = id_
        self.name = name
        self.prod_type = prod_type
        self.quantity = quantity
        self.price = price
    #:

    @classmethod
    def from_csv(cls, csv: str, csv_delim = CSV_DELIM) -> 'Product':
        attrs = csv.split(csv_delim)
        return cls(
            id_= int(attrs[0].strip()),
            name = attrs[1].strip(),
            prod_type = attrs[2].strip(),
            quantity = int(attrs[3].strip()),
            price = dec(attrs[4].strip())
        )
    #:

    def to_csv(self, csv_delim = CSV_DELIM) -> str:
        return csv_delim.join((
            str(self.id),
            self.name,
            self.prod_type,
            str(self.quantity),
            str(self.price),
        ))
    #:

    def __str__(self) -> str:
        return f'Produto[id: {self.id} nome: {self.name}]'
    #:

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return f"{cls_name}({self.id}, '{self.name}', '{self.prod_type}', {self.quantity}, Decimal('{self.price}'))"
    #:

    def __eq__(self, o) -> bool:  
        if not isinstance(o, Product):
            return False
        return self.id == o.id
    #:  

    @property
    def desc_tipo(self) -> str:
        return PRODUCT_TYPES[self.prod_type]
    #:

    @staticmethod
    def validate_name(name: str) -> bool:
        com_acento = 'ñãàáâäåéèêęēëóõôòöōíîìïįīúüùûūÑÃÀÁÂÄÅÉÈÊĘĒËÓÕÔÒÖŌÍÎÌÏĮĪÚÜÙÛŪ'
        return bool(re.fullmatch(rf"[a-zA-Z{com_acento}]{{2,}}(\s+[a-zA-Z{com_acento}]{{2,}})*", name))
    #:
#:


class InvalidProdAttr(ValueError):
    """
    Invalid Product Attribute.
    """
#:

class ProductCollection:
    def __init__(self, initial_values: Iterable[Product] = ()):
        self._products: list[Product] = []
        for prod in initial_values:
            self.append(prod)
    #:

    @classmethod
    def from_csv(cls, csv_path: str, csv_delim = CSV_DELIM, encoding = 'UTF-8') -> 'ProductCollection':
        prods = ProductCollection()
        with open(csv_path, 'rt', encoding = encoding) as file:
            for line in relevant_lines(file):
                prods.append(Product.from_csv(line, csv_delim))
        return prods
    #:

    def export_to_csv(self, csv_path: str, csv_delim = CSV_DELIM, encoding = 'UTF-8'):
        if len(self._products) == 0:
            raise ValueError("Coleccção vazia")
        with open(csv_path, 'wt', encoding = encoding) as file:
            for prod in self._products:
                print(prod.to_csv(csv_delim), file=file)
    #:

    def append(self, novo_prod: Product):
        if self.search_by_id(novo_prod.id):
            raise DuplicateValue(f'Produto já existe com id {novo_prod.id}')
        self._products.append(novo_prod)
    #:

    def search_by_id(self, id_: int) -> Product | None:
        for prod in self._products:
            if prod.id == id_:
                return prod
        return None
    #:

    def search(self, find_fn):
        for prod in self._products:
            if find_fn(prod):
                yield prod
    #:

    def __iter__(self):
        for prod in self._products:
            yield prod
    #:

    def __len__(self) -> int:
        return len(self._products)
    #:

    def remove_by_id(self, id_: int) -> Product | None:
        prod = self.search_by_id(id_)
        if prod:
            self._products.remove(prod)
        return prod
    #:

    def _dump(self):
        for prod in self._products:
            print(prod)
    #:

    def __eq__(self, col) -> bool:  
        if not isinstance(col, ProductCollection):
            return False
        return self._products == col._products
    #:  
#:

def relevant_lines(file: TextIO):
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith('#'):
            continue
        yield line
#:

class DuplicateValue(Exception):
    """
    If there is a duplicate product in a ProductCollection.
    """

