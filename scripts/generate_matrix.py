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
        
        for s in data["services"]:
            path = os.path.join("geo", slug, s["slug"], "index.html")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            title = f"{s['h1_main']} в {prep} | СДЭК"
            desc = f"{s['h1_main']} в {prep} для маркетплейсов. Скидки до 50%."
            
            html = template.replace("{{SEO_TITLE}}", title)
            html = html.replace("{{SEO_DESC}}", desc)
            html = html.replace("{{CITY_NAME}}", name)
            html = html.replace("{{CITY_PREP}}", prep)
            html = html.replace("{{H1_MAIN}}", f"{s['h1_main']} в {prep}")
            html = html.replace("{{H1_SUB}}", s["h1_sub"])
            html = html.replace("{{DESC}}", s["desc"])
            html = html.replace("{{CITY_SLUG}}", slug)
            html = html.replace("{{SERVICE_SLUG}}", s["slug"])
            
            # Заглушки для микроразметки
            html = html.replace("{{LAT}}", "55.7558").replace("{{LON}}", "37.6173").replace("{{REVIEWS}}", "250")

            with open(path, "w", encoding="utf-8") as f: f.write(html)

    print(f"✅ Готово! Все теги заменены.")

if __name__ == "__main__":
    generate_pages()
