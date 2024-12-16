"""
A console client to manage a collection of products.
"""

import sys


from vehicles import VehicleCollection, Vehicle, InvalidAttr
from console_utils import accept, ask, show_msg, show_table, cls, pause, confirm
from utils import valid_path_for_file, path_exists

################################################################################
##
##       MAIN, MENU PRINCIPAL, E INTERACÇÃO COM O UTILIZADOR
##
################################################################################

VEHICLES_CSV_PATH = 'vehicles.csv'

vehicles_collection: VehicleCollection


def main():
    global vehicles_collection
    try:
        vehicles_collection = VehicleCollection.from_csv(VEHICLES_CSV_PATH)
        exec_menu()
    except KeyboardInterrupt:
        exec_end()
    except InvalidAttr as ex:
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
        show_msg("┃   P  - Pesquisar por matrícula            ┃")
        show_msg("┃   PM - Pesquisar por marca                ┃")
        show_msg("┃   A  - Acrescentar viatura                ┃")
        show_msg("┃   E  - Eliminar viatura                   ┃")
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
                exec_list_vehicles()
            case 'P' | 'PESQUISAR':
                exec_search_by_id()
            case 'PM' | 'MARCA':
                exec_search_by_make()
            case 'A' | 'NOVO':
                exec_add_new_vehicle()
            case 'E' | 'R' | 'ELIMINAR' | 'REMOVER':
                exec_remove_vehicle()
            case 'G' | 'GUARDAR':
                exec_save()
            case  'T' | 'TERMINAR':
                exec_end()
            case _:
                show_msg(f"Opção {option} inválida ou ainda não implementada")
                pause()
#:

def exec_remove_vehicle():
    enter_menu("REMOÇÃO DE VEÍCULO")
    license_plate = accept(
        msg = "Indique a matrícula do veículo a remover: ",
        error_msg = "Matrícula {} inválida! Tente novamente.",
        check_fn = Vehicle.validate_license_plate
    )
    print()

    if vehicle := vehicles_collection.remove_by_id(license_plate):
        show_msg("Veículo encontrado e removido.")
        print()
        show_table_with_vehicles(VehicleCollection([vehicle]))
    else:
        show_msg(f"Veículo com matrícula {license_plate} não encontrado.")

    print()
    pause()
#:

def exec_list_vehicles():
    enter_menu("VIATURAS")
    show_table_with_vehicles(vehicles_collection)
    print()
    pause()
#:

def exec_search_by_id():
    enter_menu("PESQUISA POR MATRÍCULA")
    license_plate = accept(
        msg = "Indique a matrícula do veículo a pesquisar: ",
        error_msg = "Matrícula {} inválida! Tente novamente.",
        check_fn = Vehicle.validate_license_plate,
    )
    print()

    if prod := vehicles_collection.search_by_id(license_plate):
        show_msg("Veículo encontrado.")
        print()
        show_table_with_vehicles(VehicleCollection([prod]))
    else:
        show_msg(f"Veículo com matrícula {license_plate} não encontrado.")

    print()
    pause()
#:

def exec_search_by_make():
    enter_menu("PESQUISA POR MARCA")
    make = accept(
        msg = "Indique a marca de veículos a pesquisar: ",
        error_msg = "Marca {} inválida! Tente novamente",
        check_fn = Vehicle.validate_make,
    )
    print()

    if vehicles := vehicles_collection.search(lambda veh: veh.make == make):
        show_msg("Foram encontrados os veículos:")
        print()
        show_table_with_vehicles(VehicleCollection(vehicles))
    else:
        show_msg(f"Não foram encontrados veículos da marca {make}.")

    print()
    pause()
#:

def exec_add_new_vehicle():
    enter_menu("ADICIONAR NOVO VEÍCULO")
    show_msg("Insira os seguintes valores")

    label = '{:<10} : '.format

    while True:
        license_plate = accept(
            msg = label("Matrícula"),
            error_msg = "Matrícula {} inválida",
            check_fn = Vehicle.validate_license_plate,
        )
        if not vehicles_collection.search_by_id(license_plate):
            break
        show_msg(f"Já existe um veículo com a matrícula {license_plate}!")

    make = accept(
        msg = label("Marca"),
        error_msg = "Marca inválida: {}! Tente novamente.",
        check_fn = Vehicle.validate_make,
    )
    model = accept(
        msg = label("Modelo"),
        error_msg = "Modelo {} inválido! Tente novamente.",
        check_fn = Vehicle.validate_model,
    )
    date = accept(
        msg = label("Data"),
        error_msg = "Data {} inválida!. Tente novamente",
        check_fn = Vehicle.validate_date,
    )
    vehicles_collection.append(Vehicle(license_plate, make, model, date))

    show_msg(f"Veículo com matrícula {license_plate} adicionado com sucesso")
    print()
    pause()
#:

def exec_save():
    enter_menu("GUARDAR CATÁLOGO DE VIATURAS")
    file_path = accept(
        msg = "Caminho para o ficheiro onde guardar o catálogo: ",
        error_msg = "Caminho {} inválido",
        check_fn = lambda p: valid_path_for_file(p, check_w = True)
    )
    if path_exists(file_path) and not confirm("Caminho existe. Deseja escrever por cima? "):
        pause("Volte a tentar novamente...")
        return 
    vehicles_collection.export_to_csv(file_path)
    show_msg(f"Colecção de viaturas  exportada para {file_path}")
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

def show_table_with_vehicles(vehicles: VehicleCollection):
    show_table(
        vehicles,
        col_defs = {
            'license_plate': {'name': 'Matrícula', 'align': '^', 'width': 10},
            'make': {'name': 'Marca', 'align': '<', 'width': 20},
            'model': {'name': 'Modelo', 'align': '<', 'width': 20},
            'date': {'name': 'Data', 'align': '>', 'width': 12, 'convert_fn': str},
        },
    )
#:

def enter_menu(title: str):
    cls()
    show_msg(title.upper())
    print()
#:

if __name__ == '__main__':
    main()