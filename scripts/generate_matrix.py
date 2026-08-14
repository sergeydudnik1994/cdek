import json
import os
import random
from datetime import datetime

# Конфигурация
DATA_FILE = "scripts/seo_data.json"
TEMPLATE_FILE = "scripts/template.html"
CITIES_FILE = "cities.json"
BASE_OUTPUT_DIR = "geo"

# Матрица для гипер-уникальности (Яндекс это полюбит)
INTROS = ["СДЭК Маркетплейсы — ваш надежный партнер в {city_prep}.", "Обеспечиваем быструю логистику для селлеров из {city_gen}.", "Филиал СДЭК в {city_prep} расширяет возможности для бизнеса."]
LOGISTICS = ["Мы оптимизировали маршруты, учитывая специфику {city_gen}.", "Транспортная сеть в {city_prep} позволяет отгружать заказы день-в-день.", "Наличие локальных хабов сокращает время доставки на 20%."]
MARKET = ["Идеально для работы по FBS и DBS.", "Поддержка всех популярных маркетплейсов.", "Автоматизация отгрузок через API СДЭК."]
FINALE = ["Снижайте издержки на логистику вместе с нами.", "Начните масштабировать продажи уже сегодня.", "Персональный менеджер поможет с настройкой договора."]

def get_city_cases(name):
    if name.endswith('ск'): return name + 'а', name + 'е'
    if name.endswith('а'): return name[:-1] + 'ы', name[:-1] + 'е'
    return name + 'а', name + 'е'

def generate_pages():
    with open(DATA_FILE, "r", encoding="utf-8") as f: data = json.load(f)
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f: template = f.read()
    with open(CITIES_FILE, "r", encoding="utf-8") as f: cities = json.load(f)

    for city in cities:
        slug, name = city["slug"], city["name"]
        city_gen, city_prep = get_city_cases(name)
        rng = random.Random(name)
        
        # Собираем уникальный текст из 4-х блоков
        unique_text = f"{rng.choice(INTROS).format(city_prep=city_prep, city_gen=city_gen)} " \
                      f"{rng.choice(LOGISTICS).format(city_prep=city_prep, city_gen=city_gen)} " \
                      f"{rng.choice(MARKET)} {rng.choice(FINALE).format(city_gen=city_gen)}"

        for service in data["services"]:
            path = os.path.join(BASE_OUTPUT_DIR, slug, service["slug"], "index.html")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            html = template.replace("{{CITY_NAME}}", name).replace("{{CITY_PREP}}", city_info["prep"] if 'city_info' in locals() else city_prep)
            html = html.replace("{{CITY_GEN}}", city_gen).replace("{{H1_MAIN}}", f"{service['h1_main']} в {city_prep}")
            html = html.replace("{{H1_SUB}}", service["h1_sub"]).replace("{{DESC}}", service["desc"])
            html = html.replace("{{UNIQUE_CONTENT}}", unique_text)
            
            # Умное сохранение (не перезаписываем, если нет изменений)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    if f.read() == html: continue
            
            with open(path, 'w', encoding='utf-8') as f: f.write(html)

    print(f"🚀 Матрица обновлена для {len(cities)} городов.")

if __name__ == "__main__":
    generate_pages()
