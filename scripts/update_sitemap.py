import xml.etree.ElementTree as ET
from datetime import datetime
import os

NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
ET.register_namespace('', "http://www.sitemaps.org/schemas/sitemap/0.9" )

def update_sitemap():
    today = datetime.now().strftime('%Y-%m-%d')
    root = ET.Element(f"{NS}urlset")
    
    # Базовые страницы
    base_urls = [
        "https://cdek-marketplace.ru/",
        "https://cdek-marketplace.ru/services/",
        "https://cdek-marketplace.ru/geo/",
        "https://cdek-marketplace.ru/blog/"
    ]
    
    def add_url(loc, priority="0.5" ):
        u = ET.SubElement(root, f'{NS}url')
        ET.SubElement(u, f'{NS}loc').text = loc
        ET.SubElement(u, f'{NS}lastmod').text = today
        ET.SubElement(u, f'{NS}changefreq').text = 'weekly'
        ET.SubElement(u, f'{NS}priority').text = priority

    # 1. Добавляем базу
    for url in base_urls: add_url(url, "1.0")

    # 2. Сканируем услуги
    if os.path.exists("services"):
        for slug in os.listdir("services"):
            if os.path.isdir(os.path.join("services", slug)):
                add_url(f"https://cdek-marketplace.ru/services/{slug}/", "0.9" )

    # 3. ГИГАНТСКИЙ СКАН ПАПКИ GEO (Все 71 000 страниц)
    print("🔍 Начинаю глубокое сканирование папки geo...")
    count = 0
    if os.path.exists("geo"):
        for root_dir, dirs, files in os.walk("geo"):
            if "index.html" in files:
                # Превращаем путь к файлу в URL
                relative_path = os.path.relpath(root_dir, "geo")
                if relative_path == ".": continue
                
                url = f"https://cdek-marketplace.ru/geo/{relative_path}/"
                # Убираем лишние слеши в конце если они есть
                url = url.replace("\\", "/" ).replace("//", "/")
                add_url(url, "0.7")
                count += 1
                if count % 10000 == 0: print(f"--- Обработано {count} URL...")

    tree = ET.ElementTree(root)
    tree.write('sitemap.xml', encoding='utf-8', xml_declaration=True)
    print(f"✅ Карта сайта готова! Всего ссылок: {count + len(base_urls) + 20}")

if __name__ == "__main__":
    update_sitemap()
