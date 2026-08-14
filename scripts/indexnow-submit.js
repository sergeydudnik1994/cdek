const fs = require('fs');
const https = require('https' );

if (!fs.existsSync('./sitemap.xml')) { process.exit(1); }
const sitemap = fs.readFileSync('./sitemap.xml', 'utf8');
const urls = [...sitemap.matchAll(/<loc>(.*?)<\/loc>/g)].map(m => m[1]);

const host = "cdek-marketplace.ru";
const apiKey = "cdek-index-key";
const keyLocation = `https://${host}/cdek-index-key.txt`;

const chunks = [];
for (let i = 0; i < urls.length; i += 10000 ) {
    chunks.push(urls.slice(i, i + 10000));
}

async function send(urlList, index) {
    return new Promise((resolve) => {
        const payload = JSON.stringify({ host, key: apiKey, keyLocation, urlList });
        const req = https.request({
            hostname: 'api.indexnow.org',
            path: '/indexnow',
            method: 'POST',
            headers: { 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': Buffer.byteLength(payload ) }
        }, (res) => {
            console.log(`Пачка №${index + 1}: Статус ${res.statusCode}`);
            resolve();
        });
        req.on('error', (e) => { resolve(); });
        req.write(payload);
        req.end();
    });
}

async function main() {
    console.log(`🚀 Найдено ${urls.length} URL. Отправка...`);
    for (let i = 0; i < chunks.length; i++) {
        await send(chunks[i], i);
        await new Promise(r => setTimeout(r, 2000));
    }
    console.log('✅ Готово!');
}
main();
