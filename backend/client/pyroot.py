#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : PyROOT utils
"""

import functools
import json
import logging
from enum import Enum

import ROOT


class RootClasses(str, Enum):
    """ROOT C++ classes"""
    TH1F = "TH1F"


# ----------------------------------------------------------------------------

@functools.lru_cache(maxsize=128, typed=False)
def get_root_obj_as_json(file_path: str, obj_path: str):
    """Returns the JSON of the plot from ROOT file

    Args:
        file_path: ROOT file path
        obj_path: plot object directory inside ROOT file

    Returns: dict
    """
    root_f = None
    try:
        logging.debug(f"Incoming request for file:{file_path}, obj:{obj_path}")

        # Open file
        root_f = ROOT.TFile.Open(file_path)
        # Get object
        obj = root_f.Get(obj_path)

        if obj.IsZombie():
            logging.error(f"Object is zombie: file:{file_path}, obj:{obj_path}")
            raise Exception("Zombie Object")

        if obj.Class_Name() == RootClasses.TH1F:
            # Convert to JSON and return it
            return json.loads(str(ROOT.TBufferJSON.ConvertToJSON(obj)))  # returns JSON string
        else:
            raise Exception(f"Class is not {RootClasses.TH1F}")
    except Exception as e:
        logging.error(f"Error of file:{file_path}, obj:{obj_path} | Description: " + str(e))
        return None
    finally:
        # Close ROOT file
        if hasattr(root_f, "Close"):
            root_f.Close()

def get_json_file(file_path: str):
    """Returns the directories of plots in JSON format for test.

    Args:
        file_path:s list of json files that provides all plots in dict of JSON list format
    
    Returns: list[dict]
    """
    try:
        with open(file_path) as f:
            d = f.read()
            print(d)
            return json.loads(d)
    except Exception as e:
        logging.error(f"Error of file:{file_path} | Description: " + str(e))
        return None


def get_json_files(file_paths: any):
    """Returns the directories of plots in JSON format for test.

    Args:
        file_path:s list of json files that provides all plots in dict of JSON list format
    
    Returns: list[dict]
    """
    try:
        rootJsons = []
        for file_path in file_paths:
            with open(file_path, "r") as f:
                rootJsons.append(json.loads(f.read()))
        return rootJsons
    except Exception as e:
        logging.error(f"Error of file:{file_paths} | Description: " + str(e))
        return None