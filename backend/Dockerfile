# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set a working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your backend code
COPY . .

# Default command: run setup, then start the FastAPI server
CMD ["sh", "-c", "python mongo_setup.py && uvicorn api.main:app --host 0.0.0.0 --port 8000"]
