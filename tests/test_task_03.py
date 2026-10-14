"""Відкриті приклади завдання 03: Прототип ctypes за оголошенням C."""
import pytest
from conftest import load

M = load(3)
solve = M.solve

PUBLIC = [(('int abs(int x);',), 'libc.abs.argtypes = [ctypes.c_int]\nlibc.abs.restype = ctypes.c_int'),
 (('size_t strlen(const char *s);',),
  'libc.strlen.argtypes = [ctypes.c_char_p]\nlibc.strlen.restype = ctypes.c_size_t')]

HIDDEN = []


@pytest.mark.parametrize("args,expected", PUBLIC + HIDDEN)
def test_solve(args, expected):
    assert solve(*args) == expected


def test_functions_exist():
    assert callable(getattr(M, "solve", None)), "немає функції solve"
