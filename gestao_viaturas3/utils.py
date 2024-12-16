"""
Common general utilities.
"""

from collections import namedtuple
import os
import pathlib
import subprocess
import tempfile


__all__ = [
    'is_float',
    'is_int',
    'PipeData',
    'pipe_cmds',
    'valid_path_for_file',
    'is_readable',
    'is_writable',
    'is_special_entry'
]

################################################################################
#
#   TEXT UTILS
#
################################################################################

def is_float(txt: str) -> bool:
    try:
        float(txt)
    except:
        return False
    return True
#:

def is_int(txt: str, base = 10) -> bool:
    try:
        int(txt, base)
        # Note that int(23.2) => 23, but calling int(23.2, 10) (that is,
        # passing an explicit base) produces an exception. That's why
        # isint(23.2) will always be False, even though int(23.2) makes
        # an int.
    except:
        return False
    return True
#:

# ALTERNATIVA 1:
#
# def isfloat0(txt: str) -> bool:
#     return bool(re.fullmatch(r'(-|\+)?([0-9]*\.[0-9]+|[0-9]+\.?)', txt))
# #:
#
# def isint0(txt: str) -> bool:
#     return bool(re.fullmatch(r'(-|\+)?[0-9]+', txt))
# #:
#
# ALTERNATIVA 2:
#
# compilar expressão regular => mais eficiente!
# 
# import re
#
# def _mk_regex_validator(regexp_str: str):
#     regexp = re.compile(regexp_str)
#     return lambda txt: bool(re.fullmatch(regexp, txt))
# #:
# isfloat = _mk_regex_validator(r'(-|\+)?([0-9]*\.[0-9]+|[0-9]+\.?)')
# isint = _mk_regex_validator(r'(-|\+)?[0-9]+')

################################################################################
#
#   SHELL UTILS
#
################################################################################

PipeData = namedtuple('PipeData', 'returncode stdout stderr')


def pipe_cmds(cmd1_args: list[str], cmd2_args: list[str]) -> PipeData:
    """
    Pipes two commands and returns the return code and the output 
    (meaning, the contents of the standard output and standard error)
    of the second command. 
    """
    p1 = subprocess.Popen(
        cmd1_args,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
    )
    p2 = subprocess.Popen(
        cmd2_args,
        stdin = p1.stdout,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
    )
    p1.stdout.close()  # type: ignore
    data = p2.communicate()
    return PipeData(p2.returncode, data[0], data[1])
#:

################################################################################
#
#   FILE UTILS
#
################################################################################

def valid_path_for_file(
        file_path: str,
        unique = False,
        check_w = False,
        check_r = False,
) -> bool:
    """
    Returns `True` if `file_path`:
        - is not a path that is already being used by a dir., socket or 
          any type of entry other than a path available for a file
        - path to parent dir exists
        - has the right permissions, if parameters `check_w` and `check_r` are
          set to `True`
        - doesn't exist if the `unique` is True.
    """
    try:
        path = pathlib.Path(file_path)
        return (
                not is_special_entry(path)
            and not path.is_dir()
            and path.parent.exists()
            and (not unique or not path.exists())
            and (not check_w or is_writable(path))
            and (not check_r or is_readable(path))
        )
    except:
        return False
#:

def is_special_entry(path: pathlib.Path | str) -> bool:
    """
    Whether this path is a special entry. A special entry is path that
    refers to either: block device, char. device, FIFO, junction, mount
    point, socket.
    """
    path = pathlib.Path(path) if isinstance(path, str) else path
    special_entries = (
        pathlib.Path.is_block_device, 
        pathlib.Path.is_char_device, 
        pathlib.Path.is_fifo,
        pathlib.Path.is_socket,
        pathlib.Path.is_junction,
        pathlib.Path.is_mount,
    )
    return any(special_entry_pred(path) for special_entry_pred in special_entries)
#:

def is_readable(path: pathlib.Path | str) -> bool:
    """
    A path is readable if it points to an existing entry and that
    entry is readable. 
    If the path is either an existing file, or a directory, the best
    way to check if it's readable is by trying to read from it. If the
    path is a file, we try to open it for reading. If the path is a
    directory, we try to check to see if we can list it with `os.walk`.
    If the path is a special entry, we use `os.access` to query its 
    flags, otherwise opening it may block the process.
    WARNING: Tested only on macOS.
    """
    path = pathlib.Path(path) if isinstance(path, str) else path
    if path.is_dir():
        return bool(next(os.walk(path), False))
    if path.is_file():
        try:
            file = open(path, 'r')
        except OSError:
            return False
        else:
            file.close()
            return True
    return os.access(path, os.R_OK)
#:

def is_writable(path: pathlib.Path | str) -> bool:
    """
    If the path already exists and is either a file or a special entry, 
    we use `os.access` to find out if the path is writable [1].
    If the path doesn't exists or points to a directory, there is no
    sure way to find if a path is writable before actually trying to 
    open it for writing. That's what we do here.
    If the path points to a directory, we try to create a temporary
    file inside of it. If the path is not a directory, then it doesn't
    exist (see [1]). In this case, the path is writable if we can 
    create a temporary file in the parent directory.
    WARNING: Tested only on macOS.
    """
    path = pathlib.Path(path) if isinstance(path, str) else path

    if path.is_file() or is_special_entry(path):
        return os.access(path, os.W_OK)

    try:
        if not path.is_dir():
            path = path.parent
        file = tempfile.TemporaryFile(dir=str(path)) 
    except OSError:
        return False
    else:
        file.close()
        return True
#:

def path_exists(path: pathlib.Path | str) -> bool:
    return os.path.exists(path)
#: