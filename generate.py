import requests
import yaml
import re

# 下载 SOCKS5 列表
url = 'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5.txt'
response = requests.get(url)
if response.status_code != 200:
    print("无法获取代理列表")
    exit(1)

lines = response.text.strip().splitlines()

# 正则提取 IP:PORT
proxies = []
for line in lines:
    match = re.search(r'(\d+\.\d+\.\d+\.\d+:\d+)', line)
    if match:
        proxies.append(match.group(1))

# 构造 Clash 配置
proxy_list = []
for i, proxy in enumerate(proxies):
    host, port = proxy.split(":")
    proxy_list.append({
        "name": f"socks5-{i+1}",
        "type": "socks5",
        "server": host,
        "port": int(port),
        "udp": True
    })

clash_config = {
    "port": 7890,
    "socks-port": 7891,
    "allow-lan": True,
    "mode": "Rule",
    "proxies": proxy_list,
    "proxy-groups": [
        {
            "name": "auto",
            "type": "url-test",
            "proxies": [p["name"] for p in proxy_list],
            "url": "http://www.gstatic.com/generate_204",
            "interval": 300
        }
    ],
    "rules": [
        "MATCH,auto"
    ]
}

# 写入 YAML 文件
with open("proxy.yaml", "w", encoding="utf-8") as f:
    yaml.dump(clash_config, f, allow_unicode=True)
