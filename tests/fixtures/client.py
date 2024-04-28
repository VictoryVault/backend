import asyncio
from contextlib import ExitStack
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from pytest_postgresql.janitor import DatabaseJanitor
from app.main import init_app
from app.core.database import get_db, sessionmanager
from app.core.config import config


# session scoped event loop, required to not need to 
# rescreate the database connection each test
@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# unique app instance created for each test with appropriate cleanup once finished
@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield init_app(init_db=False)


# unique async client for each test that requires it, uses the unique app instance 
# TODO: set app HOST and PORT to be configurable
@pytest_asyncio.fixture
async def client(app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://0.0.0.0:80",
    ) as c:
        yield c


# create session scoped database connection, uses DatabaseJanitor context such that
# a new database is created at the start of the session, and it will crash if database 
# with specified name already exists. This database is cleaned up and deleted once the 
# session ends 
@pytest_asyncio.fixture(scope="session", autouse=True)
async def connection_test():
    with DatabaseJanitor(
        user=config.DB_USER,
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        version="16.2",
        password=config.DB_PASSWORD,
    ):
        connection_str = config.DB_CONFIG
        sessionmanager.init(connection_str)
        yield
        await sessionmanager.close()


# uncomment if testing creates custom sessionmanager, currently connection_test
# initializes global sessionmanager with testing DB within janitor
# @pytest_asyncio.fixture(scope="function", autouse=False)
# async def session_override(app, connection_test):
#     async def get_db_override():
#         print("override")
#         async with sessionmanager.session() as session:
#             yield session

#     app.dependency_overrides[get_db] = get_db_override


# used to reset the contents of the database between each test to avoid
# one test contaminating the environment of another
# fixture is specified simply to enforce it only starting once 
# the connection_test fixture has completed
@pytest_asyncio.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)


# provide each test with a unique database session created from the same connection
# fixture is specified simply to enforce it only starting once 
# the connection_test fixture has completed
@pytest_asyncio.fixture(scope="function")
async def db_session(connection_test) -> AsyncIterator[AsyncSession]:
    async with sessionmanager.session() as session:
        yield session
