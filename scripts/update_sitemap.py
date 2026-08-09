import xml.etree.ElementTree as ET
from datetime import datetime

# Регистрация неймспейса, чтобы не ломался формат XML
ET.register_namespace('', "http://www.sitemaps.org/schemas/sitemap/0.9")

def update_sitemap():
    today = datetime.now().strftime('%Y-%m-%d')
    tree = ET.parse('sitemap.xml')
    root = tree.getroot()
    
    updated_count = 0
    # Ищем все URL и обновляем дату, если это важные страницы
    for url in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        changefreq = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}changefreq')
        if changefreq is not None and changefreq.text in ['daily', 'weekly']:
            lastmod = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
            if lastmod is not None:
                lastmod.text = today
                updated_count += 1

    tree.write('sitemap.xml', encoding='utf-8', xml_declaration=True)
    print(f"✅ Успешно. Обновлена дата (lastmod: {today}) для {updated_count} страниц.")

if __name__ == "__main__":
    update_sitemap()
