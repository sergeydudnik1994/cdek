import os
import json
import re

def generate_industries():
    # 1. Загрузка данных
    with open("scripts/industry_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    icons = {
        "odezhda-i-obuv": '<path d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" stroke-width="2"/>',
        "mebel-i-interer": '<path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" stroke-width="2"/>',
        "elektronika-i-tehnika": '<path d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" stroke-width="2"/>',
        "detskie-tovary": '<path d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke-width="2"/>',
        "kosmetika-i-parfyumeriya": '<path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.673.337a4 4 0 01-2.506.326l-2.299-.46a6 6 0 01-3.712-2.328l-.706-.883a2 2 0 00-1.022-.547V3.5h16.286v11.928z" stroke-width="2"/>',
        "avtotovary-i-zapchasti": '<path d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" stroke-width="2"/>',
        "tovary-dlya-zhivotnyh": '<path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" stroke-width="2"/>',
        "sporttovary": '<path d="M13 10V3L4 14h7v7l9-11h-7z" stroke-width="2"/>',
        "stroitelstvo-i-remont": '<path d="M11 4a2 2 0 114 0v1a2 2 0 01-2 2 2 2 0 01-2-2V4zm3 11l3 1m-7 3l-2-3m-7-8l7-7m2 9v10" stroke-width="2"/>',
        "produkty-pitaniya": '<path d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" stroke-width="2"/>',
        "osveshchenie-i-svet": '<path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.543 2.22a1 1 0 01-.97.78H10.44a1 1 0 01-.97-.78l-.543-2.22z" stroke-width="2"/>',
        "kantstovary-i-ofis": '<path d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" stroke-width="2"/>',
        "sad-i-ogorod": '<path d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" stroke-width="2"/>',
        "tovary-dlya-tvorchestva": '<path d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1" stroke-width="2"/>',
        "bizhuteriya-i-aksessuary": '<path d="M12 8v4l3 2m6-2a9 9 0 11-18 0 9 9 0 0118 0z" stroke-width="2"/>',
        "instrumenty": '<path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" stroke-width="2"/>',
        "bytovaya-tekhnika": '<path d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" stroke-width="2"/>',
        "tovary-dlya-zdorovya": '<path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" stroke-width="2"/>',
        "avtoelektronika": '<path d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke-width="2"/>',
        "turizm-i-otdykh": '<path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" stroke-width="2"/>',
        "podarki-i-suveniry": '<path d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7" stroke-width="2"/>',
        "muzykalnye-instrumenty": '<path d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" stroke-width="2"/>',
        "santekhnika": '<path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" stroke-width="2"/>',
        "umnyy-dom": '<path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" stroke-width="2"/>',
        "tekstil-dlya-doma": '<path d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" stroke-width="2"/>',
        "klimaticheskaya-tekhnika": '<path d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.99 7.99 0 0120 13a7.98 7.98 0 01-2.343 5.657z" stroke-width="2"/>',
        "posuda-i-kuhnya": '<path d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke-width="2"/>',
        "rybalka-i-okhota": '<path d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" stroke-width="2"/>',
        "igrovye-pristavki": '<path d="M11 4a2 2 0 114 0v1a2 2 0 01-2 2 2 2 0 01-2-2V4zm3 11l3 1m-7 3l-2-3m-7-8l7-7m2 9v10" stroke-width="2"/>',
        "kantstovary": '<path d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" stroke-width="2"/>',
        "aksessuary-dlya-smartfonov": '<path d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" stroke-width="2"/>',
        "elektrosamokaty-i-velosipedy": '<path d="M13 10V3L4 14h7v7l9-11h-7z" stroke-width="2"/>'
    }

    os.makedirs("solutions", exist_ok=True)
    
    # 2. Генерация 32 посадочных страниц ниш с идеальным SEO
    count = 0
    for ind in data["industries"]:
        slug = ind["slug"]
        h1_main = ind["h1_main"]
        h1_sub = ind.get("h1_sub", "")
        desc = ind["desc"]
        canonical_url = f"https://cdek-marketplace.ru/solutions/{slug}/"
        
        seo_title = f"СДЭК Доставка — {h1_main} | Тарифы со скидкой до 50%"
        seo_desc = f"Официальная доставка СДЭК для селлеров и магазинов: {h1_main.lower()}. {desc} Скидки B2B до 50%, интеграция с маркетплейсами, договор за 15 минут."

        sub_block = f'<span class="block text-2xl sm:text-3xl mt-2 text-cdek">{h1_sub}</span>' if h1_sub else ""

        page_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{seo_title}</title>
  <meta name="description" content="{seo_desc}" />
  <meta name="theme-color" content="#00b341" />
  <link rel="canonical" href="{canonical_url}" />
  <link rel="icon" type="image/png" href="/favicon.png" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="СДЭК Маркетплейсы" />
  <meta property="og:locale" content="ru_RU" />
  <meta property="og:title" content="{seo_title}" />
  <meta property="og:description" content="{seo_desc}" />
  <meta property="og:image" content="https://cdek-marketplace.ru/logo.png" />
  <meta property="og:url" content="{canonical_url}" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://cdek-marketplace.ru/" }},
          {{ "@type": "ListItem", "position": 2, "name": "Решения", "item": "https://cdek-marketplace.ru/solutions/" }},
          {{ "@type": "ListItem", "position": 3, "name": "{h1_main}", "item": "{canonical_url}" }}
        ]
      }},
      {{
        "@type": "Service",
        "name": "СДЭК Доставка: {h1_main}",
        "provider": {{
          "@type": "Organization",
          "name": "СДЭК Маркетплейсы",
          "url": "https://cdek-marketplace.ru/"
        }},
        "description": "{desc}"
      }}
    ]
  }}
  </script>

  <script src="https://cdn.tailwindcss.com"></script>
  <script>tailwind.config={{theme:{{extend:{{colors: { cdek: '#00b341', dark: { 900: '#072624', 950: '#041615' } } }}}}}}}}}}</script>
</head>
<body class="bg-dark-900 text-slate-100 min-h-screen flex flex-col antialiased pb-16 md:pb-0">
  <!--#include virtual="/src/components/header.html" -->

  <main class="flex-grow max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 sm:pt-12 pb-20 w-full">
    <nav class="text-xs sm:text-sm text-slate-400 mb-6 flex flex-wrap items-center gap-1.5">
      <a href="/" class="hover:text-cdek transition-colors">Главная</a> <span>/</span>
      <a href="/solutions/" class="hover:text-cdek transition-colors">Решения</a> <span>/</span>
      <span class="text-white">{h1_main}</span>
    </nav>

    <div class="grid lg:grid-cols-12 gap-10 lg:gap-16 items-start">
      <div class="lg:col-span-7 flex flex-col items-start pt-2">
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 mb-6 rounded-full text-xs font-semibold uppercase tracking-wider bg-cdek/10 text-cdek border border-cdek/30">
          Отраслевое решение • СДЭК
        </div>

        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-black text-white leading-tight mb-4">
          {h1_main}
          {sub_block}
        </h1>

        <p class="text-slate-300 text-base sm:text-lg leading-relaxed mb-8">
          {desc} Оптимизируйте логистику для Wildberries, Ozon, Яндекс Маркета и собственного интернет-магазина. Отгружайте заказы через 4 000+ ПВЗ без очередей по корпоративным тарифам со скидкой до 50%.
        </p>

        <div class="grid grid-cols-3 gap-4 py-6 border-y border-emerald-950 w-full mb-8">
          <div>
            <p class="text-2xl sm:text-3xl font-bold text-cdek">до 50%</p>
            <p class="text-xs text-slate-400">Скидка B2B</p>
          </div>
          <div>
            <p class="text-2xl sm:text-3xl font-bold text-white">15 мин</p>
            <p class="text-xs text-slate-400">Договор онлайн</p>
          </div>
          <div>
            <p class="text-2xl sm:text-3xl font-bold text-white">4 000+</p>
            <p class="text-xs text-slate-400">ПВЗ для сдачи</p>
          </div>
        </div>
      </div>

      <div class="lg:col-span-5 sticky top-28" id="leadForm">
        <!--#include virtual="/src/components/leadform.html" -->
      </div>
    </div>

    <div class="mt-14">
      <!--#include virtual="/src/components/calculator-widget.html" -->
    </div>
  </main>

  <!--#include virtual="/src/components/footer.html" -->
  <!--#include virtual="/src/components/mobile-cta.html" -->
</body>
</html>"""
        
        dir_path = os.path.join("solutions", slug)
        os.makedirs(dir_path, exist_ok=True)
        with open(os.path.join(dir_path, "index.html"), "w", encoding="utf-8") as f:
            f.write(page_html)
        count += 1

    print(f"✅ Успешно сгенерировано {count} отраслевых решений в папке solutions/.")

if __name__ == "__main__":
    generate_industries()
