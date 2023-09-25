#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : FastAPI main.py
"""
import logging
from typing import Union, List

from fastapi import APIRouter, HTTPException, Request, Query

from backend.client import pyroot, utils
from backend.config import get_config
from .models import Request


DEFAULT_RUN_LIMIT_PER_ERA = get_config().plots.max_era_run_size

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


@router.get("/get-groups")
async def get_groups():
    """Get all available groups"""
    logging.info("Request:get-groups")
    try:
        group_names = utils.get_available_groups()
        logging.debug(f"group_names  + {str(group_names)}")
        return group_names
    except Exception as e:
        logging.error(f"Cannot get group_names Error: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Error while processing request of /get-groups ]")


@router.get("/get-eras")
async def get_eras(groups: List[str] = Query(None)):
    """Get all available eras filtered by groups"""
    logging.info(f"Request:get-eras, param [groups] : {groups}")
    try:
        eras = utils.get_available_eras(group_names=groups)
        logging.debug(f"Eras  + {str(eras)}")
        return eras
    except Exception as e:
        logging.error(f"Cannot get eras Error: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Error while processing request of /get-eras ]")


@router.get("/get-runs")
async def get_runs(
    limit: int = Query(DEFAULT_RUN_LIMIT_PER_ERA), groups: List[str] = Query(None), eras: List[str] = Query(None)
):
    """Get all available eras filtered by groups and eras"""
    logging.info(f"Request:get-runs, param [eras] : {eras}")
    try:
        eras = utils.get_available_runs(limit=limit, groups=groups, eras=eras)
        logging.debug(f"Eras  + {str(eras)}")
        return eras
    except Exception as e:
        logging.error(f"Cannot get eras Error: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Error while processing request of /get-eras ]")
