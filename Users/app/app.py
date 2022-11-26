import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from alembic.config import Config
from alembic import command
from retrying_async import retry

from app.routers import router as api_router
from app.core.config import config
from app.core.exceptions import CustomException


app = FastAPI(root_path=config.ROOT_PATH)


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content={"error_code": exc.error_code, "message": exc.message},
    )


@retry(attempts=5, delay=3)
async def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", config.DB_URL)
    command.upgrade(alembic_cfg, "head")


@app.on_event("startup")
async def startup():
    logging.basicConfig(
        level=logging.getLevelName(config.LOGGING_LEVEL),
        format="[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d].[%(funcName)s()]: %(message)s",
    )

    if config.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in config.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    await run_migrations()


@app.on_event("shutdown")
async def shutdown():
    ...


app.include_router(api_router, prefix=config.API_PREFIX)
