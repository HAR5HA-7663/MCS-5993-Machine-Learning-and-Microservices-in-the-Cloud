FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY ./app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app /app

# Create storage directories
RUN mkdir -p /app/storage/resumes /app/storage/application_resumes

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
