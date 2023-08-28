#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Client to search DQM GUI root files, directories, run numbers and datasets
"""

from backend.client.models import DqmMetaStore

DQM_META_JSON_FILE = 'downloads/formatted.json'
global META_STORE


def read_dqm_meta_json(input_file: str) -> DqmMetaStore:
    """Get DqmMetaStore from json file"""
    with open(input_file) as fin:
        return DqmMetaStore.model_validate_json(fin.read())


def init_meta_store() -> DqmMetaStore:
    global META_STORE
    if META_STORE:
        return META_STORE
    META_STORE = read_dqm_meta_json(DQM_META_JSON_FILE)
    return META_STORE


def get_last_run() -> int:
    """Get recent Run number"""
    dqm_meta = init_meta_store()
    run_number = max([item.run for item in dqm_meta.data])
    return run_number


def get_last_run_root_files() -> list[str]:
    dqm_meta = init_meta_store()
    last_run = get_last_run()
    return [item.eos_path for item in dqm_meta.data if item.run == last_run]
