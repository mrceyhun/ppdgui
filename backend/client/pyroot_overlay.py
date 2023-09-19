#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : PyROOT utils
"""
import logging
from ROOT import TBufferJSON, TCanvas, THStack, TLegend

from backend.api_v1.models import ResponseOverlayRuns, ResponsePlot, ResponseGroup
from backend.config import get_config
from .pyroot_run import get_run_histograms

# Allowed histogram classes. Only 1 dimensional hisograms can be overlayed.
AllowedRootClasses = ("TH1F",)
logging.basicConfig(level=get_config().loglevel.upper())


# Your Bible: https://root.cern.ch/doc/master/classTDirectoryFile.html


def get_overlay_histograms(run_numbers: list[int]) -> ResponseOverlayRuns:
    """Returns histograms of list of runs

    Each run response contains ordered detector groups and ordered histograms. Only same histograms (same name)
    can be overlayed using THStack and TCanvas. Because of ordered responses, indexes will be used to stack/overlay
    histograms.
    """
    runs_responses = [
        get_run_histograms(run_number=r, allowed_histogram_classes=AllowedRootClasses) for r in run_numbers
    ]
    # Should be same for each run response
    detector_groups_cnt = len(runs_responses[0].detector_histograms)
    list_response_detector_groups = []
    for index in range(detector_groups_cnt):
        list_response_detector_groups.append(
            # Get list of same detector groups in each run response
            util_join_detector_groups(
                [run_response.detector_histograms[index] for run_response in runs_responses], run_numbers
            )
        )
    return ResponseOverlayRuns(runs=run_numbers, group_plots=list_response_detector_groups)


def util_join_detector_groups(detector_groups: list[ResponseGroup], runs: list[int]):
    """Joins same detector group histograms of different runs

    Args:
        detector_groups: ResponseDetectorGroup histograms should belong to the same group of different run.
        runs: Run numbers of detector groups in order with detector_groups.
    """
    gname = detector_groups[0].group_name
    dataset = detector_groups[0].dataset
    list_response_histograms = []
    # Histograms should be identical and sorted by previous processes. Each histogram in the same index will return same histogram
    histograms_cnt = len(detector_groups[0].plots)
    for index in range(histograms_cnt):
        list_response_histograms.append(
            # Get list of same histogram in each run group
            util_join_hists_to_thstack([det_group.plots[index] for det_group in detector_groups], runs)
        )
    return ResponseGroup(
        group_name=gname,
        dataset=dataset,
        root_file=None,
        plots=list_response_histograms,
    )


def util_join_hists_to_thstack(hists: list[ResponsePlot], runs: list[int]) -> ResponsePlot:
    """Joins same histograms of different runs and join them to THStack TCanvas

    In ROOT, overlay is possible using THStack. Histograms with different color and line style is added to the THStack
    and appropriate TLegend is created for each of them. Final result is TCanvas JSON to be drawn by JSROOT.

    TODO: Compare performance of JSROOT overlaying bs PYROOT overlaying.
          .. Same operations can be done in JS side too by sending each histogram jsons and creating THStack from them, see frontend/tests.

    Args:
        hists: Same histograms of different runs.
        runs: Run numbers of histograms in order with hists.
    """
    # Create THStack
    ths = THStack()
    # Create legend, ref https://gist.github.com/skaplanhex/55982ed5ddcc966dfc2d
    leg = TLegend(0.75, 0.7, 1.0, 0.9)
    leg.SetBorderSize(1)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.35)

    c = TCanvas()
    i = 1  # will control both line style and line color

    # They are same in all histograms(same groups' same histograms, but different runs)
    histName, histTitle = "", ""
    for hist, run in zip(hists, runs):
        histRoot = TBufferJSON.ConvertFromJSON(hist.data)

        # Get meta
        histName = histRoot.GetName()
        histTitle = histRoot.GetTitle()

        # Differantiate to look better in Stack. Check refs: https://root.cern.ch/doc/master/classTAttLine.html
        histRoot.SetLineStyle(i)
        histRoot.SetLineColor(i)
        leg.AddEntry(histRoot, str(run), "l")
        ths.Add(histRoot)
        i += 1

    ths.SetName(histName)  # Set THStack histogram name same as histograms
    ths.SetTitle(histTitle)  # Set THStack histogram title same as histograms

    ths.Draw("nostack,hist")
    leg.Draw()
    c.Draw()  # Required to get all objects in "c" JSON

    return ResponsePlot(name=histName, type="TCanvas", data=str(TBufferJSON.ToJSON(c)))
