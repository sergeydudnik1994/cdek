const fs = require('fs');
const https = require('https' );

if (!fs.existsSync('./all_urls.txt')) {
    console.error('❌ Файл all_urls.txt не найден!');
    process.exit(1);
}

const urls = fs.readFileSync('./all_urls.txt', 'utf8').split('\n').filter(u => u.trim() !== '');
const host = "cdek-marketplace.ru";
const apiKey = "Aa1234567";
const keyLocation = `https://${host}/${apiKey}.txt`;

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
