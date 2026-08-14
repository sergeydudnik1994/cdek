const fs = require('fs');
const https = require('https' );

// 1. Читаем sitemap.xml
const sitemap = fs.readFileSync('./sitemap.xml', 'utf8');
const urls = [...sitemap.matchAll(/<loc>(.*?)<\/loc>/g)].map(m => m[1]);

if (urls.length === 0) {
    console.log('URL не найдены в sitemap.xml');
    process.exit(1);
}

const host = "cdek-marketplace.ru";
const apiKey = "cdek-index-key"; // Ваш ключ из файла cdek-index-key.txt
const keyLocation = "https://cdek-marketplace.ru/cdek-index-key.txt";

// Яндекс принимает максимум 10 000 URL за один запрос.
// Разбиваем наши 71 000+ ссылок на части.
const chunks = [];
for (let i = 0; i < urls.length; i += 10000 ) {
    chunks.push(urls.slice(i, i + 10000));
}

console.log(`🚀 Найдено ${urls.length} URL. Начинаю отправку ${chunks.length} пачками...`);

async function sendChunk(urlList, index) {
    return new Promise((resolve, reject) => {
        const payload = JSON.stringify({
            host: host,
            key: apiKey,
            keyLocation: keyLocation,
            urlList: urlList
        });

        const options = {
            hostname: 'yandex.com',
            path: '/indexnow',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json; charset=utf-8',
                'Content-Length': Buffer.byteLength(payload)
            }
        };

        const req = https.request(options, (res ) => {
            console.log(`Пачка №${index + 1}: Статус ${res.statusCode}`);
            resolve();
        });

        req.on('error', (e) => {
            console.error(`Ошибка в пачке №${index + 1}:`, e.message);
            reject(e);
        });

        req.write(payload);
        req.end();
    });
}

async function main() {
    for (let i = 0; i < chunks.length; i++) {
        await sendChunk(chunks[i], i);
        // Небольшая пауза между запросами, чтобы не спамить API
        await new Promise(r => setTimeout(r, 1000));
    }
    console.log('✅ Все URL успешно отправлены в Яндекс!');
}

main().catch(console.error);
