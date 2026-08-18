import os
import json
import random
import re

TOP_50_CITIES = [
    {"slug": "moskva", "name": "Москва"},
    {"slug": "sankt-peterburg", "name": "Санкт-Петербург"},
    {"slug": "novosibirsk", "name": "Новосибирск"},
    {"slug": "ekaterinburg", "name": "Екатеринбург"},
    {"slug": "kazan", "name": "Казань"},
    {"slug": "nizhniy-novgorod", "name": "Нижний Новгород"},
    {"slug": "krasnoyarsk", "name": "Красноярск"},
    {"slug": "chelyabinsk", "name": "Челябинск"},
    {"slug": "samara", "name": "Самара"},
    {"slug": "ufa", "name": "Уфа"},
    {"slug": "rostov-na-donu", "name": "Ростов-на-Дону"},
    {"slug": "omsk", "name": "Омск"},
    {"slug": "krasnodar", "name": "Краснодар"},
    {"slug": "voronezh", "name": "Воронеж"},
    {"slug": "perm", "name": "Пермь"},
    {"slug": "volgograd", "name": "Волгоград"},
    {"slug": "saratov", "name": "Саратов"},
    {"slug": "tyumen", "name": "Тюмень"},
    {"slug": "tolyatti", "name": "Тольятти"},
    {"slug": "barnaul", "name": "Барнаул"},
    {"slug": "izhevsk", "name": "Ижевск"},
    {"slug": "mahachkala", "name": "Махачкала"},
    {"slug": "habarovsk", "name": "Хабаровск"},
    {"slug": "ulyanovsk", "name": "Ульяновск"},
    {"slug": "irkutsk", "name": "Иркутск"},
    {"slug": "vladivostok", "name": "Владивосток"},
    {"slug": "yaroslavl", "name": "Ярославль"},
    {"slug": "kemerovo", "name": "Кемерово"},
    {"slug": "tomsk", "name": "Томск"},
    {"slug": "naberezhnye-chelny", "name": "Набережные Челны"},
    {"slug": "sevastopol", "name": "Севастополь"},
    {"slug": "stavropol", "name": "Ставрополь"},
    {"slug": "orenburg", "name": "Оренбург"},
    {"slug": "novokuznetsk", "name": "Новокузнецк"},
    {"slug": "ryazan", "name": "Рязань"},
    {"slug": "balashiha", "name": "Балашиха"},
    {"slug": "penza", "name": "Пенза"},
    {"slug": "cheboksary", "name": "Чебоксары"},
    {"slug": "lipetsk", "name": "Липецк"},
    {"slug": "kaliningrad", "name": "Калининград"},
    {"slug": "astrahan", "name": "Астрахань"},
    {"slug": "tula", "name": "Тула"},
    {"slug": "kirov", "name": "Киров"},
    {"slug": "sochi", "name": "Сочи"},
    {"slug": "kursk", "name": "Курск"},
    {"slug": "ivanovo", "name": "Иваново"},
    {"slug": "surgut", "name": "Сургут"},
    {"slug": "tver", "name": "Тверь"},
    {"slug": "magnitogorsk", "name": "Магнитогорск"},
    {"slug": "bryansk", "name": "Брянск"}
]

SPECIAL_CITIES = {
    "Сочи": ("Сочи", "Сочи", "в Сочи"),
    "Тольятти": ("Тольятти", "Тольятти", "в Тольятти"),
    "Улан-Удэ": ("Улан-Удэ", "Улан-Удэ", "в Улан-Удэ"),
    "Надым": ("Надыма", "Надыме", "в Надыме"),
    "Санкт-Петербург": ("Санкт-Петербурга", "Санкт-Петербурге", "в Санкт-Петербурге"),
    "Москва": ("Москвы", "Москве", "в Москве"),
    "Нижний Новгород": ("Нижнего Новгорода", "Нижнем Новгороде", "в Нижнем Новгороде"),
    "Великий Новгород": ("Великого Новгорода", "Великом Новгороде", "в Великом Новгороде"),
    "Старый Оскол": ("Старого Оскола", "Старом Осколе", "в Старом Осколе"),
    "Красное Село": ("Красного Села", "Красном Селе", "в Красном Селе"),
    "Набережные Челны": ("Набережных Челнов", "Набережных Челнах", "в Набережных Челнах"),
    "Минеральные Воды": ("Минеральных Вод", "Минеральных Водах", "в Минеральных Водах"),
    "Гусь-Хрустальный": ("Гусь-Хрустального", "Гусь-Хрустальном", "в Гусь-Хрустальном"),
    "Ростов-на-Дону": ("Ростова-на-Дону", "Ростове-на-Дону", "в Ростове-на-Дону"),
    "Иваново": ("Иванова", "Иванове", "в Иваново"),
    "Кемерово": ("Кемерова", "Кемерове", "в Кемерово"),
}

FEMININE_SOFT_CITIES = {"Казань", "Пермь", "Тюмень", "Рязань", "Тверь", "Астрахань", "Керчь", "Сызрань"}

INDUSTRIES = [
    {"slug": "odezhda-i-obuv", "title": "Логистика для магазинов одежды и обуви", "desc": "Доставка fashion-товаров с примеркой, частичным выкупом и возвратом невыкупленного ассортимента."},
    {"slug": "mebel-i-interer", "title": "Доставка мебели и товаров для дома", "desc": "Надежная транспортировка крупногабаритных товаров, корпусной мебели и предметов интерьера."},
    {"slug": "elektronika-i-tehnika", "title": "Логистика электроники и техники", "desc": "Особые регламенты для бытовой техники и электроники: полное страхование и усиленная упаковка."},
    {"slug": "detskie-tovary", "title": "Доставка детских товаров и игрушек", "desc": "Своевременная доставка товаров для детей по схемам FBS и DBS с соблюдением требований маркетплейсов."},
    {"slug": "kosmetika-i-parfyumeriya", "title": "Логистика для магазинов косметики", "desc": "Бережная доставка парфюмерии и уходовой косметики с соблюдением стандартов упаковки Wildberries и Ozon."},
    {"slug": "avtotovary-i-zapchasti", "title": "Доставка автотоваров и запчастей", "desc": "Перевозка автозапчастей, масел и автохимии до сортировочных центров и конечных покупателей."},
    {"slug": "tovary-dlya-zhivotnyh", "title": "Логистика для зоомагазинов", "desc": "Регулярная доставка кормов, наполнителей и аксессуаров для животных по выгодным B2B-тарифам."},
    {"slug": "sporttovary", "title": "Доставка спортивных товаров", "desc": "Транспортировка тренажеров, спортинвентаря и экипировки любой массы и габаритов."},
    {"slug": "stroitelstvo-i-remont", "title": "Логистика товаров для ремонта и DIY", "desc": "Надежное решение для поставщиков стройматериалов: отгрузка КГТ и доставка до двери покупателя."},
    {"slug": "produkty-pitaniya", "title": "Доставка продуктов питания (Dry Food)", "desc": "Логистика бакалеи, чая, кофе и снеков с длительным сроком хранения без нарушения товарного вида."},
    {"slug": "osveshchenie-i-svet", "title": "Доставка освещения и светильников", "desc": "Специальная обрешетка и воздушно-пузырьковая упаковка для люстр, бра и хрупких ламп."},
    {"slug": "kantstovary-i-ofis", "title": "Логистика канцтоваров и товаров для офиса", "desc": "Экономичные тарифы на мелкогабаритные посылки и комплекты канцтоваров для селлеров."},
    {"slug": "sad-i-ogorod", "title": "Логистика товаров для сада и дачи", "desc": "Сезонные решения по отгрузке садовой техники, грунтов и инструментов на склады маркетплейсов."},
    {"slug": "tovary-dlya-tvorchestva", "title": "Логистика товаров для творчества и хобби", "desc": "Фулфилмент, сборка и доставка заказов для магазинов рукоделия и товаров для художников."},
    {"slug": "bizhuteriya-i-aksessuary", "title": "Доставка бижутерии и аксессуаров", "desc": "Специальные условия страхования и выдача малогабаритных отправлений в 4 000+ ПВЗ."},
    {"slug": "instrumenty", "title": "Логистика ручного и электроинструмента", "desc": "Доставка строительного и профессионального инструмента по всей России по схемам FBS и DBS."},
    {"slug": "bytovaya-tekhnika", "title": "Доставка крупной бытовой техники", "desc": "Специальные условия перевозки холодильников, стиральных машин и плит с подъемом на этаж."},
    {"slug": "tovary-dlya-zdorovya", "title": "Доставка товаров для здоровья и ортопедии", "desc": "Соблюдение температурных режимов, быстрая отгрузка и аккуратная доставка покупателям."},
    {"slug": "avtoelektronika", "title": "Доставка автоэлектроники и видеорегистраторов", "desc": "Безопасная транспортировка высокотехнологичных гаджетов и головных устройств."},
    {"slug": "turizm-i-otdykh", "title": "Логистика товаров для туризма и кемпинга", "desc": "Отгрузка палаток, рюкзаков и туристической экипировки в сезон пиковых продаж."},
    {"slug": "podarki-i-suveniry", "title": "Доставка подарков и сувенирной продукции", "desc": "Гарантированные сроки доставки в предпраздничные периоды и высокий сезон продаж."},
    {"slug": "muzykalnye-instrumenty", "title": "Доставка музыкальных инструментов", "desc": "Индивидуальная защитная упаковка и страхование акустических и электронных инструментов."},
    {"slug": "santekhnika", "title": "Логистика сантехники и смесителей", "desc": "Перевозка ванн, раковин, душевых систем и инсталляций без сколов и повреждений."},
    {"slug": "umnyy-dom", "title": "Логистика оборудования для умного дома", "desc": "Срочная курьерская доставка датчиков, умных колонок и контроллеров до двери."},
    {"slug": "tekstil-dlya-doma", "title": "Доставка домашнего текстиля и постельного белья", "desc": "Оптимизация объемного веса текстильных изделий для снижения тарифа доставки."},
    {"slug": "klimaticheskaya-tekhnika", "title": "Доставка климатической техники и кондиционеров", "desc": "Транспортировка сплит-систем, обогревателей и увлажнителей по B2B-тарифам."},
    {"slug": "posuda-i-kuhnya", "title": "Доставка посуды и кухонных принадлежностей", "desc": "Усиленная упаковка стеклянной, керамической и чугунной посуды с гарантией сохранности."},
    {"slug": "rybalka-i-okhota", "title": "Логистика товаров для рыбалки и охоты", "desc": "Транспортировка удилищ, катушек, спецодежды и охотничьего снаряжения."},
    {"slug": "igrovye-pristavki", "title": "Доставка игровых консолей и видеоигр", "desc": "Полное страхование объявленной ценности и экспресс-доставка консолей и аксессуаров."},
    {"slug": "kantstovary", "title": "Доставка полиграфии и бумажной продукции", "desc": "Отгрузка крупных партий полиграфии и бумаги на склады маркетплейсов по паллетам."},
    {"slug": "aksessuary-dlya-smartfonov", "title": "Доставка чехлов и мобильных аксессуаров", "desc": "Минимальные тарифы на легкие отправления до 1 кг от 136.5 ₽ при интеграции по API."},
    {"slug": "elektrosamokaty-i-velosipedy", "title": "Доставка электротранспорта и велосипедов", "desc": "Специализированная перевозка электросамокатов и велосипедов с литиевыми аккумуляторами."}
]

def get_city_cases(city_name):
    city_name = city_name.strip()
    if city_name in SPECIAL_CITIES: return SPECIAL_CITIES[city_name]
    prep = "во" if city_name.startswith(("Владимир", "Владивосток", "Владикавказ", "Всеволожск")) else "в"
    words = city_name.split()
    def process_word(w):
        parts = w.split("-")
        gen_parts, prep_parts = [], []
        for idx, part in enumerate(parts):
            if len(parts) > 1 and idx == 0 and part.endswith("о"):
                gen_parts.append(part); prep_parts.append(part); continue
            if part in FEMININE_SOFT_CITIES:
                gen_parts.append(part[:-1] + "и"); prep_parts.append(part[:-1] + "и")
            elif part.endswith("ий"):
                gen_parts.append(part[:-2] + "его" if part == "Нижний" else part[:-2] + "ого")
                prep_parts.append(part[:-2] + "ем" if part == "Нижний" else part[:-2] + "ом")
            elif part.endswith("ый") or part.endswith("ой"):
                gen_parts.append(part[:-2] + "ого"); prep_parts.append(part[:-2] + "ом")
            elif part.endswith("ая"):
                gen_parts.append(part[:-2] + "ой"); prep_parts.append(part[:-2] + "ой")
            elif part.endswith("ое") or part.endswith("ее"):
                gen_parts.append(part[:-2] + "ого"); prep_parts.append(part[:-2] + "ом")
            elif part.endswith("а"):
                gen_parts.append(part[:-1] + "и" if len(part) > 2 and part[-2] in "гкхжчшщ" else part[:-1] + "ы")
                prep_parts.append(part[:-1] + "е")
            elif part.endswith("я"):
                gen_parts.append(part[:-1] + "и"); prep_parts.append(part[:-1] + "и" if part.endswith("ия") else part[:-1] + "е")
            elif part.endswith("о"):
                gen_parts.append(part[:-1] + "а"); prep_parts.append(part[:-1] + "е")
            elif part.endswith("е"):
                gen_parts.append(part[:-1] + "я"); prep_parts.append(part[:-1] + "е")
            elif part.endswith("ь"):
                gen_parts.append(part[:-1] + "я"); prep_parts.append(part[:-1] + "е")
            elif re.search(r"[бвгджзклмнпрстфхцчшщ]$", part, re.I):
                gen_parts.append(part + "а"); prep_parts.append(part + "е")
            else:
                gen_parts.append(part); prep_parts.append(part)
        return "-".join(gen_parts), "-".join(prep_parts)
    gen_words, prep_words = [], []
    for word in words:
        gw, pw = process_word(word)
        gen_words.append(gw); prep_words.append(pw)
    return " ".join(gen_words), " ".join(prep_words), f"{prep} {' '.join(prep_words)}"

def generate_industry_geo():
    host = "https://cdek-marketplace.ru"
    print(f"🚀 Генерация отраслевой гео-матрицы (ТОП-50 городов × 32 ниши)...")
    
    total_count = 0
    for city in TOP_50_CITIES:
        c_slug, c_name = city["slug"], city["name"]
        gen, prep, prep_v = get_city_cases(c_name)
        
        nearby = random.sample(TOP_50_CITIES, 5)
        
        for ind in INDUSTRIES:
            ind_slug = ind["slug"]
            ind_title = ind["title"]
            ind_desc = ind["desc"]
            
            canonical_url = f"{host}/geo/{c_slug}/solutions/{ind_slug}/"
            seo_title = f"{ind_title} {prep_v} | СДЭК Маркетплейсы"
            seo_desc = f"{ind_title} {prep_v}. {ind_desc} Спецтарифы для селлеров Wildberries, Ozon, Яндекс Маркета со скидкой до 50%."
            h1 = f"{ind_title} <span class='text-cdek'>{prep_v}</span>"
            
            links_html = " ".join([f"<a href='/geo/{c['slug']}/solutions/{ind_slug}/' class='text-cdek hover:underline mr-3'>{c['name']}</a>" for c in nearby])
            
            html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{seo_title}</title>
  <meta name="description" content="{seo_desc}" />
  <meta name="theme-color" content="#8DE21A" />
  <link rel="canonical" href="{canonical_url}" />
  
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="СДЭК Маркетплейсы" />
  <meta property="og:title" content="{seo_title}" />
  <meta property="og:description" content="{seo_desc}" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:image" content="{host}/logo.png" />
  <link rel="icon" type="image/png" href="/favicon.png" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Главная", "item": "{host}/" }},
          {{ "@type": "ListItem", "position": 2, "name": "Отраслевые решения", "item": "{host}/solutions/" }},
          {{ "@type": "ListItem", "position": 3, "name": "{ind_title}", "item": "{host}/solutions/{ind_slug}/" }},
          {{ "@type": "ListItem", "position": 4, "name": "{c_name}", "item": "{canonical_url}" }}
        ]
      }},
      {{
        "@type": "Service",
        "name": "{ind_title} {prep_v}",
        "provider": {{ "@type": "Organization", "name": "СДЭК Маркетплейсы", "url": "{host}/" }},
        "areaServed": {{ "@type": "City", "name": "{c_name}" }},
        "description": "{ind_desc}"
      }}
    ]
  }}
  </script>

  <script src="https://cdn.tailwindcss.com"></script>
  <script>tailwind.config={{theme:{{extend:{{colors:{{cdek:'#8de21a',dark:{{900:'#0b101d'}}}}}}}}}}</script>
</head>
<body class="bg-dark-900 text-slate-100 min-h-screen flex flex-col antialiased pb-16 md:pb-0">
  <!--#include virtual="/src/components/header.html" -->
  <main class="flex-grow">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 pb-12 sm:pt-10 sm:pb-16">
      <nav class="text-xs sm:text-sm text-slate-400 mb-6 flex flex-wrap items-center gap-1.5">
        <a href="/" class="hover:text-cdek transition-colors">Главная</a> <span>/</span>
        <a href="/solutions/" class="hover:text-cdek transition-colors">Решения</a> <span>/</span>
        <a href="/solutions/{ind_slug}/" class="hover:text-cdek transition-colors">{ind_title}</a> <span>/</span>
        <span class="text-white">{c_name}</span>
      </nav>

      <div class="grid lg:grid-cols-[1.1fr_0.9fr] gap-10 items-start">
        <section class="flex flex-col items-start">
          <div class="inline-flex items-center gap-2 px-3.5 py-1.5 mb-6 rounded-full text-xs font-semibold tracking-wide uppercase border bg-cdek/10 text-cdek border-cdek/30">
            <span>Отраслевая логистика для маркетплейсов</span>
          </div>

          <h1 class="text-3xl sm:text-4xl lg:text-5xl font-bold text-white leading-tight mb-5">
            {h1}
          </h1>

          <p class="text-slate-300 text-base sm:text-lg leading-relaxed mb-6">
            {ind_desc} Подключение селлеров из {gen} к логистической сети СДЭК со скидками на B2B-договоры до 50%.
          </p>

          <div class="grid grid-cols-3 gap-4 py-6 border-y border-slate-800 w-full mb-8">
            <div>
              <p class="text-xl sm:text-2xl font-black text-cdek">от 136.5 ₽</p>
              <p class="text-xs text-slate-400">Спецтариф DBS</p>
            </div>
            <div>
              <p class="text-xl sm:text-2xl font-black text-white">4 000+</p>
              <p class="text-xs text-slate-400">ПВЗ по России</p>
            </div>
            <div>
              <p class="text-xl sm:text-2xl font-black text-white">15 мин</p>
              <p class="text-xs text-slate-400">Оформление договора</p>
            </div>
          </div>

          <div class="p-6 rounded-2xl bg-slate-800/40 border border-slate-700/50 text-slate-300 text-sm leading-relaxed mb-8 w-full">
            <h3 class="text-white font-bold text-base mb-2">Особенности отгрузки {prep_v}:</h3>
            <p>Сдавайте заказы по реестру без очередей в ближайших пунктах СДЭК {prep_v} или закажите ежедневный забор партий курьером со склада поставщика. Полная интеграция статусов доставки с кабинетами Wildberries, Ozon, Яндекс Маркета и Авито.</p>
          </div>
        </section>

        <section class="relative w-full max-w-xl mx-auto lg:ml-auto" id="leadForm">
          <!--#include virtual="/src/components/leadform.html" -->
        </section>
      </div>

      <section class="mt-12">
        <!--#include virtual="/src/components/calculator-widget.html" -->
      </section>

      <section class="mt-16 pt-8 border-t border-slate-800">
        <h3 class="text-base font-semibold text-white mb-3">Эта услуга в других городах:</h3>
        <div class="flex flex-wrap gap-2 text-sm">
          {links_html}
        </div>
      </section>
    </div>
  </main>
  <!--#include virtual="/src/components/footer.html" -->
</body>
</html>"""
            
            out_dir = os.path.join("geo", c_slug, "solutions", ind_slug)
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(html)
            total_count += 1

    print(f"✅ Успешно сгенерировано {total_count} отраслевых гео-страниц.")

if __name__ == "__main__":
    generate_industry_geo()
