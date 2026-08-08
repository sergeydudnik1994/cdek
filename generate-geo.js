const fs = require('fs');
const path = require('path');

const geoDir = path.join(__dirname, 'geo');
const headerPath = path.join(__dirname, 'src', 'components', 'header.html');
const sitemapPath = path.join(__dirname, 'sitemap.xml');

// Полный и проверенный словарь всех твоих 500+ городов для идеального перевода на русский
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
  "kachkanar": "Качканар", "kashira": "Кашиira", "kashira": "Кашира", "kemerovo": "Кемерово", "kerch": "Керчь",
  "kizilyurt": "Кизилюрт", "kizlyar": "Кизляр", "kimry": "Кимры", "kingisepp": "Кингисепп", "kinel": "Кинель",
  "kineshma": "Кинешма", "kirishi": "Кириши", "kirov": "Киров", "kirovo-chepetsk": "Кирово-Чепецк", "kiselevsk": "Киселёвск",
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
  "pushkino": "Пушкино", "pyt-yah": "Пыть-Ях", "pyatigorsk": "Пятигорск", "raduzhnyy": "Радужный",
  "ramenskoe": "Раменское", "rasskazovo": "Рассказово", "revda": "Ревда", "rezh": "Реж", "reutov": "Реутов",
  "rzhev": "Ржев", "roslavl": "Рославль", "rossosh": "Россошь", "rtischevo": "Ртищево", "rubtsovsk": "Рубцовск",
  "ruzaevka": "Рузаевка", "rybinsk": "Рыбинск", "ryazan": "Рязань", "salavat": "Салават", "salehard": "Салехард",
  "salsk": "Сальск", "samara": "Самара", "sankt-peterburg": "Санкт-Петербург", "saransk": "Саранск", "sarapul": "Сарапул",
  "saratov": "Саратов", "sarov": "Саров", "satka": "Сатка", "safonovo": "Сафоново", "sayanogorsk": "Саяногорск",
  "sayansk": "Саянск", "svetlograd": "Светлоград", "svobodnyy": "Свободный", "sevastopol": "Севастополь",
  "severodvinsk": "Северодвинск", "severomorsk": "Североморск", "seversk": "Северск", "sergiev-posad": "Сергиев Посад",
  "serov": "Серов", "serpuhov": "Серпухов", "sertolovo": "Сертолово", "sestroretsk": "Сестрорецк", "sibay": "Сибай",
  "simferopol": "Симферополь", "slavyansk-na-kubani": "Славянск-на-Кубани", "slantsy": "Сланцы", "smolensk": "Смоленск",
  "snezhinsk": "Снежинск", "sovetsk": "Советск", "sovetskiy": "Советский", "sokol": "Сокол", "solikamsk": "Соликамск",
  "solnechnogorsk": "Солнечногорск", "sosnovoborsk": "Сосновоборск", "sosnovyy-bor": "Сосновый Бор", "sochi": "Сочи",
  "spassk-dalniy": "Спасск-Дальний", "stavropol": "Ставрополь", "staryy-oskol": "Старый Оскол", "sterlitamak": "Стерлитамак",
  "strezhevoy": "Стрежевой", "stupino": "Ступино", "suhoy-log": "Сухой Лог", "sunzha": "Сунжа", "surgut": "Сургут",
  "syzran": "Сызрань", "syktyvkar": "Сыктывкар", "tavda": "Тавда", "taganrog": "Таганрог", "tayshet": "Тайшет",
  "tambov": "Тамбов", "tver": "Тверь", "teykovo": "Тейково", "temryuk": "Темрюк", "tihoretsk": "Тихорецк",
  "tihvin": "Тихвин", "timashevsk": "Тимашёвск", "tobolsk": "Тобольск", "tolyatti": "Тольятти", "tomsk": "Томск",
  "torzhok": "Торжок", "tosno": "Тосно", "trehgornyy": "Трёхгорный", "troitsk": "Троицк", "tuapse": "Туапсе",
  "tula": "Тула", "tulun": "Тулун", "tutaev": "Тутаев", "tuymazy": "Туймазы", "tyumen": "Тюмень", "uchaly": "Учалы",
  "ufa": "Уфа", "uglich": "Углич", "uhta": "Ухта", "ulan-ude": "Улан-Удэ", "ulyanovsk": "Ульяновск", "uray": "Урай",
  "urus-martan": "Урус-Мартан", "uryupinsk": "Урюпинск", "usinsk": "Усинск", "usole-sibirskoe": "Усолье-Сибирское",
  "ussuriysk": "Уссурийск", "ust-dzheguta": "Усть-Джегута", "ust-ilimsk": "Усть-Илимск", "ust-kut": "Усть-Кут",
  "ust-labinsk": "Усть-Лабинск", "uzlovaya": "Узловая", "valuyki": "Валуйки", "velikie-luki": "Великие Луки",
  "velikiy-novgorod": "Великий Новгород", "verhnyaya-pyshma": "Верхняя Пышма", "verhnyaya-salda": "Верхняя Салда",
  "vidnoe": "Видное", "vladivostok": "Владивосток", "vladikavkaz": "Владикавказ", "vladimir": "Владимир",
  "volgodonsk": "Волгодонск", "volgograd": "Волгоград", "volhov": "Волхов", "vologda": "Вологда", "volsk": "Вольск",
  "volzhsk": "Волжск", "volzhskiy": "Волжский", "vorkuta": "Воркута", "voronezh": "Воронеж", "voskresensk": "Воскресенск",
  "votkinsk": "Воткинск", "vsevolozhsk": "Всеволожск", "vyazma": "Вязьма", "vyazniki": "Вязники", "vyborg": "Выборг",
  "vyksa": "Выкса", "vyshniy-volochek": "Вышний Волочёк", "yakutsk": "Якутск", "yalta": "Ялта",
  "yalutorovsk": "Ялуторовск", "yaroslavl": "Ярославль", "yartsevo": "Ярцево", "yoshkar-ola": "Йошкар-Ола",
  "yugorsk": "Югорск", "yurga": "Юрга", "yuzhno-sahalinsk": "Южно-Сахалинск", "yuzhnouralsk": "Южноуральск",
  "zainsk": "Заинск", "zarechnyy": "Заречный", "zarinsk": "Заринск", "zavolzhe": "Заволжье",
  "zelenodolsk": "Зеленодольск", "zelenogorsk": "Зеленогорск", "zelenograd": "Зеленоград",
  "zelenokumsk": "Зеленокумск", "zheleznogorsk": "Железногорск", "zhigulevsk": "Жигулёвск",
  "zhukovskiy": "Жуковский", "zlatoust": "Златоуст", "zvenigorod": "Звенигород", "krasnodar": "Краснодар",
  "kazan": "Казань", "rostov-na-donu": "Ростов-на-Дону", "chaykovskiy": "Чайковский", "chapaevsk": "Чапаевск",
  "chebarkul": "Чебаркуль", "cheboksary": "Чебоксары", "chelyabinsk": "Челябинск", "cheremhovo": "Черемхово",
  "cherepovets": "Череповец", "cherkessk": "Черкесск", "chernogorsk": "Черногорск", "chernushka": "Чернушка",
  "chernyahovsk": "Черняховск", "chehov": "Чехов", "chistopol": "Чистополь", "chita": "Чита", "chusovoy": "Чусовой",
  "shadrinsk": "Шадринск", "shali": "Шали", "sharypovo": "Шарыпово", "shatura": "Шатура", "shahty": "Шахты",
  "shebekino": "Шебекино", "shelehov": "Шелехов", "shuya": "Шуя", "schekino": "Щёкино", "schelkovo": "Щёлково",
  "scherbinka": "Щербинка", "elektrostal": "Электросталь", "elista": "Элиста", "engels": "Энгельс",
  "feodosiya": "Феодосия", "frolovo": "Фролово", "fryazino": "Фрязино", "habarovsk": "Хабаровск",
  "hanty-mansiysk": "Ханты-Мансийск", "hasavyurt": "Хасавюрт", "himki": "Химки"
};

// Функция перевода латиницы в кириллицу (на всякий случай, если добавишь город, которого нет в словаре)
function fallbackTransliterate(slug) {
  const map = {
    'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е', 'zh': 'ж', 'z': 'з', 'i': 'и', 'y': 'й', 'k': 'к',
    'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'f': 'ф', 'h': 'х',
    'c': 'ц', 'ch': 'ч', 'sh': 'ш', 'sch': 'щ', 'yy': 'ы', 'e': 'э', 'yu': 'ю', 'ya': 'я'
  };
  let result = slug;
  Object.keys(map).sort((a, b) => b.length - a.length).forEach(key => {
    result = result.split(key).join(map[key]);
  });
  return result.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

// 1. Автоматически сканируем папку geo/ на наличие созданных городов
if (!fs.existsSync(geoDir)) {
  fs.mkdirSync(geoDir, { recursive: true });
}

const slugs = fs.readdirSync(geoDir).filter(file => {
  try {
    return fs.statSync(path.join(geoDir, file)).isDirectory();
  } catch (e) {
    return false;
  }
});

// 2. Формируем список с чистыми русскими названиями
const cities = slugs.map(slug => {
  // Ищем полное совпадение в словаре
  let name = cityNamesRu[slug];
  
  // Если вдруг в папке появится совершенно новый город — переводим его автоматической функцией
  if (!name) {
    name = fallbackTransliterate(slug);
  }
  
  return { slug, name };
});

// Сортируем строго по русскому алфавиту
cities.sort((a, b) => a.name.localeCompare(b.name, 'ru'));

console.log(`Успешно просканировано городов в geo/: ${cities.length}`);

// 3. Генерируем HTML-сетку для модального окна
const citiesGridHtml = cities.map(city => 
  `<a href="/geo/${city.slug}/" class="city-item p-2 rounded-lg bg-slate-800/40 border border-slate-700/50 hover:border-cdek text-sm text-slate-300 hover:text-cdek transition-all text-center font-medium">${city.name}</a>`
).join('\n');

// 4. Внедряем собранный список в шапку сайта
if (fs.existsSync(headerPath)) {
  let headerHtml = fs.readFileSync(headerPath, 'utf-8');
  
  if (headerHtml.includes('{{CITIES_GRID}}')) {
    headerHtml = headerHtml.replace('{{CITIES_GRID}}', citiesGridHtml);
  } else {
    // Резервная замена, если маркер {{CITIES_GRID}} был удален
    headerHtml = headerHtml.replace(
      /(<div class="p-6 overflow-y-auto space-y-6 custom-scrollbar">[\s\S]*?<div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5">)[\s\S]*?(<\/div>)/,
      `$1\n${citiesGridHtml}\n$2`
    );
  }
  
  fs.writeFileSync(headerPath, headerHtml);
  console.log('Шапка сайта успешно обновлена полным русским списком.');
}

// 5. Обновляем карту сайта sitemap.xml для поисковиков
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
