"""Відкриті приклади завдання 07: Кільцевий буфер у спільній пам'яті."""
import struct

import pytest
from conftest import load

M = load(7)
Ring = M.Ring


def test_empty_buffer():
    ring = Ring(bytearray(24))
    assert ring.capacity == 16
    assert ring.used == 0
    assert ring.free == 16


def test_write_read_and_header():
    buf = bytearray(24)
    ring = Ring(buf)
    assert ring.write(b"hello") == 5
    assert buf[:8] == struct.pack("<II", 0, 5)
    assert bytes(buf[8:13]) == b"hello"
    assert ring.read(3) == b"hel"
    assert buf[:8] == struct.pack("<II", 3, 2)
    assert (ring.used, ring.free) == (2, 14)


def test_functions_exist():
    assert callable(getattr(M, "Ring", None)), "немає класу Ring"
