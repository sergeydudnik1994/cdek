import os
import re
import json
import random

SPECIAL_CITIES = {
    "Сочи": ("Сочи", "Сочи", "в Сочи"),
    "Тольятти": ("Тольятти", "Тольятти", "в Тольятти"),
    "Улан-Удэ": ("Улан-Удэ", "Улан-Удэ", "в Улан-Удэ"),
    "Надым": ("Надыма", "Надыме", "в Надыме"),
    "Санкт-Петербург": ("Санкт-Петербурга", "Санкт-Петербурге", "в Санкт-Петербурге"),
    "Нижний Новгород": ("Нижнего Новгорода", "Нижнем Новгороде", "в Нижнем Новгороде"),
    "Великий Новгород": ("Великого Новгорода", "Великом Новгороде", "в Великом Новгороде"),
    "Старый Оскол": ("Старого Оскола", "Старом Осколе", "в Старом Осколе"),
    "Красное Село": ("Красного Села", "Красном Селе", "в Красном Селе"),
    "Набережные Челны": ("Набережных Челнов", "Набережных Челнах", "в Набережных Челнах"),
    "Минеральные Воды": ("Минеральных Вод", "Минеральных Водах", "в Минеральных Водах"),
    "Гусь-Хрустальный": ("Гусь-Хрустального", "Гусь-Хрустальном", "в Гусь-Хрустальном"),
    "Ростов-на-Дону": ("Ростова-на-Дону", "Ростове-на-Дону", "в Ростове-на-Дону"),
    "Комсомольск-на-Амуре": ("Комсомольска-на-Амуре", "Комсомольске-на-Амуре", "в Комсомольске-на-Амуре"),
    "Славянск-на-Кубани": ("Славянска-на-Кубани", "Славянске-на-Кубани", "в Славянск-на-Кубани"),
    "Горячий Ключ": ("Горячего Ключа", "Горячем Ключе", "в Горячем Ключе"),
    "Сергиев Посад": ("Сергиева Посада", "Сергиевом Посаде", "в Сергиевом Посаде"),
    "Орехово-Зуево": ("Орехово-Зуева", "Орехово-Зуеве", "в Орехово-Зуеве"),
    "Переславль-Залесский": ("Переславля-Залесского", "Переславле-Залесском", "в Переславле-Залесском"),
    "Каменск-Уральский": ("Каменска-Уральского", "Каменске-Уральском", "в Каменске-Уральском"),
    "Каменск-Шахтинский": ("Каменска-Шахтинского", "Каменске-Шахтинском", "в Каменске-Шахтинском"),
    "Камень-на-Оби": ("Камня-на-Оби", "Камне-на-Оби", "в Камне-на-Оби"),
    "Новый Уренгой": ("Нового Уренгоя", "Новом Уренгое", "в Новом Уренгое"),
    "Великие Луки": ("Великих Лук", "Великих Луках", "в Великих Луках"),
    "Анжеро-Судженск": ("Анжеро-Судженска", "Анжеро-Судженске", "в Анжеро-Судженске"),
    "Аргун": ("Аргуна", "Аргуне", "в Аргуне"),
    "Химки": ("Химок", "Химках", "в Химках"),
    "Мытищи": ("Мытищ", "Мытищах", "в Мытищах"),
    "Чебоксары": ("Чебоксар", "Чебоксарах", "в Чебоксарах"),
    "Люберцы": ("Люберец", "Люберцах", "в Люберцах"),
    "Березники": ("Березников", "Березниках", "в Березниках"),
    "Шахты": ("Шахт", "Шахтах", "в Шахтах"),
}

FEMININE_SOFT_CITIES = {"Казань", "Пермь", "Тюмень", "Рязань", "Тверь", "Астрахань", "Керчь", "Сызрань"}

# Уникальные иконки для каждой из 24 услуг
SERVICE_ICONS = {
    "fbs": '<path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "dbs": '<path d="M13 10V3L4 14h7v7l9-11h-7z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "dogovor-ip": '<path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "unit-economy": '<path d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "fulfillment": '<path d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "cross-docking": '<path d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "zabor-gruza": '<path d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 011 1v1m4-1a1 1 0 011 1v1m-1-4h3a1 1 0 011 1v3M9 20a1 1 0 100-2 1 1 0 000 2zm10 0a1 1 0 100-2 1 1 0 000 2z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "ltl-shipping": '<path d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z"/><path d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 011 1v1m4-1a1 1 0 011 1v1m-1-4h3a1 1 0 011 1v3M17 11l-4-6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "kgt-delivery": '<path d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "cis-delivery": '<path d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "express-delivery": '<path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "returns-management": '<path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "packaging-services": '<path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "api-integration": '<path d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "cargo-insurance": '<path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "logistics-analytics": '<path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "storage-services": '<path d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "labeling-chestny-znak": '<path d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "courier-for-shops": '<path d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "pudo-delivery": '<path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "last-mile": '<path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "magistral-delivery": '<path d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z"/><path d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 011 1v1m4-1a1 1 0 011 1v1m-1-4h3a1 1 0 011 1v3M17 11l-4-6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "sorting-center": '<path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "cash-on-delivery": '<path d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
}

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

def build_city_html(slug, city_name, pvz_count):
    city_genitive, city_prepositional, prep_v = get_city_cases(city_name)
    with open("scripts/seo_data.json", "r", encoding="utf-8") as f: data = json.load(f)
    
    services_grid = ""
    for s in data["services"][:12]:
        icon = SERVICE_ICONS.get(s["slug"], SERVICE_ICONS["fbs"])
        services_grid += f"""
          <a href="/geo/{slug}/{s['slug']}/" class="group flex flex-col h-full p-5 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-cdek/50 transition-all">
            <div class="h-10 w-10 bg-cdek/10 text-cdek rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">{icon}</svg>
            </div>
            <h3 class="text-white font-bold group-hover:text-cdek transition-colors mb-2">{s['h1_main'].split(' в ')[0]}</h3>
            <p class="text-xs text-slate-400 leading-relaxed flex-grow">{s['desc']}</p>
          </a>"""

    rating_value = round(random.uniform(4.7, 4.9), 1)
    review_count = random.randint(150, 480)

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>СДЭК для селлеров {prep_v}: логистика FBS/DBS | Маркетплейсы</title>
  <meta name="description" content="Официальный договор со СДЭК для селлеров из {city_genitive}. Отгрузка через {pvz_count} ПВЗ {prep_v}. Интеграция с Wildberries, Ozon, Яндекс Маркетом и Авито. Скидки на логистику до 50%." />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "СДЭК для маркетплейсов {prep_v}",
    "url": "https://cdek-marketplace.ru/geo/{slug}/",
    "logo": "https://cdek-marketplace.ru/logo.png",
    "telephone": "+7-993-322-15-20",
    "priceRange": "₽₽",
    "address": {{ "@type": "PostalAddress", "addressLocality": "{city_name}", "addressCountry": "RU" }},
    "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "{rating_value}", "reviewCount": "{review_count}" }},
    "makesOffer": {{
      "@type": "Offer",
      "itemOffered": {{
        "@type": "Service",
        "name": "Подключение селлеров к логистике СДЭК {prep_v}",
        "description": "Логистика для Wildberries, Ozon, Яндекс Маркета через {pvz_count} ПВЗ {prep_v}."
      }}
    }}
  }}
  </script>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>tailwind.config={{theme:{{extend:{{colors:{{cdek:'#8de21a',dark:{{900:'#0b101d'}}}}}}}}}}</script>
</head>
<body class="bg-dark-900 text-slate-100 min-h-screen flex flex-col antialiased">
  <!--#include virtual="/src/components/header.html" -->
  <main class="flex-grow pt-8 pb-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <nav class="text-sm text-slate-400 mb-6">
        <a href="/" class="hover:text-cdek transition-colors">Главная</a> <span class="mx-2">/</span>
        <a href="/geo/" class="hover:text-cdek transition-colors">Логистика</a> <span class="mx-2">/</span>
        <span class="text-white">{city_name}</span>
      </nav>
      <div class="text-center max-w-3xl mx-auto mb-12">
        <h1 class="text-3xl sm:text-5xl font-extrabold text-white mb-5">СДЭК в <span class="text-cdek">{city_prepositional}</span> для селлеров</h1>
        <p class="text-lg text-slate-400">Скидки до 50% на FBS и DBS для бизнеса из {city_genitive}. Бесплатный договор за 15 минут.</p>
        <div class="grid grid-cols-3 gap-4 mt-8 pt-6 border-t border-slate-800">
          <div><p class="text-2xl font-bold text-cdek">0 ₽</p><p class="text-xs text-slate-500">Договор</p></div>
          <div><p class="text-2xl font-bold text-white">до 50%</p><p class="text-xs text-slate-500">Экономия</p></div>
          <div><p class="text-2xl font-bold text-white">{pvz_count}</p><p class="text-xs text-slate-500">ПВЗ</p></div>
        </div>
      </div>
      <section class="mb-16">
        <h2 class="text-2xl font-bold text-white mb-8">Услуги логистики {prep_v}</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {services_grid}
        </div>
      </section>
      <!--#include virtual="/src/components/calculator-widget.html" -->
      <section class="mt-16">
        <h2 class="text-2xl font-bold text-white mb-6">Карта ПВЗ {prep_v}</h2>
        <div class="rounded-xl overflow-hidden border border-slate-800 shadow-lg">
          <iframe src="https://yandex.ru/map-widget/v1/?text=СДЭК+ПВЗ+{city_name}" width="100%" height="400" frameborder="0"></iframe>
        </div>
      </section>
    </div>
  </main>
  <!--#include virtual="/src/components/footer.html" -->
</body>
</html>"""

def main( ):
    geo_index = os.path.join("geo", "index.html")
    if not os.path.exists(geo_index): return
    with open(geo_index, "r", encoding="utf-8") as f: content = f.read()
    matches = re.findall(r'href="/geo/([^/]+)/".*?<span[^>]*>([^<]+)</span>\s*<span[^>]*>([^<]+)</span>', content, re.DOTALL)
    for slug, name, pvz_str in matches:
        pvz_count = re.search(r"\d+", pvz_str).group() if re.search(r"\d+", pvz_str) else "3"
        html = build_city_html(slug, name.strip(), pvz_count)
        os.makedirs(os.path.join("geo", slug), exist_ok=True)
        with open(os.path.join("geo", slug, "index.html"), "w", encoding="utf-8") as f: f.write(html)
    print(f"✅ Обновлено {len(matches)} страниц городов!")

if __name__ == "__main__":
    main()
