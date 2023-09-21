#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : DQM Metadata Store Client
"""

import time

from backend.config import Config, get_config
from .models import DqmMetaStore

__METADATA_CACHE = None  # DQM Metadata Store cache
__CACHE_UPDATE_TIME = 0  # Last update time in seconds of the cache
__CACHE_REFRESH_PERIOD_SECS = get_config().dqm_meta_store.cache_retention_secs


def get_dqm_store(config: Config):
    """DqmMetaStore client to search DQM GUI root files, directories, run numbers and datasets

    Args:
        config: given Config object to get `dqm_meta_store.meta_store_json_file`
    """
    global __METADATA_CACHE, __CACHE_UPDATE_TIME
    # TODO: refresh it in each hour
    if __need_to_create_new_store_cache():
        # Get DqmMetaStore from the JSON file which is created by the EOS GRINDER
        with open(config.dqm_meta_store.meta_store_json_file) as f:
            __METADATA_CACHE = DqmMetaStore.model_validate_json(f.read())
            __CACHE_UPDATE_TIME = int(time.time())

    return __METADATA_CACHE


def __need_to_create_new_store_cache():
    if __METADATA_CACHE and __CACHE_UPDATE_TIME > 0:
        if (int(time.time()) - __CACHE_UPDATE_TIME) < __CACHE_REFRESH_PERIOD_SECS:
            return False
    return True
