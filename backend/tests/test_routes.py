#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : FastAPI tests
"""

from fastapi import __version__


def test_version(fast_api_client_test):
    response = fast_api_client_test.get("/version")
    assert response.status_code == 200
    msg = str(response.json())
    assert msg == str(__version__)


def test_mock_histograms_len(create_histograms_for_test):
    # with 3 runs per era and 5 eras in total, 1 plot for each
    assert len(create_histograms_for_test) % (5 * 3) == 0
