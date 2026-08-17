import os
import json
import random
import re

# Специальные правила для склонения городов
SPECIAL_CITIES = {
    "Сочи": ("Сочи", "Сочи", "в Сочи"),
    "Тольятти": ("Тольятти", "Тольятти", "в Тольятти"),
    "Улан-Удэ": ("Улан-Удэ", "Улан-Удэ", "в Улан-Удэ"),
    "Санкт-Петербург": ("Санкт-Петербурга", "Санкт-Петербурге", "в Санкт-Петербурге"),
    "Москва": ("Москвы", "Москве", "в Москве"),
}

FEMININE_SOFT_CITIES = {"Казань", "Пермь", "Тюмень", "Рязань", "Тверь", "Астрахань", "Керчь", "Сызрань"}

# Те самые "залетные" запросы из Яндекса для LSI-оптимизации
LSI_QUERIES = [
    "сдэк поставки на маркетплейсы",
    "доставка на маркетплейсы через сдэк",
    "отгрузка на маркетплейс через сдэк",
    "сдэк отправка на маркетплейсы",
    "маркетплейсы сдэк тарифы",
    "доставка на маркетплейсы сдэк стоимость",
    "сдэк отгрузка на маркетплейс правила"
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

def generate_pages():
    with open("scripts/seo_data.json", "r", encoding="utf-8") as f: data = json.load(f)
    with open("scripts/template.html", "r", encoding="utf-8") as f: template = f.read()
    with open("cities.json", "r", encoding="utf-8") as f: cities = json.load(f)
    
    platforms = [
        {"slug": "wildberries", "name": "Wildberries"}, 
        {"slug": "ozon", "name": "Ozon"}, 
        {"slug": "yandex-market", "name": "Яндекс Маркет"}
    ]

    print(f"🚀 Генерация расширенной SEO-матрицы...")

    for city in cities:
        slug, name = city["slug"], city["name"]
        gen, prep, prep_v = get_city_cases(name)
        
        # Генерируем блок LSI-запросов (случайный порядок для уникальности)
        shuffled_lsi = LSI_QUERIES.copy()
        random.shuffle(shuffled_lsi)
        lsi_html = f"<div class='mt-8 pt-6 border-t border-slate-800 text-xs text-slate-600'><p>Популярные запросы: {', '.join(shuffled_lsi)}</p></div>"

        unique_text = f"Официальное подключение селлеров {prep_v} к логистике СДЭК. " \
                      f"Мы обеспечиваем быструю отгрузку на маркетплейсы, соблюдая все регламенты и тайм-слоты. " \
                      f"Ваш бизнес в городе {name} получит доступ к 4000+ ПВЗ по всей стране."

        for s in data["services"]:
            canonical_base = f"https://cdek-marketplace.ru/geo/{slug}/{s['slug']}/"
            
            reps = {
                "{{SEO_TITLE}}": f"{s['h1_main']} {prep_v} | СДЭК для маркетплейсов",
                "{{SEO_DESC}}": f"{s['h1_main']} {prep_v}. Профессиональная логистика для селлеров, скидки до 50% и автоматизация отгрузок.",
                "{{H1_MAIN}}": f"{s['h1_main']} {prep_v}",
                "{{H1_SUB}}": s["h1_sub"],
                "{{DESC}}": s["desc"],
                "{{CITY_NAME}}": name,
                "{{UNIQUE_CONTENT}}": unique_text + lsi_html,
                "{{CANONICAL_URL}}": canonical_base,
                "{{CITY_SLUG}}": slug,
                "{{SERVICE_SLUG}}": s["slug"]
            }

            html = template
            for tag, val in reps.items( ):
                html = html.replace(tag, str(val))

            # Сохранение
            path = os.path.join("geo", slug, s["slug"], "index.html")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f: f.write(html)

            # Страницы маркетплейсов
            for p in platforms:
                p_canonical = f"https://cdek-marketplace.ru/geo/{slug}/{p['slug']}/{s['slug']}/"
                p_html = html.replace(reps["{{H1_MAIN}}"], f"{s['h1_main']} {p['name']} {prep_v}" )
                p_html = p_html.replace(reps["{{SEO_TITLE}}"], f"{s['h1_main']} {p['name']} {prep_v} | СДЭК")
                p_html = p_html.replace(canonical_base, p_canonical)
                
                p_path = os.path.join("geo", slug, p["slug"], s["slug"], "index.html")
                os.makedirs(os.path.dirname(p_path), exist_ok=True)
                with open(p_path, "w", encoding="utf-8") as f: f.write(p_html)

    print(f"✅ Матрица ГЕО-страниц успешно обновлена и оптимизирована под запросы Яндекса.")

if __name__ == "__main__":
    generate_pages()
