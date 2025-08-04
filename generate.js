const fs = require('fs');
const https = require('https');

const url = 'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5.txt';

https.get(url, (res) => {
  let data = '';

  res.on('data', chunk => {
    data += chunk;
  });

  res.on('end', () => {
    const lines = data.trim().split('\n').slice(0, 20);
    const proxies = lines.map((line, index) => {
      const [ip, port] = line.trim().split(':');
      return {
        name: `JS${index + 1}`,
        type: 'socks5',
        server: ip,
        port: parseInt(port),
        udp: false
      };
    });

    const config = { proxies };
    const yaml = `proxies:\n${proxies.map(p =>
      `  - name: "${p.name}"\n    type: ${p.type}\n    server: ${p.server}\n    port: ${p.port}\n    udp: ${p.udp}`
    ).join('\n')}`;

    fs.writeFileSync('proxies-node.yaml', yaml, 'utf8');
    console.log('proxies-node.yaml 已生成');
  });
}).on('error', (err) => {
  console.error('错误:', err.message);
});
