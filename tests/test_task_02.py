"""Відкриті приклади завдання 02: Сторінки віртуальної пам'яті."""
import pytest
from conftest import load

M = load(2)
solve = M.solve

PUBLIC = [((4100, 5000, 4096),
  'сторінок: 2 (від 1 до 2); зсув у першій: 4; початок першої: 0x1000; покрито: 8192 Б, не використано: 3192 '
  'Б'),
 ((0, 1, 4096),
  'сторінок: 1 (від 0 до 0); зсув у першій: 0; початок першої: 0x0; покрито: 4096 Б, не використано: 4095 Б')]

HIDDEN = []


@pytest.mark.parametrize("args,expected", PUBLIC + HIDDEN)
def test_solve(args, expected):
    assert solve(*args) == expected


def test_functions_exist():
    assert callable(getattr(M, "solve", None)), "немає функції solve"
