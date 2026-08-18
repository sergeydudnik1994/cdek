import os
import json
import re

def generate_industries():
    with open("scripts/industry_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with open("scripts/generate_global_services.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    html_match = re.search(r'html_content = f"""(.*?)"""', content, re.DOTALL)
    if not html_match: return
    page_template = html_match.group(1)

    with open("services/index.html", "r", encoding="utf-8") as f:
        hub_template = f.read()

    os.makedirs("solutions", exist_ok=True)
    
    count = 0
    for ind in data["industries"]:
        slug = ind["slug"]
        current_html = page_template.replace('<a href="/services/" class="hover:text-cdek">Услуги</a>', '<a href="/solutions/" class="hover:text-cdek">Решения</a>')
        formatted_html = current_html.format(slug=slug, h1_main=ind["h1_main"], h1_sub=ind["h1_sub"], desc=ind["desc"])
        formatted_html = formatted_html.replace(f'https://cdek-marketplace.ru/services/{slug}/', f'https://cdek-marketplace.ru/solutions/{slug}/' )
        
        dir_path = os.path.join("solutions", slug)
        os.makedirs(dir_path, exist_ok=True)
        with open(os.path.join(dir_path, "index.html"), "w", encoding="utf-8") as f: f.write(formatted_html)
        count += 1

    # Генерация Хаб-страницы
    hub_html = hub_template.replace("Все услуги СДЭК", "Отраслевые решения").replace("/services/", "/solutions/")
    industry_list_js = [{"slug": i["slug"], "title": i["h1_main"], "desc": i["desc"], "icon": "..."} for i in data["industries"]]
    hub_html = re.sub(r'const services = \[.*?\];', f'const services = {json.dumps(industry_list_js, ensure_ascii=False)};', hub_html, flags=re.DOTALL)
    
    with open("solutions/index.html", "w", encoding="utf-8") as f: f.write(hub_html)
    print(f"🚀 Сгенерировано: {count} решений + хаб.")

if __name__ == "__main__":
    generate_industries()
