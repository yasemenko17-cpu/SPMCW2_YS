"""Відкриті приклади завдання 05: Шматки PNG: структура й контрольні суми."""
import struct
import zlib

import pytest
from conftest import load

M = load(5)
solve = M.solve

SIG = b"\x89PNG\r\n\x1a\n"


def chunk(kind, body=b"", crc=None):
    value = zlib.crc32(kind + body) if crc is None else crc
    return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", value)


GOOD = (b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x01\x08\x02\x00\x00\x00{@\xe8'
 b'\xdd\x00\x00\x00\x03IDATabc3\xaf\xd6r\x00\x00\x00\x00IEND\xaeB`\x82')

PUBLIC = [((b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x01\x08\x02\x00\x00\x00{@\xe8'
   b'\xdd\x00\x00\x00\x03IDATabc3\xaf\xd6r\x00\x00\x00\x00IEND\xaeB`\x82',),
  'Зображення: 2x1, 8 біт, RGB\n'
  'IHDR: 13 байтів, CRC збігається\n'
  'IDAT: 3 байтів, CRC збігається\n'
  'IEND: 0 байтів, CRC збігається'),
 ((b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x01\x08\x02\x00\x00\x00{@\xe8'
   b'\xdd\x00\x00\x00\x03IDATabc\x00\x00\x00\x00\x00\x00\x00\x00IEND\xaeB`\x82',),
  'Зображення: 2x1, 8 біт, RGB\n'
  'IHDR: 13 байтів, CRC збігається\n'
  'IDAT: 3 байтів, CRC не збігається\n'
  'IEND: 0 байтів, CRC збігається')]

HIDDEN = []


@pytest.mark.parametrize("args,expected", PUBLIC + HIDDEN)
def test_solve(args, expected):
    assert solve(*args) == expected


def test_functions_exist():
    assert callable(getattr(M, "solve", None)), "немає функції solve"
