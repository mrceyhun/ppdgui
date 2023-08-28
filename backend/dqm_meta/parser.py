#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : To search DQM GUI root files, directories, run numbers and datasets using `tree` command results on DQM EOS
Why         : Collects We need a map kind structure to search Runs by datasets or vise versa, for this reason we need DqmRootSingleFileMeta kind of object
"""
import logging
import re

from backend.dqm_meta.models import DqmRootSingleFileMeta, DqmMetaStore

# Global compiled regex pattern to parse ROOT file name
REGEX_PATTERN = None


def get_raw_tree_out(basedir, outfile):
    """Runs linux tree command and saves results to defined outfile"""



def get_file_name_rxpat():
    """Returns the compiled regex patter for ROOT file name

    Expected input: /eos/cms/store/group/comm_dqm/DQMGUI_data/Run2023/AlCaPPSPrompt/0003658xx/DQM_V0001_R000365835__AlCaPPSPrompt__Run2023A-PromptReco-v1__DQMIO.root
    Expected output of re groupdict: {'year': '2023', 'det_group': 'AlCaPPSPrompt', 'run': '000365835', 'dataset': 'Run2023A-PromptReco-v1'}
    """
    global REGEX_PATTERN
    if not REGEX_PATTERN:
        REGEX_PATTERN = re.compile(
            r".+?/Run(?P<year>\d+)/(?P<det_group>.+?)/(.+?)/DQM_V(\d+)_R(?P<run>\d+)__(.+?)__(?P<dataset>.+?)__DQMIO.root")

    return REGEX_PATTERN


def parse_single_file_name(file):
    """Returns parsed DqmRootSingleFileMeta for a single full EOS file path

    Args:
        file: eos full path of ROOT file, i.e /eos/cms/store/group/comm_dqm/DQMGUI_data/Run2023/AlCa.../...x/DQM_V0001_...__DQMIO.root
    """
    # Remove new line
    file = file.strip()

    # Match regex
    m = re.match(get_file_name_rxpat(), file)

    # Get regex group dict in which the names are already provided in the regex pattern, so don't afraid ;)
    return DqmRootSingleFileMeta(**{**m.groupdict(), **{'eos_path': file}})


def parse_all_file_names(input_tree_file) -> DqmMetaStore:
    """Read unix tree command results, parse in required format and save as JSON

    Args:
        input_tree_file: file that stores the output of [tree -ifFl --noreport -I '*.dqminfo' -P '*DQMIO.root' /eos/cms/store/group/comm_dqm/DQMGUI_data/Run2023/]  command
    Returns: DqmMetaStore
    """
    try:
        with open(input_tree_file) as fin:
            formatted_metadata_list = [parse_single_file_name(f) for f in fin.readlines()]
            return DqmMetaStore(data=formatted_metadata_list)
    except Exception as e:
        logging.error(f"Cannot format OS tree file. "
                      f"input file:{input_tree_file}. Error: {str(e)}")
        raise


