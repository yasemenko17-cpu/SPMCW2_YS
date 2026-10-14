"""МКР. Завдання 07: Кільцевий буфер у спільній пам'яті."""


class Ring:
    """Кільцевий буфер у наданому буфері байтів."""

    def __init__(self, buf):
        raise NotImplementedError  # TODO: реалізуйте за карткою

    @property
    def used(self) -> int:
        raise NotImplementedError

    @property
    def free(self) -> int:
        raise NotImplementedError

    def write(self, data) -> int:
        raise NotImplementedError

    def read(self, n: int) -> bytes:
        raise NotImplementedError
