import os
import json

SPECIAL_CITIES = {
    "Сочи": ("Сочи", "Сочи", "в Сочи"),
    "Тольятти": ("Тольятти", "Тольятти", "в Тольятти"),
    "Улан-Удэ": ("Улан-Удэ", "Улан-Удэ", "в Улан-Удэ"),
    "Надым": ("Надыма", "Надыме", "в Надыме"),
    "Санкт-Петербург": ("Санкт-Петербурга", "Санкт-Петербурге", "в Санкт-Петербурге"),
    "Москва": ("Москвы", "Москве", "в Москве"),
    "Нижний Новгород": ("Нижнего Новгорода", "Нижнем Новгороде", "в Нижнем Новгороде"),
    "Великий Новгород": ("Великого Новгорода", "Великом Новгороде", "в Великом Новгороде"),
    "Старый Оскол": ("Старого Оскола", "Старом Осколе", "в Старом Осколе"),
    "Красное Село": ("Красного Села", "Красном Селе", "в Красном Селе"),
    "Набережные Челны": ("Набережных Челнов", "Набережных Челнах", "в Набережных Челнах"),
    "Минеральные Воды": ("Минеральных Вод", "Минеральных Водах", "в Минеральных Водах"),
    "Гусь-Хрустальный": ("Гусь-Хрустального", "Гусь-Хрустальном", "в Гусь-Хрустальном"),
    "Ростов-на-Дону": ("Ростова-на-Дону", "Ростове-на-Дону", "в Ростове-на-Дону"),
    "Иваново": ("Иванова", "Иванове", "в Иваново"),
    "Кемерово": ("Кемерова", "Кемерове", "в Кемерово"),
}

FEMININE_SOFT_CITIES = {"Казань", "Пермь", "Тюмень", "Рязань", "Тверь", "Астрахань", "Керчь", "Сызрань"}

def get_city_cases(city_name):
    city_name = city_name.strip()
    if city_name in SPECIAL_CITIES: return SPECIAL_CITIES[city_name]
    prep = "во" if city_name.startswith(("Владимир", "Владивосток", "Владикавказ", "Всеволожск")) else "в"
    words = city_name.split()
    def process_word(w):
        parts = w.split("-")
        gen_parts, prep_parts = [], []
        for idx, part in enumerate(parts):
            if len(parts) > 1 and idx == 0 and part.endswith("о"):
                gen_parts.append(part); prep_parts.append(part); continue
            if part in FEMININE_SOFT_CITIES:
                gen_parts.append(part[:-1] + "и"); prep_parts.append(part[:-1] + "и")
            elif part.endswith("ий"):
                gen_parts.append(part[:-2] + "его" if part == "Нижний" else part[:-2] + "ого")
                prep_parts.append(part[:-2] + "ем" if part == "Нижний" else part[:-2] + "ом")
            elif part.endswith("ый") or part.endswith("ой"):
                gen_parts.append(part[:-2] + "ого"); prep_parts.append(part[:-2] + "ом")
            elif part.endswith("ая"):
                gen_parts.append(part[:-2] + "ой"); prep_parts.append(part[:-2] + "ой")
            elif part.endswith("ое") or part.endswith("ее"):
                gen_parts.append(part[:-2] + "ого"); prep_parts.append(part[:-2] + "ом")
            elif part.endswith("а"):
                gen_parts.append(part[:-1] + "и" if len(part) > 2 and part[-2] in "гкхжчшщ" else part[:-1] + "ы")
                prep_parts.append(part[:-1] + "е")
            elif part.endswith("я"):
                gen_parts.append(part[:-1] + "и"); prep_parts.append(part[:-1] + "и" if part.endswith("ия") else part[:-1] + "е")
            elif part.endswith("о"):
                gen_parts.append(part[:-1] + "а"); prep_parts.append(part[:-1] + "е")
            elif part.endswith("е"):
                gen_parts.append(part[:-1] + "я"); prep_parts.append(part[:-1] + "е")
            elif part.endswith("ь"):
                gen_parts.append(part[:-1] + "я"); prep_parts.append(part[:-1] + "е")
            elif any(part.endswith(c) for c in "бвгджзклмнпрстфхцчшщ"):
                gen_parts.append(part + "а"); prep_parts.append(part + "е")
            else:
                gen_parts.append(part); prep_parts.append(part)
        return "-".join(gen_parts), "-".join(prep_parts)
    gen_words, prep_words = [], []
    for word in words:
        gw, pw = process_word(word)
        gen_words.append(gw); prep_words.append(pw)
    return " ".join(gen_words), " ".join(prep_words), f"{prep} {' '.join(prep_words)}"

HTML_TEMPLATE = """<!DOCTYPE html>
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
  <meta property="og:locale" content="ru_RU" />
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
          { "@type": "ListItem", "position": 2, "name": "Города", "item": "https://cdek-marketplace.ru/geo/" },
          { "@type": "ListItem", "position": 3, "name": "{{CITY_NAME}}", "item": "https://cdek-marketplace.ru/geo/{{CITY_SLUG}}/" },
          { "@type": "ListItem", "position": 4, "name": "{{H1_MAIN}}", "item": "{{CANONICAL_URL}}" }
        ]
      },
      {
        "@type": "Service",
        "name": "{{H1_MAIN}} {{PREP_V}}",
        "provider": {
          "@type": "Organization",
          "name": "СДЭК Маркетплейсы",
          "url": "https://cdek-marketplace.ru/"
        },
        "areaServed": {
          "@type": "City",
          "name": "{{CITY_NAME}}"
        },
        "description": "{{SEO_DESC}}"
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
      <a href="/geo/{{CITY_SLUG}}/" class="hover:text-[#00b341] transition-colors">{{CITY_NAME}}</a> <span>/</span>
      <span class="text-white">{{H1_MAIN}}</span>
    </nav>

    <div class="grid lg:grid-cols-12 gap-10 lg:gap-16 items-start">
      <div class="lg:col-span-7 flex flex-col items-start pt-2">
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 mb-6 rounded-full text-xs font-bold uppercase tracking-wider bg-[#0e3330] text-[#00b341] border border-emerald-800/80">
          Логистика {{PREP_V}} • СДЭК
        </div>

        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-black text-white leading-tight mb-4">
          {{H1_MAIN}} <span class="text-[#00b341]">{{PREP_V}}</span>
        </h1>

        <p class="text-slate-300 text-base sm:text-lg leading-relaxed mb-8">
          {{DESC}} Оптимизируйте отгрузки на склады маркетплейсов и доставку покупателям из {{GEN_NAME}}. Специальные тарифы B2B со скидкой до 50% и сдача посылок без очередей.
        </p>

        <div class="grid grid-cols-3 gap-4 py-6 border-y border-emerald-950 w-full mb-8">
          <div>
            <p class="text-2xl sm:text-3xl font-black text-[#00b341]">до 50%</p>
            <p class="text-xs text-slate-400 font-medium">Скидка B2B</p>
          </div>
          <div>
            <p class="text-2xl sm:text-3xl font-black text-white">15 мин</p>
            <p class="text-xs text-slate-400 font-medium">Договор онлайн</p>
          </div>
          <div>
            <p class="text-2xl sm:text-3xl font-black text-white">4 000+</p>
            <p class="text-xs text-slate-400 font-medium">ПВЗ для сдачи</p>
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

def generate_industry_geo():
    with open("cities.json", "r", encoding="utf-8") as f:
        cities = json.load(f)

    with open("scripts/industry_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    industries = data.get("industries", [])
    print(f"🚀 Генерация отраслевой гео-матрицы СДЭК ({len(industries)} ниш x {len(cities)} городов)...")

    count = 0
    for city in cities:
        city_slug = city["slug"]
        city_name = city["name"]
        gen_name, prep_name, prep_v = get_city_cases(city_name)

        for ind in industries:
            ind_slug = ind["slug"]
            h1_main = ind["h1_main"]
            desc = ind["desc"]

            canonical_url = f"https://cdek-marketplace.ru/geo/{city_slug}/{ind_slug}/"
            seo_title = f"СДЭК {h1_main} {prep_v} для селлеров — Доставка со скидкой 50%"
            seo_desc = f"Официальная логистика СДЭК: {h1_main.lower()} {prep_v}. {desc} Корпоративные тарифы B2B со скидкой до 50%, отгрузка через ПВЗ {prep_v}."

            page_html = HTML_TEMPLATE.replace("{{SEO_TITLE}}", seo_title)\
                                     .replace("{{SEO_DESC}}", seo_desc)\
                                     .replace("{{CANONICAL_URL}}", canonical_url)\
                                     .replace("{{CITY_NAME}}", city_name)\
                                     .replace("{{CITY_SLUG}}", city_slug)\
                                     .replace("{{H1_MAIN}}", h1_main)\
                                     .replace("{{PREP_V}}", prep_v)\
                                     .replace("{{GEN_NAME}}", gen_name)\
                                     .replace("{{DESC}}", desc)

            dir_path = os.path.join("geo", city_slug, ind_slug)
            os.makedirs(dir_path, exist_ok=True)
            with open(os.path.join(dir_path, "index.html"), "w", encoding="utf-8") as f:
                f.write(page_html)
            count += 1

    print(f"✅ Успешно сгенерировано {count} гео-отраслевых страниц в geo/.")

if __name__ == "__main__":
    generate_industry_geo()
