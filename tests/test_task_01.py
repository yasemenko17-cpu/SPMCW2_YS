"""Відкриті приклади завдання 01: Цілі з байтів: порядок і знак."""
import pytest
from conftest import load

M = load(1)
solve = M.solve

PUBLIC = [(('E8 03',), 'LE: 1000 / 1000; BE: 59395 / -6141'), (('ff',), 'LE: 255 / -1; BE: 255 / -1')]

HIDDEN = []


@pytest.mark.parametrize("args,expected", PUBLIC + HIDDEN)
def test_solve(args, expected):
    assert solve(*args) == expected


def test_functions_exist():
    assert callable(getattr(M, "solve", None)), "немає функції solve"
