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

def generate_pages():
    data = load_data()
    template = load_template()
    generated_count = 0

    for city in data['cities']:
        for service in data['services']:
            dir_path = os.path.join(BASE_OUTPUT_DIR, city['slug'], service['slug'])
            os.makedirs(dir_path, exist_ok=True)
            
            # Генерация крошек
            breadcrumbs = f"""
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2 text-sm text-slate-500">
                <a href="/" class="hover:text-cdek">Главная</a> / 
                <a href="/geo/" class="hover:text-cdek">Гео</a> / 
                <a href="/geo/{city['slug']}/" class="hover:text-cdek">{city['name']}</a> / 
                <span class="text-white">{service['h1_main'].split(' ')[0]}</span>
            </div>
            """
            
            html_content = template
            html_content = html_content.replace('{{BREADCRUMBS}}', breadcrumbs)
            html_content = html_content.replace('{{CITY_NAME}}', city['name'])
            html_content = html_content.replace('{{CITY_PREP}}', city['prep'])
            html_content = html_content.replace('{{CITY_GEN}}', city.get('gen', city['name']))
            html_content = html_content.replace('{{CITY_SLUG}}', city['slug'])
            html_content = html_content.replace('{{SERVICE_SLUG}}', service['slug'])
            html_content = html_content.replace('{{H1_MAIN}}', service['h1_main'])
            html_content = html_content.replace('{{H1_SUB}}', service['h1_sub'])
            html_content = html_content.replace('{{DESC}}', service['desc'])

            file_path = os.path.join(dir_path, 'index.html')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            generated_count += 1
            
    print(f"🚀 Сгенерировано {generated_count} страниц!")

if __name__ == "__main__":
    generate_pages()
