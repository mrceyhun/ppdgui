#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : PyROOT utils
"""

import ROOT
import logging
from enum import Enum


class RootClass(str, Enum):
    TH1F = "TH1F"


def get_obj_json(file_path: str, obj_path: str) -> str | None:
    """Returns the JSON of the plot from ROOT file

    Args:
        file_path: ROOT file path
        obj_path: plot object directory inside ROOT file

    Returns: dict
    """
    try:
        logging.warning(f"Incoming request for file:{file_path}, obj:{obj_path}")
        root_f = ROOT.TFile.Open(file_path)
        obj = root_f.Get(obj_path)
        if obj.IsZombie():
            logging.error(f"Object is zombie: file:{file_path}, obj:{obj_path}")
            raise Exception("Zombie Object")

        if obj.Class_Name() == RootClass.TH1F:
            return str(ROOT.TBufferJSON.ConvertToJSON(obj))  # returns JSON string
        else:
            raise Exception(f"Class is not {RootClass.TH1F}")
    except Exception as e:
        logging.error(f"Error of file:{file_path}, obj:{obj_path} | Description: " + str(e))
        return None
