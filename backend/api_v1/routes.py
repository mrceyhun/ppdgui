#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : FastAPI main.py
"""
import logging
from fastapi import APIRouter, HTTPException

from backend.api_v1.models import RequestRootObj
from backend.client import pyroot

# ----------------------------------------------------------------------------

# TODO: change prefix
router = APIRouter()


@router.post("/get-root-hist-or-dirs")
async def get_root_dirs_or_hist(req: RequestRootObj):
    """Get ROOT histogram in JSON format by providing its file and obj path
    """
    logging.info("Request:get-root-obj-or-dirs " + str(req))
    try:
        return pyroot.get_root_dirs_or_hist(tfile=req.file_path, tobject=req.obj_path, all_hists=req.all_hists)
    except Exception as e:
        logging.error(f"Cannot process request. Incoming=> file{req.file_path}, obj:{req.obj_path} . Error: {str(e)}")
        raise HTTPException(status_code=404, detail="Cannot read file, err: " + str(e))
