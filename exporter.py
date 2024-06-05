import os
from argparse import ArgumentParser
from prometheus_client import start_http_server, Gauge
import time

# Configuration (replace with your actual path)
PINS_DIR = "/srv/cryptpad/data/pins/"
PORT = 8000

# Prometheus metric
registered_users_gauge = Gauge(
    "cryptpad_registered_users", "Number of registered users"
)


def count_registered_users(pins_dir: os.PathLike = PINS_DIR) -> int:
    f"""Returns the number of registered users by counting the number of folders in the user data directory

    This emulates the way CryptPad counts registered users in the admin dashboard, see:
    https://github.com/cryptpad/cryptpad/blob/7dbec1bd25b46e514ba82adad209961627410025/lib/commands/admin-rpc.js#L105

    Args:
        pins_dir (os.PathLike): Path to the user pins directory (default: {PINS_DIR})

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


def update_metrics(pins_dir: os.PathLike = PINS_DIR):
    f"""Update the Prometheus metrics with the current number of registered users

    Args:
        pins_dir (os.PathLike, optional): Path to the user pins directory (default: {PINS_DIR})
    """
    user_count = count_registered_users(pins_dir)
    registered_users_gauge.set(user_count)
    print(f"Updated registered users count: {user_count}")


def main():
    parser = ArgumentParser(description="CryptPad Prometheus exporter")
    parser.add_argument(
        "--pins-dir",
        type=str,
        default=PINS_DIR,
        help=f"Path to the user pins directory (default: {PINS_DIR})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=PORT,
        help=f"Port to expose the Prometheus metrics (default: {PORT})",
    )
    args = parser.parse_args()

    pins_dir = args.pins_dir or os.environ.get("PINS_DIR") or PINS_DIR
    port = int(args.port or os.environ.get("PORT") or PORT)

    # Start up the server to expose the metrics.
    start_http_server(port)
    print("Prometheus exporter started on port " + port)

    # Update metrics every 30 seconds
    while True:
        update_metrics(pins_dir)
        time.sleep(30)


if __name__ == "__main__":
    main()
