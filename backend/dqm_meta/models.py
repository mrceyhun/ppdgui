#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : DQM Metadata Store Schema
"""

import logging
from typing import List, Union, Dict, Tuple
from collections import defaultdict

from pydantic import BaseModel, RootModel

from backend.config import get_config

logging.basicConfig(level=get_config().loglevel.upper())


class DqmMeta(BaseModel):
    """Representation of single DQM ROOT file's parsed metadata"""

    dataset: str  # Dataset name embedded in the ROOT file name: JetMET1/Run2023A-PromptReco-v1, JetMET1/Run2023D-Express-v1
    eos_directory: str  # Detector group directory: JetMET1, HLTPhysics, so on
    era: str  # Run era
    root_file: str  # full EOS path of the root file
    run: int  # Run number

    # Required for cache
    def __hash__(self):
        # Dict keys are ordered in __dict__.values, so safe.
        return hash((type(self),) + tuple(self.__dict__.values()))


class DqmMetaStore(RootModel):
    """DQM main metadata format: list of DqmMeta"""

    root: List[DqmMeta]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def get_eras_filtered(self, group_names: List[str] = []) -> List[str]:
        """Get all available era names available for the given group names"""
        conf = get_config()
        if not group_names:  # Return all
            return list(set([item.era for item in self.root]))
        else:  # Filter by group name
            available_eos_directories = conf.get_eos_directories_of_groups(group_names=group_names)
            return list(set([item.era for item in self.root if item.eos_directory in available_eos_directories]))

    def get_runs_era_tuples(self, limit: int, groups: List[str] = [], eras: List[str] = []) -> List[Tuple[int, str]]:
        """Get all run:era couple with given filters. Limit is applied to RUN size of per ERA"""
        conf = get_config()
        available_eos_directories = conf.get_eos_directories_of_groups(group_names=groups)
        group_run_era_dict = self.get_groups_and_runs_of_eras(
            eras=eras, groups_eos_dirs=available_eos_directories, runs=None, run_limit=limit
        ).values()
        run_era_dict = dict(
            sum([list(run_era_dicts.items()) for run_era_dicts in group_run_era_dict], [])
        )  # flatten and get rid of groups

        return list(run_era_dict.items())

    def get_datasets(self) -> List[str]:
        """Get all available dataset names"""
        return list(set([m.dataset for m in self.root]))

    def get_groups_and_runs_of_eras(
        self, eras: List[str] = None, groups_eos_dirs: List[str] = None, runs: List[int] = None, run_limit: int = 1000
    ) -> Dict[str, Dict[int, str]]:
        """Finds runs of eras for the given eras, groups and runs, and returns |-- {group eos dir:{run: era}} --| map

        Args:
            eras: DQM Metadata Store results filtered with given ERA list. If None, no filter
            groups_eos_dirs: DQM Metadata Store results filtered with given eos_directory list. If None, no filter
            runs: DQM Metadata Store results filtered with given RUN list. If None, no filter
            run_limit: To filter number of runs in a group's ERA result: run_era map
        """
        result = {}
        group_era_run_counts = {}  # {group: {era: run count}} to limit number of runs in each era of a group
        for item in self.root:
            # "eras" is None or item era is in "eras" list to filter. Same for runs and groups
            cond = (
                ((not eras) or (item.era in eras))
                and ((not groups_eos_dirs) or (item.eos_directory in groups_eos_dirs))
                and ((not runs) or (item.run in runs))
            )
            if cond:
                if item.eos_directory in result:
                    # If eos directory in result, it should be in group_era_run_counts too because they are initialized together(else cond.)
                    # If one era's run count for a group is less than max limit, allow it. Else there is nothing to do and skop it.
                    if group_era_run_counts[item.eos_directory][item.era] < run_limit:
                        result[item.eos_directory][item.run] = item.era
                        # Increment the group's era run count by one
                        group_era_run_counts[item.eos_directory][item.era] += 1
                    else:
                        continue
                else:
                    result[item.eos_directory] = {item.run: item.era}
                    # Set new group as deaultdict in the dict
                    group_era_run_counts[item.eos_directory] = defaultdict(int)
                    # Increment the group's era run count by one
                    group_era_run_counts[item.eos_directory][item.era] += 1

        logging.debug(f"Group eras run count for run limit: {group_era_run_counts}")
        return result

    def get_max_run(self) -> int:
        """Get max run number"""
        return max(m.run for m in self.root)

    def get_meta_by_group_and_run(self, group_directory: str, run_num: int) -> Union[DqmMeta, None]:
        """Get metadata of a group and run"""
        # For a single run+group couple there should be single ROOT file
        try:
            return [m for m in self.root if (m.run == run_num and m.eos_directory == group_directory)][0]
        except Exception as e:
            logging.warning(
                f"No dqm meta found for the given group and run: {group_directory} - {run_num}. error:{str(e)}"
            )
            return None
