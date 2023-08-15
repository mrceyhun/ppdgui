#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : FastAPI main.py
"""
import click
from fastapi import FastAPI, __version__ as fastapi_version
import uvicorn

from backend.api_v1.routes import router

BASE_API_V1_PREFIX = "/ppd-gui/api/v1"


def init_app(title, docs_url, openapi_url) -> FastAPI:
    """Initialise a FastApi app, with all the required routes and the"""
    app_ = FastAPI(title=title,
                   docs_url=docs_url,
                   openapi_url=openapi_url)

    app_.include_router(router=router,
                        prefix=BASE_API_V1_PREFIX,
                        tags=["v1"])
    return app_


app = init_app(title="FastAPI", docs_url="/api/docs", openapi_url="/api")


@app.get("/")
async def health():
    return "ok"


@app.get("/version")
async def version():
    return fastapi_version


@click.command()
@click.option("--host", "-h", type=str, default="0.0.0.0", required=False)
@click.option("--port", "-p", type=int, default=8080, required=False)
@click.option("--reload", is_flag=True, show_default=True, default=False, help="Reload on code change")
def main(host, port, reload):
    click.echo('''    
   _____   ____  _____ ______   ____  ____ ____ 
|     | /    |/ ___/|      | /    ||    \    |
|   __||  o  (   \_ |      ||  o  ||  o  )  | 
|  |_  |     |\__  ||_|  |_||     ||   _/|  | 
|   _] |  _  |/  \ |  |  |  |  _  ||  |  |  | 
|  |   |  |  |\    |  |  |  |  |  ||  |  |  | 
|__|   |__|__| \___|  |__|  |__|__||__| |____|                                            
''')
    uvicorn.run("main:app",
                host=host,
                reload=reload,
                port=port)


if __name__ == "__main__":
    main()
