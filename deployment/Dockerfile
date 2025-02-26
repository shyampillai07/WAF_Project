# Use official Python image as base
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . .

# Expose the port your Flask app runs on
EXPOSE 5000

# Command to run the app using Gunicorn
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]