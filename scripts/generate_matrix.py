from datetime import datetime
import json
import os

DATA_FILE = "scripts/seo_data.json"
TEMPLATE_FILE = "scripts/template.html"
BASE_OUTPUT_DIR = "geo"
SITEMAP_FILE = "sitemap.xml"
CITIES_JSON_FILE = "cities.json"


def get_city_cases(city_name):
  city_name = city_name.strip()

  # Словарь точных падежей для сложных городов
  special = {
      "Анжеро-Судженск": (
          "Анжеро-Судженска",
          "Анжеро-Судженске",
          "в Анжеро-Судженске",
          "Анжеро-Судженск",
      ),
      "Москва": ("Москвы", "Москве", "в Москве", "Москва"),
      "Санкт-Петербург": (
          "Санкт-Петербурга",
          "Санкт-Петербурге",
          "в Санкт-Петербурге",
          "Санкт-Петербург",
      ),
      "Краснодар": ("Краснодара", "Краснодаре", "в Краснодаре", "Краснодар"),
      "Екатеринбург": (
          "Екатеринбурга",
          "Екатеринбурге",
          "в Екатеринбурге",
          "Екатеринбург",
      ),
      "Новосибирск": (
          "Новосибирска",
          "Новосибирске",
          "в Новосибирске",
          "Новосибирск",
      ),
      "Казань": ("Казани", "Казани", "в Казани", "Казань"),
      "Нижний Новгород": (
          "Нижнего Новгорода",
          "Нижнем Новгороде",
          "в Нижнем Новгороде",
          "Нижний Новгород",
      ),
      "Челябинск": ("Челябинска", "Челябинске", "в Челябинске", "Челябинск"),
      "Самара": ("Самары", "Самаре", "в Самаре", "Самара"),
      "Ростов-на-Дону": (
          "Ростова-на-Дону",
          "Ростове-на-Дону",
          "в Ростове-на-Дону",
          "Ростов-на-Дону",
      ),
      "Химки": ("Химок", "Химках", "в Химках", "Химки"),
      "Мытищи": ("Мытищ", "Мытищах", "в Мытищах", "Мытищи"),
      "Чебоксары": ("Чебоксар", "Чебоксарах", "в Чебоксарах", "Чебоксары"),
      "Люберцы": ("Люберец", "Люберцах", "в Люберцах", "Люберцы"),
      "Березники": ("Березников", "Березниках", "в Березниках", "Березники"),
      "Шахты": ("Шахт", "Шахтах", "в Шахтах", "Шахты"),
  }

  if city_name in special:
    gen, prep, _, name = special[city_name]
    return {"name": name, "prep": prep, "gen": gen}

  # Общая морфологическая обработка для остальных городов
  if city_name.endswith("а"):
    gen = city_name[:-1] + "ы"
    prep = city_name[:-1] + "е"
  elif city_name.endswith("я"):
    gen = city_name[:-1] + "и"
    prep = city_name[:-1] + "е"
  elif city_name.endswith("о"):
    gen = city_name[:-1] + "а"
    prep = city_name[:-1] + "е"
  elif city_name.endswith("е"):
    gen = city_name[:-1] + "я"
    prep = city_name[:-1] + "е"
  elif city_name.endswith("ь"):
    gen = city_name[:-1] + "я"
    prep = city_name[:-1] + "е"
  elif city_name.endswith(("ий", "ый", "ой")):
    gen = city_name[:-2] + "ого"
    prep = city_name[:-2] + "ом"
  else:
    gen = city_name + "а"
    prep = city_name + "е"

  return {"name": city_name, "prep": prep, "gen": gen}


def load_data():
  with open(DATA_FILE, "r", encoding="utf-8") as f:
    return json.load(f)


def load_template():
  with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    return f.read()


def load_cities_map():
  """Загружает реальные русские названия из cities.json по слагу"""
  if os.path.exists(CITIES_JSON_FILE):
    with open(CITIES_JSON_FILE, "r", encoding="utf-8") as f:
      return {item["slug"]: item["name"] for item in json.load(f)}
  return {}


def generate_sitemap(city_slugs, services):
  today = datetime.now().strftime("%Y-%m-%d")
  base_url = "https://cdek-marketplace.ru"

  urls = [
      {"loc": f"{base_url}/", "priority": "1.0", "changefreq": "daily"},
      {"loc": f"{base_url}/geo/", "priority": "0.9", "changefreq": "daily"},
      {"loc": f"{base_url}/calculator/", "priority": "0.9", "changefreq": "weekly"},
      {
          "loc": f"{base_url}/calculator/dbs-1kg/",
          "priority": "0.9",
          "changefreq": "weekly",
      },
      {"loc": f"{base_url}/ozon/", "priority": "0.8", "changefreq": "weekly"},
      {
          "loc": f"{base_url}/wildberries/",
          "priority": "0.8",
          "changefreq": "weekly",
      },
      {
          "loc": f"{base_url}/yandex-market/",
          "priority": "0.8",
          "changefreq": "weekly",
      },
      {
          "loc": f"{base_url}/megamarket/",
          "priority": "0.8",
          "changefreq": "weekly",
      },
      {"loc": f"{base_url}/avito/", "priority": "0.8", "changefreq": "weekly"},
      {
          "loc": f"{base_url}/internet-magazin/",
          "priority": "0.8",
          "changefreq": "weekly",
      },
      {"loc": f"{base_url}/blog/", "priority": "0.8", "changefreq": "weekly"},
      {"loc": f"{base_url}/faq/", "priority": "0.7", "changefreq": "monthly"},
      {"loc": f"{base_url}/policy/", "priority": "0.3", "changefreq": "yearly"},
  ]

  for slug in city_slugs:
    urls.append(
        {"loc": f"{base_url}/geo/{slug}/", "priority": "0.6", "changefreq": "weekly"}
    )
    for service in services:
      urls.append({
          "loc": f"{base_url}/geo/{slug}/{service['slug']}/",
          "priority": "0.8",
          "changefreq": "weekly",
      })

  xml_lines = [
      '<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  ]

  for u in urls:
    xml_lines.append("  <url>")
    xml_lines.append(f'    <loc>{u["loc"]}</loc>')
    xml_lines.append(f"    <lastmod>{today}</lastmod>")
    xml_lines.append(f'    <changefreq>{u["changefreq"]}</changefreq>')
    xml_lines.append(f'    <priority>{u["priority"]}</priority>')
    xml_lines.append("  </url>")

  xml_lines.append("</urlset>")

  with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(xml_lines))

  print(f"🗺️ Карта sitemap.xml сгенерирована ({len(urls)} ссылок)!")


def generate_pages():
  data = load_data()
  template = load_template()
  cities_map = load_cities_map()

  if os.path.exists(BASE_OUTPUT_DIR):
    city_slugs = [
        d
        for d in os.listdir(BASE_OUTPUT_DIR)
        if os.path.isdir(os.path.join(BASE_OUTPUT_DIR, d))
    ]
  else:
    city_slugs = []

  generated_count = 0

  for slug in city_slugs:
    # Берем настоящее русское имя из cities.json
    raw_name = cities_map.get(slug, slug.replace("-", " ").title())
    city_info = get_city_cases(raw_name)

    for service in data["services"]:
      dir_path = os.path.join(BASE_OUTPUT_DIR, slug, service["slug"])
      os.makedirs(dir_path, exist_ok=True)

      breadcrumbs = f"""
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2 text-sm text-slate-500">
                <a href="/" class="hover:text-cdek">Главная</a> / 
                <a href="/geo/" class="hover:text-cdek">Логистика</a> / 
                <span class="text-slate-300">{city_info['name']}</span>
            </div>
            """

      html_content = template
      html_content = html_content.replace("{{BREADCRUMBS}}", breadcrumbs)
      html_content = html_content.replace("{{CITY_NAME}}", city_info["name"])
      html_content = html_content.replace("{{CITY_PREP}}", city_info["prep"])
      html_content = html_content.replace("{{CITY_GEN}}", city_info["gen"])
      html_content = html_content.replace("{{CITY_SLUG}}", slug)

      html_content = html_content.replace("{{SERVICE_SLUG}}", service["slug"])
      html_content = html_content.replace("{{H1_MAIN}}", service["h1_main"])
      html_content = html_content.replace("{{H1_SUB}}", service["h1_sub"])
      html_content = html_content.replace("{{DESC}}", service["desc"])

      file_path = os.path.join(dir_path, "index.html")
      with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
      generated_count += 1

  print(f"🚀 Сгенерировано {generated_count} SEO-страниц!")
  generate_sitemap(city_slugs, data["services"])


if __name__ == "__main__":
  generate_pages()
