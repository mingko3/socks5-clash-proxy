import requests
import yaml

url = "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5.txt"
response = requests.get(url)
lines = response.text.strip().split('\n')

clash_proxies = []
for index, line in enumerate(lines[:20]):
    ip, port = line.strip().split(':')
    proxy = {
        'name': f"S5_{index + 1}",
        'type': 'socks5',
        'server': ip,
        'port': int(port),
        'udp': False
    }
    clash_proxies.append(proxy)

config = {'proxies': clash_proxies}

with open('proxies.yaml', 'w') as f:
    yaml.dump(config, f, allow_unicode=True)
