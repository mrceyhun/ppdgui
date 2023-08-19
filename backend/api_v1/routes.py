#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : FastAPI main.py
"""
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.client import pyroot


class RootObj(BaseModel):
    """Post request schema to get ROOT object JSON"""
    file_path: str
    obj_path: str

class RootObj(BaseModel):
    """Post request schema to get ROOT object JSON"""
    obj_paths: list[str]


# ----------------------------------------------------------------------------

# TODO: change prefix
router = APIRouter()


@router.post("/get-root-obj")
async def get_root_obj(req: RootObj):
    """Get ROOT histogram in JSON format by providing its file and obj path
    """
    logging.warn("Request:get_root_obj "+str(req))
    try:
        return pyroot.get_root_obj_as_json(file_path=req.file_path, obj_path=req.obj_path)
    except Exception as e:
        return HTTPException(status_code=400, detail="Cannot read file, err: " + str(e))

@router.get("/get-json-file")
async def get_json_file(q: str):
    """Get JSON file content
    """
    logging.warn("Request:get_json_file "+str(q) + str())
    try:
        return pyroot.get_json_file(file_path=q)
    except Exception as e:
        return HTTPException(status_code=400, detail="Cannot read file, err: " + str(e))


@router.post("/get-json-files")
async def get_json_files(q: list[str]):
    """Get ROOT histogram in JSON format by providing its file and obj path
    """
    logging.warn("Request:get_json_files "+str(q))
    try:
        return pyroot.get_json_files(file_paths=q)
    except Exception as e:
        return HTTPException(status_code=400, detail="Cannot read file, err: " + str(e))


