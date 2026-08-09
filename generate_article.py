import os
import re
import csv
from datetime import datetime
import xml.etree.ElementTree as ET
from google import genai

# Настройки
DOMAIN = "https://cdek-marketplace.ru"
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY не найден в переменных окружения.")

client = genai.Client(api_key=API_KEY)

def slugify(text):
    translit_map = {
        'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'yo','ж':'zh',
        'з':'z','и':'i','й':'y','к':'k','л':'l','м':'m','н':'n','о':'o',
        'п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h','ц':'ts',
        'ч':'ch','ш':'sh','щ':'sch','ъ':'','ы':'y','ь':'','э':'e','ю':'yu',
        'я':'ya',' ':'-','_':'-', ',':'', '.':''
    }
    text = text.lower().strip()
    res = ''.join([translit_map.get(c, c) if c.isalnum() else '-' for c in text])
    return re.sub(r'-+', '-', res).strip('-')

def get_next_unique_keyword():
    if not os.path.exists('keywords.csv'):
        print("Файл keywords.csv не найден.")
        return None, None, None

    with open('keywords.csv', 'r', encoding='utf-8') as f:
        rows = list(csv.reader(f))
    
    if len(rows) <= 1:
        print("Нет доступных ключей для генерации.")
        return None, None, None

    header = rows[0]
    keywords = rows[1:]
    
    selected_row = None
    selected_slug = None
    remaining_rows = []

    # Ищем первый ключ, для которого еще нет папки в blog/
    for row in keywords:
        if selected_row is None:
            slug = slugify(row[0])
            folder_path = os.path.join('blog', slug)
            if not os.path.exists(folder_path):
                selected_row = row
                selected_slug = slug
                continue # Нашли уникальный ключ, остальные записываем в остаток
        remaining_rows.append(row)

    if not selected_row:
        print("Все ключи из файла уже существуют в виде статей (дубли).")
        return None, None, None

    # Перезаписываем очередь ключей
    with open('keywords.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(remaining_rows)

    # Логируем в архив
    archived_exists = os.path.exists('keywords_done.csv')
    with open('keywords_done.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if not archived_exists:
            writer.writerow(header + ['date_processed'])
        writer.writerow(selected_row + [datetime.now().strftime("%Y-%m-%d %H:%M")])

    keyword = selected_row[0].strip()
    category = selected_row[1].strip() if len(selected_row) > 1 else "Логистика"
    return keyword, category, selected_slug

def generate_article_content(keyword):
    prompt = f"""
    Ты — эксперт по B2B логистике. Напиши SEO-статью для лендинга CDEK по запросу: "{keyword}".
    
    Требования:
    1. Полезный контент для селлеров (Wildberries, Ozon, Яндекс Маркет).
    2. Упор на выгоды использования режимов FBS и DBS через CDEK (скорость, экономия).
    3. Структура: Введение, пошаговая инструкция/разбор, HTML-таблица со сравнением, частые ошибки, FAQ (3 вопроса).
    4. Выдай строго HTML-код (теги <h2>, <h3>, <p>, <ul>, <table>). Без тегов ```html в начале и конце. Без <html> и <body>.
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text.replace("```html", "").replace("```", "").strip()

def build_full_html_page(title, content, slug, category, date_str):
    canonical_url = f"{DOMAIN}/blog/{slug}/"
    
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Блог CDEK</title>
    <meta name="description" content="Всё о {title.lower()} для селлеров. Доставка FBS и DBS через CDEK.">
    <link rel="canonical" href="{canonical_url}">
    <link rel="stylesheet" href="/style.css"> 
</head>
<body>
    <header class="header">
        <!-- Ваш стандартный хедер лендинга -->
        <a href="/">На главную</a> | <a href="/blog/">Блог</a>
    </header>
    <main class="container">
        <article>
            <span class="badge">{category}</span>
            <h1>{title}</h1>
            <time>{date_str}</time>
            <div class="content">
                {content}
            </div>
            <div class="cta-banner">
                <h3>Рассчитайте доставку CDEK для вашего магазина</h3>
                <a href="/" class="btn-primary">Перейти к калькулятору</a>
            </div>
        </article>
    </main>
</body>
</html>"""

def update_sitemap(slug, date_str):
    sitemap_path = 'sitemap.xml'
    url_node = f"{DOMAIN}/blog/{slug}/"
    
    if not os.path.exists(sitemap_path):
        root = ET.Element("urlset", xmlns="[http://www.sitemaps.org/schemas/sitemap/0.9](http://www.sitemaps.org/schemas/sitemap/0.9)")
        tree = ET.ElementTree(root)
    else:
        ET.register_namespace('', "[http://www.sitemaps.org/schemas/sitemap/0.9](http://www.sitemaps.org/schemas/sitemap/0.9)")
        tree = ET.parse(sitemap_path)
        root = tree.getroot()

    for url in root.findall('{[http://www.sitemaps.org/schemas/sitemap/0.9](http://www.sitemaps.org/schemas/sitemap/0.9)}url'):
        loc = url.find('{[http://www.sitemaps.org/schemas/sitemap/0.9](http://www.sitemaps.org/schemas/sitemap/0.9)}loc')
        if loc is not None and loc.text == url_node:
            return

    new_url = ET.SubElement(root, 'url')
    loc = ET.SubElement(new_url, 'loc')
    loc.text = url_node
    lastmod = ET.SubElement(new_url, 'lastmod')
    lastmod.text = date_str

    tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)

def update_blog_index(title, slug, category, date_str):
    blog_path = 'blog/index.html'
    
    new_card = f"""
    <!-- ARTICLE_CARD_START -->
    <div class="blog-card">
        <span class="category">{category}</span>
        <h2><a href="/blog/{slug}/">{title}</a></h2>
        <time>{date_str}</time>
        <a href="/blog/{slug}/">Читать далее →</a>
    </div>
    <!-- ARTICLE_CARD_END -->
    """
    
    if os.path.exists(blog_path):
        with open(blog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ищем место для вставки. Желательно после открывающего тега контейнера
        # Если у вас есть <div id="blog-grid"> или <main>, скрипт вставит карточку после него
        insert_marker = '<div class="blog-grid">'
        if insert_marker in content:
            content = content.replace(insert_marker, insert_marker + new_card, 1)
            with open(blog_path, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            print("Внимание: Не найден маркер <div class='blog-grid'> в blog/index.html. Карточка не добавлена на главную.")

def main():
    keyword, category, slug = get_next_unique_keyword()
    if not keyword:
        return

    print(f"Генерируем статью: {keyword} -> /blog/{slug}/")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    content = generate_article_content(keyword)
    full_html = build_full_html_page(keyword.capitalize(), content, slug, category, date_str)

    folder_path = os.path.join('blog', slug)
    os.makedirs(folder_path, exist_ok=True)
    
    file_path = os.path.join(folder_path, 'index.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    update_sitemap(slug, date_str)
    update_blog_index(keyword.capitalize(), slug, category, date_str)
    print("Готово!")

if __name__ == "__main__":
    main()
