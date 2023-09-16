#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : PyROOT util tests
"""

from backend.client import pyroot_run
from . import TEST_BIG_ROOT_FILE


class TestPyroot:
    """Tests for client.pyroot functions"""

    def test_get_root_dirs_or_hist(self):
        """Test client.pyroot.util.get_obj_json"""

        # th1f json
        r1 = pyroot_run.get_root_dirs_or_hist(TEST_BIG_ROOT_FILE,
                                          "DQMData/Run 366713/EcalPreshower/Run summary/ESRecoSummary/recHits_ES_energyMax")
        # None, because it requires full obj path
        r2 = pyroot_run.get_root_dirs_or_hist(TEST_BIG_ROOT_FILE, "recHits_ES_energyMax")

        r3 = pyroot_run.get_root_dirs_or_hist(TEST_BIG_ROOT_FILE, "DQMData/Run 366713")

        # dirs
        r4 = pyroot_run.get_root_dirs_or_hist(TEST_BIG_ROOT_FILE, "DQMData/")

        assert r1.hist_json[0]['_typename'] == pyroot_run.RootClasses.TH1F
        assert r2.dirs is None and r2.hist_json is None
        assert len(r3.dirs) == 22  # length of sub dirs
        assert r4.dirs == ['Run 366713']  # length of sub dirs

    def test_boolean(self):
        a = True
        b = True
        assert a == b
