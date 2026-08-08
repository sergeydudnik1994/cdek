const fs = require('fs');
const path = require('path');

const geoDir = path.join(__dirname, 'geo');
const headerPath = path.join(__dirname, 'src', 'components', 'header.html');
const sitemapPath = path.join(__dirname, 'sitemap.xml');

// Полный словарь соответствия слагов папок geo/ и русских названий
const cityNamesRu = {
  "abakan": "Абакан", "abinsk": "Абинск", "aznakaevo": "Азнакаево", "azov": "Азов", "aksay": "Аксай",
  "alapaevsk": "Алапаевск", "alatyr": "Алатырь", "aleksandrov": "Александров", "alekseevka": "Алексеевка",
  "aleksin": "Алексин", "alushta": "Алушта", "almetevsk": "Альметьевск", "amursk": "Амурск", "anapa": "Анапа",
  "angarsk": "Ангарск", "anzhero-sudzhensk": "Анжеро-Судженск", "apatity": "Апатиты", "aprelevka": "Апрелевка",
  "apsheronsk": "Апшеронск", "argun": "Аргун", "arhangelsk": "Архангельск", "armavir": "Армавир",
  "arsenev": "Арсеньев", "artem": "Артём", "arzamas": "Арзамас", "asbest": "Асбест", "astrahan": "Астрахань",
  "ahtubinsk": "Ахтубинск", "achinsk": "Ачинск", "baksan": "Баксан", "balaklava": "Балаклава",
  "balakovo": "Балаково", "balahna": "Балахна", "balashiha": "Балашиха", "balashov": "Балашов",
  "barnaul": "Барнаул", "bataysk": "Батайск", "belaya-kalitva": "Белая Калитва", "belgorod": "Белгород",
  "belebey": "Белебей", "belogorsk": "Белогорск", "belorechensk": "Белореченск", "beloretsk": "Белорецк",
  "belovo": "Белово", "berdsk": "Бердск", "berezniki": "Березники", "berezovskiy": "Берёзовский",
  "beslan": "Беслан", "birobidzhan": "Биробиджан", "birsk": "Бирск", "biysk": "Бийск",
  "blagodarnyy": "Благодарный", "blagoveschensk": "Благовещенск", "bogorodsk": "Богородск",
  "bolshoy-kamen": "Большой Камень", "bor": "Бор", "borisoglebsk": "Борисоглебск", "borovichi": "Боровичи",
  "bratsk": "Братск", "bryansk": "Брянск", "bugulma": "Бугульма", "buguruslan": "Бугуруслан",
  "budennovsk": "Будённовск", "buzuluk": "Бузулук", "buynaksk": "Буйнакск", "valuyki": "Валуйки",
  "velikie-luki": "Великие Луки", "velikiy-novgorod": "Великий Новгород", "verhnyaya-pyshma": "Верхняя Пышма",
  "verhnyaya-salda": "Верхняя Салда", "vidnoe": "Видное", "vladivostok": "Владивосток",
  "vladikavkaz": "Владикавказ", "vladimir": "Владимир", "volgograd": "Волгоград", "volgodonsk": "Волгодонск",
  "volzhsk": "Волжск", "volzhskiy": "Волжский", "vologda": "Вологда", "volhov": "Волхов", "volsk": "Вольск",
  "vorkuta": "Воркута", "voronezh": "Воронеж", "voskresensk": "Воскресенск", "votkinsk": "Воткинск",
  "vsevolozhsk": "Всеволожск", "vyborg": "Выборг", "vyksa": "Выкса", "vyshniy-volochek": "Вышний Волочёк",
  "vyazniki": "Вязники", "vyazma": "Вязьма", "gatchina": "Гатчина", "gelendzhik": "Геленджик",
  "georgievsk": "Георгиевск", "glazov": "Глазов", "gorno-altaysk": "Горно-Алтайск", "goryachiy-klyuch": "Горячий Ключ",
  "groznyy": "Грозный", "gryazi": "Грязи", "gubkin": "Губкин", "gubkinskiy": "Губкинский", "gudermes": "Гудермес",
  "gukovo": "Гуково", "gulkevichi": "Гулькевичи", "gus-hrustalnyy": "Гусь-Хрустальный", "gay": "Гай",
  "dagestanskie-ogni": "Дагестанские Огни", "dalnegorsk": "Дальнегорск", "derbent": "Дербент",
  "dzhankoy": "Джанкой", "dzerzhinsk": "Дзержинск", "dzerzhinskiy": "Дзержинский", "dimitrovgrad": "Димитровград",
  "dmitrov": "Дмитров", "dolgoprudnyy": "Долгопрудный", "domodedovo": "Домодедово", "donetsk": "Донецк",
  "donskoy": "Донской", "dubna": "Дубна", "dyurtyuli": "Дюртюли", "evpatoriya": "Евпатория",
  "egorevsk": "Егорьевск", "eysk": "Ейск", "ekaterinburg": "Екатеринбург", "elabuga": "Елабуга",
  "elets": "Елец", "elizovo": "Елизово", "essentuki": "Ессентуки", "efremov": "Ефремов",
  "zheleznogorsk": "Железногорск", "zhigulevsk": "Жигулёвск", "zhukovskiy": "Жуковский", "zavolzhe": "Заволжье",
  "zainsk": "Заинск", "zarechnyy": "Заречный", "zarinsk": "Заринск", "zvenigorod": "Звенигород",
  "zelenogorsk": "Зеленогорск", "zelenograd": "Зеленоград", "zelenodolsk": "Зеленодольск",
  "zelenokumsk": "Зеленокумск", "zlatoust": "Златоуст", "ivanovo": "Иваново", "ivanteevka": "Ивантеевка",
  "izhevsk": "Ижевск", "izberbash": "Избербаш", "izobilnyy": "Изобильный", "irbit": "Ирбит",
  "irkutsk": "Иркутск", "iskitim": "Искитим", "istra": "Истра", "ishim": "Ишим", "ishimbay": "Ишимбай",
  "yoshkar-ola": "Йошкар-Ола", "kaliningrad": "Калининград", "kaluga": "Калуга", "kamenka": "Каменка",
  "kamensk-uralskiy": "Каменск-Уральский", "kamensk-shahtinskiy": "Каменск-Шахтинский", "kamen-na-obi": "Камень-на-Оби",
  "kamyshin": "Камышин", "kanash": "Канаш", "kansk": "Канск", "karabulak": "Карабулак", "kaspiysk": "Каспийск",
  "kachkanar": "Качканар", "kashira": "Кашира", "kemerovo": "Кемерово", "kerch": "Керчь", "kizilyurt": "Кизилюрт",
  "kizlyar": "Кизляр", "kimry": "Кимры", "kingisepp": "Кингисепп", "kinel": "Кинель", "kineshma": "Кинешма",
  "kirishi": "Кириши", "kirov": "Киров", "kirovo-chepetsk": "Кирово-Чепецк", "kiselevsk": "Киселёвск",
  "kislovodsk": "Кисловодск", "klin": "Клин", "klintsy": "Клинцы", "kovrov": "Ковров", "kogalym": "Когалым",
  "kolomna": "Коломна", "kolpino": "Колпино", "kolchugino": "Кольчугино", "komsomolsk-na-amure": "Комсомольск-на-Амуре",
  "konakovo": "Конаково", "kopeysk": "Копейск", "korenovsk": "Кореновск", "korkino": "Коркино",
  "korolev": "Королёв", "korsakov": "Корсаков", "koryazhma": "Коряжма", "kostroma": "Кострома",
  "kotelniki": "Котельники", "kotlas": "Котлас", "kohma": "Кохма", "krasnogorsk": "Красногорск",
  "krasnoe-selo": "Красное Село", "krasnoznamensk": "Краснознаменск", "krasnokamensk": "Краснокаменск",
  "krasnokamsk": "Краснокамск", "krasnoturinsk": "Краснотурьинск", "krasnoufimsk": "Красноуфимск",
  "krasnoyarsk": "Красноярск", "krasnyy-sulin": "Красный Сулин", "kronshtadt": "Кронштадт", "kropotkin": "Кропоткин",
  "krymsk": "Крымск", "kstovo": "Кстово", "kudrovo": "Кудрово", "kuznetsk": "Кузнецк", "kuybyshev": "Куйбышев",
  "kulebaki": "Кулебаки", "kumertau": "Кумертау", "kungur": "Кунгур", "kurgan": "Курган", "kurganinsk": "Курганинск",
  "kursk": "Курск", "kurchatov": "Курчатов", "kyzyl": "Кызыл", "kyshtym": "Кыштым", "labinsk": "Лабинск",
  "langepas": "Лангепас", "leninogorsk": "Лениногорск", "leninsk-kuznetskiy": "Ленинск-Кузнецкий",
  "lesnoy": "Лесной", "lesozavodsk": "Лесозаводск", "lesosibirsk": "Лесосибирск", "livny": "Ливны",
  "likino-dulevo": "Ликино-Дулёво", "lipetsk": "Липецк", "liski": "Лиски", "lobnya": "Лобня",
  "lomonosov": "Ломоносов", "luga": "Луга", "lysva": "Лысьва", "lytkarino": "Лыткарино", "lyubertsy": "Люберцы",
  "lyudinovo": "Людиново", "lyantor": "Лянтор", "magadan": "Магадан", "magnitogorsk": "Магнитогорск",
  "maykop": "Майкоп", "malgobek": "Малгобек", "maloyaroslavets": "Малоярославец", "mariinsk": "Мариинск",
  "mahachkala": "Махачкала", "megion": "Мегион", "mezhdurechensk": "Междуреченск", "meleuz": "Мелеуз",
  "miass": "Миасс", "millerovo": "Миллерово", "mineralnye-vody": "Минеральные Воды", "minusinsk": "Минусинск",
  "mirnyy": "Мирный", "mihaylovka": "Михайловка", "mihaylovsk": "Михайловск", "michurinsk": "Мичуринск",
  "mozhaysk": "Можайск", "mozhga": "Можга", "mozdok": "Моздок", "monchegorsk": "Мончегорск", "morshansk": "Моршанск",
  "moskva": "Москва", "moskovskiy": "Московский", "murino": "Мурино", "murmansk": "Мурманск", "murom": "Муром",
  "mtsensk": "Мценск", "myski": "Мыски", "mytischi": "Мытищи", "naberezhnye-chelny": "Набережные Челны",
  "nadym": "Надым", "nazarovo": "Назарово", "nazran": "Назрань", "nalchik": "Нальчик", "naro-fominsk": "Наро-Фоминск",
  "nartkala": "Нарткала", "nahodka": "Находка", "nevinnomyssk": "Невинномысск", "neryungri": "Нерюнгри",
  "neftekamsk": "Нефтекамск", "nefteyugansk": "Нефтеюганск", "nizhnevartovsk": "Нижневартовск",
  "nizhnekamsk": "Нижнекамск", "nizhniy-novgorod": "Нижний Новгород", "nizhniy-tagil": "Нижний Тагил",
  "novoaltaysk": "Новоалтайск", "novodvinsk": "Новодвинск", "novozybkov": "Новозыбков", "novokubansk": "Новокубанск",
  "novokuznetsk": "Новокузнецк", "novokuybyshevsk": "Новокуйбышевск", "novomoskovsk": "Новомосковск",
  "novorossiysk": "Новороссийск", "novosibirsk": "Новосибирск", "novotroitsk": "Новотроицк", "novouralsk": "Новоуральск",
  "novocheboksarsk": "Новочебоксарск", "novocherkassk": "Новочеркасск", "novoshahtinsk": "Новошахтинск",
  "novyy-urengoy": "Новый Уренгой", "noginsk": "Ногинск", "norilsk": "Норильск", "noyabrsk": "Ноябрьск",
  "nurlat": "Нурлат", "nyagan": "Нягань", "obninsk": "Обнинск", "odintsovo": "Одинцово", "ozersk": "Озёрск",
  "oktyabrskiy": "Октябрьский", "omsk": "Омск", "orel": "Орёл", "orenburg": "Оренбург", "orehovo-zuevo": "Орехово-Зуево",
  "orsk": "Орск", "osinniki": "Осинники", "ostrogozhsk": "Острогожск", "otradnyy": "Отрадный", "pavlovo": "Павлово",
  "pavlovskiy-posad": "Павловский Посад", "partizansk": "Партизанск", "penza": "Пенза", "pervouralsk": "Первоуральск",
  "pereslavl-zalesskiy": "Переславль-Залесский", "perm": "Пермь", "petergof": "Петергоф", "petrozavodsk": "Петрозаводск",
  "petropavlovsk-kamchatskiy": "Петропавловск-Камчатский", "pechora": "Печора", "podolsk": "Подольск",
  "polevskoy": "Полевской", "primorsko-ahtarsk": "Приморско-Ахтарск", "prokopevsk": "Прокопьевск",
  "protvino": "Протвино", "prohladnyy": "Прохладный", "pskov": "Псков", "pugachev": "Пугачёв", "pushkin": "Пушкин",
  "pushkino": "Пушкино", "pyatigorsk": "Пятигорск", "pyt-yah": "Пыть-Ях", "raduzhnyy": "Радужный",
  "ramenskoe": "Раменское", "rasskazovo": "Рассказово", "reutov": "Реутов", "revda": "Ревда", "rezh": "Реж",
  "roslavl": "Рославль", "rossosh": "Россошь", "rostov-na-donu": "Ростов-на-Дону", "rtischevo": "Ртищево",
  "rubtsovsk": "Рубцовск", "ruzaevka": "Рузаевка", "rybinsk": "Рыбинск", "ryazan": "Рязань", "salavat": "Салават",
  "salehard": "Салехард", "salsk": "Сальск", "samara": "Самара", "sankt-peterburg": "Санкт-Петербург",
  "saransk": "Саранск", "sarapul": "Сарапул", "saratov": "Саратов", "sarov": "Саров", "satka": "Сатка",
  "sayanogorsk": "Саяногорск", "sayansk": "Саянск", "svetlograd": "Светлоград", "svobodnyy": "Свободный",
  "sevastopol": "Севастополь", "severodvinsk": "Северодвинск", "severomorsk": "Североморск", "seversk": "Северск",
  "shadrinsk": "Шадринск", "shahty": "Шахты", "shali": "Шали", "sharypovo": "Шарыпово", "shatura": "Шатура",
  "shebekino": "Шебекино", "shelehov": "Шелехов", "shuya": "Шуя", "schekino": "Щёкино", "schelkovo": "Щёлково",
  "scherbinka": "Щербинка", "elektrostal": "Электросталь", "elista": "Элиста", "engels": "Энгельс",
  "yugorsk": "Югорск", "yuzhno-sahalinsk": "Южно-Сахалинск", "yuzhnouralsk": "Южноуральск", "yurga": "Юрга",
  "yakutsk": "Якутск", "yalta": "Ялта", "yalutorovsk": "Ялуторовск", "yaroslavl": "Ярославль", "yartsevo": "Ярцево",
  "yoshkar-ola": "Йошкар-Ола", "zainsk": "Заинск", "zarechnyy": "Заречный", "zarinsk": "Заринск",
  "zavolzhe": "Заволжье", "zelenodolsk": "Зеленодольск", "zelenogorsk": "Зеленогорск", "zelenograd": "Зеленоград",
  "zelenokumsk": "Зеленокумск", "zheleznogorsk": "Железногорск", "zhigulevsk": "Жигулёвск", "zhukovskiy": "Жуковский",
  "zlatoust": "Златоуст", "zvenigorod": "Звенигород", "krasnodar": "Краснодар", "kazan": "Казань"
};

if (!fs.existsSync(geoDir)) {
  console.error("Папка geo/ не найдена!");
  process.exit(1);
}

// Автоматическое сканирование ВСЕХ папок из директории geo/
const slugs = fs.readdirSync(geoDir).filter(file => {
  try {
    return fs.statSync(path.join(geoDir, file)).isDirectory();
  } catch (e) {
    return false;
  }
});

// Собираем массив всех городов динамически, подставляя правильное русское имя
const cities = slugs.map(slug => {
  const name = cityNamesRu[slug] || slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  return { slug, name };
});

// Сортировка по русскому алфавиту
cities.sort((a, b) => a.name.localeCompare(b.name, 'ru'));

console.log(`Успешно загружено и обработано городов из geo/: ${cities.length}`);

// Генерация HTML-сетки для модального окна шапки
const citiesGridHtml = cities.map(city => 
  `<a href="/geo/${city.slug}/" class="city-item p-2 rounded-lg bg-slate-800/40 border border-slate-700/50 hover:border-cdek text-sm text-slate-300 hover:text-cdek transition-all text-center font-medium">${city.name}</a>`
).join('\n');

// Внедрение полного списка в шапку сайта
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
  console.log('Шапка сайта успешно обновлена полным списком всех городов на русском языке.');
}

// Автоматическое обновление sitemap.xml для всех найденных городов
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
