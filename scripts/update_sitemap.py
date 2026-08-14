import os
from datetime import datetime

def generate_sitemap():
    today = datetime.now().strftime('%Y-%m-%d')
    host = "https://cdek-marketplace.ru"
    
    # 1. Собираем БАЗОВЫЕ ссылки
    main_urls = [f"{host}/", f"{host}/services/", f"{host}/geo/", f"{host}/blog/"]
    if os.path.exists("services" ):
        for slug in os.listdir("services"):
            if os.path.isdir(os.path.join("services", slug)):
                main_urls.append(f"{host}/services/{slug}/")

    # 2. Собираем ГЕО ссылки
    geo_urls = []
    if os.path.exists("geo"):
        for root_dir, dirs, files in os.walk("geo"):
            if "index.html" in files:
                rel = os.path.relpath(root_dir, "geo").replace("\\", "/")
                if rel != ".": geo_urls.append(f"{host}/geo/{rel}/")

    # 3. Функция записи файла части
    def write_xml(filename, urls, is_index=False):
        with open(filename, "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            if is_index:
                f.write('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' )
                for u in urls:
                    f.write(f'  <sitemap><loc>{u}</loc><lastmod>{today}</lastmod></sitemap>\n')
                f.write('</sitemapindex>')
            else:
                f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' )
                for u in urls:
                    priority = "0.9" if "services" in u else "0.7"
                    f.write(f'  <url><loc>{u}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>{priority}</priority></url>\n')
                f.write('</urlset>')

    # 4. Генерируем части
    write_xml("sitemap_main.xml", main_urls)
    
    chunk_size = 40000
    chunks = [geo_urls[i:i + chunk_size] for i in range(0, len(geo_urls), chunk_size)]
    geo_files = []
    for idx, chunk in enumerate(chunks):
        fname = f"sitemap_geo_{idx+1}.xml"
        write_xml(fname, chunk)
        geo_files.append(f"{host}/{fname}")

    # 5. Создаем ГЛАВНЫЙ ИНДЕКС
    index_urls = [f"{host}/sitemap_main.xml"] + geo_files
    write_xml("sitemap.xml", index_urls, is_index=True)
    
    # 6. Список для IndexNow
    with open("all_urls.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(main_urls + geo_urls))

    print(f"✅ Успех! Создан индекс и {len(geo_files)+1} частей. Всего: {len(main_urls)+len(geo_urls)} URL.")

if __name__ == "__main__":
    generate_sitemap()
