#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : FastAPI main.py
"""
import logging
import os

import click
import uvicorn
import yaml
from fastapi import FastAPI, __version__ as fastapi_version
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.api_v1.routes import router


class Config(BaseModel):
    """FastApi config schema"""
    host: str
    port: int
    base_url: str
    api_v1_prefix: str
    loglevel: str
    environment: str
    allowed_cors_origins: list[str]


def read_config_yaml(file_path: str) -> Config:
    with open(file_path, 'r') as stream:
        config = yaml.safe_load(stream)

    return Config(**config)


# Get config as object
CONFIG = read_config_yaml(
    os.getenv(
        key="FAST_API_CONF",
        default=os.path.join(os.path.dirname(__file__), "config.yaml"),
    ))
print(CONFIG.model_dump())

# Production: https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/
app = FastAPI(title="FastAPI")
app.add_middleware(CORSMiddleware,
                   allow_origins=CONFIG.allowed_cors_origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"], )

# Add router
app.include_router(router=router, prefix=CONFIG.api_v1_prefix, tags=["v1"])


@app.get("/")
async def health():
    return "ok"


@app.get("/version")
async def version():
    return fastapi_version


if __name__ == "__main__":
    uvicorn.run("main:app",
                host=CONFIG.host,
                port=CONFIG.port,
                log_level=CONFIG.loglevel,
                reload=True if CONFIG.environment == 'dev' else False)
