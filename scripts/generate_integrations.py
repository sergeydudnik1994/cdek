import os
import json

# Базовый чистый HTML-шаблон для страниц модулей
ITEM_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
  <!-- Yandex.Metrika counter -->
  <script type="text/javascript">
    (function(m,e,t,r,i,k,a){
        m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    })(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=111090265', 'ym');
    ym(111090265, 'init', {ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true});
  </script>
  <noscript><div><img src="https://mc.yandex.ru/watch/111090265" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
  <!-- /Yandex.Metrika counter -->

  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{{SEO_TITLE}}</title>
  <meta name="description" content="{{SEO_DESC}}" />
  <meta name="theme-color" content="#072624" />
  <link rel="canonical" href="{{CANONICAL_URL}}" />
  <link rel="icon" type="image/png" href="/favicon.png" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="СДЭК Маркетплейсы" />
  <meta property="og:title" content="{{SEO_TITLE}}" />
  <meta property="og:description" content="{{SEO_DESC}}" />
  <meta property="og:image" content="https://cdek-marketplace.ru/logo.png" />
  <meta property="og:url" content="{{CANONICAL_URL}}" />

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://cdek-marketplace.ru/" },
          { "@type": "ListItem", "position": 2, "name": "Интеграции", "item": "https://cdek-marketplace.ru/integrations/" },
          { "@type": "ListItem", "position": 3, "name": "{{NAME}}", "item": "{{CANONICAL_URL}}" }
        ]
      },
      {
        "@type": "Service",
        "name": "Интеграция СДЭК с {{NAME}}",
        "provider": {
          "@type": "Organization",
          "name": "СДЭК Маркетплейсы",
          "url": "https://cdek-marketplace.ru/"
        },
        "description": "{{DESC}}"
      }
    ]
  }
  </script>

  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            cdek: '#00b341',
            dark: { 900: '#072624', 950: '#041615' }
          }
        }
      }
    }
  </script>
</head>
<body class="bg-dark-900 text-slate-100 min-h-screen flex flex-col antialiased pb-16 md:pb-0 selection:bg-[#00b341] selection:text-white">
  <!--#include virtual="/src/components/header.html" -->

  <main class="flex-grow max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 sm:pt-12 pb-20 w-full">
    <nav class="text-xs sm:text-sm text-slate-400 mb-6 flex flex-wrap items-center gap-1.5">
      <a href="/" class="hover:text-[#00b341] transition-colors">Главная</a> <span>/</span>
      <a href="/integrations/" class="hover:text-[#00b341] transition-colors">Интеграции</a> <span>/</span>
      <span class="text-white">{{NAME}}</span>
    </nav>

    <div class="grid lg:grid-cols-12 gap-10 lg:gap-16 items-start">
      <div class="lg:col-span-7 flex flex-col items-start pt-2">
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 mb-6 rounded-full text-xs font-bold uppercase bg-[#0e3330] text-[#00b341] border border-emerald-800/80">
          {{CATEGORY}} • Готовое решение
        </div>

        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-black text-white leading-tight mb-4">
          Интеграция СДЭК с <span class="text-[#00b341]">{{NAME}}</span>
        </h1>

        <p class="text-slate-300 text-base sm:text-lg leading-relaxed mb-8">
          {{DESC}} Официальный плагин связывает витрину с логистической базой СДЭК для мгновенного расчета стоимости, выбора ПВЗ на карте и автоматической генерации накладных.
        </p>

        <div class="grid grid-cols-3 gap-4 py-6 border-y border-emerald-950 w-full mb-8">
          <div>
            <p class="text-2xl sm:text-3xl font-black text-[#00b341]">до 50%</p>
            <p class="text-xs text-slate-400 font-medium">Скидка B2B</p>
          </div>
          <div>
            <p class="text-2xl sm:text-3xl font-black text-white">15 мин</p>
            <p class="text-xs text-slate-400 font-medium">Настройка API</p>
          </div>
          <div>
            <p class="text-2xl sm:text-3xl font-black text-white">4 000+</p>
            <p class="text-xs text-slate-400 font-medium">ПВЗ на карте</p>
          </div>
        </div>
      </div>

      <div class="lg:col-span-5 sticky top-28" id="leadForm">
        <!--#include virtual="/src/components/leadform.html" -->
      </div>
    </div>
  </main>

  <!--#include virtual="/src/components/footer.html" -->
</body>
</html>"""

# Базовый HTML-шаблон для каталога /integrations/
CATALOG_HUB_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
  <!-- Yandex.Metrika counter -->
  <script type="text/javascript">
    (function(m,e,t,r,i,k,a){
        m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    })(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=111090265', 'ym');
    ym(111090265, 'init', {ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true});
  </script>
  <noscript><div><img src="https://mc.yandex.ru/watch/111090265" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
  <!-- /Yandex.Metrika counter -->

  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Модули интеграции СДЭК — Официальный каталог готовых решений для CMS, CRM и маркетплейсов</title>
  <meta name="description" content="Полный каталог официальных модулей интеграции СДЭК: 1C-Битрикс, Tilda, InSales, WooCommerce, МойСклад, 1С, RetailCRM, Битрикс24, amoCRM, OpenCart и 20+ других систем." />
  <meta name="theme-color" content="#072624" />
  <link rel="canonical" href="https://cdek-marketplace.ru/integrations/" />
  <link rel="icon" type="image/png" href="/favicon.png" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="СДЭК Маркетплейсы" />
  <meta property="og:title" content="Модули интеграции СДЭК — 30 готовых решений" />
  <meta property="og:description" content="Официальное подключение логистики СДЭК к любой CMS, CRM и учетной системе за 15 минут со скидкой до 50%." />
  <meta property="og:url" content="https://cdek-marketplace.ru/integrations/" />
  <meta property="og:image" content="https://cdek-marketplace.ru/logo.png" />

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://cdek-marketplace.ru/" },
      { "@type": "ListItem", "position": 2, "name": "Интеграции", "item": "https://cdek-marketplace.ru/integrations/" }
    ]
  }
  </script>

  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            cdek: '#00b341',
            dark: { 900: '#072624', 950: '#041615' }
          }
        }
      }
    }
  </script>
</head>
<body class="bg-dark-900 text-slate-100 min-h-screen flex flex-col antialiased pb-16 md:pb-0 selection:bg-[#00b341] selection:text-white">
  <!--#include virtual="/src/components/header.html" -->

  <main class="flex-grow max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-10 pb-20 w-full">
    <div class="mb-14 text-center">
      <div class="inline-flex items-center gap-2 px-3.5 py-1.5 mb-4 rounded-full text-xs font-bold uppercase tracking-wider bg-[#0e3330] text-[#00b341] border border-emerald-800/80">
        Ready-to-use API & CMS Modules
      </div>
      <h1 class="text-4xl md:text-5xl lg:text-6xl font-black text-white mb-4 tracking-tight">
        Модули интеграции <span class="text-[#00b341]">СДЭК</span>
      </h1>
      <p class="text-slate-300 text-base md:text-lg max-w-3xl mx-auto">
        Официальные модули и плагины для автоматического расчета тарифов, интерактивной карты ПВЗ и пакетного создания накладных в вашей системе за 15 минут.
      </p>
    </div>

    {{CATEGORIES_CONTENT}}

    <div class="mt-16">
      <!--#include virtual="/src/components/calculator-widget.html" -->
    </div>
  </main>

  <!--#include virtual="/src/components/footer.html" -->
  <!--#include virtual="/src/components/mobile-cta.html" -->
</body>
</html>"""

def load_data():
    data_path = "scripts/integrations_data.json"
    if not os.path.exists(data_path):
        return []
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("integrations", data) if isinstance(data, dict) else data

def generate_catalog_hub(items):
    # Группировка по категориям
    grouped = {}
    for item in items:
        cat = item.get("category", "Готовые решения")
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(item)

    categories_html = []
    for cat_name, cat_items in grouped.items():
        cards_html = []
        for item in cat_items:
            slug = item["slug"]
            name = item["name"]
            desc = item.get("desc", f"Официальный модуль СДЭК для {name}.")
            
            card = f"""
            <a href="/integrations/{slug}/" class="group flex flex-col justify-between bg-[#0b3330]/60 border border-emerald-800/60 hover:border-[#00b341] hover:bg-[#0e3330] rounded-2xl p-5 sm:p-6 transition-all duration-300 shadow-md">
              <div>
                <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 mb-3 rounded-md text-[10px] font-extrabold uppercase tracking-wider bg-[#072624] text-[#00b341] border border-emerald-800/80">
                  {cat_name}
                </div>
                <h3 class="text-lg sm:text-xl font-bold text-white mb-2 group-hover:text-[#00b341] transition-colors">{name}</h3>
                <p class="text-slate-300 text-xs sm:text-sm leading-relaxed mb-4">{desc}</p>
              </div>
              <div class="flex items-center justify-between pt-4 border-t border-emerald-900/80 text-xs">
                <span class="text-slate-400 font-medium">Готовый модуль</span>
                <span class="text-[#00b341] font-bold group-hover:translate-x-1 transition-transform">Подключить →</span>
              </div>
            </a>"""
            cards_html.append(card)

        section = f"""
        <div class="mb-14">
          <div class="flex items-center gap-3 mb-6 pb-2 border-b border-emerald-950">
            <span class="w-2.5 h-2.5 rounded-full bg-[#00b341]"></span>
            <h2 class="text-xl sm:text-2xl font-black text-white uppercase tracking-wide">{cat_name}</h2>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 sm:gap-6">
            {''.join(cards_html)}
          </div>
        </div>"""
        categories_html.append(section)

    return CATALOG_HUB_TEMPLATE.replace("{{CATEGORIES_CONTENT}}", "\n".join(categories_html))

def generate_all():
    items = load_data()
    if not items:
        print("⚠️ Нет данных для генерации интеграций.")
        return

    os.makedirs("integrations", exist_ok=True)

    # 1. Генерация каталога /integrations/index.html
    print("🚀 Генерация полного каталога СДЭК (30 официальных модулей интеграции)...")
    hub_content = generate_catalog_hub(items)
    with open(os.path.join("integrations", "index.html"), "w", encoding="utf-8") as f:
        f.write(hub_content)

    # 2. Генерация отдельных посадочных страниц
    count = 0
    for item in items:
        slug = item["slug"]
        name = item["name"]
        desc = item.get("desc", f"Официальный модуль интеграции СДЭК для {name}.")
        category = item.get("category", "Готовое решение")
        canonical_url = f"https://cdek-marketplace.ru/integrations/{slug}/"

        seo_title = f"СДЭК Интеграция с {name} — Официальный модуль доставки"
        seo_desc = f"Официальный модуль интеграции СДЭК для {name}. {desc} Подключение за 15 минут со скидками до 50%."

        page_html = ITEM_PAGE_TEMPLATE.replace("{{SEO_TITLE}}", seo_title)\
                                      .replace("{{SEO_DESC}}", seo_desc)\
                                      .replace("{{CANONICAL_URL}}", canonical_url)\
                                      .replace("{{NAME}}", name)\
                                      .replace("{{CATEGORY}}", category)\
                                      .replace("{{DESC}}", desc)

        dir_path = os.path.join("integrations", slug)
        os.makedirs(dir_path, exist_ok=True)
        with open(os.path.join(dir_path, "index.html"), "w", encoding="utf-8") as f:
            f.write(page_html)
        count += 1

    print(f"✅ Успешно сгенерировано {count} страниц модулей интеграции и каталог integrations/index.html.")

if __name__ == "__main__":
    generate_all()
