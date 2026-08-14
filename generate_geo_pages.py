import os
import re
import json

# Список городов для услуги "Сборный груз" (LTL)
LTL_CITIES = {
    "moskva", "sankt-peterburg", "krasnodar", "ekaterinburg", "novosibirsk", "kazan", 
    "nizhniy-novgorod", "chelyabinsk", "samara", "rostov-na-donu", "ufa", "omsk", 
    "voronezh", "perm", "volgograd", "tyumen", "saratov", "tolyatti", "izhevsk", 
    "barnaul", "ulyanovsk", "irkutsk", "khabarovsk", "yaroslavl", "vladivostok", 
    "makhachkala", "tomsk", "orenburg", "kemerovo", "novokuznetsk", "ryazan", 
    "naberezhnye-chelny", "astrakhan", "penza", "kirov", "lipetsk", "balashikha",
    "cheboksary", "kaliningrad", "tula", "kursk", "stavropol", "sevastopol", "sochi"
}

SPECIAL_CITIES = {
    "Сочи": ("Сочи", "Сочи", "в Сочи"),
    "Тольятти": ("Тольятти", "Тольятти", "в Тольятти"),
    "Улан-Удэ": ("Улан-Удэ", "Улан-Удэ", "в Улан-Удэ"),
    "Санкт-Петербург": ("Санкт-Петербурга", "Санкт-Петербурге", "в Санкт-Петербурге"),
    "Москва": ("Москвы", "Москве", "в Москве"),
    "Краснодар": ("Краснодара", "Краснодаре", "в Краснодаре")
}

def get_city_cases(city_name):
    city_name = city_name.strip()
    if city_name in SPECIAL_CITIES: return SPECIAL_CITIES[city_name]
    if city_name.endswith("а"): return city_name[:-1]+"ы", city_name[:-1]+"е", "в "+city_name[:-1]+"е"
    if city_name.endswith("я"): return city_name[:-1]+"и", city_name[:-1]+"е", "в "+city_name[:-1]+"е"
    return city_name+"а", city_name+"е", "в "+city_name+"е"

def build_services_grid(slug, prep_v):
    seo_path = os.path.join("scripts", "seo_data.json")
    if not os.path.exists(seo_path): return ""
    with open(seo_path, "r", encoding="utf-8") as f:
        services = json.load(f).get("services", [])
    
    # Целевые услуги для отображения в городах
    target_slugs = ["fbs", "dbs", "dogovor-ip", "unit-economy", "api-integration", "fulfillment", "kgt-delivery", "zabor-gruza", "packaging-services", "cargo-insurance"]
    if slug in LTL_CITIES: target_slugs.append("ltl-shipping")

    html = ""
    for s in services:
        if s["slug"] in target_slugs:
            html += f"""
          <a href="/geo/{slug}/{s['slug']}/" class="p-5 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-cdek/50 transition-all group">
            <h3 class="text-white font-bold group-hover:text-cdek transition-colors mb-2">{s['h1_main']}</h3>
            <p class="text-xs text-slate-400">{s['desc']}</p>
          </a>"""
    return html

def build_city_html(slug, city_name, pvz_count):
    gen, prep, prep_v = get_city_cases(city_name)
    services_grid = build_services_grid(slug, prep_v)
    
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>СДЭК для селлеров {prep_v}: логистика FBS/DBS | {city_name}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{ theme: {{ extend: {{ colors: {{ cdek: '#8de21a', dark: {{ 900: '#0b101d' }} }} }} }} }}
  </script>
</head>
<body class="bg-dark-900 text-slate-100 min-h-screen flex flex-col antialiased pb-16 md:pb-0">
  <!--#include virtual="/src/components/header.html" -->
  <main class="flex-grow pt-8 pb-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <nav class="text-sm text-slate-400 mb-6">
        <a href="/" class="hover:text-cdek">Главная</a> / <a href="/geo/" class="hover:text-cdek">Логистика</a> / <span class="text-white">{city_name}</span>
      </nav>
      <div class="text-center max-w-3xl mx-auto mb-12">
        <h1 class="text-4xl font-extrabold text-white mb-5">Подключение к СДЭК в <span class="text-cdek">{prep}</span></h1>
        <p class="text-lg text-slate-400">Специальные условия для бизнеса из {gen} при отгрузках на маркетплейсы. Скидки до 50% на доставку по моделям FBS и DBS.</p>
        <div class="grid grid-cols-3 gap-4 max-w-xl mx-auto mt-8 pt-6 border-t border-slate-800">
          <div><p class="text-3xl font-bold text-cdek">0 ₽</p><p class="text-xs text-slate-500">Договор</p></div>
          <div><p class="text-3xl font-bold text-white">до 50%</p><p class="text-xs text-slate-500">Экономия</p></div>
          <div><p class="text-3xl font-bold text-white">{pvz_count}</p><p class="text-xs text-slate-500">ПВЗ</p></div>
        </div>
      </div>
      <section class="mt-12 mb-16">
        <h2 class="text-2xl font-bold text-white mb-6">Условия логистики СДЭК {prep_v}</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {services_grid}
        </div>
      </section>
      <!--#include virtual="/src/components/calculator-widget.html" -->
      <section class="mt-16">
        <h2 class="text-2xl font-bold text-white mb-6">Карта ПВЗ в г. {city_name}</h2>
        <iframe src="https://yandex.ru/map-widget/v1/?text=СДЭК+ПВЗ+{city_name}" width="100%" height="400" frameborder="0"></iframe>
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
    
    print(f"Найдено {len(matches)} городов. Начинаю обновление...")
    for slug, name, pvz_str in matches:
        pvz_count = re.search(r"\d+", pvz_str).group() if re.search(r"\d+", pvz_str) else "3"
        html = build_city_html(slug, name.strip(), pvz_count)
        with open(os.path.join("geo", slug, "index.html"), "w", encoding="utf-8") as f: f.write(html)
    print("✅ Все страницы городов обновлены!")

if __name__ == "__main__":
    main()
