#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : FastAPI tests
"""

from fastapi import __version__


def test_version(client_test):
    response = client_test.get("/version")
    assert response.status_code == 200
    msg = str(response.json())
    assert msg == str(__version__)
