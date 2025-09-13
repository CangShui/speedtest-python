# Multi-Threaded Speedtest Downloader

A Python script to perform high-speed downloads from multiple Speedtest servers using multiple threads per server. It includes features like automatic thread restart on slow connections and total traffic limit enforcement.

## Features

* Download from multiple Speedtest servers simultaneously.
* Configurable total number of threads.
* Automatic thread restart if download speed drops below a threshold (50 KB/s by default).
* Tracks total data usage and stops automatically when a user-specified traffic limit (GB) is reached.
* Displays all download servers at startup, with countries highlighted in red.
* Real-time display of downloaded traffic and instantaneous speed (refreshed every second).

## Requirements

* Python 3.11+
* `requests` library

### Installing dependencies

```bash
# Using pip in a virtual environment
python3 -m venv venv
source venv/bin/activate
pip install requests
```

> **Note:** Installing packages system-wide on Debian/Ubuntu may require using `apt` or `pipx`.

## Usage

1. Clone or download the script to your local machine.
2. Run the script:

```bash
python3 speedtest_downloader.py
```

3. Enter the following when prompted:

* **Total traffic limit** in GB (e.g., `10` for 10 GB)
* **Total number of threads** (e.g., `80`)

4. The script will fetch available Speedtest servers and display each server’s host and country in red.
5. Downloads will start automatically. The script will show real-time traffic and speed:

```
Downloaded: 1.23 GB | Instant speed: 12.4 MB/s
```

6. When the total downloaded traffic reaches the limit, the script will automatically stop.

## Output Format

All download servers are displayed in the following format:

```
- speedtest11.hotspot.koeln.prod.hosts.ooklaserver.net:8080 [Germany]
```

## Configuration

You can adjust:

* **Speed threshold** for restarting slow threads by editing `SPEED_THRESHOLD` in the script (default: 50 KB/s)
* **Speed check delay** in seconds (`SPEED_CHECK_DELAY`, default: 3s)

## Notes

* Make sure your internet connection can handle the number of threads you configure. Using too many threads may cause network congestion or local performance issues.
* The script uses `requests` for HTTP downloads. It does not split individual files; each thread downloads the entire file independently.

## License

MIT License. Free to use and modify.
