"""Відкриті приклади завдання 10: Симулятор лімітів cgroup: OOM і pids.max."""
import pytest
from conftest import load

M = load(10)
solve = M.solve

PUBLIC = [(({'/app': {'memory.max': 100, 'pids.max': 2}},
   [('fork', 1, '/app'), ('fork', 2, '/app'), ('fork', 3, '/app')]),
  {'alive': [(1, '/app', 0), (2, '/app', 0)],
   'killed': [],
   'rejected': [3],
   'oom_kill': {},
   'pids_max': {'/app': 1}}),
 (({'/g': {'memory.max': 100}},
   [('fork', 1, '/g'), ('fork', 2, '/g'), ('alloc', 1, 60), ('alloc', 2, 30), ('alloc', 2, 20)]),
  {'alive': [(2, '/g', 50)], 'killed': [1], 'rejected': [], 'oom_kill': {'/g': 1}, 'pids_max': {}})]

HIDDEN = []


@pytest.mark.parametrize("args,expected", PUBLIC + HIDDEN)
def test_solve(args, expected):
    assert solve(*args) == expected


def test_functions_exist():
    assert callable(getattr(M, "solve", None)), "немає функції solve"
