import requests
import uuid
import threading
import time

# 下载速度阈值：50KB/s
SPEED_THRESHOLD = 50 * 1024  
SPEED_CHECK_DELAY = 3  # 秒

# 全局流量统计
total_downloaded = 0
total_downloaded_lock = threading.Lock()
stop_event = threading.Event()

def generate_download_url(host, size=25_000_000):
    uid = str(uuid.uuid4())
    return f"http://{host}/download?nocache={uid}&size={size}&guid={uid}"

def download_thread(url):
    global total_downloaded
    while not stop_event.is_set():
        try:
            start_time = time.time()
            r = requests.get(url, stream=True, timeout=10)
            r.raise_for_status()
            downloaded = 0
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    downloaded += len(chunk)
                    elapsed = time.time() - start_time
                    if elapsed > SPEED_CHECK_DELAY:
                        speed = downloaded / elapsed
                        if speed < SPEED_THRESHOLD:
                            r.close()
                            break  # 重启线程
                    # 更新全局流量
                    with total_downloaded_lock:
                        total_downloaded += len(chunk)
                    if stop_event.is_set():
                        r.close()
                        break
            r.close()
        except Exception:
            time.sleep(0.1)

def start_downloads(links, total_threads):
    num_links = len(links)
    if num_links == 0:
        print("没有获取到下载链接，无法启动线程")
        return []
    threads_per_link = max(1, total_threads // num_links)
    print(f"总线程数: {total_threads}，下载链接数: {num_links}，每个链接线程数: {threads_per_link}")
    threads = []
    for url in links:
        for i in range(threads_per_link):
            t = threading.Thread(target=download_thread, args=(url,), daemon=True)
            t.start()
            threads.append(t)
    return threads

def human_readable(size_bytes):
    if size_bytes >= 1<<30:
        return f"{size_bytes/(1<<30):.2f} GB"
    elif size_bytes >= 1<<20:
        return f"{size_bytes/(1<<20):.2f} MB"
    elif size_bytes >= 1<<10:
        return f"{size_bytes/(1<<10):.2f} KB"
    else:
        return f"{size_bytes} B"

if __name__ == "__main__":
    # 输入总流量和总线程数
    total_limit_gb = float(input("请输入本次跑多少流量(GB): "))
    total_threads = int(input("请输入总线程数: "))
    total_limit_bytes = total_limit_gb * (1<<30)

    # 获取Speedtest节点host
    api_url = "https://www.speedtest.net/api/js/servers?engine=js"
    servers = requests.get(api_url, timeout=10).json()

    download_links = []
    print("获取到以下下载节点信息:")
    for s in servers:
        host = s['host']
        country = s.get('country', '未知国家')
        download_links.append(generate_download_url(host))
        print(f"- {host} [\033[31m{country}\033[0m]")  # 红色显示国家


    # 启动线程
    threads = start_downloads(download_links, total_threads)

    prev_total = 0
    try:
        while not stop_event.is_set():
            time.sleep(1)
            with total_downloaded_lock:
                consumed = total_downloaded
            speed = consumed - prev_total
            prev_total = consumed
            print(f"\r已消耗流量: {human_readable(consumed)} | 实时速率: {human_readable(speed)}/s", end="")
            if consumed >= total_limit_bytes:
                print("\n已达到总流量限制，脚本自动终止。")
                stop_event.set()
                break
    except KeyboardInterrupt:
        stop_event.set()
