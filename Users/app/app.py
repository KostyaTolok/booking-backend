from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from alembic.config import Config
from alembic import command
from retry import retry

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


if config.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in config.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@retry(Exception, tries=5, delay=3)
def run_migrations():
    alembic_cfg = Config('alembic.ini')
    command.upgrade(alembic_cfg, 'head')


run_migrations()

app.include_router(api_router, prefix=config.API_PREFIX)
