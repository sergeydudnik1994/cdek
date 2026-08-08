const fs = require('fs');
const path = require('path');

const geoDir = path.join(__dirname, 'geo');
const headerPath = path.join(__dirname, 'src', 'components', 'header.html');
const sitemapPath = path.join(__dirname, 'sitemap.xml');

// 1. Автоматически сканируем папку geo/
if (!fs.existsSync(geoDir)) {
  fs.mkdirSync(geoDir, { recursive: true });
}

const slugs = fs.readdirSync(geoDir).filter(file => {
  try {
    return fs.statSync(path.join(geoDir, file)).isDirectory();
  } catch (e) {
    return false;
  }
});

// Словарь точных ручных соответствий для самых сложных городов
const exactRuNames = {
  "rostov-na-donu": "Ростов-на-Дону",
  "sankt-peterburg": "Санкт-Петербург",
  "nizhniy-novgorod": "Нижний Новгород",
  "nizhniy-tagil": "Нижний Тагил",
  "staryy-oskol": "Старый Оскол",
  "velikiy-novgorod": "Великий Новгород",
  "kamen-na-obi": "Камень-на-Оби",
  "goryachiy-klyuch": "Горячий Ключ",
  "gus-hrustalnyy": "Гусь-Хрустальный",
  "velikie-luki": "Великие Луки",
  "mineralnye-vody": "Минеральные Воды",
  "krasnodar": "Краснодар",
  "kazan": "Казань",
  "moskva": "Москва",
  "ekaterinburg": "Екатеринбург"
};

// 2. Универсальная функция красивого преобразования любого слага в русское название
function formatCityName(slug) {
  if (exactRuNames[slug]) {
    return exactRuNames[slug];
  }

  // Если города нет в словаре, автоматически красиво форматируем слаг
  return slug
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

const cities = slugs.map(slug => {
  return {
    slug: slug,
    name: formatCityName(slug)
  };
});

// Сортируем по русскому алфавиту
cities.sort((a, b) => a.name.localeCompare(b.name, 'ru'));

console.log(`Всего обнаружено и обработано городов: ${cities.length}`);

// 3. Генерируем HTML-сетку для модального окна в шапке
const citiesGridHtml = cities.map(city => 
  `<a href="/geo/${city.slug}/" class="city-item p-2 rounded-lg bg-slate-800/40 border border-slate-700/50 hover:border-cdek text-sm text-slate-300 hover:text-cdek transition-all text-center font-medium">${city.name}</a>`
).join('\n');

// 4. Внедряем полный список в файл шапки header.html
if (fs.existsSync(headerPath)) {
  let headerHtml = fs.readFileSync(headerPath, 'utf-8');
  
  if (headerHtml.includes('{{CITIES_GRID}}')) {
    headerHtml = headerHtml.replace('{{CITIES_GRID}}', citiesGridHtml);
  } else {
    headerHtml = headerHtml.replace(
      /(<div class="p-6 overflow-y-auto space-y-6 custom-scrollbar">[\s\S]*?<div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5">)[\s\S]*?(<\/div>)/,
      `$1\n${citiesGridHtml}\n$2`
    );
  }
  
  fs.writeFileSync(headerPath, headerHtml);
  console.log('Шапка сайта успешно обновлена полным списком на русском языке.');
}

// 5. Автоматически обновляем sitemap.xml для всех городов
const baseUrl = "https://cdek-marketplace.ru";
let sitemapUrls = [
  `${baseUrl}/`,
  `${baseUrl}/calculator/`,
  `${baseUrl}/blog/`
];

cities.forEach(city => {
  sitemapUrls.push(`${baseUrl}/geo/${city.slug}/`);
});

const sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${sitemapUrls.map(url => `  <url>
    <loc>${url}</loc>
    <changefreq>weekly</changefreq>
    <priority>${url === baseUrl + '/' ? '1.0' : '0.8'}</priority>
  </url>`).join('\n')}
</urlset>`;

fs.writeFileSync(sitemapPath, sitemapXml);
console.log('Файл sitemap.xml успешно обновлен.');
