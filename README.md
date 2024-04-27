# backend
The backend code serving the VictoryVault API.

# Project structure
`\alembic`: alembic migrations for automated database management

`\app\__init__.py`: defines init_app() used to start application with uvicorn

`\app\core\config.py`: configure environment variables for database connections

`\app\core\database.py`: define async database manager and helper function to provide async db sessions 

`\app\crud\user.py`: sqlalchemy database CRUD (Create, Read, Update, Delete) operations relating to user model

`\app\models\user.py`: SQLModels used by Pydantic and SQLAlchemy relating to user models

`\app\models\util.py`: generic SQLModels used by Pydantic and SQLAlchemy


# Environment setup (TODO: update)
`\requirements` contains two separate sets of pip requirements, those used during development, and those required to solely run the webapp

The following environment variables must be set:
```
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
DB_NAME
```

A PostgreSQL database is expected to be accessible locally (either directly installed and running, or through docker)

A connection to a PostgresQL database will be attempted at the specified address:
```python
f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
```

Alembic should be triggered to configure the database by calling: 
```
Alembic upgrade HEAD
```
### pytest_asyncio version specified as 0.21.1
As a result of the currently [known issue](https://pytest-asyncio.readthedocs.io/en/latest/reference/changelog.html) with creating session scoped event loops in pytest_asyncio 0.23, the version has been locked to 0.21 until this is resolved, to avoid warnings over deprecation.

A session scoped event loop is preferred over a module scoped one to avoid the need for recreating database connections multiple times during the testing procedure. This functionality has been deprecated in the latest version of pytest_asyncio however is currently being reviewed due to this exact usecase.

# Running webapp (TODO: update)
Calling `python -m main` from within `\backend` will start the webapp at `http:\\localhost:8080`.

The api docs can be accessed at `http:\\localhost:8080\docs` once the webapp has started.

# Running tests (TODO: update)
Ensure a different DB_NAME is specified as compared to the general dev DB, as the test DB will have all tables dropped before every test. A single database connection is used for all tests, but between each a new session is generated, and all tables are dropped before being recreated to ensure no cross contamination between tests. 

Calling `python -m pytest` from within `\backend` will trigger all tests. 

Current tests are not comprehensive, however showcase mocking the crud layer with monkeypatch to test API routes, testing solely the crud layer, and performing an integration test where multiple routes are called without mocking the db layer to ensure the outcome of each sequential call is as expected. 