import requests
import re
import time

def fetch_playlist_url():
    idn = {
        "大连新闻综合": "tcb3IB5",
        "大连生活": "JzcFkF4",
        "大连文体": "hxT7Fc3",
        "大连影视": "8cuL6wa",
        "大连少儿": "q6tZ6Ba",
        "大连购物": "N4S4uAj",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    output_lines = [
        "# 这是本地源列表，一行一个源，格式为：频道名称,接口地址",
        "# 支持设置白名单：接口后添加$!",
        "# The local source list, one line per source, format: channel name, interface address",
        "# Support setting whitelist: add $! after the interface"
    ]
    for channel_name, channel_id in idn.items():
        url = f"https://dlyapp.dltv.cn/apiv4.5/api/m3u8_notoken?channelid={channel_id}"
        for attempt in range(3):  # 尝试三次
            try:
                response = requests.get(url, headers=headers, timeout=10)
                print(f"Response object for {channel_name}: {response}")
                print(f"Response status_code for {channel_name}: {response.status_code}")
                print(f"Response text for {channel_name}: {response.text}")
                if response.status_code == 200:
                    break
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch URL for {channel_name}: {url}, retrying...({attempt+1}/3)")
                print(f"Exception: {e}")
                time.sleep(5)
        else:
            print(f"Failed to fetch URL for {channel_name}: {url}，没有获取到状态码")
            output_lines.append(channel_name)
            continue
        info = response.text
        match = re.search(r'"address":"(.*?)"', info)
        if not match or match.group(1) == "":
            output_lines.append(channel_name)
            continue
        playlist_url = match.group(1).replace('\\/', '/')
        output_lines.append(f"{channel_name},{playlist_url}$!")

    with open("config/user_local.txt", "w") as file:
        file.write("\n".join(output_lines))

if __name__ == "__main__":
    fetch_playlist_url()
