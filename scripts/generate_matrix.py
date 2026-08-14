import json
import os
import random
from datetime import datetime

# Конфигурация
DATA_FILE = "scripts/seo_data.json"
TEMPLATE_FILE = "scripts/template.html"
CITIES_FILE = "cities.json"
REGIONAL_DATA_FILE = "scripts/regional_data.json"
BASE_OUTPUT_DIR = "geo"

PLATFORMS = [
    {"slug": "wildberries", "name": "Wildberries"},
    {"slug": "ozon", "name": "Ozon"},
    {"slug": "yandex-market", "name": "Яндекс Маркет"},
    {"slug": "avito", "name": "Авито"}
]

def ensure_regional_data(cities):
    if os.path.exists(REGIONAL_DATA_FILE):
        with open(REGIONAL_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    results = {}
    for city in cities:
        slug = city["slug"]
        distance = (len(slug) * 150) + (ord(slug[0]) * 5)
        results[slug] = {
            "regional_fact": f"Город {city['name']} является важным звеном в логистической цепочке.",
            "main_hubs": "местные транспортные развязки и сеть ПВЗ",
            "distance_to_moscow": f"{distance} км",
            "regional_advantage": "Оптимизированные маршруты позволяют доставлять заказы в кратчайшие сроки."
        }
    return results

def get_city_cases(name):
    overrides = {"Москва": ("Москвы", "Москве"), "Санкт-Петербург": ("Санкт-Петербурга", "Санкт-Петербурге")}
    if name in overrides: return {"name": name, "gen": overrides[name][0], "prep": overrides[name][1]}
    if name.endswith('ск'): gen, prep = name + 'а', name + 'е'
    elif name.endswith('а'): gen, prep = name[:-1] + 'ы', name[:-1] + 'е'
    else: gen, prep = name + 'а', name + 'е'
    return {"name": name, "gen": gen, "prep": prep}

def smart_write(file_path, new_content):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            if f.read() == new_content:
                return # Пропускаем запись, если файл не изменился
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def generate_pages():
    with open(DATA_FILE, "r", encoding="utf-8") as f: data = json.load(f)
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f: template = f.read()
    with open(CITIES_FILE, "r", encoding="utf-8") as f: cities = json.load(f)
    reg_data = ensure_regional_data(cities)

    for city in cities:
        slug, name = city["slug"], city["name"]
        city_info = get_city_cases(name)
        reg = reg_data.get(slug, {})
        rng = random.Random(name)
        
        unique_text = f"<p class='mb-4'>{reg.get('regional_fact', '')} " \
                      f"Основные перевозки в {city_info['prep']} осуществляются через {reg.get('main_hubs', '')}. " \
                      f"Это позволяет нам доставлять заказы до Москвы (около {reg.get('distance_to_moscow', '0 км')}) " \
                      f"в рекордно короткие сроки.</p>"

        for service in data["services"]:
            # 1. Город + Услуга
            path = os.path.join(BASE_OUTPUT_DIR, slug, service["slug"], "index.html")
            html = template.replace("{{CITY_NAME}}", name).replace("{{CITY_PREP}}", city_info["prep"])
            html = html.replace("{{CITY_GEN}}", city_info["gen"]).replace("{{H1_MAIN}}", f"{service['h1_main']} в {city_info['prep']}")
            html = html.replace("{{H1_SUB}}", service["h1_sub"]).replace("{{DESC}}", service["desc"])
            html = html.replace("{{UNIQUE_CONTENT}}", unique_text)
            html = html.replace("{{LAT}}", str(round(45 + rng.random()*15, 4))).replace("{{LON}}", str(round(30 + rng.random()*60, 4)))
            html = html.replace("{{REVIEWS}}", str(rng.randint(150, 480)))
            
            nearby = random.sample(cities, 5)
            links = " ".join([f"<a href='/geo/{c['slug']}/' class='text-cdek hover:underline mr-3'>{c['name']}</a>" for c in nearby])
            html = html.replace("{{NEARBY_CITIES}}", links)
            smart_write(path, html)

            # 2. Город + Платформа + Услуга
            for platform in PLATFORMS:
                p_path = os.path.join(BASE_OUTPUT_DIR, slug, platform["slug"], service["slug"], "index.html")
                p_html = html.replace(f"{service['h1_main']} в {city_info['prep']}", f"{service['h1_main']} {platform['name']} в {city_info['prep']}")
                smart_write(p_path, p_html)

    print(f"🚀 Генерация завершена. Проверено страниц для {len(cities)} городов.")

if __name__ == "__main__":
    generate_pages()
