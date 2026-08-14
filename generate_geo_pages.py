import os
import re
import json

# Полный список спец-городов из вашего оригинального файла
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
    "Березники": ("Березников", "Березниках", "в Березники"),
    "Шахты": ("Шахт", "Шахтах", "в Шахтах"),
}

FEMININE_SOFT_CITIES = {"Казань", "Пермь", "Тюмень", "Рязань", "Тверь", "Астрахань", "Керчь", "Сызрань"}

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
            html += f"""
          <a href="/geo/{slug}/{s['slug']}/" class="group flex flex-col h-full p-6 rounded-2xl bg-slate-800/40 border border-slate-700/50 hover:border-cdek/50 hover:bg-slate-800/60 transition-all duration-300">
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
