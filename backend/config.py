#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Main config file parser
"""
import os
import yaml
from pydantic import BaseModel


class ConfigDqmMetaStore(BaseModel):
    """DQM meta store config"""
    base_dqm_eos_dir: str
    find_tmp_results_file: str
    meta_store_json_file: str
    last_n_run_years: int
    file_suffix_pat: str


class Config(BaseModel):
    """Config schema"""
    host: str
    port: int
    base_url: str
    api_v1_prefix: str
    loglevel: str
    environment: str
    allowed_cors_origins: list[str]
    dqm_meta_store: ConfigDqmMetaStore


def read_config_yaml(file_path: str) -> Config:
    with open(file_path, 'r') as stream:
        config = yaml.safe_load(stream)

    return Config(**config)


def get_config():
    """Returns the Config object"""
    # Get config as object
    return read_config_yaml(
        os.getenv(
            key="FAST_API_CONF",
            default=os.path.join(os.path.dirname(__file__), "config.yaml"),
        ))
