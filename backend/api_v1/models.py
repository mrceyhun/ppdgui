#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Models of FastApi client
"""

from typing import Dict, List

from pydantic import BaseModel, RootModel


class Request(BaseModel):
    """Post request schema to get ROOT object JSON for overlay which use multiple run numbers"""

    eras: list[str] | None = None  # List of eras to filter, None is use all eras
    groups: list[str] | None = None  # List of filtered eras, None is no filter and use all
    datasets: list[str] | None = None  # List of filtered datasets, None is no filter and use all
    runs: list[int] | None = None  # List of runs for overlay, None means the most recent run without overlay


class ResponsePlot(BaseModel):
    """Representation of a plot/histogram"""

    id: str  # hash of the histogram name with 'id' prefix
    data: str | None = None  # Histogram JSON created using TBufferJSON
    dqm_url: str | None = None  # DQMGUI url
    draw_opt: str | None = None  # Histogram JSROOT draw option
    hist_name: str | None = None  # Histogram name
    conf_name: str | None = None  # Histogram name in the plots.yaml config file (more descriptive)
    run: int | None = None  # Run number which helps to find ERA too
    type: str | None = None  # Histogram type: TH1F, TH2F, TProfile


class ResponsePlotsDict(RootModel):
    """Representation of a key: plot name, value: plots/histograms data

    Used to store all histograms of a group for easy access
    """

    root: Dict[str, ResponsePlot]

    def get_plots_only(self) -> List[ResponsePlot]:
        return list(self.root.values())

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


class ResponseGroup(BaseModel):
    """Representation of histogram"""

    group_name: str | None = None  # Detector group name: L1T, HLT
    dataset: str | None = None  # Detector group data root file's dataset name
    root_file: str | None = None  # Detector group root file full EOS path
    plots: List[ResponsePlot] | List = []  # Histogram data of the detector group


class ResponseMain(BaseModel):
    """Main response schema to overlay histograms requests"""

    eras: List[str] | None = None  # Eras
    groups: List[str] | None = None  # Groups
    groups_data: List[ResponseGroup] | List = []  # Detector groups results list
    runs: List[int] | None = None  # Run numbers
