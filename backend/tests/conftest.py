#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Pytest FastAPI test client initializer
"""
import pathlib, shutil, os
from typing import Any, Generator, List
from datetime import datetime


from ROOT import TFile, TH1F
import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.config import get_config, Config, ConfigPlotsGroup


@pytest.fixture(scope="session")
def config_test() -> Generator[Config, Any, None]:
    """Create modified Config for test"""
    conf = get_config()
    conf.dqm_meta_store.base_dqm_eos_dir = "backend/tests/DQMGUI_data"
    yield conf


@pytest.fixture(scope="session")
def fast_api_client_test() -> Generator[TestClient, Any, None]:
    """Create a new FastAPI TestClient"""
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def create_histograms_for_test(config_test) -> List[str]:
    """Create all histograms in plots.yaml for each group and each era.

    To not include another parameter in pytest as "--basetemp", tmp_path_factory is not used
    example eos dir: /eos/cms/store/group/comm_dqm/DQMGUI_data/Run2023/JetMET1/0003707xx/DQM_V0001_R000370717__JetMET1__Run2023D-PromptReco-v2__DQMIO.root
    """
    all_created_files = []
    # Mock up the base DQM EOS dirctory for root files
    year = datetime.now().year
    base_directory = pathlib.Path(config_test.dqm_meta_store.base_dqm_eos_dir) / f"Run{year}"

    root_file_fmt = "DQM_V0001_R{run9d}__{eosdir}__{era}-TEST-DATASET__DQMIO.root"
    run_size = 3  # For each ERA of a group
    era_run_jump = 100  # ERAs are mostly in different 0001234xx directories

    eras = [f"Run{year}{e}" for e in ["A", "B", "C", "D", "E"]]  # eras full name, i.e. Run2023A

    # Iterare all groups and creates all histograms defined in plots.yaml in each era
    for group_conf in config_test.plots.groups:
        # Each group will have same histograms of same numbers
        first_run = 100000  # First Run number with 6 digit, max Run digit is 9

        group_dir = base_directory / group_conf.eos_directory

        for era in eras:
            for run in range(first_run, first_run + run_size):
                run_xx_dir = group_dir / f"{str(int(first_run / 100))}xx".zfill(9)
                run_xx_dir.mkdir(parents=True, exist_ok=True)

                # Create all plots of the group in the ROOT file
                root_f = run_xx_dir / root_file_fmt.format(
                    run9d=str(run).zfill(9), eosdir=group_conf.eos_directory, era=era
                )
                util_create_root_hist(root_file=str(root_f), group_conf=group_conf, run=run)
                all_created_files.append(root_f)
            first_run += era_run_jump  # to change run_xx directory which depends on last 2 digit of the run number

    yield all_created_files
    # Delete after session
    # shutil.rmtree(base_directory.parent)  # DQMGUI_data is parent


def util_create_root_hist(root_file: str, group_conf: ConfigPlotsGroup, run: int):
    """Creates test histograms in th root file with the definitions in plots.yaml config only for TH1F"""
    tdirectory = group_conf.tdirectory.format(run_num_int=run)

    # PYROOT's limited functionality force to create directory only once
    plot_dirs = set([tdirectory + "/" + p.name for p in group_conf.plots])
    for dir_str in plot_dirs:
        with TFile(root_file, "UPDATE") as tf:
            for dir in dir_str.split("/")[:-1]:
                if not tf.Get(dir):  # If subdir is not created before
                    subdir = tf.mkdir(dir)
                    tf.cd(dir)

    for dir_str in plot_dirs:
        dir = "".join(dir_str.split("/")[:-1])  # before last
        name = dir_str.split("/")[-1]  # last
        with TFile(root_file, "UPDATE") as tf:
            tf.cd(dir)
            h = TH1F(name, name, 64, -4, 4)
            h.FillRandom("gaus")
            tf.WriteObject(h, "myHist")
            tf.Save()
            del h
