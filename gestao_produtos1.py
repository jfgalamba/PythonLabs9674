"""
Programa para gestão do catálogo de produtos. Este programa permite:
    - Listar o catálogo
    - Pesquisar por alguns campos 
    - Eliminar um registo do catálogo
    - Guardar o catálogo em ficheiro
"""

from decimal import Decimal as dec
import re


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
#:

def valida_nome(nome: str) -> bool:
    return bool(re.fullmatch(r"[a-zA-Zã]{2,}(\s+[a-zA-Zã]{2,})*", nome))
#:

# def valida_nome2(nome: str) -> bool:
#     palavras = nome.split()
#     if len(palavras) < 2:
#         return False
#     return all(len(palavra) >= 2 for palavra in palavras)
# #:

# def valida_nome(nome: str) -> bool:
#     palavras = nome.split()
#     if len(palavras) < 2:
#         return False
#     for palavra in palavras:
#         if len(palavra) < 2:
#             return False
#     return True
# #:

class InvalidProdAttr(ValueError):
    """
    Invalid Product Attribute.
    """
#:

# class A(B):
#     """
#     Classe A deriva de B (ou seja, A herda de B)
#     """
# #:


def main():
    # 30987,pão de milho,AL,2,1
    try:
        prod1 = Produto(
            id_=-30987,
            nome="pão de milho",
            tipo="AL",
            quantidade=2,
            preco=dec("1"),
        )

        prod2 = Produto(
            id_=30098,
            nome="Leite mimosa",
            tipo="AL",
            quantidade=10,
            preco=dec("2"),
        )

        print(f"Produto ID: {prod1.id} NOME: {prod1.nome} ")
        print(f"Produto ID: {prod2.id} NOME: {prod2.nome} ")
    except ValueError as ex:
        print("Erro: atributo inválido")
        print(ex)
#:


if __name__ == "__main__":  # verifica se o script foi executado
    main()  # na linha de comandos
