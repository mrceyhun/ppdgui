#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : FastAPI main.py
"""
import click
from fastapi import FastAPI, __version__ as fastapi_version
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.api_v1.routes import router


origins = [
    "http://localhost:5173",
    "https://localhost:80",
    "http://localhost",
    "http://localhost:8080",
]

@click.command()
@click.option("--host", "-h", type=str, default="0.0.0.0", required=False)
@click.option("--port", "-p", type=int, default=80, required=False)
@click.option("--base_url", "-u", type=str, default="/ppdgui/api", required=False)
@click.option("--reload", "-r", is_flag=True, show_default=True, default=False, help="Reload on code change")
def main(host, port, base_url, reload):
    click.echo('''Fast API''')
    # Production: https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/
    app = FastAPI(title="FastAPI")
    app.add_middleware(
    CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router=router,
                       prefix="/api/v1",
                       tags=["v1"])

    @app.get("/")
    async def health():
        return "ok"

    @app.get("/version")
    async def version():
        return fastapi_version

    print(base_url)
    uvicorn.run(
        app,
        port=port,
        host=host,
        reload=reload,
    )


if __name__ == "__main__":
    main()
