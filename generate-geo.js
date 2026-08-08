const fs = require('fs');
const path = require('path');

// Базовый массив городов для генерации и наполнения шапки
const cities = [
  { name: "Москва", slug: "moskva", city_prep: "Москве", city_gen: "Москвы" },
  { name: "Санкт-Петербург", slug: "sankt-peterburg", city_prep: "Санкт-Петербурге", city_gen: "Санкт-Петербурга" },
  { name: "Краснодар", slug: "krasnodar", city_prep: "Краснодаре", city_gen: "Краснодара" },
  { name: "Екатеринбург", slug: "ekaterinburg", city_prep: "Екатеринбурге", city_gen: "Екатеринбурга" },
  { name: "Новосибирск", slug: "novosibirsk", city_prep: "Новосибирске", city_gen: "Новосибирска" },
  { name: "Казань", slug: "kazan", city_prep: "Казани", city_gen: "Казани" },
  { name: "Нижний Новгород", slug: "nizhniy-novgorod", city_prep: "Нижнем Новгороде", city_gen: "Нижнего Новгорода" },
  { name: "Челябинск", slug: "chelyabinsk", city_prep: "Челябинске", city_gen: "Челябинска" },
  { name: "Самара", slug: "samara", city_prep: "Самаре", city_gen: "Самары" },
  { name: "Омск", slug: "omsk", city_prep: "Омске", city_gen: "Омска" },
  { name: "Ростов-на-Дону", slug: "rostov-na-donu", city_prep: "Ростове-на-Дону", city_gen: "Ростова-на-Дону" },
  { name: "Уфа", slug: "ufa", city_prep: "Уфе", city_gen: "Уфы" },
  { name: "Красноярск", slug: "krasnoyarsk", city_prep: "Красноярске", city_gen: "Красноярска" },
  { name: "Воронеж", slug: "voronezh", city_prep: "Воронеже", city_gen: "Воронежа" },
  { name: "Пермь", slug: "perm", city_prep: "Перми", city_gen: "Перми" },
  { name: "Волгоград", slug: "volgograd", city_prep: "Волгограде", city_gen: "Волгограда" }
];

// Убедимся, что директория geo существует
const geoOutputDir = path.join(__dirname, 'geo');
if (!fs.existsSync(geoOutputDir)) {
  fs.mkdirSync(geoOutputDir, { recursive: true });
}

// Читаем шаблон страницы города
const cityTemplatePath = path.join(__dirname, 'city-template.html');
const cityTemplate = fs.existsSync(cityTemplatePath) ? fs.readFileSync(cityTemplatePath, 'utf-8') : '';

// 1. Генерируем папки и файлы страниц для каждого города
cities.forEach(city => {
  if (cityTemplate) {
    let pageContent = cityTemplate
      .replace(/\{\{CITY\}\}/g, city.name)
      .replace(/\{\{CITY_PREP\}\}/g, city.city_prep)
      .replace(/\{\{CITY_GEN\}\}/g, city.city_gen)
      .replace(/\{\{SLUG\}\}/g, city.slug);

    const cityDir = path.join(geoOutputDir, city.slug);
    if (!fs.existsSync(cityDir)) {
      fs.mkdirSync(cityDir, { recursive: true });
    }
    fs.writeFileSync(path.join(cityDir, 'index.html'), pageContent);
  }
});

// 2. Формируем сетку элементов для модального окна шапки
const citiesGridHtml = cities.map(city => 
  `<a href="/geo/${city.slug}/" class="city-item p-2 rounded-lg bg-slate-800/40 border border-slate-700/50 hover:border-cdek text-sm text-slate-300 hover:text-cdek transition-all text-center font-medium">${city.name}</a>`
).join('\n');

// 3. Интегрируем список в header.html
const headerPath = path.join(__dirname, 'src', 'components', 'header.html');
if (fs.existsSync(headerPath)) {
  let headerHtml = fs.readFileSync(headerPath, 'utf-8');
  headerHtml = headerHtml.replace('{{CITIES_GRID}}', citiesGridHtml);
  fs.writeFileSync(headerPath, headerHtml);
}

// 4. Обновляем sitemap.xml
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

fs.writeFileSync(path.join(__dirname, 'sitemap.xml'), sitemapXml);

console.log(`Успешно обработано городов: ${cities.length}, sitemap.xml и шапка обновлены.`);
