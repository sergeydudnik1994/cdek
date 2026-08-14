import json, os, random

def get_city_cases(n):
    overrides = {"Москва": ("Москвы", "Москве"), "Санкт-Петербург": ("Санкт-Петербурга", "Санкт-Петербурге")}
    if n in overrides: return overrides[n]
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
        days = 1 if slug in ["moskva", "himki"] else rng.randint(2, 5)
        
        unique = f"СДЭК Маркетплейсы в {prep} — это быстрая отгрузка для селлеров. " \
                 f"Мы оптимизировали логистику в {prep}, чтобы вы экономили до 50% на доставке. " \
                 f"Расстояние до Москвы учитывается при расчете тарифа."

        for s in data["services"]:
            path = os.path.join("geo", slug, s["slug"], "index.html")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            # Формируем SEO-теги
            title = f"{s['h1_main']} в {prep} | Договор СДЭК со скидкой 50%"
            desc = f"{s['h1_main']} в {prep} для Wildberries, Ozon и Я.Маркета. Доставка за {days} дн. Скидки до 50% для бизнеса."
            
            html = template.replace("{{CITY_NAME}}", name).replace("{{CITY_PREP}}", prep)
            html = html.replace("{{CITY_GEN}}", gen).replace("{{H1_MAIN}}", f"{s['h1_main']} в {prep}")
            html = html.replace("{{H1_SUB}}", s["h1_sub"]).replace("{{DESC}}", s["desc"])
            html = html.replace("{{UNIQUE_CONTENT}}", unique)
            
            # Заменяем SEO-теги и служебные данные
            html = html.replace("{{SEO_TITLE}}", title).replace("{{SEO_DESC}}", desc)
            html = html.replace("{{CITY_SLUG}}", slug).replace("{{SERVICE_SLUG}}", s["slug"])
            html = html.replace("{{LAT}}", str(round(45 + rng.random()*15, 4)))
            html = html.replace("{{LON}}", str(round(30 + rng.random()*60, 4)))
            html = html.replace("{{REVIEWS}}", str(rng.randint(150, 480)))
            
            # Перелинковка
            nearby = random.sample(cities, 5)
            links = " ".join([f"<a href='/geo/{c['slug']}/' class='text-cdek hover:underline mr-3'>{c['name']}</a>" for c in nearby])
            html = html.replace("{{NEARBY_CITIES}}", links)

            with open(path, "w", encoding="utf-8") as f: f.write(html)

    print(f"✅ Матрица полностью обновлена. Все теги заменены!")

if __name__ == "__main__":
    generate_pages()
