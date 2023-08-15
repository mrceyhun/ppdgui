#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Pytest FastAPI test client initializer
"""

from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient

from backend.main import app


@pytest.fixture()
def client_test() -> Generator[TestClient, Any, None]:
    """Create a new FastAPI TestClient"""
    with TestClient(app) as client:
        yield client
