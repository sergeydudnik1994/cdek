const fs = require('fs');
const path = require('path');

// Базовый домен
const baseUrl = 'https://cdek-marketplace.ru';

// Список всех гео-папок
const geoNames = [
    'aksay', 'armavir', 'blagoveshchensk', 'bryansk', 'chelyabinsk', 'cherkessk',
    'derbent', 'irkutsk', 'izhevsk', 'kamensk-shakhtinsky', 'kanash', 'kazan',
    'khabarovsk', 'khasavyurt', 'komsomolsk-na-amure', 'krasnodar', 'krasnoyarsk', 'kursk',
    'makhachkala', 'moscow', 'nalchik', 'nizhny-novgorod', 'novocheboksarsk',
    'novorossiysk', 'novosibirsk', 'omsk', 'perm', 'rostov-na-donu', 'saint-petersburg',
    'salavat', 'samara', 'smolensk', 'sochi', 'stavropol', 'sterlitamak',
    'taganrog', 'tuapse', 'tyumen', 'ufa', 'ulan-ude', 'ulyanovsk',
    'vladikavkaz', 'vladivostok', 'volgodonsk', 'volgograd', 'voronezh', 'yekaterinburg'
];

// Основные страницы и разделы
const routes = [
    { path: 'index.html', url: '/' }, // Главная страница
    { path: 'calculator/index.html', url: '/calculator/' },
    { path: 'blog/index.html', url: '/blog/' },
    { path: 'faq/index.html', url: '/faq/' },
    { path: 'policy/index.html', url: '/policy/' },
    { path: 'internet-magazin/index.html', url: '/internet-magazin/' },
    { path: 'wildberries/index.html', url: '/wildberries/' },
    { path: 'ozon/index.html', url: '/ozon/' },
    { path: 'avito/index.html', url: '/avito/' },
    { path: 'megamarket/index.html', url: '/megamarket/' },
    { path: 'yandex-market/index.html', url: '/yandex-market/' },
    { path: 'blog/fbs-vs-fbo-cdek/index.html', url: '/blog/fbs-vs-fbo-cdek/' },
    { path: 'blog/kakoj-tarif-cdek-vybrat/index.html', url: '/blog/kakoj-tarif-cdek-vybrat/' },
    { path: 'blog/obemnyj-ves-cdek/index.html', url: '/blog/obemnyj-ves-cdek/' },
    { path: 'calculator/dbs-1kg/index.html', url: '/calculator/dbs-1kg/' }
];

// Динамически добавляем гео-страницы
geoNames.forEach(slug => {
    routes.push({ path: `geo/${slug}/index.html`, url: `/geo/${slug}/` });
});

// Проход по файлам
routes.forEach(route => {
    const filePath = path.join(__dirname, route.path);
    if (fs.existsSync(filePath)) {
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Проверяем, чтобы не добавить тег дважды
        if (!content.includes('rel="canonical"')) {
            const canonicalTag = `\n    <link rel="canonical" href="${baseUrl}${route.url}" />\n</head>`;
            content = content.replace('</head>', canonicalTag);
            fs.writeFileSync(filePath, content, 'utf8');
            console.log(`✅ Добавлен canonical: ${route.path}`);
        } else {
            console.log(`⏭️ Пропущен (уже есть): ${route.path}`);
        }
    } else {
        console.log(`❌ Файл не найден: ${route.path}`);
    }
});

console.log('🎉 Готово! Canonical теги успешно расставлены.');
