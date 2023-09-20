#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Config models and config file parser
"""
import os
import yaml
from pydantic import BaseModel

__config_cache = None  # holds config object to not read files again
__default_config_path = "backend/config"


class ConfigDqmMetaStore(BaseModel):
    """DQM meta store config"""

    base_dqm_eos_dir: str  # Base DQMGUI EOS directory, currently /eos/cms/store/group/comm_dqm/DQMGUI_data
    find_tmp_results_file: str  # The file that holds the results of unix find command results: each line is full ROOT file in the DQM EOS
    meta_store_json_file: str  # The file that holds results of formatted (grinded using eos_grinder.py) JSON of find_tmp_results_file
    last_n_run_years: int  # Number of past years to parse EOS directories, important to find "base_dqm_eos_dir/RunYYYY"
    file_suffix_pat: str  # DQM ROOT files has different suffixes, so define them while parsing. Default used is "*DQMIO.root"


class ConfigPlot(BaseModel):
    """Single plot/histogram's required config"""

    name: str  # Name of the plot
    dqm_link: str  # DQMGUI link of the plot
    draw_opt: str  # JSROOT draw option: hist,colz...
    type: str  # Its type: TH1F, TH2F, TProfile...


class ConfigGroup(BaseModel):
    """Group config (detector like L1T HLT) with their plots"""

    group_name: str  # Group name: L1T, HLT
    eos_directory: str  # Group directory, separate group name: JetMET1, HLTPhysics, ...
    tdirectory: str  # Holds the TDirectory pattern(requires run number) of the required histograms in the ROOT file
    description: str | None = None  # Optional description
    plots: list[ConfigPlot]  # Configs of group's plots


class Config(BaseModel):
    """Main config schema"""

    host: str  # Uvicorn host
    port: int  # Uvicorn port
    base_url: str  # API base url, check for proxy
    api_v1_prefix: str
    loglevel: str
    environment: str  # Dev or prod
    allowed_cors_origins: list[str]  # Middleware green light for the domains/url:ports for CORS
    dqm_meta_store: ConfigDqmMetaStore  # DQM Meta Store configs
    plots_config: list[ConfigGroup]  # [HISTOGRAMS_CONFIG_NAME] Config of each detector group for their histograms


def read_file(file_path: str):
    """Read config from given file and return it"""
    with open(file_path, "r") as stream:
        return yaml.safe_load(stream)


def get_config():
    """Returns the ConfigServer object"""
    # Get server config as object. FAST_API_CONF env variable should be defined in k8s manifest or before server run
    global __config_cache

    # It will be appended main config with this name
    HISTOGRAMS_CONFIG_NAME = "plots_config"
    if __config_cache:
        return __config_cache

    # Get server configs, type:dict
    server_config_dict = read_file(
        os.path.join(os.getenv(key="FAST_API_CONF", default=__default_config_path), "server.yaml")
    )

    # Get histogram configs, type:list
    histograms_config_dict = read_file(
        os.path.join(os.getenv(key="FAST_API_CONF", default=__default_config_path), "plots.yaml")
    )

    # join configs
    server_config_dict.update({HISTOGRAMS_CONFIG_NAME: histograms_config_dict})

    __config_cache = Config(**server_config_dict)
    return __config_cache


def get_config_group_directories() -> list:
    """Returns detector group directories"""
    c = get_config()
    return [item.eos_directory for item in c.plots_config]
