from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pathlib import Path

from app.routers import bill
from app.routers.bill import (
    router as bills_router
)

app = FastAPI(
    title="Split The Bill API",
    description="Extract restaurant bills from photographs and split costs fairly",
    version="1.0.0"
)


# Project directories

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


FRONTEND_DIR = (
    BASE_DIR /
    "frontend"
)


# Static files

app.mount(
    "/static",
    StaticFiles(
        directory=FRONTEND_DIR
    ),
    name="static"
)


# Include routers

app.include_router(
    bill.router
)


# Home

@app.get("/")
def serve_home():

    return FileResponse(
        FRONTEND_DIR /
        "index.html"
    )


# Health

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }