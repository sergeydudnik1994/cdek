const fs = require('fs');
const path = require('path');

const geoDir = path.join(__dirname, 'geo');
const headerPath = path.join(__dirname, 'src', 'components', 'header.html');
const sitemapPath = path.join(__dirname, 'sitemap.xml');

// Функция транслитерации: нужна для того, чтобы превратить "Санкт-Петербург" из JSON в "sankt-peterburg" 
// и сопоставить с названием вашей папки
function createSlug(word) {
  const letters = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh",
    "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "ts",
    "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya"
  };
  return word.toLowerCase().split('').map(char => letters[char] !== undefined ? letters[char] : char)
    .join('').replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
}

async function buildGeo() {
  console.log('Скачиваем базу городов по ссылке...');
  
  let cityNamesRu = {};
  
  try {
    // 1. Подтягиваем вашу базу городов
    const response = await fetch('https://raw.githubusercontent.com/pensnarik/russian-cities/master/russian-cities.json');
    const citiesDatabase = await response.json();
    
    // 2. Строим "умный" словарь { "slug": "Русское Название" }
    citiesDatabase.forEach(city => {
      const slug = createSlug(city.name);
      cityNamesRu[slug] = city.name;
    });
    
    // Ручная страховка для парочки городов (на случай расхождений транслита)
    cityNamesRu['moskva'] = 'Москва';
    cityNamesRu['sankt-peterburg'] = 'Санкт-Петербург';
    
  } catch (error) {
    console.error('Ошибка загрузки JSON базы городов:', error.message);
    process.exit(1);
  }

  // 3. Читаем все папки из geo/
  if (!fs.existsSync(geoDir)) {
    fs.mkdirSync(geoDir, { recursive: true });
  }

  const slugs = fs.readdirSync(geoDir).filter(file => {
    try { return fs.statSync(path.join(geoDir, file)).isDirectory(); } 
    catch (e) { return false; }
  });

  // 4. Сопоставляем слаги (названия папок) с русскими названиями из JSON
  const cities = slugs.map(slug => {
    let name = cityNamesRu[slug];
    
    // Резервный вариант, если вдруг город в JSON не найден
    if (!name) {
      name = slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    }
    return { slug, name };
  });

  // Сортируем по русскому алфавиту
  cities.sort((a, b) => a.name.localeCompare(b.name, 'ru'));
  console.log(`Успешно обработано городов: ${cities.length}`);

  // 5. Внедряем HTML-сетку в шапку
  const citiesGridHtml = cities.map(city => 
    `<a href="/geo/${city.slug}/" class="city-item p-2 rounded-lg bg-slate-800/40 border border-slate-700/50 hover:border-cdek text-sm text-slate-300 hover:text-cdek transition-all text-center font-medium">${city.name}</a>`
  ).join('\n');

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
    console.log('Шапка сайта успешно обновлена!');
  }

  // 6. Обновляем sitemap.xml
  const baseUrl = "https://cdek-marketplace.ru";
  let sitemapUrls = [`${baseUrl}/`, `${baseUrl}/calculator/`, `${baseUrl}/blog/`];
  
  cities.forEach(city => sitemapUrls.push(`${baseUrl}/geo/${city.slug}/`));

  const sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${sitemapUrls.map(url => `  <url>\n    <loc>${url}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>${url === baseUrl + '/' ? '1.0' : '0.8'}</priority>\n  </url>`).join('\n')}\n</urlset>`;
  
  fs.writeFileSync(sitemapPath, sitemapXml);
  console.log('Файл sitemap.xml успешно обновлен!');
}

// Запуск асинхронной функции
buildGeo();
