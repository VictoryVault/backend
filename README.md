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

# Alembic overview
Alembic provides for the creation, management, and invocation of change management scripts for a relational database, using SQLAlchemy as the underlying engine.

Usage of Alembic starts with creation of the Migration Environment. This is a directory of scripts that is specific to a particular application. The migration environment is created just once, and is then maintained along with the application’s source code itself. The environment is created using the init command of Alembic, and is then customizable to suit the specific needs of the application.

Creating migration environment and running migrations: [docs](https://alembic.sqlalchemy.org/en/latest/tutorial.html)


# SQLModel, SQLALchemy, Pydantic
A lot of the groundwork for the FastAPI database handling was taken from this excellent [blog](https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html). 

SQLAlchemy is absolute wizardry. It serves as the ORM for the project, handling the layer between Python and the SQL database. It is well integrated with FastAPI and allows for incredibly powerful declarative model based python definitions to govern the database structure and operations. An overview of using it with FastAPI can be found [here](https://fastapi.tiangolo.com/tutorial/sql-databases/). A full explanation for SQLAlchemy can be found in their [docs](https://docs.sqlalchemy.org/en/20/tutorial/index.html). 

Pydantic provides type validation in Python, and is especially useful when passing complicated datatypes around. [Docs](https://docs.pydantic.dev/latest/)

SQLModel is used as it incorporates both Pydantic for enforcing types in Python and SQLAlchemy declarative models, allowing for the same declarative structures to be used in both. [Docs](https://sqlmodel.tiangolo.com/).  

# Testing framework
Pytest is used for testing, with pytest_async ensuring async testing of all async functions. 

Pytest_postgresql provides a database janitor for PostgreSQL to ensure a new testdb is created for the testing run that does not risk overwriting anything with the DB, and cleans up once the run completes regardless of outcome.


### Fixtures
Setup for testing environment to create database and API testing client, handle cleanup and ensure no test can affect other tests

### Conftest.py
Used by pytest to import fixtures into the testing session

### Integration
Used for calling multiple endpoints in the same context to check expected behaviour and interaction between sequential calls of specific endpoints (e.g. create a new user and then check the user can be retrieved)

### Unit\crud
Unit testing database operations

### Unit\routes
Unit testing API endpoints. Monkeypatch is used to overwrite CRUD functions called by endpoints with custom mock
functions to ensure isolated testing of functionality within the endpoint function itself. Monkeypatch overview [here](https://pytest-with-eric.com/mocking/pytest-monkeypatch/), docs [here](https://docs.pytest.org/en/latest/how-to/monkeypatch.html). 

# Environment setup (TODO: update)
Python version 3.12 is being used 

[Poetry](https://python-poetry.org/docs/) is used for package management within this project, with poetry.lock and pyproject.toml provided.

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
Calling `python -m main` from within `\backend` will start the webapp at `http://localhost:8080`.

The api docs can be accessed at `http://localhost:8080\docs` once the webapp has started.

# Running tests (TODO: update)
Ensure a different DB_NAME is specified as compared to the general dev DB, as the test DB will have all tables dropped before every test. A single database connection is used for all tests, but between each a new session is generated, and all tables are dropped before being recreated to ensure no cross contamination between tests. 

Calling `python -m pytest` from within `\backend` will trigger all tests. 

Current tests are not comprehensive, however showcase mocking the crud layer with monkeypatch to test API routes, testing solely the crud layer, and performing an integration test where multiple routes are called without mocking the db layer to ensure the outcome of each sequential call is as expected. 