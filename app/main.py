from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import config
from app.core.database import sessionmanager
from app.api.v1.user import router as user_router


def init_app(init_db=True):
    lifespan = None

    # make DB initialization optional, to support configuring database
    # after startup for testing purposes
    if init_db:
        sessionmanager.init(config.DB_CONFIG)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    # lifespan gracefully handles closing the DB connection on app shutdown
    server = FastAPI(title="FastAPI server", lifespan=lifespan)

    # add routers to app (adding /api prefix to router path)
    server.include_router(user_router, prefix="/api")

    return server