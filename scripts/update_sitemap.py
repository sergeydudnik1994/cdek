import xml.etree.ElementTree as ET
from datetime import datetime
import os

NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
ET.register_namespace('', "http://www.sitemaps.org/schemas/sitemap/0.9" )

def create_sitemap_file(filename, urls):
    root = ET.Element(f"{NS}urlset")
    today = datetime.now().strftime('%Y-%m-%d')
    for loc, priority in urls:
        u = ET.SubElement(root, f'{NS}url')
        ET.SubElement(u, f'{NS}loc').text = loc
        ET.SubElement(u, f'{NS}lastmod').text = today
        ET.SubElement(u, f'{NS}changefreq').text = 'weekly'
        ET.SubElement(u, f'{NS}priority').text = priority
    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)
    print(f"--- Создан файл {filename} ({len(urls)} URL)")

def update_sitemap():
    today = datetime.now().strftime('%Y-%m-%d')
    all_urls = []
    
    # 1. Базовые ссылки
    main_urls = [
        ("https://cdek-marketplace.ru/", "1.0" ),
        ("https://cdek-marketplace.ru/services/", "0.9" ),
        ("https://cdek-marketplace.ru/geo/", "0.8" ),
        ("https://cdek-marketplace.ru/blog/", "0.8" )
    ]
    if os.path.exists("services"):
        for slug in os.listdir("services"):
            if os.path.isdir(os.path.join("services", slug)):
                main_urls.append((f"https://cdek-marketplace.ru/services/{slug}/", "0.8" ))

    # 2. Собираем все ГЕО ссылки
    geo_urls = []
    if os.path.exists("geo"):
        for root_dir, dirs, files in os.walk("geo"):
            if "index.html" in files:
                rel = os.path.relpath(root_dir, "geo").replace("\\", "/")
                if rel == ".": continue
                geo_urls.append((f"https://cdek-marketplace.ru/geo/{rel}/", "0.7" ))

    # 3. Генерируем части
    create_sitemap_file("sitemap_main.xml", main_urls)
    
    chunk_size = 40000
    geo_chunks = [geo_urls[i:i + chunk_size] for i in range(0, len(geo_urls), chunk_size)]
    for idx, chunk in enumerate(geo_chunks):
        create_sitemap_file(f"sitemap_geo_{idx+1}.xml", chunk)

    # 4. Создаем ГЛАВНЫЙ ИНДЕКС (sitemap.xml)
    root = ET.Element(f"{NS}sitemapindex")
    files_to_index = ["sitemap_main.xml"] + [f"sitemap_geo_{idx+1}.xml" for idx in range(len(geo_chunks))]
    for f_name in files_to_index:
        s = ET.SubElement(root, f'{NS}sitemap')
        ET.SubElement(s, f'{NS}loc').text = f"https://cdek-marketplace.ru/{f_name}"
        ET.SubElement(s, f'{NS}lastmod' ).text = today
    
    tree = ET.ElementTree(root)
    tree.write('sitemap.xml', encoding='utf-8', xml_declaration=True)
    
    # 5. Создаем список ВСЕХ ссылок для скрипта IndexNow (простой текст)
    with open("all_urls.txt", "w", encoding="utf-8") as f:
        for loc, p in main_urls + geo_urls:
            f.write(loc + "\n")
            
    print(f"✅ Готово! Индекс создан. Всего ссылок: {len(main_urls) + len(geo_urls)}")

if __name__ == "__main__":
    update_sitemap()
