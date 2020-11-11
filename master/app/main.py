import logging
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from app.api import router
from app.costum_logging import CustomizeLogger

logger = logging.getLogger(__name__)

config_path = Path(__file__).with_name("logging_config.json")


def create_app() -> FastAPI:
    app = FastAPI(title='Master App log', debug=False)
    logger = CustomizeLogger.make_logger(config_path)
    app.logger = logger
    app.include_router(router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
