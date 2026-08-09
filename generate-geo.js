const fs = require('fs');
const path = require('path');

const geoDir = path.join(__dirname, 'geo');
const templatePath = path.join(__dirname, 'city-template.html');
const headerPath = path.join(__dirname, 'src', 'components', 'header.html');
const sitemapPath = path.join(__dirname, 'sitemap.xml');

// База ПВЗ для миллионников
const MAJOR_CITIES_PVZ = {
  'Москва': 600, 'Санкт-Петербург': 420, 'Новосибирск': 130, 'Екатеринбург': 120,
  'Казань': 100, 'Нижний Новгород': 90, 'Красноярск': 85, 'Челябинск': 80,
  'Самара': 75, 'Уфа': 75, 'Ростов-на-Дону': 95, 'Омск': 60, 'Краснодар': 150,
  'Воронеж': 65, 'Пермь': 55, 'Волгоград': 50, 'Саратов': 45, 'Тюмень': 70,
  'Хабаровск': 40, 'Владивосток': 45, 'Барнаул': 35, 'Ижевск': 35, 'Ульяновск': 30,
  'Иркутск': 40, 'Ярославль': 35, 'Севастополь': 25, 'Ставрополь': 35, 'Сочи': 45,
  'Набережные Челны': 30, 'Балашиха': 40, 'Тула': 30, 'Калуга': 25
};

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

function calculatePvzCount(cityName, population) {
  if (MAJOR_CITIES_PVZ[cityName]) return MAJOR_CITIES_PVZ[cityName];
  if (!population || population <= 0) return 3;
  const estimated = Math.round(population / 14000);
  return Math.max(2, estimated);
}

async function buildGeo() {
  console.log('🚀 Запуск генератора гео-страниц...');
  
  let cityDetailsMap = {};
  
  try {
    const response = await fetch('https://raw.githubusercontent.com/pensnarik/russian-cities/master/russian-cities.json');
    const citiesDatabase = await response.json();
    
    citiesDatabase.forEach(city => {
      const slug = createSlug(city.name);
      cityDetailsMap[slug] = {
        name: city.name,
        population: city.population || 0
      };
    });
    
    cityDetailsMap['moskva'] = { name: 'Москва', population: 13000000 };
    cityDetailsMap['sankt-peterburg'] = { name: 'Санкт-Петербург', population: 5600000 };
    
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
    let details = cityDetailsMap[slug];
    let name = details ? details.name : slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    let population = details ? details.population : 0;

    const cases = getCityCases(name);
    const pvzCount = calculatePvzCount(name, population);
    
    return { slug, name, prep: cases.prep, gen: cases.gen, pvzCount };
  });

  cities.sort((a, b) => a.name.localeCompare(b.name, 'ru'));

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
        .replace(/\{\{CITY_GEN\}\}/g, city.gen)
        .replace(/\{\{PVZ_COUNT\}\}/g, city.pvzCount);

      fs.writeFileSync(path.join(cityFolder, 'index.html'), pageHtml);
    });
    console.log(`✅ Успешно сгенерированы HTML-страницы для ${cities.length} городов!`);
  }

  // --- 2. СБОРКА СТРАНИЦЫ-ХАБА ВСЕХ ГОРОДОВ (/geo/index.html) ---
  const hubCardsHtml = cities.map(city => 
    `<a href="/geo/${city.slug}/" class="city-card p-4 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-cdek/50 hover:bg-slate-800/60 transition-all flex flex-col justify-between group">
      <span class="text-white font-bold group-hover:text-cdek transition-colors text-base">${city.name}</span>
      <span class="text-xs text-slate-500 mt-1">${city.pvzCount}+ ПВЗ СДЭК</span>
    </a>`
  ).join('\n');

  const hubHtml = `<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  
  <!-- Yandex.Metrika counter -->
  <script type="text/javascript">
      (function(m,e,t,r,i,k,a){
          m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
          m[i].l=1*new Date();
          for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
          k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
      })(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=111090265', 'ym');

      ym(111090265, 'init', {ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true});
  </script>
  <noscript><div><img src="https://mc.yandex.ru/watch/111090265" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
  <!-- /Yandex.Metrika counter -->

  <title>Логистика СДЭК для селлеров по городам России | FBS и DBS</title>
  <meta name="description" content="Выберите ваш город для официального подключения к логистике СДЭК. Специальные тарифы и скидки до 50% для селлеров Wildberries, Ozon, Яндекс Маркета и Авито." />
  <link rel="canonical" href="https://cdek-marketplace.ru/geo/" />
  <meta name="theme-color" content="#8DE21A" />
  <link rel="icon" type="image/png" href="/favicon.png" />

  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: { cdek: '#8de21a', dark: { 900: '#0b101d' } }
        }
      }
    }
  </script>
</head>
<body class="bg-dark-900 text-slate-100 min-h-screen flex flex-col antialiased selection:bg-cdek selection:text-dark-900">

  <!--#include virtual="/src/components/header.html" -->

  <main class="flex-grow pt-8 pb-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- ХЛЕБНЫЕ КРОШКИ -->
      <nav class="text-sm text-slate-400 mb-6">
        <a href="/" class="hover:text-cdek transition-colors">Главная</a>
        <span class="mx-2">/</span>
        <span class="text-white">Логистика для селлеров</span>
      </nav>

      <div class="text-center max-w-3xl mx-auto mb-10">
        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white mb-4">
          Логистика СДЭК для селлеров в <span class="text-cdek">городах РФ</span>
        </h1>
        <p class="text-slate-400 text-base sm:text-lg">
          Подключение к договору СДЭК со скидками до 50% на отгрузки FBS и DBS для маркетплейсов в вашем регионе.
        </p>

        <!-- Поиск города -->
        <div class="mt-8 max-w-md mx-auto relative">
          <input type="text" id="city-search" placeholder="Поиск вашего города..." autocomplete="off" class="w-full px-5 py-3.5 bg-slate-900 border border-slate-700 rounded-2xl text-white placeholder-slate-500 focus:outline-none focus:border-cdek text-sm shadow-xl" />
        </div>
      </div>

      <!-- Сетка городов -->
      <div id="cities-grid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3 sm:gap-4">
        ${hubCardsHtml}
      </div>

    </div>
  </main>

  <!--#include virtual="/src/components/footer.html" -->

  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const searchInput = document.getElementById('city-search');
      const cards = document.querySelectorAll('.city-card');

      searchInput.addEventListener('input', (e) => {
        const val = e.target.value.toLowerCase().trim();
        cards.forEach(card => {
          const name = card.querySelector('span').textContent.toLowerCase();
          if (name.includes(val)) {
            card.classList.remove('hidden');
          } else {
            card.classList.add('hidden');
          }
        });
      });
    });
  </script>
</body>
</html>`;

  fs.writeFileSync(path.join(geoDir, 'index.html'), hubHtml);
  console.log(`✅ Успешно сгенерирована страница-хаб /geo/index.html!`);

  // --- 3. ВНЕДРЕНИЕ СЕТКИ В ШАПКУ ---
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
  }

  // --- 4. ОБНОВЛЕНИЕ SITEMAP.XML ---
  const baseUrl = "https://cdek-marketplace.ru";
  const today = new Date().toISOString().split('T')[0];

  const mainPages = [
    { url: `${baseUrl}/`, priority: '1.0', changefreq: 'daily' },
    { url: `${baseUrl}/geo/`, priority: '0.9', changefreq: 'daily' },
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
  console.log(`✅ Файл sitemap.xml успешно обновлен!`);
}

buildGeo();
