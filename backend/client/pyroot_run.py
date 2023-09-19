#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : PyROOT utils
"""
import functools
import logging

from ROOT import TFile, TBufferJSON

from backend.api_v1.models import ResponseSingleRun, ResponsePlot, ResponseGroup
from backend.config import get_config
from backend.dqm_meta.client import DqmMetadataClient

# Allowed histogram classes
AllowedRootClasses = ("TH1F", "TH2F")
logging.basicConfig(level=get_config().loglevel.upper())


# Your Bible: https://root.cern.ch/doc/master/classTDirectoryFile.html


def get_run_histograms(
    run_number: int = 0, allowed_histogram_classes: tuple = AllowedRootClasses
) -> ResponseSingleRun:
    """Returns histograms of a specific run number of a run year

    run number 0 returns the last run
    """
    conf = get_config()
    dqm_store_client = DqmMetadataClient(config=conf)
    detector_groups_dirs = [grp.eos_directory for grp in conf.plots_config]

    # If both run number is not defined, return latest run
    if run_number <= 0:
        my_run_number = dqm_store_client.last_run_number(detector_groups_dirs)
    else:
        my_run_number = run_number

    logging.debug(f"my_run_number={my_run_number}")

    detector_group_list_resp, my_run_year = [], 0
    # Iterate items of "ConfigDetectorGroup"
    for group_conf in conf.plots_config:
        # histograms_tdirectory_pattern includes formatted string patterns to format it
        hists_tdirectory = group_conf.tdirectory.format(**{"run_num_int": my_run_number})
        logging.debug(f"Detector group histograms TDirectory={hists_tdirectory}")

        # Histograms full path in the root file: TDirectory of the parent directory + histogram name
        __full_paths = tuple([str(hists_tdirectory + "/" + __hist_conf.name) for __hist_conf in group_conf.plots])

        # Get detector group histograms and year of the run
        detector_group_histograms, my_run_year = util_get_detector_group_histograms(
            dqm_store_client=dqm_store_client,
            group_name=group_conf.group_name,
            group_directory=group_conf.eos_directory,
            histograms_full_paths=__full_paths,
            run_number=my_run_number,
            allowed_histogram_classes=allowed_histogram_classes,
        )
        # Append to the main response list
        detector_group_list_resp.append(detector_group_histograms)

        logging.debug(f"Detector group histograms list={detector_group_list_resp}")

    return ResponseSingleRun(
        run_year=my_run_year, run_number=my_run_number, detector_histograms=detector_group_list_resp
    )


def util_get_detector_group_histograms(
    dqm_store_client: DqmMetadataClient,
    group_name: str,
    group_directory: str,
    histograms_full_paths: tuple[str],
    run_number: int,
    allowed_histogram_classes: tuple = None,
) -> tuple[ResponseGroup, int]:
    """Returns ResponseDetectorGroup which includes detector group's histograms and run year

    Args:
        dqm_store_client: DqmMetaStoreClient to get DQM EOS ROOT files' metadata
        group_name: Detector group's name HLT,J1T.
        group_directory: Detector group's EOS directory name: HLTPhysics, JetMET1, etc.
        histograms_full_paths: Full object paths of the histograms of the detector group
        run_number: run number to find the ROOT file of the group
        allowed_histogram_classes: Allowed ROOT histogram classes. For instance, in overlaying plots, only TH1F can be used in THStack
    """
    # Find the ROOT file metadata from DQM store client via EOS directory structure
    root_file_meta = dqm_store_client.get_det_group_root_file(run_number=run_number, group_directory=group_directory)
    logging.debug(f"root_file_meta={root_file_meta}")

    # Histogram jsons of detector group
    group_histograms = util_get_histogram_jsons(
        tfile=root_file_meta.root_file,
        histograms_full_paths=histograms_full_paths,
        allowed_histogram_classes=allowed_histogram_classes,
    )

    return (
        ResponseGroup(
            group_name=group_name,
            dataset=root_file_meta.dataset,
            root_file=root_file_meta.root_file,
            plots=group_histograms,
        ),
        root_file_meta.year,
    )


@functools.lru_cache(maxsize=1000, typed=False)  # Caches responses, params are hashabel so it works
def util_get_histogram_jsons(
    tfile: str, histograms_full_paths: tuple[str] = None, allowed_histogram_classes: tuple = None
) -> list[ResponsePlot]:
    """Returns list of histogram JSONs of requested root objects, used mostly for single Detector Group's histograms

    Args:
        tfile: Reachable ROOT file path
        histograms_full_paths: ROOT objects full paths inside the ROOT file
        allowed_histogram_classes: Allowed ROOT histogram classes. For instance, in overlaying plots, only TH1F can be used in THStack
    Returns:
        list of histogram JSONs
    """
    hist_jsons = []
    with TFile(tfile, "read") as tf:
        logging.debug(f"TFile={tfile}")
        for obj in histograms_full_paths:
            logging.debug(f"Obj={obj}")
            assumed_hist = tf.Get(obj)
            if not assumed_hist.IsZombie():
                assumed_hist_class = assumed_hist.ClassName()
                if assumed_hist_class in allowed_histogram_classes:
                    # Histogram object path is provided, so return its JSON
                    hist_resp = ResponsePlot(
                        name=assumed_hist.GetName(),
                        type=assumed_hist_class,
                        data=str(TBufferJSON.ToJSON(assumed_hist)),
                    )
                    hist_jsons.append(hist_resp)
                else:
                    logging.warning(
                        f"Given object is not a histogram. "
                        f"=> file {tfile}, obj: {obj}, obj class: {assumed_hist_class}"
                    )
            else:
                logging.warning(
                    f"Given object is a friendly Zombie with full of enjoyment. " f"=> file: {tfile}, obj path: {obj}"
                )
    return hist_jsons
