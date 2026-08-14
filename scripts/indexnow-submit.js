const fs = require('fs');
const https = require('https' );

// 1. Читаем карту сайта
if (!fs.existsSync('./sitemap.xml')) {
    console.error('❌ Файл sitemap.xml не найден!');
    process.exit(1);
}

const sitemap = fs.readFileSync('./sitemap.xml', 'utf8');
const urls = [...sitemap.matchAll(/<loc>(.*?)<\/loc>/g)].map(m => m[1]);

if (urls.length === 0) {
    console.error('❌ URL не найдены в sitemap.xml');
    process.exit(1);
}

const host = "cdek-marketplace.ru";
const apiKey = "cdek-index-key"; 
const keyLocation = `https://${host}/cdek-index-key.txt`;

// Разбиваем на пачки по 10 000 (лимит API )
const chunks = [];
for (let i = 0; i < urls.length; i += 10000) {
    chunks.push(urls.slice(i, i + 10000));
}

console.log(`🚀 Найдено ${urls.length} URL. Начинаю отправку в Яндекс и Bing через IndexNow...`);

async function sendIndexNow(urlList, index) {
    return new Promise((resolve) => {
        const payload = JSON.stringify({
            host: host,
            key: apiKey,
            keyLocation: keyLocation,
            urlList: urlList
        });

        const options = {
            hostname: 'api.indexnow.org',
            path: '/indexnow',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json; charset=utf-8',
                'Content-Length': Buffer.byteLength(payload)
            }
        };

        const req = https.request(options, (res ) => {
            console.log(`Пачка №${index + 1}: Статус ${res.statusCode} (IndexNow)`);
            resolve();
        });

        req.on('error', (e) => {
            console.error(`❌ Ошибка IndexNow в пачке №${index + 1}:`, e.message);
            resolve();
        });

        req.write(payload);
        req.end();
    });
}

async function pingSitemaps() {
    const sitemapUrl = `https://${host}/sitemap.xml`;
    const services = [
        { name: 'Google', url: `https://www.google.com/ping?sitemap=${sitemapUrl}` },
        { name: 'Bing/Yahoo', url: `https://www.bing.com/ping?sitemap=${sitemapUrl}` }
    ];

    for (const service of services ) {
        https.get(service.url, (res ) => {
            console.log(`📡 Сигнал в ${service.name} отправлен. Статус: ${res.statusCode}`);
        }).on('error', (e) => {
            console.error(`❌ Ошибка пинга ${service.name}:`, e.message);
        });
    }
}

async function main() {
    // Сначала IndexNow (Яндекс + Bing)
    for (let i = 0; i < chunks.length; i++) {
        await sendIndexNow(chunks[i], i);
        await new Promise(r => setTimeout(r, 1000));
    }
    
    // Затем прямой пинг карты сайта (Google + Fallback Bing)
    console.log('📡 Отправляю финальные уведомления в Google и Bing...');
    await pingSitemaps();
    
    console.log('✅ Все операции по индексации завершены!');
}

main().catch(console.error);
