#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Pytest FastAPI test client initializer
"""
import os
from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.config import get_config, Config


@pytest.fixture()
def client_test() -> Generator[TestClient, Any, None]:
    """Create a new FastAPI TestClient"""
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def config_test() -> Generator[Config, None]:
    """Create a new FastAPI TestClient"""
    os.environ['FAST_API_CONF'] = 'backend/tests/config_test.yaml'
    yield get_config()
