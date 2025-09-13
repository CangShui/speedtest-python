# Multi-Threaded Speedtest Downloader

![screen](https://i.imgur.com/z4HFOsX.png)



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

