const fs = require('fs');
const path = require('path');

const geoDir = path.join(__dirname, 'geo');
const templatePath = path.join(__dirname, 'city-template.html');
const headerPath = path.join(__dirname, 'src', 'components', 'header.html');
const sitemapPath = path.join(__dirname, 'sitemap.xml');

// 1. Функция транслитерации для слагов
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

// 2. Функция склонения городов по падежам (Предложный и Родительный)
function getCityCases(name) {
  const exceptions = {
    'Москва': { prep: 'Москве', gen: 'Москвы' },
    'Санкт-Петербург': { prep: 'Санкт-Петербурге', gen: 'Санкт-Петербурга' },
    'Ростов-на-Дону': { prep: 'Ростове-на-Дону', gen: 'Ростова-на-Дону' },
    'Нижний Новгород': { prep: 'Нижнем Новгороде', gen: 'Нижнего Новгорода' },
    'Великий Новгород': { prep: 'Великом Новгороде', gen: 'Великого Новгорода' },
    'Набережные Челны': { prep: 'Набережных Челнах', gen: 'Набережных Челнов' },
    'Минеральные Воды': { prep: 'Минеральных Водах', gen: 'Минеральных Вод' },
    'Старый Оскол': { prep: 'Старом Осколе', gen: 'Старого Оскола' },
    'Горячий Ключ': { prep: 'Горячем Ключе', gen: 'Горячего Ключа' },
    'Гусь-Хрустальный': { prep: 'Гусь-Хрустальном', gen: 'Гусь-Хрустального' },
    'Камень-на-Оби': { prep: 'Камне-на-Оби', gen: 'Камня-на-Оби' }
  };

  if (exceptions[name]) return exceptions[name];

  let prep = name;
  let gen = name;

  if (name.endsWith('а')) {
    prep = name.slice(0, -1) + 'е';
    gen = name.slice(0, -1) + 'ы';
  } else if (name.endsWith('я')) {
    prep = name.slice(0, -1) + 'е';
    gen = name.slice(0, -1) + 'и';
  } else if (name.endsWith('ий') || name.endsWith('ый')) {
    prep = name.slice(0, -2) + 'ом';
    gen = name.slice(0, -2) + 'ого';
  } else if (name.endsWith('ь')) {
    prep = name.slice(0, -1) + 'и';
    gen = name.slice(0, -1) + 'и';
  } else if (/[бвгдзклмнпрстфхцчшщ]$/i.test(name)) {
    prep = name + 'е';
    gen = name + 'а';
  }

  return { prep, gen };
}

async function buildGeo() {
  console.log('🚀 Запуск генератора гео-страниц...');
  
  let cityNamesRu = {};
  
  try {
    const response = await fetch('https://raw.githubusercontent.com/pensnarik/russian-cities/master/russian-cities.json');
    const citiesDatabase = await response.json();
    
    citiesDatabase.forEach(city => {
      const slug = createSlug(city.name);
      cityNamesRu[slug] = city.name;
    });
    
    cityNamesRu['moskva'] = 'Москва';
    cityNamesRu['sankt-peterburg'] = 'Санкт-Петербург';
    
  } catch (error) {
    console.error('Ошибка загрузки JSON базы городов:', error.message);
    process.exit(1);
  }

  if (!fs.existsSync(geoDir)) {
    fs.mkdirSync(geoDir, { recursive: true });
  }

  const slugs = fs.readdirSync(geoDir).filter(file => {
    try { return fs.statSync(path.join(geoDir, file)).isDirectory(); } 
    catch (e) { return false; }
  });

  const cities = slugs.map(slug => {
    let name = cityNamesRu[slug];
    if (!name) {
      name = slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    }
    const cases = getCityCases(name);
    return { slug, name, prep: cases.prep, gen: cases.gen };
  });

  cities.sort((a, b) => a.name.localeCompare(b.name, 'ru'));
  console.log(`Успешно сопоставлено городов: ${cities.length}`);

  // --- 1. СБОРКА HTML-СТРАНИЦ ИЗ ШАБЛОНА ---
  if (fs.existsSync(templatePath)) {
    const templateHtml = fs.readFileSync(templatePath, 'utf-8');
    
    cities.forEach(city => {
      const cityFolder = path.join(geoDir, city.slug);
      if (!fs.existsSync(cityFolder)) {
        fs.mkdirSync(cityFolder, { recursive: true });
      }

      const pageHtml = templateHtml
        .replace(/\{\{CITY\}\}/g, city.name)
        .replace(/\{\{SLUG\}\}/g, city.slug)
        .replace(/\{\{CITY_PREP\}\}/g, city.prep)
        .replace(/\{\{CITY_GEN\}\}/g, city.gen);

      fs.writeFileSync(path.join(cityFolder, 'index.html'), pageHtml);
    });
    console.log(`✅ Успешно сгенерированы HTML-страницы для ${cities.length} городов!`);
  } else {
    console.warn('⚠️ Внимание: файл city-template.html не найден, страницы не обновлены.');
  }

  // --- 2. ВНЕДРЕНИЕ СЕТКИ В ШАПКУ ---
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
    console.log('✅ Шапка сайта успешно обновлена!');
  }

  // --- 3. ОБНОВЛЕНИЕ SITEMAP.XML С LASTMOD И ИЕРАРХИЕЙ ПРИОРИТЕТОВ ---
  const baseUrl = "https://cdek-marketplace.ru";
  const today = new Date().toISOString().split('T')[0];

  // Основные важные страницы (идут ПЕРВЫМИ в sitemap)
  const mainPages = [
    { url: `${baseUrl}/`, priority: '1.0', changefreq: 'daily' },
    { url: `${baseUrl}/calculator/`, priority: '0.9', changefreq: 'weekly' },
    { url: `${baseUrl}/calculator/dbs-1kg/`, priority: '0.9', changefreq: 'weekly' },
    { url: `${baseUrl}/ozon/`, priority: '0.8', changefreq: 'weekly' },
    { url: `${baseUrl}/wildberries/`, priority: '0.8', changefreq: 'weekly' },
    { url: `${baseUrl}/yandex-market/`, priority: '0.8', changefreq: 'weekly' },
    { url: `${baseUrl}/megamarket/`, priority: '0.8', changefreq: 'weekly' },
    { url: `${baseUrl}/avito/`, priority: '0.8', changefreq: 'weekly' },
    { url: `${baseUrl}/internet-magazin/`, priority: '0.8', changefreq: 'weekly' },
    { url: `${baseUrl}/blog/`, priority: '0.8', changefreq: 'weekly' },
    { url: `${baseUrl}/faq/`, priority: '0.7', changefreq: 'monthly' },
    { url: `${baseUrl}/policy/`, priority: '0.3', changefreq: 'yearly' }
  ];

  // Гео-страницы (идут ВТОРОЙ пачкой)
  const geoPages = cities.map(city => ({
    url: `${baseUrl}/geo/${city.slug}/`,
    priority: '0.6',
    changefreq: 'weekly'
  }));

  const allSitemapEntries = [...mainPages, ...geoPages];

  const sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allSitemapEntries.map(entry => `  <url>
    <loc>${entry.url}</loc>
    <lastmod>${today}</lastmod>
    <changefreq>${entry.changefreq}</changefreq>
    <priority>${entry.priority}</priority>
  </url>`).join('\n')}
</urlset>`;

  fs.writeFileSync(sitemapPath, sitemapXml);
  console.log(`✅ Файл sitemap.xml успешно обновлен! Всего ссылок: ${allSitemapEntries.length} (Основные: ${mainPages.length}, Гео: ${geoPages.length})`);
}

buildGeo();
