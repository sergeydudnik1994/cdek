import json
import os

DATA_FILE = 'scripts/seo_data.json'
TEMPLATE_FILE = 'scripts/template.html'
BASE_OUTPUT_DIR = 'geo'

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_template():
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return f.read()

# Словарь для городов с особенностями склонения
CITY_EXCEPTIONS = {
    "moskva": {"name": "Москва", "prep": "Москве", "gen": "Москвы"},
    "sankt-peterburg": {"name": "Санкт-Петербург", "prep": "Санкт-Петербурге", "gen": "Санкт-Петербурга"},
    "nizhniy-novgorod": {"name": "Нижний Новгород", "prep": "Нижнем Новгороде", "gen": "Нижнего Новгорода"},
    "rostov-na-donu": {"name": "Ростов-на-Дону", "prep": "Ростове-на-Дону", "gen": "Ростов-на-Дону"}
}

def get_city_forms(slug):
    if slug in CITY_EXCEPTIONS:
        return CITY_EXCEPTIONS[slug]
    
    # Автоматическое форматирование для остальных папок (например, krasnodar -> Краснодар)
    name = slug.replace('-', ' ').title()
    return {
        "name": name,
        "prep": name + "е",
        "gen": name + "а"
    }

def generate_pages():
    data = load_data()
    template = load_template()
    
    # АВТОМАТИЧЕСКИ сканируем все папки в директории geo/
    if os.path.exists(BASE_OUTPUT_DIR):
        city_slugs = [d for d in os.listdir(BASE_OUTPUT_DIR) if os.path.isdir(os.path.join(BASE_OUTPUT_DIR, d))]
    else:
        city_slugs = []

    generated_count = 0

    for slug in city_slugs:
        city_info = get_city_forms(slug)
        
        for service in data['services']:
            dir_path = os.path.join(BASE_OUTPUT_DIR, slug, service['slug'])
            os.makedirs(dir_path, exist_ok=True)
            
            # Генерация хлебных крошек
            breadcrumbs = f"""
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2 text-sm text-slate-500">
                <a href="/" class="hover:text-cdek">Главная</a> / 
                <a href="/geo/" class="hover:text-cdek">Гео</a> / 
                <a href="/geo/{slug}/" class="hover:text-cdek">{city_info['name']}</a> / 
                <span class="text-white">{service['h1_main'].split(' ')[0]}</span>
            </div>
            """
            
            html_content = template
            html_content = html_content.replace('{{BREADCRUMBS}}', breadcrumbs)
            html_content = html_content.replace('{{CITY_NAME}}', city_info['name'])
            html_content = html_content.replace('{{CITY_PREP}}', city_info['prep'])
            html_content = html_content.replace('{{CITY_GEN}}', city_info['gen'])
            html_content = html_content.replace('{{CITY_SLUG}}', slug)
            
            html_content = html_content.replace('{{SERVICE_SLUG}}', service['slug'])
            html_content = html_content.replace('{{H1_MAIN}}', service['h1_main'])
            html_content = html_content.replace('{{H1_SUB}}', service['h1_sub'])
            html_content = html_content.replace('{{DESC}}', service['desc'])

            file_path = os.path.join(dir_path, 'index.html')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            generated_count += 1
            
    print(f"🚀 Успешно сгенерировано {generated_count} страниц для {len(city_slugs)} городов из папки geo!")

if __name__ == "__main__":
    generate_pages()
