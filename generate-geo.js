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

        const geoDir = path.join(__dirname, 'geo');
        if (fs.existsSync(geoDir)) {
            fs.rmSync(geoDir, { recursive: true, force: true });
        }
        fs.mkdirSync(geoDir);

        topCities.forEach(c => {
            let cityName = c.name;
            // Фикс сломанной кодировки в исходном JSON-файле
            if (cityName.includes('ест') && cityName.includes('Ас')) cityName = 'Асбест';
            if (cityName.includes('стра') && !cityName.includes('Истра') && cityName.length < 7) cityName = 'Истра';

            c.name = cityName; // сохраняем исправленное имя обратно

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
        });

        const headerPath = path.join(__dirname, 'src', 'components', 'header.html');
        if (fs.existsSync(headerPath)) {
            let headerContent = fs.readFileSync(headerPath, 'utf8');
            const sortedCities = [...topCities].sort((a, b) => a.name.localeCompare(b.name, 'ru'));
            
            let linksHtml = '\n';
            sortedCities.forEach(c => {
                const slug = slugify(c.name);
                linksHtml += `          <a href="/geo/${slug}/" class="city-item p-2 rounded-lg hover:bg-slate-800/60 text-sm text-slate-300 hover:text-cdek transition-colors">${c.name}</a>\n`;
            });

            const marker = 'Все города</div>';
            const markerIndex = headerContent.indexOf(marker);
            
            if (markerIndex !== -1) {
                const gridStartIndex = headerContent.indexOf('<div class="grid', markerIndex);
                if (gridStartIndex !== -1) {
                    const gridInnerStart = headerContent.indexOf('>', gridStartIndex) + 1;
                    const gridInnerEnd = headerContent.indexOf('</div>', gridInnerStart);
                    
                    headerContent = headerContent.substring(0, gridInnerStart) + linksHtml + '        ' + headerContent.substring(gridInnerEnd);
                    fs.writeFileSync(headerPath, headerContent);
                }
            }
        }

        console.log(`Успешно пересоздано 500 городов и обновлен список в шапке!`);
    });
});
