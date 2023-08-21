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
from ROOT import TFile

from backend.api_v1.models import ResponseRootObj, HistogramJson


class RootClasses(str, Enum):
    """ROOT C++ classes"""
    TH1F = "TH1F"
    TDirectoryFile = "TDirectoryFile"


# Your Bible: https://root.cern.ch/doc/master/classTDirectoryFile.html

# ----------------------------------------------------------------------------

@functools.lru_cache(maxsize=1000, typed=False)  # Cache responses, params are hashabel so it works
def get_root_dirs_or_hist(tfile: str, tobject: str = None, all_hists: bool = False) -> ResponseRootObj:
    """Returns directories or histogram JSONs of requested root object according to its type

    Args:
        tfile: Reachable ROOT file path
        tobject: ROOT object inside the file, full object path
        all_hists: Return all histograms in the Directory, no subdirectories of course

    Returns: List of directories or JSON dict

    """
    RESPONSE = ResponseRootObj()

    if tobject:
        tobject = tobject.strip("/")

    try:
        with TFile(tfile, "read") as tf:
            if not tobject or tobject.strip() == "":
                RESPONSE.dirs = [directory.GetName() for directory in tf.GetListOfKeys()]
            else:
                obj = tf.Get(tobject)
                obj_class = obj.ClassName()

                # Check object is TH1F or Directory
                if obj_class == RootClasses.TDirectoryFile and not all_hists:
                    # Only directory provided, so return subdirectories

                    RESPONSE.dirs = [i.GetName() for i in obj.GetListOfKeys()]
                elif obj_class == RootClasses.TH1F:
                    # Histogram object path is provided, so return its JSON
                    h = HistogramJson(**{
                        "name": obj.GetName(),
                        "data": json.loads(str(ROOT.TBufferJSON.ToJSON(obj)))
                    })
                    RESPONSE.hist_json.append(h)
                elif obj_class == RootClasses.TDirectoryFile and all_hists:
                    # A subdirectory provided and requests all histograms in it
                    __hists = []
                    __dirs = [i.GetName() for i in obj.GetListOfKeys()]
                    for d in __dirs:
                        __full_path = tobject + "/" + d
                        __obj = tf.Get(__full_path)
                        __obj_class = __obj.ClassName()
                        if __obj_class == RootClasses.TH1F:
                            RESPONSE.hist_json.append(
                                HistogramJson(**{
                                    "name": d,
                                    "data": json.loads(str(ROOT.TBufferJSON.ToJSON(__obj)))
                                })
                            )
            return RESPONSE
    except Exception as e:
        logging.error(f"Object neither TH1F nor Directory. Incoming=> file{tfile}, obj:{tobject} . Error: {str(e)}")
        raise
