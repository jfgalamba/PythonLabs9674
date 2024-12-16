"""
Programa para gestão do catálogo de produtos. Este programa permite:
    - Listar o catálogo
    - Pesquisar por alguns campos 
    - Eliminar um registo do catálogo
    - Guardar o catálogo em ficheiro
"""

from decimal import Decimal as dec
import re
from typing import TextIO


CSV_DELIM = ','
PRODUCT_TYPES = {
    "AL": "Alimentação",
    "DL": "Detergentes p/ Loiça",
    "FRL": "Frutas e Legumes",
}


class Produto:
    # id, designacao,tipo/categoria,quantidade,preco unitário
    def __init__(
            self,
            id_: int,  # > 0 e cinco dígitos
            nome: str,  # pelo menos 2 palavras com pelo menos 2 cars.
            tipo: str,  # tipo só pode ser 'AL', 'DL', 'FRL'
            quantidade: int,  # >= 0
            preco: dec,  # >= 0
    ):
        # 1. Validar parâmetros
        if id_ <= 0 or len(str(id_)) != 5:
            raise InvalidProdAttr(f"{id_=} inválido (deve ser > 0 e ter 5 dígitos)")

        if not valida_nome(nome):
            raise InvalidProdAttr(f"{nome=} inválido")

        if tipo not in PRODUCT_TYPES:
            raise InvalidProdAttr(f"{tipo=}: tipo não reconhecido.")

        if quantidade < 0:
            raise InvalidProdAttr(f"{quantidade=} inválida (deve ser >= 0)")

        if preco < 0:
            raise InvalidProdAttr(f"{preco=} inválido (deve ser >= 0)")

        # 2. Inicializar/definir o objecto
        self.id = id_
        self.nome = nome
        self.tipo = tipo
        self.quantidade = quantidade
        self.preco = preco
    #:

    @classmethod
    def from_csv(cls, csv: str, csv_delim = CSV_DELIM) -> 'Produto':
        attrs = csv.split(csv_delim)
        return Produto(
            id_= int(attrs[0]),
            nome = attrs[1],
            tipo = attrs[2],
            quantidade = int(attrs[3]),
            preco = dec(attrs[4])
        )
    #:

    def __str__(self) -> str:
        return f'Produto[id: {self.id} nome: {self.nome}]'
    #:

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return f"{cls_name}({self.id}, '{self.nome}', '{self.tipo}', {self.quantidade}, Decimal('{self.preco}'))"
    #:

    @property
    def desc_tipo(self) -> str:
        return PRODUCT_TYPES[self.tipo]
    #:
#:

def valida_nome(nome: str) -> bool:
    com_acento = 'ñãàáâäåéèêęēëóõôòöōíîìïįīúüùûūÑÃÀÁÂÄÅÉÈÊĘĒËÓÕÔÒÖŌÍÎÌÏĮĪÚÜÙÛŪ'
    return bool(re.fullmatch(rf"[a-zA-Z{com_acento}]{{2,}}(\s+[a-zA-Z{com_acento}]{{2,}})*", nome))
#:

class InvalidProdAttr(ValueError):
    """
    Invalid Product Attribute.
    """
#:

class ProductCollection:
    def __init__(self):
        self._produtos: list[Produto] = []
    #:

    @classmethod
    def from_csv(cls, csv_path: str) -> 'ProductCollection':
        prods = ProductCollection()
        with open(csv_path, 'rt') as file:
            for line in relevant_lines(file):
                prods.append(Produto.from_csv(line))
        return prods
    #:

    def append(self, novo_prod: Produto):
        if self.search_by_id(novo_prod.id):
            raise DuplicateValue(f'Produto já existe com id {novo_prod.id}')
        self._produtos.append(novo_prod)
    #:

    def search_by_id(self, id_: int) -> Produto | None:
        for prod in self._produtos:
            if prod.id == id_:
                return prod
        return None
    #:

    def _dump(self):
        for prod in self._produtos:
            print(prod)
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

def main():
    try: 
        prods = ProductCollection.from_csv('produtos.csv')
    except InvalidProdAttr as ex:
        print("Erro ao carregar produtos")
        print(ex)
    else:  # noexception:
        prods._dump()
#:

# def main():
#     # produtos = ler ficheiro 'produtos.csv'
#     try:
#         prod1 = Produto(
#             id_=30987,
#             nome="pão de milho",
#             tipo="AL",
#             quantidade=2,
#             preco=dec("1"),
#         )

#         prod2 = Produto(
#             id_=30098,
#             nome="Leite mimosa",
#             tipo="AL",
#             quantidade=10,
#             preco=dec("2"),
#         )

#         prod3 = Produto.from_csv('21109,fairy,DL,20,3')

#         produtos = ProductCollection()
#         produtos.append(prod1)
#         produtos.append(prod2)
#         produtos.append(prod3)
#         produtos.append(prod3)
        
#         produtos._dump()
    
#     except ValueError as ex:
#         print("Erro: atributo inválido")
#         print(ex)
#     except DuplicateValue as ex:
#         print("Erro: produto duplicado")
#         print(ex)
# #:


if __name__ == "__main__":  # verifica se o script foi executado
    main()  # na linha de comandos
