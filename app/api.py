#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : FastAPI main.py
"""
import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pyroot import utils

# TODO: change prefix
router = APIRouter(
    prefix="/ppd-gui/api/v1",
    responses={404: {"description": "Not found"}},
)


class RootObj(BaseModel):
    """Post request schema to get ROOT object JSON"""
    file_path: str
    obj_path: str


@router.post("/get-plots")
async def get_plots(req: RootObj):
    """Get ROOT histogram in JSON format by providing its file and obj path
    """
    print("heyy", req)
    json_obj = utils.get_obj_json(file_path=req.file_path, obj_path=req.obj_path)
    if json_obj is None:
        HTTPException(status_code=400, detail="No Jessica token provided")

    return json.loads(json_obj)
