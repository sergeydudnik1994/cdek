import os
import re
import json

# Полный список спец-городов
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
    "Славянск-на-Кубани": ("Славянска-на-Кубани", "Славянске-на-Кубани", "в Славянске-на-Кубани"),
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

# Иконки для услуг
ICONS = {
    "fbs": '<path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "dbs": '<path d="M13 10V3L4 14h7v7l9-11h-7z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "dogovor-ip": '<path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "unit-economy": '<path d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "fulfillment": '<path d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "kgt-delivery": '<path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "zabor-gruza": '<path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "packaging-services": '<path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "api-integration": '<path d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "cargo-insurance": '<path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "ltl-shipping": '<path d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 011 1v2.5a.5.5 0 01-.5.5H13m-1-4h1m4-10h2a1 1 0 011 1v10a1 1 0 01-1 1h-1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
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
                gen_parts.append(part[:-2] + "кой" if part.endswith("ская") else part[:-2] + "ой")
                prep_parts.append(part[:-2] + "кой" if part.endswith("ская") else part[:-2] + "ой")
            elif part.endswith("ое") or part.endswith("ее"):
                gen_parts.append(part[:-2] + "ого"); prep_parts.append(part[:-2] + "ом")
            elif part.endswith("а"):
                if len(part) > 2 and part[-2] in "гкхжчшщ": gen_parts.append(part[:-1] + "и")
                else: gen_parts.append(part[:-1] + "ы")
                prep_parts.append(part[:-1] + "е")
            elif part.endswith(("ск", "ов", "ин", "бург", "град")):
                gen_parts.append(part + "а"); prep_parts.append(part + "е")
            else: gen_parts.append(part); prep_parts.append(part)
        return "-".join(gen_parts), "-".join(prep_parts)
    res_gen, res_prep = zip(*[process_word(w) for w in words])
    return " ".join(res_gen), " ".join(res_prep), f"{prep} {' '.join(res_prep)}"

def build_services_grid(slug):
    seo_path = os.path.join("scripts", "seo_data.json")
    if not os.path.exists(seo_path): return ""
    with open(seo_path, "r", encoding="utf-8") as f:
        services = json.load(f).get("services", [])
    target_slugs = ["fbs", "dbs", "dogovor-ip", "unit-economy", "fulfillment", "kgt-delivery", "zabor-gruza", "packaging-services", "api-integration", "cargo-insurance"]
    html = ""
    for s in services:
        if s["slug"] in target_slugs:
            icon_svg = ICONS.get(s["slug"], '<path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
            html += f"""
          <a href="/geo/{slug}/{s['slug']}/" class="group flex flex-col h-full p-6 rounded-2xl bg-slate-800/40 border border-slate-700/50 hover:border-cdek/50 hover:bg-slate-800/60 transition-all duration-300">
            <div class="h-10 w-10 bg-cdek/10 text-cdek rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">{icon_svg}</svg>
            </div>
            <h3 class="text-lg font-bold text-white group-hover:text-cdek transition-colors mb-3">{s['h1_main']}</h3>
            <p class="text-sm text-slate-400 leading-relaxed flex-grow">{s['desc']}</p>
          </a>"""
    return html

def build_city_html(slug, city_name, pvz_count):
    city_genitive, city_prepositional, prep_v = get_city_cases(city_name)
    services_grid = build_services_grid(slug)
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>СДЭК для селлеров {prep_v}: логистика FBS/DBS | {city_name}</title>
  <meta name="description" content="Официальное подключение к СДЭК в {city_prepositional}. Логистика для селлеров Wildberries, Ozon и Яндекс Маркет. Скидки до 50% и {pvz_count} ПВЗ для отгрузки." />
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{ theme: {{ extend: {{ colors: {{ cdek: '#8de21a', dark: {{ 900: '#0b101d' }} }} }} }} }}
  </script>
</head>
<body class="bg-dark-900 text-slate-100 min-h-screen flex flex-col antialiased pb-16 md:pb-0">
  <!--#include virtual="/src/components/header.html" -->
  <main class="flex-grow pt-8 pb-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <nav class="text-sm text-slate-400 mb-8">
        <a href="/" class="hover:text-cdek transition-colors">Главная</a> / <a href="/geo/" class="hover:text-cdek transition-colors">Логистика</a> / <span class="text-white">{city_name}</span>
      </nav>
      <div class="text-center max-w-3xl mx-auto mb-16">
        <h1 class="text-4xl md:text-5xl font-extrabold text-white mb-6">Подключение к СДЭК в <span class="text-cdek">{city_prepositional}</span></h1>
        <p class="text-lg text-slate-400 leading-relaxed">Специальные условия логистики для бизнеса из {city_genitive} при отгрузках на маркетплейсы. Бесплатный договор и скидки до 50% на доставку по моделям FBS и DBS.</p>
        <div class="grid grid-cols-3 gap-4 max-w-xl mx-auto mt-10 pt-8 border-t border-slate-800">
          <div><p class="text-3xl font-bold text-cdek">0 ₽</p><p class="text-xs text-slate-500 uppercase tracking-wider mt-1">Договор</p></div>
          <div><p class="text-3xl font-bold text-white">до 50%</p><p class="text-xs text-slate-500 uppercase tracking-wider mt-1">Экономия</p></div>
          <div><p class="text-3xl font-bold text-white">{pvz_count}</p><p class="text-xs text-slate-500 uppercase tracking-wider mt-1">ПВЗ</p></div>
        </div>
      </div>
      <section class="mb-20">
        <h2 class="text-2xl font-bold text-white mb-8">Условия логистики СДЭК {prep_v}</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">{services_grid}</div>
      </section>
      <!--#include virtual="/src/components/calculator-widget.html" -->
      <section class="mt-20">
        <h2 class="text-2xl font-bold text-white mb-8">Карта пунктов выдачи в г. {city_name}</h2>
        <div class="rounded-2xl overflow-hidden border border-slate-800 shadow-2xl">
          <iframe src="https://yandex.ru/map-widget/v1/?text=СДЭК+ПВЗ+{city_name}" width="100%" height="450" frameborder="0"></iframe>
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
    print(f"✅ Успешно обновлено {len(matches)} страниц городов!")

if __name__ == "__main__":
    main()
