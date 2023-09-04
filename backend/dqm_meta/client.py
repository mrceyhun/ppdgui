#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Client to search DQM GUI root files, directories, run numbers and datasets
"""
from pydantic import BaseModel, RootModel
from backend.config import Config
import logging


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
        self.logging = logging.getLogger(__name__)
        self.logging.setLevel(config.loglevel)
        self.store = None
        # TODO: refresh it in each 10 minutes
        with open(config.dqm_meta_store.meta_store_json_file) as f:
            self.store = DqmMetaStore.model_validate_json(f.read())

    def last_run_number(self, detector_group_directories: list[str], year: int | None = None) -> (int, int):
        """Get recent common Run number for the given detector groups and for the given year or recent year by default"""
        # If year is not given, set as last year
        my_year = year if year else max([item.year for item in self.store.root])

        run_numbers = set()  # holds recent run numbers of detector groups
        for group_dir in detector_group_directories:
            tmp_run_number = max(
                [item.run for item in self.store.root if (item.year == my_year and item.group_directory == group_dir)]
            )
            run_numbers.add(tmp_run_number)
        self.logging.info(f"Detector group last runs list{list(run_numbers)}")
        # Most probablt minimum run number will be common for all the detector groups
        run_number = min(run_numbers)

        return run_number, my_year

    def get_root_files_of_run(self, run_number: int) -> list[str]:
        """ "Get all ROOT files of a run"""
        return [item.root_file for item in self.store.root if item.run == run_number]

    def get_det_group_root_file(self, run_number: int, group_directory: str) -> DqmFileMetadata:
        """ "Get all ROOT files of a detector group for the given run"""
        # For a single run there should be single ROOT file
        return [
            group_item
            for group_item in self.store.root
            if (group_item.run == run_number and group_item.group_directory == group_directory)
        ][0]
