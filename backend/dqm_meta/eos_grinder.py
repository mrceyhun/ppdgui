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
from typing import Tuple

from backend.config import get_config, get_config_group_directories
from .client import DqmMainMetadata, DqmMeta, DqmKeyOfEraDatasetRun

logging.basicConfig(level=get_config().loglevel.upper())


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


def get_formatted_meta_from_raw_input(input_file, allowed_group_directories) -> DqmMainMetadata:
    """Read raw ROOT file names from input file and format them in DqmMetaStore schema and return

    Args:
        input_file: file that stores raw output of find results
        allowed_group_directories: group directories from config
    """
    try:
        with open(input_file) as fin:
            dqm_main_metadata = {}
            for root_file_name in fin.readlines():
                dqm_key_era_dataset_run, dqm_meta = _get_detector_group_meta(root_file_name, allowed_group_directories)
                if dqm_key_era_dataset_run:
                    # add to dict
                    dqm_main_metadata.update({dqm_key_era_dataset_run: dqm_meta})

            return DqmMainMetadata(dqm_main_metadata)
    except Exception as e:
        logging.error(f"Cannot parse data of given input file. input file:{input_file}. Error: {str(e)}")
        raise


# Compiled regex pattern to parse ROOT file name
#   Expected input: /eos/cms/store/group/comm_dqm/DQMGUI_data/Run2023/AlCaPPSPrompt/0003658xx/DQM_V0001_R000365835__AlCaPPSPrompt__Run2023A-PromptReco-v1__DQMIO.root
#   Expected output of re groupdict: {'year': '2023', 'group_directory': 'AlCaPPSPrompt', 'run': '000365835', 'dataset_prefix': 'AlCaPPSPrompt', 'era': 'Run2023A', 'dataset_suffix': 'Run2023A-PromptReco-v1'}
DQM_EOS_ROOT_RE = re.compile(
    r".+?/Run(?P<year>\d+)/(?P<group_directory>.+?)/(.+?)/DQM_V(\d+)_R(?P<run>\d+)__(?P<dataset_pref>.+?)__(?P<era>.+?)-(?P<dataset_suff>.+?)__DQMIO.root"
)


def _get_detector_group_meta(file_name, allowed_group_directories) -> Tuple[DqmKeyOfEraDatasetRun, DqmMeta]:
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
        return DqmKeyOfEraDatasetRun(
            dataset=dataset_name,
            era=re_match_dict["era"],
            run=re_match_dict["run"],
        ), DqmMeta(
            dataset=dataset_name,
            eos_directory=re_match_dict["group_directory"],
            era=re_match_dict["era"],
            root_file=file_name,
            run=re_match_dict["run"],
        )
