# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the poetry configuration files
COPY pyproject.toml poetry.lock* /app/

# Install project dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy the rest of your application's code
COPY . /app

# Command to run the application
CMD ["uvicorn", "todo_core_apis.main:app", "--host", "0.0.0.0", "--port", "8000"]
