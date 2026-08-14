import json, os, random

def get_city_cases(n):
    if n.endswith('ск'): return n+'а', n+'е'
    if n.endswith('а'): return n[:-1]+'ы', n[:-1]+'е'
    return n+'а', n+'е'

def generate_pages():
    with open("scripts/seo_data.json", "r", encoding="utf-8") as f: data = json.load(f)
    with open("scripts/template.html", "r", encoding="utf-8") as f: template = f.read()
    with open("cities.json", "r", encoding="utf-8") as f: cities = json.load(f)

    for city in cities:
        slug, name = city["slug"], city["name"]
        gen, prep = get_city_cases(name)
        rng = random.Random(name)
        
        # Уникальный текст для Яндекса
        unique = f"СДЭК Маркетплейсы в {prep} — это быстрая отгрузка для селлеров. " \
                 f"Мы оптимизировали логистику в {prep}, чтобы вы экономили до 50% на доставке. " \
                 f"Работаем по FBS и DBS с гарантией сроков."

        # Создаем ГЛАВНУЮ страницу города (Hub)
        city_dir = os.path.join("geo", slug)
        os.makedirs(city_dir, exist_ok=True)
        hub_html = template.replace("{{CITY_NAME}}", name).replace("{{CITY_PREP}}", prep)
        hub_html = hub_html.replace("{{H1_MAIN}}", f"СДЭК для маркетплейсов в {prep}")
        hub_html = hub_html.replace("{{UNIQUE_CONTENT}}", unique).replace("{{DESC}}", "Официальное подключение.")
        with open(os.path.join(city_dir, "index.html"), "w", encoding="utf-8") as f: f.write(hub_html)

        # Создаем страницы УСЛУГ
        for s in data["services"]:
            path = os.path.join("geo", slug, s["slug"])
            os.makedirs(path, exist_ok=True)
            html = template.replace("{{CITY_NAME}}", name).replace("{{CITY_PREP}}", prep)
            html = html.replace("{{H1_MAIN}}", f"{s['h1_main']} в {prep}")
            html = html.replace("{{UNIQUE_CONTENT}}", unique).replace("{{DESC}}", s["desc"])
            with open(os.path.join(path, "index.html"), "w", encoding="utf-8") as f: f.write(html)

    print(f"✅ Матрица готова!")

if __name__ == "__main__":
    generate_pages()
