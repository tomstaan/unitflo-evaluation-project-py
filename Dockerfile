# Use the official lightweight Python image.
FROM python:3.8-slim

# Set the working directory.
WORKDIR /app

# Copy the requirements file into the image.
COPY requirements.txt .

# Install dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Install additional tools needed for testing and mutation testing.
RUN pip install --no-cache-dir pytest mutmut coverage flake8

# Copy the rest of the application code.
COPY . .

# Ensure the pyproject.toml is included.
COPY pyproject.toml .

# Set the entry point to the evaluation script.
ENTRYPOINT ["python", "evaluate_tests.py"]
