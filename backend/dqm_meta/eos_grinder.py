#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Stores metadata of DQMGui ROOT files by parsing last N years Runs. Metadata consists of all EOS ROOT files with their paths, run number, dataset name and detector name
How         :
- Get the main EOS directory of DQMGUI and `find` all the ROOT files with their full paths depending on Run years, and store them in intermediary txt file
- There is a simple regex pattern to extract run year, dataset name, run number, detector group(naming refers to HLT, L1T, etc.)
- All these metadata are strictly structured using a pydantic model class: DqmFileMetadata
- And parsed and formatted metadata stored in JSON file.
- We use this metadata file to find histograms of detector groups or histograms of specific run number. 
- eos_grinder is runs in the start of the container, and it is added as CRON job with 10 mins period.
- Process time is less than ~1 mins and JSON file size is <40 MB for Run2022 and Run2023.
- In the future, it can be moved to a DB according to requirements.
"""

import logging
import os
import re
import subprocess
import time
from datetime import datetime
from pydantic import BaseModel, RootModel
from typing import List

from backend.config import Config, get_config, get_config_group_directories

logging.basicConfig(level=get_config().loglevel.upper())

# SCHEMA ---------------------------------------------------------------------


class DqmMeta(BaseModel):
    """Representation of single DQM ROOT file's parsed metadata"""

    dataset: str  # Dataset name embedded in the ROOT file name: JetMET1/Run2023A-PromptReco-v1, JetMET1/Run2023D-Express-v1
    eos_directory: str  # Detector group directory: JetMET1, HLTPhysics, so on
    era: str  # Run era
    root_file: str  # full EOS path of the root file
    run: int  # Run number


class DqmMetaStore(RootModel):
    """DQM main metadata format: list of DqmMeta"""

    root: List[DqmMeta]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def get_eras(self) -> List[str]:
        """Get all available era names"""
        return list(set([item.era for item in self.root]))

    def get_datasets(self) -> List[str]:
        """Get all available dataset names"""
        return list(set([m.dataset for m in self.root]))

    def get_runs(self, limit: int = 100) -> List[int]:
        """Get run numbers with a return limit"""
        return sorted({m.run for m in self.root}, reverse=True)[:limit]

    def get_max_run(self) -> int:
        """Get max run number"""
        return max(m.run for m in self.root)

    def get_meta_by_dataset(self, dataset: str, limit: int = 10) -> List[DqmMeta]:
        """Get metadata list of a dataset sorted by run"""
        return sorted([m for m in self.root if m.dataset == dataset], key=lambda x: x.run, reverse=True)[:limit]

    def get_meta_by_run(self, run: int, limit: int = 10) -> List[DqmMeta]:
        """Get metadata list of a run sorted by run"""
        return sorted([m for m in self.root if m.run == run], key=lambda x: x.run, reverse=True)[:limit]

    def get_meta_by_era(self, era: str, limit: int = 10) -> List[DqmMeta]:
        """Get metadata list of an era sorted by run"""
        return sorted([m for m in self.root if m.era == era], key=lambda x: x.run, reverse=True)[:limit]

    def get_meta_by_group_and_run(self, group_directory: str, run: int) -> DqmMeta:
        """Get metadata of a group and run"""
        # For a single run+group couple there should be single ROOT file
        try:
            return [m for m in self.root if (m.run == run and m.eos_directory == group_directory)][0]
        except:
            return None


# CLIENT ---------------------------------------------------------------------
def get_dqm_store(config: Config):
    """DqmMetaStore client to search DQM GUI root files, directories, run numbers and datasets

    Args:
        config: given Config object to get `dqm_meta_store.meta_store_json_file`
    """
    # TODO: refresh it in each 10 minutes
    with open(config.dqm_meta_store.meta_store_json_file) as f:
        return DqmMetaStore.model_validate_json(f.read())


# GRINDER --------------------------------------------------------------------


def run():
    """Run with given yaml config"""
    # Get config as object
    __start_time = time.time()
    dqm_meta_conf = get_config().dqm_meta_store

    # Get config group directories to discard others
    conf_group_directories = get_config_group_directories()
    logging.info(f"DQM EOS grinder is starting... Allowed directories: {conf_group_directories}")

    create_dqm_store(
        dqm_eos_dir=dqm_meta_conf.base_dqm_eos_dir,
        find_tmp_results_file=dqm_meta_conf.find_tmp_results_file,
        meta_store_json_file=dqm_meta_conf.meta_store_json_file,
        last_n_run_years=dqm_meta_conf.last_n_run_years,
        file_suffix_pat=dqm_meta_conf.file_suffix_pat,
        allowed_group_directories=conf_group_directories,
    )
    logging.info(f"DQM EOS grinder is finished. Elapsed time : {str(int(time.time() - __start_time))} seconds.")


def create_dqm_store(
    dqm_eos_dir,
    find_tmp_results_file,
    meta_store_json_file,
    last_n_run_years,
    file_suffix_pat,
    allowed_group_directories,
):
    """Find DQMGui ROOT files in EOS directories in last 2 Run years and store them as DqmMetaStore schema

    Args:
        dqm_eos_dir: Base DQM EOS directory of Run years. i.e.="/eos/cms/store/group/comm_dqm/DQMGUI_data"
        find_tmp_results_file: Intermediary file to store raw find command results. i.e.:"dqm_root_files.txt"
        meta_store_json_file: Final parsed DqmMetaStore formatted json file which will be used as metadata store. i.e.:"dqm_meta.json"
        last_n_run_years: Required to fetch which Runs /DQMGUI_data/Run20XX directories. If 2 given, Run2023 and Run2023 will be used in year 2023.
        file_suffix_pat: find command '-iname' suffix pattern like '*DQMIO.root' for ROOT files. i.e.:"*DQMIO.root"
        allowed_group_directories: Group directories defined in the config; only their metadata will be created
    """
    current_year = datetime.now().year
    run_years = range(current_year - last_n_run_years + 1, current_year + 1)

    # Full directory path list for "last_n_run_years"
    base_eos_run_year_dirs = []

    # Check directory exists
    for run_dir in [f"{dqm_eos_dir.rstrip('/')}/Run{str(year)}" for year in run_years]:
        if os.path.exists(run_dir):
            base_eos_run_year_dirs.append(run_dir)
        else:
            logging.warning(f"Run directory not exist: {run_dir}")

    # Run find script and store its data in
    run_sh_find_cmd(base_eos_run_year_dirs, find_tmp_results_file, file_suffix_pat)
    dqm_meta_data = get_formatted_meta_from_raw_input(find_tmp_results_file, allowed_group_directories)
    with open(meta_store_json_file, "w+") as f:
        f.write(dqm_meta_data.model_dump_json())


def run_sh_find_cmd(base_search_dirs: list[str], outfile: str, file_suffix_pat: str):
    """Runs linux find command and saves results to defined outfile

    Args:
        base_search_dirs: Base EOS directories to run find command
        outfile: file to store find command results
        file_suffix_pat: find command "-iname" suffix pattern like '*DQMIO.root'
    """
    # find "${baseEosDirs[@]}" -iname '*DQMIO.root' >"$outputFile"
    cmd = f"find {' '.join(base_search_dirs)} -iname '{file_suffix_pat}' >{outfile}"
    # cmd = f"find {' '.join(base_search_dirs)} \( -path '*/JetMET1/*' -o -path '*/HLTPhysics/*' \) -iname '{file_suffix_pat}' >{outfile}"
    r = subprocess.run(cmd, capture_output=True, shell=True, check=True)
    if r.returncode:
        logging.warning(
            f"Exit code: {r.returncode} , Stdout: {r.stdout.decode('utf-8')}, Stderr: {r.stderr.decode('utf-8')}"
        )
    r.check_returncode()


def get_formatted_meta_from_raw_input(input_file, allowed_group_directories) -> DqmMetaStore:
    """Read raw ROOT file names from input file and format them in DqmMetaStore schema and return

    Args:
        input_file: file that stores raw output of find results
        allowed_group_directories: group directories from config
    """
    try:
        with open(input_file) as fin:
            dqm_main_meta_list = [
                get_group_meta(root_file_name, allowed_group_directories) for root_file_name in fin.readlines()
            ]
            # Remove None
            dqm_main_meta_list = [item for item in dqm_main_meta_list if item is not None]
            return DqmMetaStore(dqm_main_meta_list)
    except Exception as e:
        logging.error(f"Cannot parse data of given input file. input file:{input_file}. Error: {str(e)}")
        raise


# Compiled regex pattern to parse ROOT file name
#   Expected input: /eos/cms/store/group/comm_dqm/DQMGUI_data/Run2023/AlCaPPSPrompt/0003658xx/DQM_V0001_R000365835__AlCaPPSPrompt__Run2023A-PromptReco-v1__DQMIO.root
#   Expected output of re groupdict: {'year': '2023', 'group_directory': 'AlCaPPSPrompt', 'run': '000365835', 'dataset_prefix': 'AlCaPPSPrompt', 'era': 'Run2023A', 'dataset_suffix': 'Run2023A-PromptReco-v1'}
DQM_EOS_ROOT_RE = re.compile(
    r".+?/Run(?P<year>\d+)/(?P<group_directory>.+?)/(.+?)/DQM_V(\d+)_R(?P<run>\d+)__(?P<dataset_pref>.+?)__(?P<era>.+?)-(?P<dataset_suff>.+?)__DQMIO.root"
)


def get_group_meta(file_name, allowed_group_directories) -> DqmMeta:
    """Parsea and formats single DQM EOS ROOT file name

    Args:
        file_name: EOS full path of ROOT file, i.e /eos/cms/store/group/comm_dqm/DQMGUI_data/Run2023/AlCa.../...x/DQM_V0001_...__DQMIO.root
        allowed_group_directories: Only given group directories in the config file will be used.
    """

    file_name = file_name.strip()  # Remove new line
    re_match_dict = re.match(DQM_EOS_ROOT_RE, file_name).groupdict()  # Match regex and get key-value pairs as dict

    # Get regex group dict in which the names are already provided in the regex pattern
    if re_match_dict["group_directory"] in allowed_group_directories:
        # 'dataset_prefix': 'AlCaPPSPrompt', 'era': 'Run2023A', 'dataset_suffix': 'Run2023A-PromptReco-v1'
        dataset_name = re_match_dict["dataset_pref"] + "/" + re_match_dict["era"] + "-" + re_match_dict["dataset_suff"]
        return DqmMeta(
            dataset=dataset_name,
            eos_directory=re_match_dict["group_directory"],
            era=re_match_dict["era"],
            root_file=file_name,
            run=re_match_dict["run"],
        )
    else:
        return None
