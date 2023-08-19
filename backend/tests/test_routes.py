#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : FastAPI tests
"""

import json
import os

from fastapi import __version__

from backend.api_v1.routes import RootObj
from . import BASE_TEST_DATA_DIR


def test_version(client_test):
    response = client_test.get("/version")
    assert response.status_code == 200
    msg = str(response.json())
    assert msg == str(__version__)


def test_get_plots(client_test):
    post_req = RootObj(file_path=os.path.join(BASE_TEST_DATA_DIR, "th1f.root"), obj_path="myHist").model_dump_json()
    response = client_test.post("/get-plots", json=json.loads(post_req))
    with open(os.path.join(BASE_TEST_DATA_DIR, "th1f.json")) as f:
        expected_json = json.loads(f.read())
    assert response.status_code == 200
    assert response.json() == expected_json
