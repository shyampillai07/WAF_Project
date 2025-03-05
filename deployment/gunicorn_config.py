import multiprocessing

bind = "0.0.0.0:5000"  # Binds to all interfaces on port 5000
workers = multiprocessing.cpu_count() * 2 + 1  # Dynamically set workers
threads = 4  # Number of threads per worker
timeout = 120  # Kill workers if unresponsive for 120 seconds
keepalive = 10  # Keep connections open for 10 seconds
errorlog = "-"  # Log errors to standard output
accesslog = "-"  # Log requests to standard output
loglevel = "info"  # Log level (debug, info, warning, error, critical)
preload_app = True  # Preload app to reduce memory usage

# Graceful restarts to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50