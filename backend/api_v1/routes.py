#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : FastAPI main.py
"""
import logging
from fastapi import APIRouter, HTTPException

from typing import Union
from .models import RequestHistograms
from backend.client import pyroot
from backend.config import get_config

# ----------------------------------------------------------------------------

# TODO: change prefix
router = APIRouter()
logging.basicConfig(level=get_config().loglevel.upper())


@router.post("/get-histogram-jsons")
async def get_root_dirs_or_hist(req: Union[RequestHistograms, None]):
    """Get ROOT histogram in JSON format by providing run year and run number

    Default 0 values of run number or nobody request returns the latest run.
    """
    logging.info("Request:get-histogram-jsons " + str(req))
    try:
        return pyroot.get_all_histograms(run_number=req.run_number)
    except Exception as e:
        logging.error(f"Cannot process request. Incoming request => {str(req)}. Error: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Error while processing request of [ run:{req.run_number} ]")
