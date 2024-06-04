import os
from prometheus_client import start_http_server, Gauge
import time

# Configuration (replace with your actual path)
PINS_DIR = '/srv/cryptpad/data/pins/'
PORT = 8000

# Prometheus metric
registered_users_gauge = Gauge('cryptpad_registered_users', 'Number of registered users')

def count_registered_users(pins_dir: os.PathLike) -> int:
    """Returns the number of registered users by counting the number of folders in the user data directory

    This emulates the way CryptPad counts registered users in the admin dashboard, see: 
    https://github.com/cryptpad/cryptpad/blob/7dbec1bd25b46e514ba82adad209961627410025/lib/commands/admin-rpc.js#L105

    Args:
        pins_dir (os.PathLike): Path to the user pins directory (e.g. /srv/cryptpad/data/pins/)

    Returns:
        int: Number of registered users
    """

    try:
        users_count = 0
        for folder in os.listdir(pins_dir):
            folder_path = os.path.join(pins_dir, folder)
            if os.path.isdir(folder_path):
                users_count += len(os.listdir(folder_path))
        return users_count
    except Exception as e:
        print(f"Error counting registered users: {e}")
        return 0

def update_metrics():
    """Update the Prometheus metrics with the current number of registered users"""
    user_count = count_registered_users(PINS_DIR)
    registered_users_gauge.set(user_count)
    print(f"Updated registered users count: {user_count}")

def main():
    # Start up the server to expose the metrics.
    start_http_server(PORT)
    print("Prometheus exporter started on port " + PORT)

    # Update metrics every 30 seconds
    while True:
        update_metrics()
        time.sleep(30)


if __name__ == '__main__':
    main()
