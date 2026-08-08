const fs = require('fs');
const path = require('path');

const geoDir = path.join(__dirname, 'geo');
const headerPath = path.join(__dirname, 'src', 'components', 'header.html');
const sitemapPath = path.join(__dirname, 'sitemap.xml');

// 1. Автоматически читаем все папки из директории geo/
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

// 2. Превращаем папки (слаги) в массив объектов городов с красивыми именами
const cities = slugs.map(slug => {
  // Базовое форматирование: заменяем дефисы на дефисы/пробелы и делаем заглавные буквы
  let name = slug
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join('-');

  // Точечная корректировка для сложных составных названий городов
  if (slug === 'sankt-peterburg') name = 'Санкт-Петербург';
  else if (slug === 'rostov-na-donu') name = 'Ростов-на-Дону';
  else if (slug === 'nizhniy-novgorod') name = 'Нижний Новгород';
  else if (slug === 'nizhniy-tagil') name = 'Нижний Тагил';
  else if (slug === 'staryy-oskol') name = 'Старый Оскол';
  else if (slug === 'velikiy-novgorod') name = 'Великий Новгород';
  else if (slug === 'kamen-na-obi') name = 'Камень-на-Оби';
  else if (slug === 'goryachiy-klyuch') name = 'Горячий Ключ';
  else if (slug === 'gus-hrustalnyy') name = 'Гусь-Хрустальный';
  else if (slug === 'velikie-luki') name = 'Великие Луки';
  else if (slug === 'mineralnye-vody') name = 'Минеральные Воды';
  else if (slug === 'kamen-na-obi') name = 'Камень-на-Оби';
  else {
    // Для остальных названий возвращаем нормальный вид с пробелами, если они через дефис
    name = slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  }

  return { slug, name };
});

// Сортируем города по алфавиту для порядка в модальном окне
cities.sort((a, b) => a.name.localeCompare(b.name, 'ru'));

console.log(`Автоматически обнаружено городов в папке geo/: ${cities.length}`);

// 3. Генерируем HTML-сетку со всеми городами для шапки
const citiesGridHtml = cities.map(city => 
  `<a href="/geo/${city.slug}/" class="city-item p-2 rounded-lg bg-slate-800/40 border border-slate-700/50 hover:border-cdek text-sm text-slate-300 hover:text-cdek transition-all text-center font-medium">${city.name}</a>`
).join('\n');

// 4. Внедряем полученный список в файл шапки header.html
if (fs.existsSync(headerPath)) {
  let headerHtml = fs.readFileSync(headerPath, 'utf-8');
  
  if (headerHtml.includes('{{CITIES_GRID}}')) {
    headerHtml = headerHtml.replace('{{CITIES_GRID}}', citiesGridHtml);
  } else {
    // Заменяем блок сетки внутри модального окна автоматически
    headerHtml = headerHtml.replace(
      /(<div class="p-6 overflow-y-auto space-y-6 custom-scrollbar">[\s\S]*?<div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5">)[\s\S]*?(<\/div>)/,
      `$1\n${citiesGridHtml}\n$2`
    );
  }
  
  fs.writeFileSync(headerPath, headerHtml);
  console.log('Шапка сайта успешно обновлена динамическим списком городов.');
}

// 5. Автоматически обновляем sitemap.xml для всех найденных городов
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
