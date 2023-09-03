#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Client to search DQM GUI root files, directories, run numbers and datasets
"""
from pydantic import BaseModel, RootModel
from backend.config import Config


class DqmFileMetadata(BaseModel):
    """Representation of single DQM ROOT file's parsed metadata"""
    year: int  # Run year
    run: int  # Run number
    group_directory: str  # Detector group directory: JetMET1, HLTPhysics, so on
    dataset: str  # Dataset name embedded in the ROOT file name: Run2023A-PromptReco-v1, Run2023D-Express-v1
    root_file: str  # full EOS path of the root file


class DqmMetaStore(RootModel):
    """Main DQM ROOT files metadata format"""
    root: list[DqmFileMetadata]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


class DqmMetaStoreClient:
    """DqmMetaStore client"""

    def __init__(self, config: Config):
        """Get DqmMetaStore from json file

        Args:
            config: given Config object to get `dqm_meta_store.meta_store_json_file`
        """
        self.store = None
        # TODO: refresh it in each 10 minutes
        with open(config.dqm_meta_store.meta_store_json_file) as f:
            self.store = DqmMetaStore.model_validate_json(f.read())

    def last_run_number(self, year: int | None = None) -> (int, int):
        """Get recent Run number with given year or with recent year by default"""
        if year:
            run_number = max([item.run for item in self.store.root if item.year == year])
        else:
            # recent year and its last run
            year = max([item.year for item in self.store.root])
            run_number = max([item.run for item in self.store.root if item.year == year])

        return run_number, year

    def get_root_files_of_run(self, run_number: int) -> list[str]:
        """"Get all ROOT files of a run"""
        return [item.root_file for item in self.store.root if item.run == run_number]

    def get_det_group_root_file(self, run_number: int, group_directory: str) -> DqmFileMetadata:
        """"Get all ROOT files of a detector group for the given run"""
        # For a single run there should be single ROOT file
        return [
            group_item for group_item in self.store.root
            if (group_item.run == run_number and group_item.group_directory == group_directory)
        ][0]
