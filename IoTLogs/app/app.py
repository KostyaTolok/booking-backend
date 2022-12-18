from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import config
from app.core.exceptions import CustomException
from app.routers import router

app = FastAPI(root_path=config.ROOT_PATH)


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content={"detail": exc.message},
    )


app.include_router(router, prefix=config.API_PREFIX)
