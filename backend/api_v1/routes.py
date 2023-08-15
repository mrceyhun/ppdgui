#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : FastAPI main.py
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.client import pyroot


class RootObj(BaseModel):
    """Post request schema to get ROOT object JSON"""
    file_path: str
    obj_path: str


# ----------------------------------------------------------------------------

# TODO: change prefix
router = APIRouter()


@router.post("/get-plots")
async def get_plots(req: RootObj):
    """Get ROOT histogram in JSON format by providing its file and obj path
    """
    try:
        return pyroot.get_obj_json(file_path=req.file_path, obj_path=req.obj_path)
    except Exception as e:
        return HTTPException(status_code=400, detail="Cannot read file, err: " + str(e))
