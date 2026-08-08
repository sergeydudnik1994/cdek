const fs = require('fs');
const path = require('path');
const https = require('https');

// Таблица транслитерации для чистых URL (ЧПУ)
const cyrillicToLatin = {
    'а':'a', 'б':'b', 'в':'v', 'г':'g', 'д':'d', 'е':'e', 'ё':'e', 'ж':'zh', 'з':'z', 'и':'i',
    'й':'y', 'к':'k', 'л':'l', 'м':'m', 'н':'n', 'о':'o', 'п':'p', 'р':'r', 'с':'s', 'т':'t',
    'у':'u', 'ф':'f', 'х':'h', 'ц':'ts', 'ч':'ch', 'ш':'sh', 'щ':'sch', 'ъ':'', 'ы':'y', 'ь':'',
    'э':'e', 'ю':'yu', 'я':'ya', ' ':'-', '-':'-'
};

function slugify(text) {
    return text.toLowerCase().split('').map(char => cyrillicToLatin[char] || char).join('').replace(/[^a-z0-9-]/g, '').replace(/-+/g, '-');
}

// Умное склонение: "в ком/чем?" (Предложный падеж)
function getPrep(name) {
    if (name.includes(' ') || name.includes('-')) return 'г. ' + name;
    if (name.endsWith('а') || name.endsWith('я')) return name.slice(0, -1) + 'е';
    if (name.endsWith('ь')) return name.slice(0, -1) + 'и';
    if (name.endsWith('й')) return name.slice(0, -1) + 'е';
    if (name.endsWith('о') || name.endsWith('е') || name.endsWith('и') || name.endsWith('у') || name.endsWith('ы')) return 'г. ' + name;
    if (/[бвгджзклмнпрстфхцчшщ]$/i.test(name)) return name + 'е';
    return 'г. ' + name;
}

// Умное склонение: "из кого/чего?" (Родительный падеж)
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
        
        // Сортируем по населению и берем топ-500 самых крупных городов
        cities.sort((a, b) => b.population - a.population);
        const topCities = cities.slice(0, 500);

        const templatePath = path.join(__dirname, 'city-template.html');
        const template = fs.readFileSync(templatePath, 'utf8');

        // Создаем главную папку geo, если её вдруг нет
        const geoDir = path.join(__dirname, 'geo');
        if (!fs.existsSync(geoDir)) fs.mkdirSync(geoDir);

        topCities.forEach(c => {
            const slug = slugify(c.name);
            const prep = getPrep(c.name); // например, "Самаре"
            const gen = getGen(c.name);   // например, "Самары"

            const cityHtml = template
                .replace(/{{CITY}}/g, c.name)
                .replace(/{{CITY_PREP}}/g, prep)
                .replace(/{{CITY_GEN}}/g, gen)
                .replace(/{{SLUG}}/g, slug);

            const cityDir = path.join(geoDir, slug);
            if (!fs.existsSync(cityDir)) fs.mkdirSync(cityDir, { recursive: true });

            fs.writeFileSync(path.join(cityDir, 'index.html'), cityHtml);
        });

        console.log(`Успешно сгенерировано ${topCities.length} городов! Проверьте папку geo.`);
    });
}).on("error", (err) => {
    console.error("Ошибка при скачивании списка городов:", err.message);
});
