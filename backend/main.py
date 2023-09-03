#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : FastAPI main.py
"""
import uvicorn
from fastapi import FastAPI, __version__ as fastapi_version
from fastapi.middleware.cors import CORSMiddleware

from api_v1.routes import router
from config import get_config

# Get config as object
CONFIG = get_config()
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
