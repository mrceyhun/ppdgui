#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Config models and config file parser
"""
import os
import yaml
from pydantic import BaseModel


class ConfigDqmMetaStore(BaseModel):
    """DQM meta store config"""
    base_dqm_eos_dir: str  # Base DQMGUI EOS directory, currently /eos/cms/store/group/comm_dqm/DQMGUI_data
    find_tmp_results_file: str  # The file that holds the results of unix find command results: each line is full ROOT file in the DQM EOS
    meta_store_json_file: str  # The file that holds results of formatted (grinded using eos_grinder.py) JSON of find_tmp_results_file
    last_n_run_years: int  # Number of past years to parse EOS directories, important to find "base_dqm_eos_dir/RunYYYY"
    file_suffix_pat: str  # DQM ROOT files has different suffixes, so define them while parsing. Default used is "*DQMIO.root"


class ConfigHistogram(BaseModel):
    """Single histogram required config"""
    name: str  # Name of the histogram
    type: str  # Its type: TH1F, TH2F


class ConfigDetectorGroup(BaseModel):
    """Histogram group for a detector like L1T HLT"""
    group: str  # Group name: L1T, HLT
    group_directory: str  # Group directory, separate group name: JetMET1, HLTPhysics, ...
    histograms_tdirectory_pattern: str  # Holds the TDirectory pattern(requires run number) of the required histograms in the ROOT file
    description: str | None = None  # Optional description
    histograms: list[ConfigHistogram]  # Configs of detector's histograms: names and types of histograms


class Config(BaseModel):
    """Config schema"""
    host: str  # Uvicorn host
    port: int  # Uvicorn port
    base_url: str  # API base url, check for proxy
    api_v1_prefix: str
    loglevel: str
    environment: str  # Dev or prod
    allowed_cors_origins: list[str]  # Middleware green light for the domains/url:ports for CORS
    dqm_meta_store: ConfigDqmMetaStore  # DQM Meta Store configs
    detector_histogram_groups: list[ConfigDetectorGroup]  # Config of each detector group for their histograms


def read_config_yaml(file_path: str) -> Config:
    """Read config from given file and return it"""
    with open(file_path, 'r') as stream:
        config = yaml.safe_load(stream)

    return Config(**config)


def get_config():
    """Returns the Config object"""
    # Get config as object. FAST_API_CONF is defined in k8s manifest
    return read_config_yaml(
        os.getenv(
            key="FAST_API_CONF",
            default=os.path.join(os.path.dirname(__file__), "config.yaml"),
        ))
