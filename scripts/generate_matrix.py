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
            
            # Генерируем динамическую HTML-цепочку крошек
            # Убираем старые крошки из заголовка (в CSS можно скрыть)
            breadcrumbs = f"""
            <nav class="flex text-sm text-slate-500 mb-4" aria-label="Breadcrumb">
                <ol class="flex items-center space-x-2">
                    <li><a href="/" class="hover:text-cdek">Главная</a></li>
                    <li>/</li>
                    <li><a href="/geo/" class="hover:text-cdek">Логистика для селлеров</a></li>
                    <li>/</li>
                    <li><a href="/geo/{city['slug']}/" class="hover:text-cdek">{city['name']}</a></li>
                    <li>/</li>
                    <li class="text-white" aria-current="page">{service['h1_main'].split(' ')[0]}</li>
                </ol>
            </nav>
            """
            
            html_content = template
            # Вставляем динамические крошки
            html_content = html_content.replace('{{BREADCRUMBS}}', breadcrumbs)
            
            # Остальные замены
            html_content = html_content.replace('{{CITY_NAME}}', city['name'])
            html_content = html_content.replace('{{CITY_PREP}}', city['prep'])
            html_content = html_content.replace('{{CITY_GEN}}', city.get('gen', city['name']))
            html_content = html_content.replace('{{CITY_SLUG}}', city['slug'])
            html_content = html_content.replace('{{SERVICE_SLUG}}', service['slug'])
            html_content = html_content.replace('{{H1_MAIN}}', service['h1_main'])
            html_content = html_content.replace('{{H1_SUB}}', service['h1_sub'])
            html_content = html_content.replace('{{PRICE}}', service['price'])
            html_content = html_content.replace('{{DESC}}', service['desc'])

            file_path = os.path.join(dir_path, 'index.html')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            generated_count += 1
            
    print(f"🚀 Сгенерировано {generated_count} страниц с крошками!")

if __name__ == "__main__":
    generate_pages()
