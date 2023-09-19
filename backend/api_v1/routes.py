#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : FastAPI main.py
"""
import logging
from fastapi import APIRouter, HTTPException

from typing import Union
from .models import RequestSingleRun, RequestOverlay
from backend.client import pyroot_run, pyroot_overlay
from backend.config import get_config

# ----------------------------------------------------------------------------

# TODO: change prefix
router = APIRouter()
logging.basicConfig(level=get_config().loglevel.upper())


@router.post("/get-run-hists")
async def get_run_hists(req: Union[RequestSingleRun, None]):
    """Get ROOT histogram in JSON format by providing run year and run number

    Default 0 values of run number or nobody request returns the latest run.
    """
    logging.info("Request:get-run-hists " + str(req))
    try:
        return pyroot_run.get_run_histograms(run_number=req.run)
    except Exception as e:
        logging.error(f"Cannot process request. Incoming request => {str(req)}. Error: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Error while processing request of [ run:{req.run} ]")


@router.post("/get-overlay-hists")
async def get_overlay_hists(req: Union[RequestOverlay, None]):
    """Get ROOT overlayed histograms in JSON of TCanvas  format by providing run numbers"""
    logging.info("Request:get-overlay-hists " + str(req))
    try:
        return pyroot_overlay.get_overlay_histograms(run_numbers=req.runs)
    except Exception as e:
        logging.error(f"Cannot process request. Incoming request => {str(req)}. Error: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Error while processing request of [ run numbers:{req.runs} ]")
