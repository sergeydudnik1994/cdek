import csv
from datetime import datetime
import json
import os
import re
import time
import xml.etree.ElementTree as ET
from google import genai

# Настройки
DOMAIN = "[https://cdek-marketplace.ru](https://cdek-marketplace.ru)"
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
  raise ValueError(
      "GEMINI_API_KEY не найден в переменных окружения. Убедитесь, что он"
      " добавлен в GitHub Secrets."
  )

client = genai.Client(api_key=API_KEY)


def slugify(text):
  translit_map = {
      "а": "a",
      "б": "b",
      "в": "v",
      "г": "g",
      "д": "d",
      "е": "e",
      "ё": "yo",
      "ж": "zh",
      "з": "z",
      "и": "i",
      "й": "y",
      "к": "k",
      "л": "l",
      "м": "m",
      "н": "n",
      "о": "o",
      "п": "p",
      "р": "r",
      "с": "s",
      "т": "t",
      "у": "u",
      "ф": "f",
      "х": "h",
      "ц": "ts",
      "ч": "ch",
      "ш": "sh",
      "щ": "sch",
      "ъ": "",
      "ы": "y",
      "ь": "",
      "э": "e",
      "ю": "yu",
      "я": "ya",
      " ": "-",
      "_": "-",
      ",": "",
      ".": "",
  }
  text = text.lower().strip()
  res = "".join([translit_map.get(c, c) if c.isalnum() else "-" for c in text])
  return re.sub(r"-+", "-", res).strip("-")


def get_next_unique_keyword():
  if not os.path.exists("keywords.csv"):
    print("Файл keywords.csv не найден.")
    return None, None, None

  with open("keywords.csv", "r", encoding="utf-8") as f:
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
      folder_path = os.path.join("blog", slug)
      if not os.path.exists(folder_path):
        selected_row = row
        selected_slug = slug
        continue
    remaining_rows.append(row)

  if not selected_row:
    print("Все ключи из файла уже обработаны.")
    return None, None, None

  with open("keywords.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(remaining_rows)

  archived_exists = os.path.exists("keywords_done.csv")
  with open("keywords_done.csv", "a", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    if not archived_exists:
      writer.writerow(header + ["date_processed"])
    writer.writerow(selected_row + [datetime.now().strftime("%Y-%m-%d %H:%M")])

  keyword = selected_row[0].strip()
  category = (
      selected_row[1].strip()
      if len(selected_row) > 1
      else "Блог для селлеров"
  )
  return keyword, category, selected_slug


def generate_article_content(keyword, category):
  prompt = f"""
    Ты — эксперт по B2B логистике. Напиши полезную SEO-статью по запросу: "{keyword}".
    Целевая аудитория: селлеры Wildberries, Ozon, Яндекс Маркета.
    
    Верни ответ СТРОГО в формате валидного JSON (без форматирования markdown типа ```json):
    {{
      "title": "Привлекательный H1 заголовок (без названия бренда)",
      "description": "Краткое описание на 2-3 предложения (для карточки превью).",
      "html_body": "HTML код самой статьи (БЕЗ БЛОКА FAQ В КОНЦЕ)",
      "faq": [
        {{
          "question": "Первый частый вопрос по теме статьи?",
          "answer": "Развернутый понятный ответ на вопрос."
        }},
        {{
          "question": "Второй частый вопрос по теме статьи?",
          "answer": "Развернутый понятный ответ на вопрос."
        }}
      ]
    }}

    Требования к html_body:
    1. Не используй теги <html>, <body>, <article> или <h1>. Начинай сразу с текста <p> или подзаголовка <h2>.
    2. Обязательно используй классы Tailwind CSS для оформления:
       - Для <h2>: class="text-2xl sm:text-3xl font-bold text-white pt-6 pb-2 border-b border-slate-800"
       - Для <p>: оставляй просто <p> без классов.
       - Для <ul>: class="list-disc list-inside space-y-1 ml-2"
       - Если делаешь таблицу, используй структуру:
          <div class="overflow-x-auto my-6"><table class="w-full text-left text-sm sm:text-base"><thead><tr class="bg-slate-800 text-white"><th class="p-4 rounded-tl-xl font-bold">...</th></tr></thead><tbody class="divide-y divide-slate-800 bg-slate-900/50"><tr><td class="p-4">...</td></tr></tbody></table></div>
    3. Добавь акцентный блок:
       <div class="bg-cdek/10 border-l-4 border-cdek p-4 rounded-r-xl text-white"><strong>Важно:</strong> Текст...</div>
    4. НЕ вставляй блок FAQ в html_body — передай вопросы и ответы строго в массиве "faq".
    5. Статья должна быть подробной, с примерами, сравнениями FBS/FBO или тарифов СДЭК.
    """

  max_retries = 3
  retry_delay = 45  # Пауза для сброса минутного лимита токенов (Free Tier)

  for attempt in range(1, max_retries + 1):
    try:
      print(f"Запрос к Gemini API (попытка {attempt}/{max_retries})...")
      response = client.models.generate_content(
          model="gemini-2.0-flash",
          contents=prompt,
      )

      text_response = (
          response.text.replace("```json", "").replace("```", "").strip()
      )

      try:
        data = json.loads(text_response)
        return data
      except json.JSONDecodeError:
        print("Ошибка парсинга JSON от Gemini. Получен текст:", text_response)
        return {
            "title": keyword.capitalize(),
            "description": (
                "Полезная статья о том, как использовать логистику CDEK для"
                f" запроса: {keyword}."
            ),
            "html_body": f"<p>{text_response}</p>",
            "faq": [],
        }

    except Exception as e:
      print(
          f"Предупреждение: ошибка обращения к API (попытка {attempt}): {e}"
      )
      if attempt < max_retries:
        print(f"Ждем {retry_delay} секунд для сброса лимита запросов...")
        time.sleep(retry_delay)
      else:
        print("Превышено максимальное число попыток.")
        raise e


def build_full_html_page(
    title, description, content, slug, category, date_str, faq_list
):
  canonical_url = f"{DOMAIN}/blog/{slug}/"

  # 1. Формируем единую микроразметку Schema.org (BreadcrumbList + BlogPosting + FAQPage)
  schema_graph = [
      {
          "@type": "BreadcrumbList",
          "itemListElement": [
              {
                  "@type": "ListItem",
                  "position": 1,
                  "name": "Главная",
                  "item": f"{DOMAIN}/",
              },
              {
                  "@type": "ListItem",
                  "position": 2,
                  "name": "Блог",
                  "item": f"{DOMAIN}/blog/",
              },
              {
                  "@type": "ListItem",
                  "position": 3,
                  "name": title,
                  "item": canonical_url,
              },
          ],
      },
      {
          "@type": "BlogPosting",
          "headline": title,
          "description": description,
          "datePublished": date_str,
          "dateModified": date_str,
          "author": {"@type": "Organization", "name": "CDEK Marketplace"},
          "publisher": {
              "@type": "Organization",
              "name": "CDEK Marketplace",
              "logo": {
                  "@type": "ImageObject",
                  "url": f"{DOMAIN}/favicon.png",
              },
          },
          "mainEntityOfPage": {"@type": "WebPage", "@id": canonical_url},
      },
  ]

  # Если есть вопросы и ответы, добавляем в схему блок FAQPage
  if faq_list:
    faq_entities = []
    for item in faq_list:
      q = item.get("question", "")
      a = item.get("answer", "")
      if q and a:
        faq_entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        })
    if faq_entities:
      schema_graph.append({
          "@type": "FAQPage",
          "mainEntity": faq_entities,
      })

  schema_json = json.dumps(
      {"@context": "https://schema.org", "@graph": schema_graph},
      ensure_ascii=False,
      indent=2,
  )

  # 2. Формируем визуальный блок FAQ в конце статьи
  faq_html = ""
  if faq_list:
    details_items = []
    for item in faq_list:
      q = item.get("question", "")
      a = item.get("answer", "")
      if q and a:
        details_items.append(f"""            <details class="group bg-slate-900/50 p-5 rounded-2xl border border-slate-800">
              <summary class="font-bold text-white cursor-pointer list-none flex justify-between items-center">
                <span>{q}</span>
                <span class="text-cdek transition-transform group-open:rotate-180">&darr;</span>
              </summary>
              <p class="mt-3 text-slate-400 text-sm sm:text-base">{a}</p>
            </details>""")

    if details_items:
      # ИСПРАВЛЕНИЕ: Вынесли join за пределы f-строки
      joined_items = "\n".join(details_items)
      faq_html = f"""
        <!-- Блок FAQ для расширенного сниппета -->
        <div class="mt-12 pt-8 border-t border-slate-800">
          <h2 class="text-2xl sm:text-3xl font-bold text-white mb-6">Часто задаваемые вопросы</h2>
          <div class="space-y-4">
{joined_items}
          </div>
        </div>"""

  # 3. Собираем итоговую HTML-страницу
  return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  
  <title>{title} — CDEK для маркетплейсов</title>
  <meta name="description" content="{description}" />
  <link rel="icon" type="image/png" href="/favicon.png" />

  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{ extend: {{ colors: {{ cdek: '#8de21a', dark: {{ 900: '#0b101d' }} }} }} }}
    }}
  </script>

  <!-- SEO Микроразметка: BreadcrumbList + BlogPosting + FAQPage -->
  <script type="application/ld+json">
{schema_json}
  </script>
</head>
<body class="bg-dark-900 text-slate-100 min-h-screen flex flex-col antialiased selection:bg-cdek selection:text-dark-900 pb-16 md:pb-0">

  <!--#include virtual="/src/components/header.html" -->

  <main class="flex-grow py-12 sm:py-16">
    <article class="max-w-3xl mx-auto px-4 sm:px-6">
      
      <header class="mb-10 sm:mb-14 text-center">
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 mb-6 rounded-full text-xs font-semibold tracking-wide uppercase border bg-cdek/10 text-cdek border-cdek/30">
          <span>{category}</span>
        </div>
        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-black text-white mb-6 leading-tight tracking-tight">
          {title}
        </h1>
      </header>

      <div class="glass p-6 sm:p-10 rounded-3xl border border-slate-800 text-slate-300 text-base sm:text-lg leading-relaxed space-y-6">
        {content}
        {faq_html}
      </div>
    </article>

    <!--#include virtual="/src/components/related-articles.html" -->

    <div class="max-w-3xl mx-auto px-4 sm:px-6 mt-12" id="leadForm">
      <!--#include virtual="/src/components/leadform.html" -->
    </div>
  </main>

  <!--#include virtual="/src/components/footer.html" -->
  <!--#include virtual="/src/components/mobile-cta.html" -->

</body>
</html>"""


def update_sitemap(slug, date_str):
  sitemap_path = "sitemap.xml"
  url_node = f"{DOMAIN}/blog/{slug}/"
  ns = "http://www.sitemaps.org/schemas/sitemap/0.9"

  try:
    ET.register_namespace("", ns)
    tree = ET.parse(sitemap_path)
    root = tree.getroot()

    for url in root.findall(f"{{{ns}}}url"):
      loc = url.find(f"{{{ns}}}loc")
      if loc is not None and loc.text == url_node:
        return

    new_url = ET.Element("url")
    loc = ET.SubElement(new_url, "loc")
    loc.text = url_node

    lastmod = ET.SubElement(new_url, "lastmod")
    lastmod.text = date_str

    changefreq = ET.SubElement(new_url, "changefreq")
    changefreq.text = "weekly"

    priority = ET.SubElement(new_url, "priority")
    priority.text = "0.8"

    root.insert(2, new_url)

    tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)
    print(f"Ссылка добавлена в {sitemap_path}")
  except Exception as e:
    print(f"Ошибка обновления sitemap.xml: {e}")


def update_blog_index(title, description, slug, category):
  blog_path = "src/components/blog-grid.html"

  new_card = f"""
  <a href="/blog/{slug}/" class="group block p-6 rounded-3xl bg-slate-900/50 border border-slate-800 hover:border-cdek/50 transition-colors duration-300 flex flex-col justify-between">
    <div>
      <div class="text-cdek text-xs font-bold uppercase tracking-wide mb-3">{category}</div>
      <h3 class="text-xl font-bold text-white mb-3 group-hover:text-cdek transition-colors">{title}</h3>
      <p class="text-sm text-slate-400 mb-6 line-clamp-3">{description}</p>
    </div>
    <span class="text-cdek text-sm font-semibold inline-flex items-center gap-1 group-hover:translate-x-1 transition-transform">
      Читать статью &rarr;
    </span>
  </a>"""

  if os.path.exists(blog_path):
    with open(blog_path, "r", encoding="utf-8") as f:
      content = f.read()

    insert_marker = (
        '<div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl'
        ' mx-auto px-4 sm:px-6">'
    )

    if insert_marker in content:
      content = content.replace(
          insert_marker, insert_marker + "\n" + new_card, 1
      )
      with open(blog_path, "w", encoding="utf-8") as f:
        f.write(content)
      print("Сетка блога (blog-grid.html) обновлена.")
    else:
      print(
          "Внимание: Не найден тег сетки в blog-grid.html. Вставка в начало"
          " файла..."
      )
      with open(blog_path, "w", encoding="utf-8") as f:
        f.write(new_card + "\n" + content)
  else:
    print(
        f"Файл {blog_path} не найден! Убедитесь, что запускаете скрипт из корня"
        " репозитория."
    )


def main():
  keyword, category, slug = get_next_unique_keyword()
  if not keyword:
    return

  print(f"Генерируем статью: {keyword} -> /blog/{slug}/")
  date_str = datetime.now().strftime("%Y-%m-%d")

  ai_data = generate_article_content(keyword, category)

  title = ai_data.get("title", keyword.capitalize())
  description = ai_data.get("description", f"Статья на тему {keyword}")
  html_body = ai_data.get("html_body", "<p>Контент готовится...</p>")
  faq_list = ai_data.get("faq", [])

  full_html = build_full_html_page(
      title, description, html_body, slug, category, date_str, faq_list
  )

  folder_path = os.path.join("blog", slug)
  os.makedirs(folder_path, exist_ok=True)

  file_path = os.path.join(folder_path, "index.html")
  with open(file_path, "w", encoding="utf-8") as f:
    f.write(full_html)
  print(f"Файл создан: {file_path}")

  update_sitemap(slug, date_str)
  update_blog_index(title, description, slug, category)
  print("Процесс успешно завершен!")


if __name__ == "__main__":
  main()
