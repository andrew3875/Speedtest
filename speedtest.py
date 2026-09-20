import argparse
import time

import requests


REQUESTS_COUNT = 10
TIMEOUT = 30


def measure_speed(url):
    total_time = 0
    total_bytes = 0
    successful_requests = 0

    for i in range(REQUESTS_COUNT):
        try:
            start_time = time.perf_counter()

            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()

            data_size = len(response.content)

            elapsed = time.perf_counter() - start_time

            total_time += elapsed
            total_bytes += data_size
            successful_requests += 1

            speed = data_size / elapsed / (1024 * 1024)

            print(
                f"Request {i + 1}: "
                f"{elapsed:.3f} s, "
                f"{data_size / (1024 * 1024):.2f} MB, "
                f"{speed:.2f} MB/s"
            )

        except requests.RequestException as error:
            print(f"Request {i + 1}: error - {error}")

    if successful_requests == 0:
        print("No successful requests.")
        return

    average_time = total_time / successful_requests
    average_speed = total_bytes / total_time / (1024 * 1024)

    print("\nResults:")
    print(f"Successful requests: {successful_requests}/{REQUESTS_COUNT}")
    print(f"Average request time: {average_time:.3f} s")
    print(f"Downloaded data: {total_bytes / (1024 * 1024):.2f} MB")
    print(f"Average speed: {average_speed:.2f} MB/s")


def main():
    parser = argparse.ArgumentParser(
        description="Measure internet download speed"
    )
    parser.add_argument(
        "url",
        help="URL of a large file to download"
    )

    args = parser.parse_args()

    measure_speed(args.url)


if __name__ == "__main__":
    main()