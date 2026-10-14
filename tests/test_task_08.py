"""Відкриті приклади завдання 08: Ефективні ліміти дерева cgroup."""
import pytest
from conftest import load

M = load(8)
solve = M.solve

PUBLIC = [(({'/': {},
    '/app': {'memory.max': '1073741824', 'cpu.max': '200000 100000'},
    '/app/web': {'memory.max': '268435456', 'memory.current': 100663296, 'cpu.max': 'max 100000'},
    '/app/db': {'memory.current': 419430400}},),
  ["/app/db: пам'ять 1 ГіБ; використано 400 МіБ; у межах; CPU 2.00",
   "/app/web: пам'ять 256 МіБ; використано 96 МіБ; у межах; CPU 2.00"]),
 (({'/svc': {'memory.max': '1048576', 'memory.current': 1572864}},),
  ["/svc: пам'ять 1 МіБ; використано 1536 КіБ; перевищення 512 КіБ; CPU без обмежень"])]

HIDDEN = []


@pytest.mark.parametrize("args,expected", PUBLIC + HIDDEN)
def test_solve(args, expected):
    assert solve(*args) == expected


def test_functions_exist():
    assert callable(getattr(M, "solve", None)), "немає функції solve"
