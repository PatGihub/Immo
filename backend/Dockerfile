# Multi-stage build for FastAPI backend
FROM python:3.11-slim as builder

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application code
COPY . .

# Copy .env.production as .env (for load_dotenv to find it)
# Using shell form to handle missing file gracefully
RUN if [ -f .env.production ]; then cp .env.production .env; fi

# Create logs directory
RUN mkdir -p logs

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Run the application on port 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
