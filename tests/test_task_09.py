"""Відкриті приклади завдання 09: Аналізатор помилок пам'яті в коді ctypes."""
import pytest
from conftest import load

M = load(9)
solve = M.solve

PUBLIC = [(('import ctypes\nlibc = ctypes.CDLL(None)\np = libc.malloc(16)\nlibc.free(p)',),
  ['Рядок 3: у libc.malloc не задано argtypes',
   'Рядок 3: у libc.malloc не задано restype (повертає вказівник; ctypes припускає int)',
   'Рядок 4: у libc.free не задано argtypes']),
 (('import ctypes\n'
   'libc = ctypes.CDLL(None)\n'
   'libc.memcpy.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]\n'
   'libc.memcpy.restype = ctypes.c_void_p\n'
   'buf = ctypes.create_string_buffer(8)\n'
   'libc.memcpy(buf, b"0123456789abcdef", 16)',),
  ['Рядок 6: memcpy може записати 16 байтів у буфер buf розміром 8'])]

HIDDEN = []


@pytest.mark.parametrize("args,expected", PUBLIC + HIDDEN)
def test_solve(args, expected):
    assert solve(*args) == expected


def test_functions_exist():
    assert callable(getattr(M, "solve", None)), "немає функції solve"
