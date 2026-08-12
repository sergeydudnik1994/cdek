const fs = require('fs');
const https = require('https');

// Читаем sitemap.xml
const sitemap = fs.readFileSync('./sitemap.xml', 'utf8');
const urls = [...sitemap.matchAll(/<loc>(.*?)<\/loc>/g)].map(m => m[1]);

if (urls.length === 0) {
    console.log('URL не найдены в sitemap.xml');
    process.exit(1);
}

const payload = JSON.stringify({
  host: "cdek-marketplace.ru",
  key: "cdek-index-key", // Имя txt-файла ключа без расширения
  keyLocation: "https://cdek-marketplace.ru/cdek-index-key.txt",
  urlList: urls
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

const req = https.request(options, (res) => {
  console.log(`Статус ответа Yandex IndexNow: ${res.statusCode}`);
  res.on('data', (d) => process.stdout.write(d));
});

req.on('error', (e) => console.error(e));
req.write(payload);
req.end();

console.log(`🚀 Отправлено ${urls.length} URL в Яндекс на срочную индексацию`);
