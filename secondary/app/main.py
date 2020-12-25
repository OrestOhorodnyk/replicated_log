import logging

import uvicorn
from fastapi import FastAPI

from app.api import router
from app.logger.costum_logging import CustomizeLogger

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(title='Secondary App log', debug=False)
    logger = CustomizeLogger.make_logger()
    app.logger = logger
    app.include_router(router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
