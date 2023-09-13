#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Client to search DQM GUI root files, directories, run numbers and datasets
"""
import logging
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
        self.logging = logging.getLogger(__name__)
        self.logging.setLevel(config.loglevel.upper())
        self.store = None
        # TODO: refresh it in each 10 minutes
        with open(config.dqm_meta_store.meta_store_json_file) as f:
            self.store = DqmMetaStore.model_validate_json(f.read())

    def last_run_number(self, detector_group_directories: list[str]) -> int:
        """Get recent common Run number for the given detector groups

        Get each detector groups' last run and set the max run as their overall minimum run number,
        because "a last run" should include all the histograms of the detector groups.

        In short: MIN( max(runs that have HLT root files), max(runs that have L1T root files), ...)
        """
        max_group_runs = set()  # holds latest run number of detector groups
        for group_dir in detector_group_directories:
            max_group_runs.add(
                # max run number that has this detector group's root files
                max([item.run for item in self.store.root if (item.group_directory == group_dir)])
            )

        self.logging.info(f"Detector group last runs list: {list(max_group_runs)}")

        # !ASSUMPTION! Most probably minimum run number will have histograms for all the detector groups
        return min(max_group_runs)

    def get_root_files_of_run(self, run_number: int) -> list[str]:
        """Get all ROOT files of a run"""
        return [item.root_file for item in self.store.root if item.run == run_number]

    def get_year_of_run(self, run_number: int) -> int:
        """Get year of given run number"""
        for item in self.store.root:
            if item.run == run_number:
                return item.year  # return in firs occurance

        return 0  # on fail

    def get_det_group_root_file(self, run_number: int, group_directory: str) -> DqmFileMetadata:
        """Get all ROOT files of a detector group for the given run"""
        # For a single run there should be single ROOT file
        return [
            group_item
            for group_item in self.store.root
            if (group_item.run == run_number and group_item.group_directory == group_directory)
        ][0]
