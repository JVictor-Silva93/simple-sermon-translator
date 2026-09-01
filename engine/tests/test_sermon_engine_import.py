# engine/tests/test_import.py
from importlib import import_module


def test_sermon_engine_imports():
    import_module("sermon_engine")