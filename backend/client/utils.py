#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Client utils
"""
from typing import List, Dict, Tuple

from backend.config import get_config
from backend.dqm_meta.client import get_dqm_store


def get_formatted_hist_path(tdirectory: str, name: str, run: int):
    """Returns formatted histogram objects full path inside the ROOT file"""
    return tdirectory.format(run_num_int=run).rstrip("/") + "/" + name.lstrip("/")


def get_formatted_hist_dqm_url(conf_url: str, dataset: str, run: int):
    """Returns formatted histogram object dqm url"""
    return conf_url.format(run_num_int=run, dataset=dataset)


def get_available_groups() -> List[str]:
    """Get all groups defined in the group"""
    conf = get_config()
    return [group.group_name for group in conf.plots.groups]


def get_available_eras(group_names: List[str]) -> List[str]:
    """Get eras in DQM Metadata Store"""
    conf = get_config()
    dqm_meta_store = get_dqm_store(conf)
    return dqm_meta_store.get_eras_filtered(group_names=group_names)


def get_available_runs(limit: int, groups: List[str], eras: List[str]) -> List[Tuple[int, str]]:
    """Get runs:era couples by limit filter by groups and eras"""
    conf = get_config()
    dqm_meta_store = get_dqm_store(conf)
    return dqm_meta_store.get_runs_era_tuples(limit=limit, groups=groups, eras=eras)
