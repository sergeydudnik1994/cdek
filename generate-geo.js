const fs = require('fs');
const path = require('path');
const https = require('https');

const cyrillicToLatin = {
    'а':'a', 'б':'b', 'в':'v', 'г':'g', 'д':'d', 'е':'e', 'ё':'e', 'ж':'zh', 'з':'z', 'и':'i',
    'й':'y', 'к':'k', 'л':'l', 'м':'m', 'н':'n', 'о':'o', 'п':'p', 'р':'r', 'с':'s', 'т':'t',
    'у':'u', 'ф':'f', 'х':'h', 'ц':'ts', 'ч':'ch', 'ш':'sh', 'щ':'sch', 'ъ':'', 'ы':'y', 'ь':'',
    'э':'e', 'ю':'yu', 'я':'ya', ' ':'-', '-':'-'
};

function slugify(text) {
    return text.toLowerCase().split('').map(char => cyrillicToLatin[char] || char).join('').replace(/[^a-z0-9-]/g, '').replace(/-+/g, '-');
}

function getPrep(name) {
    if (name.includes(' ') || name.includes('-')) return 'г. ' + name;
    if (name.endsWith('а') || name.endsWith('я')) return name.slice(0, -1) + 'е';
    if (name.endsWith('ь')) return name.slice(0, -1) + 'и';
    if (name.endsWith('й')) return name.slice(0, -1) + 'е';
    if (name.endsWith('о') || name.endsWith('е') || name.endsWith('и') || name.endsWith('у') || name.endsWith('ы')) return 'г. ' + name;
    if (/[бвгджзклмнпрстфхцчшщ]$/i.test(name)) return name + 'е';
    return 'г. ' + name;
}

function getGen(name) {
    if (name.includes(' ') || name.includes('-')) return 'г. ' + name;
    if (name.endsWith('а')) {
        let root = name.slice(0, -1);
        if (/[гкхжшщч]$/i.test(root)) return root + 'и';
        return root + 'ы';
    }
    if (name.endsWith('я') || name.endsWith('ь')) return name.slice(0, -1) + 'и';
    if (name.endsWith('й')) return name.slice(0, -1) + 'я';
    if (name.endsWith('о') || name.endsWith('е') || name.endsWith('и') || name.endsWith('у') || name.endsWith('ы')) return 'г. ' + name;
    if (/[бвгджзклмнпрстфхцчшщ]$/i.test(name)) return name + 'а';
    return 'г. ' + name;
}

const url = "https://raw.githubusercontent.com/pensnarik/russian-cities/master/russian-cities.json";

https.get(url, (res) => {
    let body = "";
    res.on("data", (chunk) => { body += chunk; });
    res.on("end", () => {
        const cities = JSON.parse(body);
        
        cities.sort((a, b) => b.population - a.population);
        const topCities = cities.slice(0, 500);

        const templatePath = path.join(__dirname, 'city-template.html');
        const template = fs.readFileSync(templatePath, 'utf8');

        // 1. Создаем посадочные страницы городов
        const geoDir = path.join(__dirname, 'geo');
        if (fs.existsSync(geoDir)) {
            fs.rmSync(geoDir, { recursive: true, force: true });
        }
        fs.mkdirSync(geoDir);

        let linksHtml = '';

        // Сортируем для вывода в меню по алфавиту и чиним кодировку Истры/Асбеста
        const sortedCities = [...topCities].sort((a, b) => {
            let nameA = a.name; let nameB = b.name;
            if (nameA.includes('ест') && nameA.includes('Ас')) nameA = 'Асбест';
            if (nameA.includes('стра') && !nameA.includes('Истра') && nameA.length < 7) nameA = 'Истра';
            if (nameB.includes('ест') && nameB.includes('Ас')) nameB = 'Асбест';
            if (nameB.includes('стра') && !nameB.includes('Истра') && nameB.length < 7) nameB = 'Истра';
            return nameA.localeCompare(nameB, 'ru');
        });

        sortedCities.forEach(c => {
            let cityName = c.name;
            if (cityName.includes('ест') && cityName.includes('Ас')) cityName = 'Асбест';
            if (cityName.includes('стра') && !cityName.includes('Истра') && cityName.length < 7) cityName = 'Истра';

            const slug = slugify(cityName);
            const prep = getPrep(cityName);
            const gen = getGen(cityName);

            const cityHtml = template
                .replace(/{{CITY}}/g, cityName)
                .replace(/{{CITY_PREP}}/g, prep)
                .replace(/{{CITY_GEN}}/g, gen)
                .replace(/{{SLUG}}/g, slug);

            const cityDir = path.join(geoDir, slug);
            fs.mkdirSync(cityDir, { recursive: true });
            fs.writeFileSync(path.join(cityDir, 'index.html'), cityHtml);

            // Собираем HTML ссылки для компонента
            linksHtml += `<a href="/geo/${slug}/" class="city-item p-2 rounded-lg hover:bg-slate-800/60 text-sm text-slate-300 hover:text-cdek transition-colors">${cityName}</a>\n`;
        });

        // 2. Создаем компонент списка городов для Nginx
        const componentsDir = path.join(__dirname, 'src', 'components');
        if (!fs.existsSync(componentsDir)) fs.mkdirSync(componentsDir, { recursive: true });
        
        const cityListPath = path.join(componentsDir, 'city-list.html');
        fs.writeFileSync(cityListPath, linksHtml);

        console.log(`Успешно пересоздано 500 городов и сгенерирован компонент city-list.html!`);
    });
});
