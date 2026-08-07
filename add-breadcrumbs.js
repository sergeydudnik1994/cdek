const fs = require('fs');
const path = require('path');

// Словарь городов для перевода
const geoNames = {
    'aksay': 'Аксай', 'armavir': 'Армавир', 'blagoveshchensk': 'Благовещенск',
    'bryansk': 'Брянск', 'chelyabinsk': 'Челябинск', 'cherkessk': 'Черкесск',
    'derbent': 'Дербент', 'irkutsk': 'Иркутск', 'izhevsk': 'Ижевск',
    'kamensk-shakhtinsky': 'Каменск-Шахтинский', 'kanash': 'Канаш', 'kazan': 'Казань',
    'khabarovsk': 'Хабаровск', 'khasavyurt': 'Хасавюрт', 'komsomolsk-na-amure': 'Комсомольск-на-Амуре',
    'krasnodar': 'Краснодар', 'krasnoyarsk': 'Красноярск', 'kursk': 'Курск',
    'makhachkala': 'Махачкала', 'moscow': 'Москва', 'nalchik': 'Нальчик',
    'nizhny-novgorod': 'Нижний Новгород', 'novocheboksarsk': 'Новочебоксарск',
    'novorossiysk': 'Новороссийск', 'novosibirsk': 'Новосибирск', 'omsk': 'Омск',
    'perm': 'Пермь', 'rostov-na-donu': 'Ростов-на-Дону', 'saint-petersburg': 'Санкт-Петербург',
    'salavat': 'Салават', 'samara': 'Самара', 'smolensk': 'Смоленск',
    'sochi': 'Сочи', 'stavropol': 'Ставрополь', 'sterlitamak': 'Стерлитамак',
    'taganrog': 'Таганрог', 'tuapse': 'Туапсе', 'tyumen': 'Тюмень',
    'ufa': 'Уфа', 'ulan-ude': 'Улан-Удэ', 'ulyanovsk': 'Ульяновск',
    'vladikavkaz': 'Владикавказ', 'vladivostok': 'Владивосток', 'volgodonsk': 'Волгодонск',
    'volgograd': 'Волгоград', 'voronezh': 'Воронеж', 'yekaterinburg': 'Екатеринбург'
};

// Базовые страницы (2 и 3 уровень)
const routes = [
    { path: 'calculator/index.html', title: 'Калькулятор', parent: null },
    { path: 'blog/index.html', title: 'Блог', parent: null },
    { path: 'faq/index.html', title: 'Частые вопросы', parent: null },
    { path: 'policy/index.html', title: 'Политика конфиденциальности', parent: null },
    { path: 'internet-magazin/index.html', title: 'Интернет-магазинам', parent: null },
    { path: 'wildberries/index.html', title: 'Wildberries', parent: null },
    { path: 'ozon/index.html', title: 'Ozon', parent: null },
    { path: 'avito/index.html', title: 'Авито', parent: null },
    { path: 'megamarket/index.html', title: 'Мегамаркет', parent: null },
    { path: 'yandex-market/index.html', title: 'Яндекс Маркет', parent: null },
    
    // Блог и калькулятор (вложенные)
    { path: 'blog/fbs-vs-fbo-cdek/index.html', title: 'FBS vs FBO СДЭК', parent: { name: 'Блог', url: '/blog/' } },
    { path: 'blog/kakoj-tarif-cdek-vybrat/index.html', title: 'Какой тариф СДЭК выбрать', parent: { name: 'Блог', url: '/blog/' } },
    { path: 'blog/obemnyj-ves-cdek/index.html', title: 'Объемный вес СДЭК', parent: { name: 'Блог', url: '/blog/' } },
    { path: 'calculator/dbs-1kg/index.html', title: 'Расчет DBS 1 кг', parent: { name: 'Калькулятор', url: '/calculator/' } }
];

// Динамически добавляем все гео-страницы
for (const [slug, name] of Object.entries(geoNames)) {
    routes.push({ path: `geo/${slug}/index.html`, title: name, parent: null });
}

// Функция генерации JSON-LD
function generateLdJson(route) {
    let urlPath = route.path.replace('index.html', '');
    let items = [
        { "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://cdek-marketplace.ru/" }
    ];

    if (route.parent) {
        items.push({ "@type": "ListItem", "position": 2, "name": route.parent.name, "item": `https://cdek-marketplace.ru${route.parent.url}` });
        items.push({ "@type": "ListItem", "position": 3, "name": route.title, "item": `https://cdek-marketplace.ru/${urlPath}` });
    } else {
        items.push({ "@type": "ListItem", "position": 2, "name": route.title, "item": `https://cdek-marketplace.ru/${urlPath}` });
    }

    const jsonLd = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    };

    return `\n    <script type="application/ld+json">\n    ${JSON.stringify(jsonLd, null, 4)}\n    </script>\n`;
}

// Проход по файлам и вставка скрипта
routes.forEach(route => {
    const filePath = path.join(__dirname, route.path);
    if (fs.existsSync(filePath)) {
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Проверка, чтобы не добавить разметку дважды при повторном запуске
        if (!content.includes('BreadcrumbList')) {
            const scriptTag = generateLdJson(route);
            content = content.replace('</head>', `${scriptTag}</head>`);
            fs.writeFileSync(filePath, content, 'utf8');
            console.log(`✅ Обновлен: ${route.path}`);
        } else {
            console.log(`⏭️ Пропущен (уже есть разметка): ${route.path}`);
        }
    } else {
        console.log(`❌ Файл не найден: ${route.path}`);
    }
});

console.log('🎉 Готово! Проверьте файлы и отправляйте коммит в GitHub.');
