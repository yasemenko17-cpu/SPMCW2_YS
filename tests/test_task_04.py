"""Відкриті приклади завдання 04: Правила зміни ліміту ресурсу."""
import pytest
from conftest import load

M = load(4)
solve = M.solve

PUBLIC = [(((1024, 4096), (512, 4096), False), "OK: м'який=512, жорсткий=4096"),
 (((1024, 4096), (1024, 8192), False), 'EPERM')]

HIDDEN = []


@pytest.mark.parametrize("args,expected", PUBLIC + HIDDEN)
def test_solve(args, expected):
    assert solve(*args) == expected


def test_functions_exist():
    assert callable(getattr(M, "solve", None)), "немає функції solve"
