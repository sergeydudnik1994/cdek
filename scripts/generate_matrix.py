import json
import os
from datetime import datetime

DATA_FILE = 'scripts/seo_data.json'
TEMPLATE_FILE = 'scripts/template.html'
BASE_OUTPUT_DIR = 'geo'
SITEMAP_FILE = 'sitemap.xml'

# Четкий словарь русских названий и падежей для папок
CITY_DICTIONARY = {
    "krasnodar": {"name": "Краснодар", "prep": "Краснодаре", "gen": "Краснодара"},
    "moskva": {"name": "Москва", "prep": "Москве", "gen": "Москвы"},
    "ekaterinburg": {"name": "Екатеринбург", "prep": "Екатеринбурге", "gen": "Екатеринбурга"},
    "sankt-peterburg": {"name": "Санкт-Петербург", "prep": "Санкт-Петербурге", "gen": "Санкт-Петербурга"},
    "novosibirsk": {"name": "Новосибирск", "prep": "Новосибирске", "gen": "Новосибирска"},
    "kazan": {"name": "Казань", "prep": "Казани", "gen": "Казани"},
    "nizhniy-novgorod": {"name": "Нижний Новгород", "prep": "Нижнем Новгороде", "gen": "Нижнего Новгорода"},
    "chelyabinsk": {"name": "Челябинск", "prep": "Челябинске", "gen": "Челябинска"},
    "samara": {"name": "Самара", "prep": "Самаре", "gen": "Самары"},
    "rostov-na-donu": {"name": "Ростов-на-Дону", "prep": "Ростове-на-Дону", "gen": "Ростова-на-Дону"}
}

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_template():
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def get_city_forms(slug):
    if slug in CITY_DICTIONARY:
        return CITY_DICTIONARY[slug]
    name = slug.replace('-', ' ').title()
    return {"name": name, "prep": name + "е", "gen": name + "а"}

def generate_sitemap(city_slugs, services):
    today = datetime.now().strftime('%Y-%m-%d')
    base_url = "https://cdek-marketplace.ru"
    
    # Основные статические страницы сайта
    urls = [
        {"loc": f"{base_url}/", "priority": "1.0", "changefreq": "daily"},
        {"loc": f"{base_url}/geo/", "priority": "0.9", "changefreq": "daily"},
        {"loc": f"{base_url}/calculator/", "priority": "0.9", "changefreq": "weekly"},
        {"loc": f"{base_url}/calculator/dbs-1kg/", "priority": "0.9", "changefreq": "weekly"},
        {"loc": f"{base_url}/ozon/", "priority": "0.8", "changefreq": "weekly"},
        {"loc": f"{base_url}/wildberries/", "priority": "0.8", "changefreq": "weekly"},
        {"loc": f"{base_url}/yandex-market/", "priority": "0.8", "changefreq": "weekly"},
        {"loc": f"{base_url}/megamarket/", "priority": "0.8", "changefreq": "weekly"},
        {"loc": f"{base_url}/avito/", "priority": "0.8", "changefreq": "weekly"},
        {"loc": f"{base_url}/internet-magazin/", "priority": "0.8", "changefreq": "weekly"},
        {"loc": f"{base_url}/blog/", "priority": "0.8", "changefreq": "weekly"},
        {"loc": f"{base_url}/faq/", "priority": "0.7", "changefreq": "monthly"},
        {"loc": f"{base_url}/policy/", "priority": "0.3", "changefreq": "yearly"}
    ]
    
    # Добавляем хабы всех городов и все динамические страницы услуг
    for slug in city_slugs:
        urls.append({"loc": f"{base_url}/geo/{slug}/", "priority": "0.6", "changefreq": "weekly"})
        for service in services:
            urls.append({"loc": f"{base_url}/geo/{slug}/{service['slug']}/", "priority": "0.8", "changefreq": "weekly"})

    # Формируем XML-структуру
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    
    for u in urls:
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{u["loc"]}</loc>')
        xml_lines.append(f'    <lastmod>{today}</lastmod>')
        xml_lines.append(f'    <changefreq>{u["changefreq"]}</changefreq>')
        xml_lines.append(f'    <priority>{u["priority"]}</priority>')
        xml_lines.append('  </url>')
        
    xml_lines.append('</urlset>')

    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))
        
    print(f"🗺️ Карта sitemap.xml сгенерирована ({len(urls)} ссылок)!")

def generate_pages():
    data = load_data()
    template = load_template()
    
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
            
            # Динамические хлебные крошки
            breadcrumbs = f"""
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2 text-sm text-slate-500">
                <a href="/" class="hover:text-cdek">Главная</a> / 
                <a href="/geo/" class="hover:text-cdek">Логистика</a> / 
                <span class="text-slate-300">{city_info['name']}</span>
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
            
    print(f"🚀 Сгенерировано {generated_count} SEO-страниц!")
    
    # Автоматически обновляем sitemap.xml при каждом запуске
    generate_sitemap(city_slugs, data['services'])

if __name__ == "__main__":
    generate_pages()
