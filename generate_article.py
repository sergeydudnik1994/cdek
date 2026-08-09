import os
import re
import csv
import json
from datetime import datetime
import xml.etree.ElementTree as ET
from google import genai

# Настройки
DOMAIN = "https://cdek-marketplace.ru"
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY не найден в переменных окружения. Убедитесь, что он добавлен в GitHub Secrets.")

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

    for row in keywords:
        if selected_row is None:
            slug = slugify(row[0])
            folder_path = os.path.join('blog', slug)
            if not os.path.exists(folder_path):
                selected_row = row
                selected_slug = slug
                continue
        remaining_rows.append(row)

    if not selected_row:
        print("Все ключи из файла уже обработаны.")
        return None, None, None

    with open('keywords.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(remaining_rows)

    archived_exists = os.path.exists('keywords_done.csv')
    with open('keywords_done.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if not archived_exists:
            writer.writerow(header + ['date_processed'])
        writer.writerow(selected_row + [datetime.now().strftime("%Y-%m-%d %H:%M")])

    keyword = selected_row[0].strip()
    category = selected_row[1].strip() if len(selected_row) > 1 else "Блог"
    return keyword, category, selected_slug

def generate_article_content(keyword, category):
    prompt = f"""
    Ты — эксперт по B2B логистике. Напиши полезную SEO-статью по запросу: "{keyword}".
    Целевая аудитория: селлеры Wildberries, Ozon, Яндекс Маркета.
    
    Верни ответ СТРОГО в формате валидного JSON (без форматирования markdown типа ```json):
    {{
      "title": "Привлекательный H1 заголовок (без названия бренда)",
      "description": "Краткое описание на 2-3 предложения (для карточки превью).",
      "html_body": "HTML код самой статьи"
    }}

    Требования к html_body:
    1. Не используй теги <html>, <body>, <article> или <h1>. Начинай сразу с текста <p> или подзаголовка <h2>.
    2. Обязательно используй классы Tailwind CSS для оформления:
       - Для <h2>: class="text-2xl sm:text-3xl font-bold text-white pt-6 pb-2 border-b border-slate-800"
       - Для <p>: оставляй просто <p> без классов.
       - Для <ul>: class="list-disc list-inside space-y-1 ml-2"
       - Если делаешь таблицу, используй структуру:
         <div class="overflow-x-auto my-6"><table class="w-full text-left text-sm sm:text-base"><thead><tr class="bg-slate-800 text-white"><th class="p-4 rounded-tl-xl font-bold">...</th>...</tr></thead><tbody class="divide-y divide-slate-800 bg-slate-900/50"><tr><td class="p-4">...</td>...</tr></tbody></table></div>
    3. Добавь блок с акцентом через:
       <div class="bg-cdek/10 border-l-4 border-cdek p-4 rounded-r-xl text-white"><strong>Важно:</strong> Текст...</div>
    4. Статья должна быть подробной, с примерами, сравнениями FBS/FBO или тарифов.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )

        text_response = response.text.replace("```json", "").replace("```", "").strip()

