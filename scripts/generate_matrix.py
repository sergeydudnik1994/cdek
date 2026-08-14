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

def get_city_cases(name):
    overrides = {
        "Москва": ("Москвы", "Москве"),
        "Санкт-Петербург": ("Санкт-Петербурга", "Санкт-Петербурге"),
        "Нижний Новгород": ("Нижнего Новгорода", "Нижнем Новгороде"),
        "Ростов-на-Дону": ("Ростова-на-Дону", "Ростове-на-Дону"),
    }
    if name in overrides: return {"name": name, "gen": overrides[name][0], "prep": overrides[name][1]}
    if name.endswith('ск'): gen, prep = name + 'а', name + 'е'
    elif name.endswith('а'): gen, prep = name[:-1] + 'ы', name[:-1] + 'е'
    elif name.endswith('ль'): gen, prep = name[:-1] + 'я', name[:-1] + 'е'
    else: gen, prep = name + 'а', name + 'е'
    return {"name": name, "gen": gen, "prep": prep}

def generate_pages():
    # Загрузка данных
    with open(DATA_FILE, "r", encoding="utf-8") as f: data = json.load(f)
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f: template = f.read()
    with open(CITIES_FILE, "r", encoding="utf-8") as f: cities = json.load(f)
    with open(REGIONAL_DATA_FILE, "r", encoding="utf-8") as f: reg_data = json.load(f)

    for city in cities:
        slug, name = city["slug"], city["name"]
        city_info = get_city_cases(name)
        reg = reg_data.get(slug, {})
        rng = random.Random(name) # Для стабильности данных на странице
        
        # Генерация уникального блока контента
        unique_text = f"<p class='mb-4'>{reg.get('regional_fact', '')} " \
                      f"Основные перевозки в {city_info['prep']} осуществляются через {reg.get('main_hubs', '')}. " \
                      f"Это позволяет нам доставлять заказы до Москвы (около {reg.get('distance_to_moscow', '0 км')}) " \
                      f"в рекордно короткие сроки. {reg.get('regional_advantage', '')}</p>"

        for service in data["services"]:
            # Создаем папку города/услуги
            path = os.path.join(BASE_OUTPUT_DIR, slug, service["slug"])
            os.makedirs(path, exist_ok=True)
            
            # Замена плейсхолдеров
            html = template.replace("{{CITY_NAME}}", name)
            html = html = html.replace("{{CITY_PREP}}", city_info["prep"])
            html = html.replace("{{CITY_GEN}}", city_info["gen"])
            html = html.replace("{{H1_MAIN}}", f"{service['h1_main']} в {city_info['prep']}")
            html = html.replace("{{H1_SUB}}", service["h1_sub"])
            html = html.replace("{{DESC}}", service["desc"])
            html = html.replace("{{UNIQUE_CONTENT}}", unique_text)
            
            # Микроразметка (LocalBusiness)
            html = html.replace("{{LAT}}", str(round(45 + rng.random()*15, 4)))
            html = html.replace("{{LON}}", str(round(30 + rng.random()*60, 4)))
            html = html.replace("{{REVIEWS}}", str(rng.randint(150, 480)))
            
            # Перелинковка (Соседние города)
            nearby = random.sample(cities, 5)
            links = " ".join([f"<a href='/geo/{c['slug']}/' class='text-cdek hover:underline mr-3'>{c['name']}</a>" for c in nearby])
            html = html.replace("{{NEARBY_CITIES}}", links)

            with open(os.path.join(path, "index.html"), "w", encoding="utf-8") as f:
                f.write(html)

    print(f"✅ Матрица для {len(cities)} городов обновлена!")

if __name__ == "__main__":
    generate_pages()
