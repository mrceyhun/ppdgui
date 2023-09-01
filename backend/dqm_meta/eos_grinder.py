#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Stores metadata of DQMGui ROOT files by parsing last N years Runs. Metadata consists of all ROOT files with their paths, run number, dataset name and detector name
"""
import logging
import os
import re
import subprocess
from datetime import datetime

from backend.config import get_config
from backend.dqm_meta.models import DqmFileMetadata, DqmMetaStore

logger = logging.getLogger(__name__)


def main():
    """Run with given yaml config"""
    # Get config as object
    conf = get_config()
    dqm_meta_conf = conf.dqm_meta_store
    run(dqm_eos_dir=dqm_meta_conf.base_dqm_eos_dir,
        find_tmp_results_file=dqm_meta_conf.find_tmp_results_file,
        meta_store_json_file=dqm_meta_conf.meta_store_json_file,
        last_n_run_years=dqm_meta_conf.last_n_run_years,
        file_suffix_pat=dqm_meta_conf.file_suffix_pat)


def run(dqm_eos_dir, find_tmp_results_file, meta_store_json_file, last_n_run_years, file_suffix_pat):
    """Find DQMGui ROOT files in EOS directories in last 2 Run years and store them as DqmMetaStore schema

    Args:
        dqm_eos_dir: Base DQM EOS directory of Run years. i.e.="/eos/cms/store/group/comm_dqm/DQMGUI_data"
        find_tmp_results_file: Intermediary file to store raw find command results. i.e.:"dqm_root_files.txt"
        meta_store_json_file: Final parsed DqmMetaStore formatted json file which will be used as metadata store. i.e.:"dqm_meta.json"
        last_n_run_years: Required to fetch which Runs /DQMGUI_data/Run20XX directories. If 2 given, Run2023 and Run2023 will be used in year 2023.
        file_suffix_pat: find command '-iname' suffix pattern like '*DQMIO.root' for ROOT files. i.e.:"*DQMIO.root"
    """
    current_year = datetime.now().year
    run_years = range(current_year - last_n_run_years + 1, current_year + 1)
    base_search_dirs = []

    # Check directory exists
    for run_dir in [f"{dqm_eos_dir.rstrip('/')}/Run{str(year)}" for year in run_years]:
        if os.path.exists(run_dir):
            base_search_dirs.append(run_dir)
        else:
            logger.warning(f"Run directory not exist: {run_dir}")

    # Run find script and store its data in
    run_sh_find_cmd(base_search_dirs, find_tmp_results_file, file_suffix_pat)
    dqm_meta_data = get_formatted_meta_from_raw_input(find_tmp_results_file)
    with open(meta_store_json_file, 'w+') as f:
        f.write(dqm_meta_data.model_dump_json())


def run_sh_find_cmd(base_eos_dirs: list[str], outfile: str, file_suffix_pat: str):
    """Runs linux find command and saves results to defined outfile

    Args:
        base_eos_dirs: Base EOS directories to run find command
        outfile: file to store find command results
        file_suffix_pat: find command "-iname" suffix pattern like '*DQMIO.root'
    """
    # find "${baseEosDirs[@]}" -iname '*DQMIO.root' >"$outputFile"
    cmd = f"find {' '.join(base_eos_dirs)} -iname '{file_suffix_pat}' >{outfile}"
    r = subprocess.run(cmd, capture_output=True, shell=True, check=True)

    logger.info(f"Exit code: {r.returncode}")
    logger.info(f"Stdout: {r.stdout.decode('utf-8')}")
    logger.info(f"Stderr: {r.stderr.decode('utf-8')}")
    r.check_returncode()


def get_formatted_meta_from_raw_input(input_file) -> DqmMetaStore:
    """Read raw ROOT file names from input file and format them in DqmMetaStore schema and return

    Args:
        input_file: file that stores raw output of find results
    Returns:
        DqmMetaStore
    """
    # Compiled regex pattern to parse ROOT file name
    #   Expected input: /eos/cms/store/group/comm_dqm/DQMGUI_data/Run2023/AlCaPPSPrompt/0003658xx/DQM_V0001_R000365835__AlCaPPSPrompt__Run2023A-PromptReco-v1__DQMIO.root
    #   Expected output of re groupdict: {'year': '2023', 'group_directory': 'AlCaPPSPrompt', 'run': '000365835', 'dataset': 'Run2023A-PromptReco-v1'}
    regex_pattern = re.compile(
        r".+?/Run(?P<year>\d+)/(?P<group_directory>.+?)/(.+?)/DQM_V(\d+)_R(?P<run>\d+)__(.+?)__(?P<dataset>.+?)__DQMIO.root")

    try:
        with open(input_file) as fin:
            formatted_metadata_list = [_get_one_file_meta(f, regex_pattern) for f in fin.readlines()]
            return DqmMetaStore(formatted_metadata_list)
    except Exception as e:
        logger.error(f"Cannot parse data of given input file. input file:{input_file}. Error: {str(e)}")
        raise


def _get_one_file_meta(file, rxpat) -> DqmFileMetadata:
    """Returns parsed DqmRootFileMetadata for a single DQM ROOT file

    Args:
        file: eos full path of ROOT file, i.e /eos/cms/store/group/comm_dqm/DQMGUI_data/Run2023/AlCa.../...x/DQM_V0001_...__DQMIO.root
        rxpat: compiled regex pattern to parse EOS file full path. See the caller function for more details.
    Returns:
        DqmRootFileMetadata
    """

    file = file.strip()  # Remove new line
    mdict = re.match(rxpat, file).groupdict()  # Match regex and get key-value pairs as dict

    # Get regex group dict in which the names are already provided in the regex pattern, so don't afraid ;)
    return DqmFileMetadata(
        year=mdict['year'],
        run=mdict['run'],
        group_directory=mdict['group_directory'],
        dataset=mdict['dataset'],
        root_file=file
    )


if __name__ == "__main__":
    main()
