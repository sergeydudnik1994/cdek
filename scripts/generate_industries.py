import os
import json

def generate_industries():
    with open("scripts/industry_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Используем ваш основной шаблон
    with open("scripts/template.html", "r", encoding="utf-8") as f:
        template = f.read()
    
    os.makedirs("solutions", exist_ok=True)
    count = 0
    
    for ind in data["industries"]:
        slug = ind["slug"]
        canonical = f"https://cdek-marketplace.ru/solutions/{slug}/"
        
        reps = {
            "{{SEO_TITLE}}": f"{ind['h1_main']} | СДЭК для бизнеса",
            "{{SEO_DESC}}": f"{ind['h1_main']}. {ind['desc']} Официальное подключение со скидкой до 50%.",
            "{{H1_MAIN}}": ind["h1_main"],
            "{{H1_SUB}}": ind["h1_sub"],
            "{{DESC}}": ind["desc"],
            "{{CITY_NAME}}": "России", # Глобальная страница
            "{{UNIQUE_CONTENT}}": f"<p class='mt-4'>{ind['desc']}</p><p class='mt-2'>Мы предлагаем специализированные тарифы и условия для категории {ind['h1_main']}. Работайте по FBS и DBS с надежным партнером.</p>",
            "{{CANONICAL_URL}}": canonical,
            "{{CITY_SLUG}}": "russia",
            "{{SERVICE_SLUG}}": slug
        }
        
        html = template
        for tag, val in reps.items( ):
            html = html.replace(tag, str(val))
        
        dir_path = os.path.join("solutions", slug)
        os.makedirs(dir_path, exist_ok=True)
        with open(os.path.join(dir_path, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        count += 1
        
    print(f"🚀 Сгенерировано отраслевых решений: {count}")

if __name__ == "__main__":
    generate_industries()
