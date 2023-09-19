#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Client to search DQM GUI root files, directories, run numbers and datasets
"""
import logging
from pydantic import BaseModel, RootModel
from typing import Dict

from backend.config import Config


# SCHEMA ---------------------------------------------------------------------


class DqmMeta(BaseModel):
    """Representation of single DQM ROOT file's parsed metadata"""

    dataset: str  # Dataset name embedded in the ROOT file name: JetMET1/Run2023A-PromptReco-v1, JetMET1/Run2023D-Express-v1
    eos_directory: str  # Detector group directory: JetMET1, HLTPhysics, so on
    era: int  # Run era
    root_file: str  # full EOS path of the root file
    run: int  # Run number


class DqmKeyOfEraDatasetRun(BaseModel):
    """Era, Dataset and Run couples: Era > Dataset > Run"""

    dataset: str  # Dataset name
    era: str  # Era of dataset
    run: int  # Run number of the dataset


class DqmMainMetadata(RootModel):
    """DQM main metadata format: dict(RUN NUMBER, dict(GROUP DIRECTORY, DqmMeta))

    Makes it fast to find era, dataset, run number and detector group directory
    """

    root: Dict[DqmKeyOfEraDatasetRun, DqmMeta]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


# CLIENT ---------------------------------------------------------------------


class DqmMetadataClient:
    """DqmMetaStore client"""

    def __init__(self, config: Config):
        """Get DqmMetadata from json file

        Args:
            config: given Config object to get `dqm_meta_store.meta_store_json_file`
        """
        self.logging = logging.getLogger(__name__)
        self.logging.setLevel(config.loglevel.upper())
        self.store = None
        # TODO: refresh it in each 10 minutes
        with open(config.dqm_meta_store.meta_store_json_file) as f:
            self.store = DqmMainMetadata.model_validate_json(f.read())

    def last_run_number(self, detector_group_directories: list[str]) -> int:
        """Get recent common Run number for the given detector groups

        Get each detector groups' last run and set the max run as their overall minimum run number,
        because "a last run" should include all the histograms of the detector groups.

        In short: MIN( max(runs that have HLT root files), max(runs that have L1T root files), ...)
        """
        max_group_runs = set()  # holds the latest run number for each detector group
        for group_dir in detector_group_directories:
            max_group_runs.add(
                # max run number that has this detector group's root files
                max([run for (run, group_meta_dict) in self.store.root.items() if (group_dir in group_meta_dict)])
            )

        self.logging.info(f"Detector group last runs list: {list(max_group_runs)}")

        # !ASSUMPTION! Most probably minimum run number will have histograms for all the detector groups
        return min(max_group_runs)

    def get_det_group_root_file(self, run_number: int, group_directory: str) -> DqmMeta:
        """Get all ROOT files of a detector group for the given run"""
        # For a single run there should be single ROOT file
        return self.store.root[run_number][group_directory]
