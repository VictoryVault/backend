import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel


class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    # allow database connection to be separately initialized
    # such that the app can start and then have the database
    # be configured separately. Vital for clean interaction
    # with database janitor for test cleanup
    def init(self, host: str):
        self._engine = create_async_engine(host)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    # used for graceful database connection closure after tests complete
    # or when app shuts down
    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    # keep handling of connection contexts clean
    # used when connection is made e.g.
    # async with sessionmanager.connect() as connection:
    # this ensures that all the code before yield runs to 
    # create the connection setup, and if something should go
    # wrong within the context, the connection is rolled back
    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    # keep handling of session contexts clean, used in get_db bellow
    # this ensures that all the code before yield runs to 
    # create the session to be used, and if something should go
    # wrong within the context, the session is correctly rolled back
    # before being closed 
    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # SQLAlchemy functions to create/drop all tables defined by SQLModels in the connected database
    # only to be used during testing, as permament databases should have their tables created/updated
    # through migrations (handled by Alembic)
    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(SQLModel.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(SQLModel.metadata.drop_all)


sessionmanager = DatabaseSessionManager()


# passed as a dependency to any FastAPI routes that will require a DB session
# this guarantees each call of a route gets it's own async independant DB session
# that is governed by the context manager code above for error/exception handling
async def get_db() -> AsyncIterator[AsyncSession]:
    async with sessionmanager.session() as session:
        yield session
