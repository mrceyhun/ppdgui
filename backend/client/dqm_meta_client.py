#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Client to search DQM GUI root files, directories, run numbers and datasets
"""
from backend.config import Config
from backend.dqm_meta.models import DqmMetaStore


class DqmMetaStoreClient:
    """DqmMetaStore client"""

    def __init__(self, config: Config):
        """Get DqmMetaStore from json file

        Args:
            config: given Config object to get `dqm_meta_store.meta_store_json_file`
        """
        self.store = None
        with open(config.dqm_meta_store.meta_store_json_file) as f:
            self.store = DqmMetaStore.model_validate_json(f.read())

    def get_last_run(self) -> int:
        """Get recent Run number"""
        run_number = max([item.run for item in self.store.data])
        return run_number

    def get_last_run_root_files(self) -> list[str]:
        last_run = self.get_last_run()
        return [item.eos_path for item in self.store.data if item.run == last_run]
