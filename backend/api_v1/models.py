#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Models of FastApi client
"""

from pydantic import BaseModel


class RequestSingleRun(BaseModel):
    """Post request schema to get ROOT object JSO for a single run response"""

    run: int | None = None  # Run number, None means the most recent run


class RequestOverlay(BaseModel):
    """Post request schema to get ROOT object JSON for overlay which use multiple run numbers"""

    runs: list[int] | None = None  # List of runs for overlay, None means the most recent run without overlay


class ResponsePlot(BaseModel):
    """Representation of a plot/histogram"""

    data: str | None = None  # Histogram JSON created using TBufferJSON
    dqm_url: str | None = None  # DQMGUI url
    draw_opt: str | None = None  # Histogram JSROOT draw option
    name: str | None = None  # Histogram name
    type: str | None = None  # Histogram type: TH1F, TH2F, TProfile


class ResponseGroup(BaseModel):
    """Representation of histogram"""

    group_name: str | None = None  # Detector group name: L1T, HLT
    dataset: str | None = None  # Detector group data root file's dataset name
    root_file: str | None = None  # Detector group root file full EOS path
    plots: list[ResponsePlot] | list = []  # Histogram data of the detector group


class ResponseSingleRun(BaseModel):
    """Main response schema to histograms requests"""

    run: int | None = None  # Run number
    detector_histograms: list[ResponseGroup] | list = []  # Histogram detector groups list


class ResponseOverlayRuns(BaseModel):
    """Main response schema to overlay histograms requests"""

    runs: list[int] | None = None  # Run numbers
    group_plots: list[ResponseGroup] | list = []  # Detector groups lists
