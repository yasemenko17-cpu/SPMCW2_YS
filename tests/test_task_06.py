"""Відкриті приклади завдання 06: Лічильник посилань і цикли."""
import pytest
from conftest import load

M = load(6)
solve = M.solve

PUBLIC = [((['a', 'b', 'c', 'd'], [('a', 'b'), ('b', 'a'), ('c', 'd')], ['a', 'c'], ['a', 'c']),
  (['c', 'd'], [], ['a', 'b'])),
 ((['a', 'b', 'c', 'd'], [('a', 'b'), ('b', 'a'), ('c', 'd')], ['a', 'c'], ['c']),
  (['c', 'd'], ['a', 'b'], []))]

HIDDEN = []


@pytest.mark.parametrize("args,expected", PUBLIC + HIDDEN)
def test_solve(args, expected):
    assert solve(*args) == expected


def test_functions_exist():
    assert callable(getattr(M, "solve", None)), "немає функції solve"
