#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : FastAPI main.py
"""
import logging
from fastapi import APIRouter, HTTPException

from .models import RequestHistograms
from backend.client import pyroot
from backend.config import get_config

# ----------------------------------------------------------------------------

# TODO: change prefix
router = APIRouter()
logging.basicConfig(level=get_config().loglevel.upper())


@router.post("/get-histogram-jsons")
async def get_root_dirs_or_hist(req: RequestHistograms):
    """Get ROOT histogram in JSON format by providing its file and obj path"""
    logging.info("Request:get-histogram-jsons " + str(req))
    try:
        return pyroot.get_all_histograms(run_year=req.run_year, run_number=req.run_number)
    except Exception as e:
        logging.error(f"Cannot process request. Incoming request => {str(req)}. Error: {str(e)}")
        raise HTTPException(status_code=404, detail="Cannot read file, err: " + str(e))
