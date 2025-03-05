# Stage 1: Build dependencies
FROM python:3.12 AS builder

WORKDIR /app

# Copy only requirements first (optimizes Docker caching)
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final lightweight image
FROM python:3.12-slim AS final

WORKDIR /app

# Create a non-root user for better security
RUN useradd -m appuser
USER appuser

# Copy dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

# Copy the project files
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the app using Gunicorn
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]