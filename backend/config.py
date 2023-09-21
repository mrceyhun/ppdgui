#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Config models and config file parser
"""
import os
from typing import Dict, List

import yaml
from pydantic import BaseModel

__config_cache = None  # holds config object to not read files again
__default_config_path = "backend/config"


class ConfigDqmMetaStore(BaseModel):
    """DQM meta store config"""

    base_dqm_eos_dir: str  # Base DQMGUI EOS directory, currently /eos/cms/store/group/comm_dqm/DQMGUI_data
    find_tmp_results_file: str  # The file that holds the results of unix find command results: each line is full ROOT file path in the DQM EOS
    meta_store_json_file: str  # The file that holds DQM Metadata Store JSON which is formatted by eos_grinder.py using of find_tmp_results_file as input
    last_n_run_years: int  # Number of past years to parse EOS directories, important to find "base_dqm_eos_dir/RunYYYY"
    file_suffix_pat: str  # DQM ROOT files has different suffixes, so define them while parsing. Default used is "*DQMIO.root"
    cache_retention_secs: int  # DQM Metadata Store cache retention time in seconds to update cache object by reading JSON file again


class ConfigPlotsGroupsHist(BaseModel):
    """Single histogram's required config"""

    name: str  # Name of the histogram
    dqm_link: str  # DQMGUI link of the histogram
    type: str  # Its type: TH1F, TH2F, TProfile...


class ConfigPlotsGroup(BaseModel):
    """Group config (detector like L1T HLT) with their histogram"""

    group_name: str  # Group name: L1T, HLT
    eos_directory: str  # Group directory, separate group name: JetMET1, HLTPhysics, ...
    tdirectory: str  # Holds the TDirectory pattern(requires run number) of the required histograms in the ROOT file
    description: str | None = None  # Optional description
    plots: List[ConfigPlotsGroupsHist]  # Configs of group's plots/histograms

    # Required for cache
    def __hash__(self):
        # Create hash from ordered dict values except for [! "plots" !] which makes hashing fast
        not_used_field = "plots"  # un-hashable and unneeded to make hash unique
        return hash((type(self),) + tuple(v for k, v in self.__dict__.items() if (k != not_used_field)))


class ConfigPlots(BaseModel):
    """plots.yaml config class"""

    draw_options: Dict[str, str]  # key: ROOT class, value: draw option, Draw options of the ROOT histogram classes
    groups: List[ConfigPlotsGroup]  # [HISTOGRAMS_CONFIG_NAME] Config of each detector group for their histograms


class Config(BaseModel):
    """Main config schema"""

    host: str  # Uvicorn host
    port: int  # Uvicorn port
    base_url: str  # API base url, check for proxy
    api_v1_prefix: str
    loglevel: str
    environment: str  # Dev or prod
    allowed_cors_origins: List[str]  # Middleware green light for the domains/url:ports for CORS
    dqm_meta_store: ConfigDqmMetaStore  # DQM Meta Store configs
    plots: ConfigPlots  # plots.yaml config

    def get_plots_group_eos_dir_map(self) -> Dict[str, str]:
        """Returns map of {group name:group eos directory}"""
        return {item.group_name: item.eos_directory for item in self.plots.groups}


def read_file(file_path: str):
    """Read config from given file and return it"""
    with open(file_path, "r") as stream:
        return yaml.safe_load(stream)


def get_config():
    """Returns the ConfigServer object"""
    # Get server config as object. FAST_API_CONF env variable should be defined in k8s manifest or before server run
    global __config_cache

    # It will be appended main config with this name
    HISTOGRAMS_CONFIG_NAME = "plots"
    if __config_cache:
        return __config_cache

    # Get server configs, type:dict
    server_config_dict = read_file(
        os.path.join(os.getenv(key="FAST_API_CONF", default=__default_config_path), "server.yaml")
    )

    # Get histogram configs, type:list
    plots_config_dict = read_file(
        os.path.join(os.getenv(key="FAST_API_CONF", default=__default_config_path), "plots.yaml")
    )

    # join configs
    server_config_dict.update({HISTOGRAMS_CONFIG_NAME: plots_config_dict})

    __config_cache = Config(**server_config_dict)
    return __config_cache


def get_config_group_directories() -> List:
    """Returns detector group directories"""
    c = get_config()
    return [item.eos_directory for item in c.plots.groups]
