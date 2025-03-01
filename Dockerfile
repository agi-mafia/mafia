# Use Python 3.10 image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install uv
RUN pip install --upgrade pip
RUN pip install uv

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies using uv with --system flag
RUN uv pip install --system --no-cache-dir -r requirements.txt

# Expose port (adjust as needed)
EXPOSE 8000

# For development, we don't copy the code at build time
# Instead, we'll mount the code as a volume when running the container

# Command to run the FastAPI application with uvicorn's reload flag
# This will automatically restart the server when code changes are detected
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]