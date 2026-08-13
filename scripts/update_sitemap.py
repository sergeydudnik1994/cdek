import xml.etree.ElementTree as ET
from datetime import datetime
import os

# Регистрация неймспейса
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
ET.register_namespace('', "http://www.sitemaps.org/schemas/sitemap/0.9")

def update_sitemap():
    today = datetime.now().strftime('%Y-%m-%d')
    tree = ET.parse('sitemap.xml')
    root = tree.getroot()
    
    # 1. Обновляем даты для существующих страниц
    updated_count = 0
    for url in root.findall(f'{NS}url'):
        changefreq = url.find(f'{NS}changefreq')
        if changefreq is not None and changefreq.text in ['daily', 'weekly']:
            lastmod = url.find(f'{NS}lastmod')
            if lastmod is not None:
                lastmod.text = today
                updated_count += 1

    # 2. Собираем список уже существующих URL, чтобы не дублировать
    existing_urls = {u.find(f'{NS}loc').text for u in root.findall(f'{NS}url')}

    # 3. Сканируем папку services/ и добавляем новые услуги
    services_dir = "services"
    added_count = 0
    if os.path.exists(services_dir):
        for slug in os.listdir(services_dir):
            path = os.path.join(services_dir, slug)
            if os.path.isdir(path) and os.path.exists(os.path.join(path, "index.html")):
                url = f"https://cdek-marketplace.ru/services/{slug}/"
                if url not in existing_urls:
                    u_el = ET.SubElement(root, f'{NS}url')
                    ET.SubElement(u_el, f'{NS}loc').text = url
                    ET.SubElement(u_el, f'{NS}lastmod').text = today
                    ET.SubElement(u_el, f'{NS}changefreq').text = 'weekly'
                    ET.SubElement(u_el, f'{NS}priority').text = '0.8'
                    added_count += 1

    tree.write('sitemap.xml', encoding='utf-8', xml_declaration=True)
    print(f"✅ Успешно. Обновлено lastmod: {updated_count} страниц. Добавлено новых услуг: {added_count}.")

if __name__ == "__main__":
    update_sitemap()
