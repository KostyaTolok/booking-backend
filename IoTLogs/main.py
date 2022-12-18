import uvicorn

from app.core.config import config


if __name__ == "__main__":
    uvicorn.run(
        app="app.app:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=False,
        workers=1,
    )
