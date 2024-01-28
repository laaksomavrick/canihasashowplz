from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    monkeypatch.setenv("SM_MODEL_DIR", "./monkeypatched")
    monkeypatch.setenv("PYTHON_ENV", "test")
