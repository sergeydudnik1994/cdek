import os
import json
import random
import re

SPECIAL_CITIES = {
    "Сочи": ("Сочи", "Сочи", "в Сочи"),
    "Тольятти": ("Тольятти", "Тольятти", "в Тольятти"),
    "Улан-Удэ": ("Улан-Удэ", "Улан-Удэ", "в Улан-Удэ"),
    "Санкт-Петербург": ("Санкт-Петербурга", "Санкт-Петербурге", "в Санкт-Петербурге"),
    "Москва": ("Москвы", "Москве", "в Москве"),
}
FEMININE_SOFT_CITIES = {"Казань", "Пермь", "Тюмень", "Рязань", "Тверь", "Астрахань", "Керчь", "Сызрань"}

LSI_QUERIES = [
    "сдэк поставки на маркетплейсы",
    "доставка на маркетплейсы через сдэк",
    "отгрузка на маркетплейс через сдэк",
    "сдэк отправка на маркетплейсы",
    "маркетплейсы сдэк тарифы",
    "доставка на маркетплейсы сдэк стоимость"
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
            elif part.endswith("а"):
                gen_parts.append(part[:-1] + "и" if len(part) > 2 and part[-2] in "гкхжчшщ" else part[:-1] + "ы")
                prep_parts.append(part[:-1] + "е")
            elif part.endswith("я"):
                gen_parts.append(part[:-1] + "и"); prep_parts.append(part[:-1] + "и" if part.endswith("ия") else part[:-1] + "е")
            elif part.endswith("о"):
                gen_parts.append(part[:-1] + "а"); prep_parts.append(part[:-1] + "е")
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

def generate_pages():
    with open("scripts/seo_data.json", "r", encoding="utf-8") as f: data = json.load(f)
    with open("scripts/industry_data.json", "r", encoding="utf-8") as f: ind_data = json.load(f)
    with open("scripts/template.html", "r", encoding="utf-8") as f: template = f.read()
    with open("cities.json", "r", encoding="utf-8") as f: cities = json.load(f)
    
    platforms = [{"slug": "wildberries", "name": "Wildberries"}, {"slug": "ozon", "name": "Ozon"}, {"slug": "yandex-market", "name": "Яндекс Маркет"}]

    print(f"🚀 Генерация МЕГА-матрицы (Услуги + Отрасли)...")

    for city in cities:
        slug, name = city["slug"], city["name"]
        _, _, prep_v = get_city_cases(name)
        
        # 1. Генерация стандартных УСЛУГ для города
        for s in data["services"]:
            canonical = f"https://cdek-marketplace.ru/geo/{slug}/{s['slug']}/"
            html = template.replace("{{SEO_TITLE}}", f"{s['h1_main']} {prep_v} | СДЭК" )
            html = html.replace("{{H1_MAIN}}", f"{s['h1_main']} {prep_v}")
            html = html.replace("{{CANONICAL_URL}}", canonical)
            html = html.replace("{{CITY_NAME}}", name)
            html = html.replace("{{DESC}}", s["desc"])
            html = html.replace("{{UNIQUE_CONTENT}}", f"Профессиональные логистические решения {prep_v} для вашего бизнеса.")
            
            path = os.path.join("geo", slug, s["slug"], "index.html")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f: f.write(html)

        # 2. НОВОЕ: Генерация ОТРАСЛЕВЫХ РЕШЕНИЙ для города
        for ind in ind_data["industries"]:
            canonical = f"https://cdek-marketplace.ru/geo/{slug}/{ind['slug']}/"
            
            # Уникализируем контент под город и отрасль
            ind_unique = f"Специализированная {ind['h1_main']} {prep_v}. " \
                         f"Мы учитываем специфику категории {ind['h1_main']} и предлагаем оптимальные маршруты из города {name}."
            
            html = template.replace("{{SEO_TITLE}}", f"{ind['h1_main']} {prep_v} | СДЭК Маркетплейс" )
            html = html.replace("{{H1_MAIN}}", f"{ind['h1_main']} {prep_v}")
            html = html.replace("{{H1_SUB}}", ind["h1_sub"])
            html = html.replace("{{DESC}}", ind["desc"])
            html = html.replace("{{CANONICAL_URL}}", canonical)
            html = html.replace("{{CITY_NAME}}", name)
            html = html.replace("{{UNIQUE_CONTENT}}", ind_unique)
            
            path = os.path.join("geo", slug, ind["slug"], "index.html")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f: f.write(html)

    print(f"✅ МЕГА-матрица готова. Добавлено 5000+ отраслевых страниц по городам.")

if __name__ == "__main__":
    generate_pages()
