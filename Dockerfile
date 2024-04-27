# Use an official Python runtime as a parent image
FROM python:3.12.2-slim-bookworm

# Set the working directory in the container to /app
WORKDIR /backend

# Install poetry and disable virtual envs
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Copy only the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry install --only main

# Add the current directory contents into the container at /app
COPY ./app app
COPY ./run.py run.py

# set environment variables for DB connection
ENV DB_USER=$DB_USER
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_HOST=$DB_HOST
ENV DB_PORT=$DB_PORT
ENV DB_NAME=$DB_NAME

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the command to start uvicorn
CMD ["poetry", "run", "python", "run.py"]