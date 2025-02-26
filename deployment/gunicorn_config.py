# gunicorn_config.py

bind = "0.0.0.0:5000"  # Binds to all interfaces on port 5000
workers = 4  # Number of worker processes (adjust based on CPU cores)
threads = 2  # Number of threads per worker (for handling multiple requests)
timeout = 120  # Kill workers if unresponsive for 120 seconds
keepalive = 5  # Keep connections open for 5 seconds
errorlog = "-"  # Log errors to standard output
accesslog = "-"  # Log requests to standard output
loglevel = "info"  # Log level (debug, info, warning, error, critical)
preload_app = True  # Preload app to reduce memory usage