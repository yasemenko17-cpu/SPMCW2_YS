"""Допоміжний завантажувач: підключає файл завдання з теки tasks/. Додатково - сторожовий таймер."""
import importlib.util
import os
import signal
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent
WATCHDOG_SECONDS = 20


def load(number):
    """Повертає модуль завдання з номером number."""
    base = Path(os.environ.get("VARIANT_DIR", ROOT.parent / "tasks"))
    for prefix in ("variant", "lab", "task"):
        path = base / f"{prefix}_{number:02d}.py"
        if path.exists():
            spec = importlib.util.spec_from_file_location(f"{prefix}_{number:02d}", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    raise FileNotFoundError(f"Не знайдено файл завдання {number:02d} у {base}")


@pytest.fixture(autouse=True)
def watchdog():
    """Зупиняє тест, що завис (типово - забутий кінець каналу), через WATCHDOG_SECONDS секунд."""

    def on_alarm(signum, frame):
        raise TimeoutError("Тест перевищив ліміт часу: перевірте, чи закрито зайві кінці каналів і чи дочекано дітей")

    previous = signal.signal(signal.SIGALRM, on_alarm)
    signal.alarm(WATCHDOG_SECONDS)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)
