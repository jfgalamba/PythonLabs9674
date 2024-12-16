"""
A console client to manage a collection of products.
"""

import sys
from decimal import Decimal as dec


from products import ProductCollection, Product, PRODUCT_TYPES, InvalidProdAttr
from console_utils import accept, ask, show_msg, cls, pause, show_table, confirm
from utils import is_float, valid_path_for_file, path_exists

################################################################################
##
##       MAIN, MENU PRINCIPAL, E INTERACÇÃO COM O UTILIZADOR
##
################################################################################

PRODUCTS_CSV_PATH = 'products.csv'

prods_collection: ProductCollection

"""
        ..  Git Tutorial for Beginners: Learn Git in 1 Hour: 
            https://www.youtube.com/watch?v=8JJ101D3knE

        ..  Git and GitHub - CS50W (Lesson 1)
            https://www.youtube.com/watch?v=NcoBAfJ6l2Q
"""

def main():
    global prods_collection
    try:
        prods_collection = ProductCollection.from_csv(PRODUCTS_CSV_PATH)
        exec_menu()
    except KeyboardInterrupt:
        exec_end()
    except InvalidProdAttr as ex:
        show_msg("Erro ao ler catálogo de produtos:")
        show_msg(ex)
#:

def exec_menu():
    while True:
        cls()
        print()
        show_msg("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        show_msg("┃                                           ┃")
        show_msg("┃   L  - Listar catálogo                    ┃")
        show_msg("┃   P  - Pesquisar por id                   ┃")
        show_msg("┃   PT - Pesquisar por tipo                 ┃")
        show_msg("┃   A  - Acrescentar produto                ┃")
        show_msg("┃   E  - Eliminar produto                   ┃")
        show_msg("┃   G  - Guardar catálogo em ficheiro       ┃")
        show_msg("┃                                           ┃")
        show_msg("┃   T  - Terminar programa                  ┃")
        show_msg("┃                                           ┃")
        show_msg("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        print()

        option = ask("  OPÇÃO> ")
        if len(option.strip()) == 0:
            continue

        match option.upper():
            case 'L' | 'LISTAR':
                exec_list_products()
            case 'P' | 'PESQUISAR':
                exec_search_by_id()
            case 'PT' | 'TIPO':
                exec_search_by_type()
            case 'A' | 'NOVO':
                exec_add_new_product()
            case 'E' | 'R' | 'ELIMINAR' | 'REMOVER':
                exec_remove_product()
            case 'G' | 'GUARDAR':
                exec_save()
            case  'T' | 'TERMINAR':
                exec_end()
            case _:
                show_msg(f"Opção {option} inválida ou ainda não implementada")
                pause()
#:

def exec_list_products():
    enter_menu("PRODUTOS")
    show_table_with_prods(prods_collection)
    print()
    pause()
#:

def exec_search_by_id():
    enter_menu("PESQUISA POR ID")
    id_ = accept(
        msg = "Indique o ID do produto a pesquisar: ",
        error_msg = "ID {} inválido! Tente novamente.",
        convert_fn = int,
    )
    print()

    if prod := prods_collection.search_by_id(id_):
        show_msg("Produto encontrado.")
        print()
        show_table_with_prods(ProductCollection([prod]))
    else:
        show_msg(f"Produto com ID {id_} não encontrado.")

    print()
    pause()
#:

def exec_search_by_type():
    enter_menu("PESQUISA POR TIPO")
    prod_type = accept(
        msg = "Indique o tipo do produto a pesquisar: ",
        error_msg = "Tipo {} inválido! Tente novamente",
        check_fn = lambda prod: prod in PRODUCT_TYPES,
    )
    print()

    if prods := prods_collection.search(lambda prod: prod.prod_type == prod_type):
        show_msg("Foram encontrados os seguintes produtos:")
        print()
        show_table_with_prods(ProductCollection(prods))
    else:
        show_msg(f"Não foram encontrados produtos com tipo {prod_type}.")

    print()
    pause()
#:

def exec_add_new_product():
    enter_menu("ADICIONAR NOVO PRODUTO")
    show_msg("Insira os seguintes valores")

    label = '{:<10} : '.format
    # EQUIVALENTE A:
    #   def label(msg: str) -> str:
    #       return f'{msg:<10} : '

    while True:
        id_ = accept(
            msg = label("ID"),
            error_msg = "ID {} inválido",
            check_fn = lambda id_: id_.isdigit() and len(id_) == 5 and id_[0] != 0,
            convert_fn = int,
        )
        if not prods_collection.search_by_id(id_):
            break
        show_msg(f"Já existe um produto com o ID {id_}!")

    name = accept(
        msg = label("Designação"),
        error_msg = "Designação inválida: {}! Tente novamente.",
        check_fn = Product.validate_name,
    )
    prod_type = accept(
        msg = label("Tipo"),
        error_msg = "Tipo {} inválido! Tente novamente.",
        check_fn = lambda prod: prod in PRODUCT_TYPES,
    )
    quantity = accept(
        msg = label("Quantidade"),
        error_msg = "Quantidade {} inválida",
        check_fn = str.isdigit,
        convert_fn = int,
    )
    price = accept(
        msg = label("Preço"),
        error_msg = "Preço {} inválido",
        check_fn = is_float,
        convert_fn = dec,
    )
    prods_collection.append(Product(id_, name, prod_type, quantity, price))

    show_msg("Produto {id_} adicionado com sucesso")
    print()
    pause()
#:

def exec_remove_product():
    enter_menu("REMOÇÃO DE PRODUTO")
    id_ = accept(
        msg = "Indique o ID do produto a remover: ",
        error_msg = "ID {} inválido! Tente novamente.",
        convert_fn = int,
    )
    print()

    if prod := prods_collection.remove_by_id(id_):
        show_msg("Produto encontrado e removido.")
        print()
        show_table_with_prods(ProductCollection([prod]))
    else:
        show_msg(f"Produto com ID {id_} não encontrado.")

    print()
    pause()
#:

def exec_save():
    enter_menu("GUARDAR CATÁLOGO DE PRODUTOS")
    file_path = accept(
        msg = "Caminho para o ficheiro onde guardar o catálogo: ",
        error_msg = "Caminho {} inválido",
        check_fn = lambda p: valid_path_for_file(p, check_w = True)
    )
    if path_exists(file_path) and not confirm("Caminho existe. Deseja escrever por cima? "):
        pause("Volte a tentar novamente...")
        return 
    prods_collection.export_to_csv(file_path)
    show_msg(f"Colecção de produtos exportada para {file_path}")

    print()
    pause()
#:

def exec_end():
    cls()
    print()
    show_msg("O programa vai terminar...", indent = 0)
    print()
    sys.exit(0)
#:

def show_table_with_prods(prods: ProductCollection):
    show_table(
        prods,
        col_defs = {
            'id': {'name': 'ID', 'align': '^', 'width': 8},
            'name': {'name': 'Nome', 'align': '<', 'width': 26},
            'prod_type': {'name': 'Tipo', 'align': '<', 'width': 8},
            'quantity': {'name': 'Quantidade', 'align': '>', 'width': 16},
            'price' : {'name': 'Preço', 'align': '>', 'width': 14,
                       'decimal_places': 2, 'unit': '€'},
        }
    )
#:

def enter_menu(title: str):
    cls()
    show_msg(title.upper())
    print()
#:

if __name__ == '__main__':
    main()
