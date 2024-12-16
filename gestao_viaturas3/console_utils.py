"""
Utilities useful to develop simple console/terminal/text-mode based 
applications.
"""

import os
import subprocess
from typing import Iterable


__all__ = [
    'accept',
    'show_msg',
    'confirm',
    'ask',
    'show_msg',
    'show_msgs',
    'show_table',
    'pause',
    'cls',
]

DEFAULT_INDENTATION = 3


def accept(
        msg: str, 
        error_msg: str, 
        check_fn = lambda _: True,
        convert_fn = lambda x: x, 
        indent = DEFAULT_INDENTATION
):
    """
    Accepts a value read from the standard input, optionally 
    validating it with `check_fn` and converting it to another type
    with `convert_fn`. Note that the value will only be accepted 
    if `check_fn` returns `True` and `convert_fn` successfully 
    completes. Thus, `check_fn` should be a boolean function, while 
    `convert_fn` should signal a failed conversion by raising an 
    exception. `check_fn` is called before `convert_fn` and is applied
    directly to the string value read from stdin. Of course, you can
    implement all the validation logic in `convert_fn`, without ever 
    needing to use `check_fn`.

    Examples:
    1. Accept an integer:
        accept(
            msg = "Enter an integer: ",
            error_msg = "Invalid integer {}",
            convert_fn = int,
        )

    2. Accept a positive integer:
        accept(
            msg = "Enter a positive integer: ",
            error_msg = "Invalid value {}",
            check_fn = str.isdigit,
            convert_fn = int,
        )

    3. Accept a positive integer, 2nd version:
        def to_positive_int(val: str) -> int:
            int_val = int(val)
            if int_val <= 0:
                raise ValueError(f'{val} is not a positive integer')
            return int_val

        accept(
            msg = "Enter a positive integer: ",
            error_msg = "Invalid value {}",
            convert_fn = to_positive_int,
        )

    4. Accept a positive integer with exactly five digits:
        accept(
            msg = "Enter a valid ID: ",
            error_msg = "Invalid text {}",
            check_fn = lambda id_: id_.isdigit() and len(id_) == 5 and id_[0] != 0,
            convert_fn = int,
        )

    5. Accept a non-emtpy string with at least two characters:
        accept(
            msg = "Enter valid text: ",
            error_msg = "Invalid ID {}",
            check_fn = lambda txt: len(txt.strip()) >= 2,
        )
    """
    while True:
        value_str = ask(msg, indent = indent)
        if check_fn(value_str):
            try:
                return convert_fn(value_str)
            except Exception:
                pass
        # we reached this point iif the check failed or an
        # exception was raised
        show_msg(error_msg.format(value_str))
        pause('')
        cls()
#:

def confirm(msg: str, default = '', indent = DEFAULT_INDENTATION) -> bool:
    """
    >>> confirm("Do you like peanuts? ")
    Do you like peanuts? [yn] maybe
    Please answer Y or N.
    Do you like peanuts? [yn]
    An explicit answer is required. Please answer Y or N.
    Do you like peanuts? [yn] n
    False
    >>> confirm("Will it rain tomorrow? ", default = 'Y')
    Will it rain tomorrow? [Yn] ja
    Please answer Y or N.
    Will it rain tomorrow? [Yn]
    True
    >>> confirm("Tomorrow is the day after yesterday? ", default = 'N')
    Tomorrow is the day after yesterday? [yN] nein
    Please answer Y or N.
    Tomorrow is the day after yesterday? [yN]
    False
    >>> confirm("Tomorrow is the day after yesterday? ", default = 'BATATAS')
    Traceback (most recent call last):
    ...
    ValueError: Invalid default value: BATATAS
    """
    default_text = {
        'Y': '[Yn]',
        'N': '[yN]',
        '': '[yn]'
    }.get(default)
    if default_text is None:
        raise ValueError(f"Invalid default value: {default}")
    msg += f'{default_text} '
    while True:
        ans = ask(msg, indent = indent).strip()
        match ans.upper():
            case 'Y' | 'YES':
                return True
            case 'N' | 'NO':
                return False
            case '':
                if default:
                    return default == 'Y'
                show_msg("An explicit answer is required. Please answer Y or N.", indent = indent)
            case _:
                print("Please answer Y or N.")
#:

def ask(msg: str, indent = DEFAULT_INDENTATION) -> str:
    return input(f"{indent * ' '}{msg}")
#:

def show_msg(*args, indent = DEFAULT_INDENTATION, **kargs):
    print_args = [' ' * (indent - 1), *args] if indent > 0 else [*args]
    print(*print_args, **kargs)
#:

def show_msgs(msgs: Iterable[str], *args, indent = DEFAULT_INDENTATION, **kargs):
    for msg in msgs:
        show_msg(msg, *args, indent = indent, **kargs)
#:

def show_table(
        elements: Iterable, 
        col_defs: dict[str, dict], 
        *show_args, 
        **show_kargs
):
    # Generate HEADER
    header_fmt = ' | '.join(f"{{:^{col['width']}}}" for col in col_defs.values())
    header = header_fmt.format(*(col['name'] for col in col_defs.values()))

    # Generate SEPARATOR between HEADER and DATA
    # Generate `width + 2` dashes for all columns except for the first
    # and last columns; in this case, generate `width + 1` dashes.
    sep_fmt = '+'.join('{}' for _ in col_defs)
    col_defs_values = list(col_defs.values())
    sep = sep_fmt.format(
        *[
            f"{'-' * (col_defs_values[0]['width'] + 1)}",
            *(f"{'-' * (col_def['width'] + 2)}" for col_def in col_defs_values[1:-1]),
            f"{'-' * (col_defs_values[-1]['width'] + 1)}",
        ]
    )

    # Generate DATA LINES
    def data_field_fmt_spec(col_def: dict) -> str:
        align = f"{col_def['align']}"
        width = f"{col_def['width']}"
        return f"{{:{align}{width}}}"
    #:
    data_line_fmt = ' | '.join(
        data_field_fmt_spec(col_def) for col_def in col_defs_values
    )

    data_lines = []
    for elem in elements:
        args = []
        for attr, col_def in col_defs.items():
            val = getattr(elem, attr)
            convert_fn = col_def.get('convert_fn', lambda x: x)
            val = convert_fn(val)
            if 'decimal_places' in col_def:
                decimal_places_fmt = f'{{:.{col_def['decimal_places']}f}}' 
                val = decimal_places_fmt.format(val)
            unit = col_def.get('unit', '')
            args.append(f'{val}{unit}')
        data_lines.append(data_line_fmt.format(*args))

    if not data_lines:
        raise ValueError('Asked to generate table for empty collection/iterable.')

    # Now show everything 
    show_msg(header, *show_args, **show_kargs)
    show_msg(sep, *show_args, **show_kargs)
    show_msgs(data_lines, *show_args, **show_kargs)
#:

def pause(msg: str="Pressione ENTER para continuar...", indent = DEFAULT_INDENTATION):
    if msg:
        show_msg(msg, indent = indent)
    match os.name:
        case 'nt':      # Windows (excepto Win9X)
            os.system("pause>null|set/p=''")
        case 'posix':   # Unixes e compatíveis
            if os.path.exists('/bin/bash'):
                os.system('/bin/bash -c "read -s -n 1"')
            else:
                input()
        case _:
            input()
#:

def cls():
    """
    https://stackoverflow.com/questions/4553129/when-to-use-os-name-sys-platform-or-platform-system
    """
    match os.name:
        case 'nt':      # Windows (excepto Win9X)
            subprocess.run(['cls'], shell=True)
        case 'posix':   # Unixes e compatíveis
            subprocess.run(['clear'])
#:

def posix_shell_in_use() -> str:
    return os.environ.get('SHELL', '/bin/sh')
#:


"""
PROGRAMAÇÃO FUNCIONAL (INTRO);

# def filtra_pares(nums: Iterable) -> list:
#     encontrados = []
#     for num in nums:
#         if num % 2 == 0:
#             encontrados.append(num)
#     return encontrados
# #:

# def filtra_positivos(nums: Iterable) -> list:
#     encontrados = []
#     for num in nums:
#         if num > 0:
#             encontrados.append(num)
#     return encontrados
# #:

# criterio -> função que recebe um elemento e devolve ou True ou False
#             (ou seja, é uma função booleana)

nums = [10, -20, 31, 44, 73]
nomes = ('Alberto', 'Ana', 'Arnaldo', 'Zé')

def filtra(elems: Iterable, criterio) -> list:
    encontrados = []
    for elem in elems:
        if criterio(elem):
            encontrados.append(elem)
    return encontrados
#:

def is_positive(num) -> bool:
    return num > 0
#:

def cinco_ou_mais(txt: str) -> bool:
    return len(txt) >= 5
#:

filtra(nums, is_positive)
filtra(nomes, cinco_ou_mais)

filtra(nums, lambda num: num > 0)
filtra(nomes, lambda nome: len(nome) >= 5)


# EM PSEUDO-JS:
# 
# filtra(nums, (num) => num > 0)
# filtra(nums, function(num) { 
#     return num > 0;
# })

"""

# col_defs1 = [
#     {'attr': 'id','name': 'ID', 'align': '^', 'width': 8},
#     {'attr': 'name','name': 'Nome', 'align': '<', 'width': 26},
#     {'attr': 'prod_type','name': 'Tipo', 'align': '<', 'width': 8},
#     {'attr': 'quantity','name': 'Quantidade', 'align': '>', 'width': 16},
#     {'attr': 'price','name': 'Preço', 'align': '>', 'width': 14, 'decimal_places': 2},
# ]

# import products
# elements1 = products.ProductCollection.from_csv('products.csv')
# show_table(elements1, col_defs1)

# col_defs2 = [
#     {'attr': 'firstname', 'name': 'First Name', 'align': '^', 'width': 10},
# ]
# class Person:
#     def __init__(self, firstname):
#         self.firstname = firstname

# elements2 = [Person('Manel'), Person('Fernando')]
# show_table(elements2, col_defs2)

