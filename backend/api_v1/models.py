#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Models of FastApi client
"""

from pydantic import BaseModel


class RequestSingleRun(BaseModel):
    """Post request schema to get ROOT object JSON"""

    run_number: int | None = None  # Histograms of a run number, None means recent run


class RequestOverlay(BaseModel):
    """Post request schema to get ROOT object JSON for overlay which use multiple run numbers"""

    run_numbers: list[int] | None = None  # Histograms of a run number, None means recent run


class ResponseHistogram(BaseModel):
    """Representation of histogram"""

    name: str | None = None  # Histogram name
    type: str | None = None  # Histogram type
    data: str | None = None  # JSON


class ResponseDetectorGroup(BaseModel):
    """Representation of histogram"""

    gname: str | None = None  # Detector group name: L1T, HLT
    dataset: str | None = None  # Detector group data root file's dataset name
    root_file: str | None = None  # Detector group root file full EOS path
    histograms: list[ResponseHistogram] | list = []  # Histogram data of the detector group


class ResponseRun(BaseModel):
    """Main response schema to histograms requests"""

    run_year: int | None = None  # Run year
    run_number: int | None = None  # Run number
    detector_histograms: list[ResponseDetectorGroup] | list = []  # Histogram detector groups list


class ResponseOverlay(BaseModel):
    """Main response schema to overlay histograms requests"""

    run_numbers: list[int] | None = None  # Run number
    detector_histograms: list[ResponseDetectorGroup] | list = []  # Histogram detector groups list
