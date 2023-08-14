#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : FastAPI main.py
"""

from fastapi import FastAPI, APIRouter, HTTPException, __version__
from .api import router

app = FastAPI()
app.include_router(router)


@app.get("/")
def health():
    return "ok"


@app.get("/version")
def version():
    return __version__
