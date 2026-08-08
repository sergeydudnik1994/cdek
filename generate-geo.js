const fs = require('fs');
const path = formatPath => path.join(__dirname, formatPath);

// Пути к директориям
const geoDir = path('geo');
const headerPath = path('src/components/header.html');
const sitemapPath = path('sitemap.xml');

// 1. Автоматически читаем все папки из директории geo/ (все 500+ городов)
if (!fs.existsSync(geoDir)) {
  console.error('Папка geo/ не найдена!');
  process.exit(1);
}

const slugs = fs.readdirSync(geoDir).filter(file => {
  return fs.statSync(path(`geo/${file}`)).isDirectory();
});

// Превращаем слаги в красивый массив объектов для шапки и карты сайта
const cities = slugs.map(slug => {
  // Превращаем слаг (например, "rostov-na-donu" или "sankt-peterburg") в читаемое имя
  const formattedName = slug
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join('-'); // Сохраняем дефисы для составных названий

  return {
    slug: slug,
    name: formattedName
  };
});

// Сортируем города по алфавиту для удобства в модальном окне
cities.sort((a, b) => a.name.localeCompare(b.name, 'ru'));

console.log(`Обнаружено гео-папок: ${cities.length}`);

// 2. Генерируем HTML-сетку со всеми городами для шапки сайта
const citiesGridHtml = cities.map(city => 
  `<a href="/geo/${city.slug}/" class="city-item p-2 rounded-lg bg-slate-800/40 border border-slate-700/50 hover:border-cdek text-sm text-slate-300 hover:text-cdek transition-all text-center font-medium">${city.name}</a>`
).join('\n');

// 3. Внедряем полный список в файл шапки header.html вместо метки {{CITIES_GRID}}
if (fs.existsSync(headerPath)) {
  let headerHtml = fs.readFileSync(headerPath, 'utf-8');
  headerHtml = headerHtml.replace('{{CITIES_GRID}}', citiesGridHtml);
  fs.writeFileSync(headerPath, headerHtml);
  console.log('Шапка сайта успешно обновлена полным списком городов.');
} else {
  console.warn('Файл header.html не найден по пути src/components/header.html');
}

// 4. Автоматическое обновление sitemap.xml для всех страниц и городов
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
