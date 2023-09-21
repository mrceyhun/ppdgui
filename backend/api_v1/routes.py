#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : FastAPI main.py
"""
import logging
from typing import Union

from fastapi import APIRouter, HTTPException

from backend.client import pyroot, utils
from backend.config import get_config
from .models import Request

# ----------------------------------------------------------------------------

# TODO: change prefix
router = APIRouter()
logging.basicConfig(level=get_config().loglevel.upper())


@router.post("/get-hists")
async def get_run_hists(req: Union[Request, None]):
    """Get ROOT histogram JSONs either overlaid or raw"""
    logging.info(f"Request:get-hists req: {str(req)}")
    try:
        return pyroot.get_histograms(runs=req.runs, groups=req.groups, eras=req.eras)
    except Exception as e:
        logging.error(f"Cannot process request. Incoming request => {str(req)}. Error: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Error while processing request of [ run:{req.runs} ]")


# TODO: add filters like groups,datasets, runs filters
@router.get("/get-eras")
async def get_eras():
    """Get all available eras"""
    logging.info("Request:get-eras")
    try:
        eras = utils.get_available_eras()
        logging.debug(f"Eras  + {str(eras)}")
        return eras
    except Exception as e:
        logging.error(f"Cannot get eras Error: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Error while processing request of /get-eras ]")
