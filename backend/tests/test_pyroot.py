#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : PyROOT util tests
"""

import os
import json

from backend.client import pyroot
from . import BASE_TEST_DATA_DIR


class TestPyroot:
    """Tests for client.pyroot functions"""

    def test_get_obj_json(self):
        """Test client.pyroot.util.get_obj_json"""

        # Get JSON from test ROOT file
        th1f_json = pyroot.get_obj_json(os.path.join(BASE_TEST_DATA_DIR, "th1f.root"), "myHist")

        # Get JSON of the saved test object
        with open(os.path.join(BASE_TEST_DATA_DIR, "th1f.json")) as f:
            expected_json = json.loads(f.read())

        assert th1f_json == expected_json

    def test_boolean(self):
        a = True
        b = True
        assert a == b
