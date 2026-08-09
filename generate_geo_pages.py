import os
import re

# Словарь для городов с особыми/сложными формами склонения
SPECIAL_CITIES = {
    "Сочи": ("Сочи", "Сочи", "в Сочи"),
    "Тольятти": ("Тольятти", "Тольятти", "в Тольятти"),
    "Улан-Удэ": ("Улан-Удэ", "Улан-Удэ", "в Улан-Удэ"),
    "Надым": ("Надыма", "Надыме", "в Надыме"),
    "Санкт-Петербург": (
        "Санкт-Петербурга",
        "Санкт-Петербурге",
        "в Санкт-Петербурге",
    ),
    "Нижний Новгород": (
        "Нижнего Новгорода",
        "Нижнем Новгороде",
        "в Нижнем Новгороде",
    ),
    "Великий Новгород": (
        "Великого Новгорода",
        "Великом Новгороде",
        "в Великом Новгороде",
    ),
    "Старый Оскол": ("Старого Оскола", "Старом Осколе", "в Старом Осколе"),
    "Красное Село": ("Красного Села", "Красном Селе", "в Красном Селе"),
    "Набережные Челны": (
        "Набережных Челнов",
        "Набережных Челнах",
        "в Набережных Челнах",
    ),
    "Минеральные Воды": (
        "Минеральных Вод",
        "Минеральных Водах",
        "в Минеральных Водах",
    ),
    "Гусь-Хрустальный": (
        "Гусь-Хрустального",
        "Гусь-Хрустальном",
        "в Гусь-Хрустальном",
    ),
    "Ростов-на-Дону": (
        "Ростова-на-Дону",
        "Ростове-на-Дону",
        "в Ростове-на-Дону",
    ),
    "Комсомольск-на-Амуре": (
        "Комсомольска-на-Амуре",
        "Комсомольске-на-Амуре",
        "в Комсомольске-на-Амуре",
    ),
    "Славянск-на-Кубани": (
        "Славянска-на-Кубани",
        "Славянске-на-Кубани",
        "в Славянске-на-Кубани",
    ),
    "Горячий Ключ": ("Горячего Ключа", "Горячем Ключе", "в Горячем Ключе"),
    "Сергиев Посад": ("Сергиева Посада", "Сергиевом Посаде", "в Сергиевом Посаде"),
    "Орехово-Зуево": ("Орехово-Зуева", "Орехово-Зуеве", "в Орехово-Зуеве"),
    "Переславль-Залесский": (
        "Переславля-Залесского",
        "Переславле-Залесском",
        "в Переславле-Залесском",
    ),
    "Каменск-Уральский": (
        "Каменска-Уральского",
        "Каменске-Уральском",
        "в Каменске-Уральском",
    ),
    "Каменск-Шахтинский": (
        "Каменска-Шахтинского",
        "Каменске-Шахтинском",
        "в Каменске-Шахтинском",
    ),
    "Камень-на-Оби": ("Камня-на-Оби", "Камне-на-Оби", "в Камне-на-Оби"),
    "Новый Уренгой": ("Нового Уренгоя", "Новом Уренгое", "в Новом Уренгое"),
    "Великие Луки": ("Великих Лук", "Великих Луках", "в Великих Луках"),
}

FEMININE_SOFT_CITIES = {
    "Казань",
    "Пермь",
    "Тюмень",
    "Рязань",
    "Тверь",
    "Астрахань",
    "Керчь",
    "Ярославль",
    "Сызрань",
    "Рославль",
}


def get_city_cases(city_name):
  city_name = city_name.strip()
  if city_name in SPECIAL_CITIES:
    return SPECIAL_CITIES[city_name]

  prep = "во" if city_name.startswith(("Владимир", "Владивосток")) else "в"
  words = city_name.split()

  def process_word(w):
    parts = w.split("-")
    gen_parts, prep_parts = [], []

    for part in parts:
      if part in FEMININE_SOFT_CITIES:
        gen_parts.append(part[:-1] + "и")
        prep_parts.append(part[:-1] + "и")
      elif part.endswith("ий"):
        gen_parts.append(
            part[:-2] + "его"
            if part in ["Нижний", "Великий"]
            else part[:-2] + "ого"
        )
        prep_parts.append(
            part[:-2] + "ем"
            if part in ["Нижний", "Великий"]
            else part[:-2] + "ом"
        )
      elif part.endswith("ый") or part.endswith("ой"):
        gen_parts.append(part[:-2] + "ого")
        prep_parts.append(part[:-2] + "ом")
      elif part.endswith("ая"):
        gen_parts.append(part[:-2] + "ой")
        prep_parts.append(part[:-2] + "ой")
      elif part.endswith("ое") or part.endswith("ее"):
        gen_parts.append(part[:-2] + "ого")
        prep_parts.append(part[:-2] + "ом")
      elif part.endswith("а"):
        if len(part) > 2 and part[-2] in "гкхжчшщ":
          gen_parts.append(part[:-1] + "и")
        else:
          gen_parts.append(part[:-1] + "ы")
        prep_parts.append(part[:-1] + "е")
      elif part.endswith("я"):
        if part.endswith("ия"):
          gen_parts.append(part[:-1] + "и")
          prep_parts.append(part[:-1] + "и")
        else:
          gen_parts.append(part[:-1] + "и")
          prep_parts.append(part[:-1] + "е")
      elif part.endswith("о"):
        gen_parts.append(part[:-1] + "а")
        prep_parts.append(part[:-1] + "е")
      elif part.endswith("е"):
        gen_parts.append(part[:-1] + "я")
        prep_parts.append(part[:-1] + "е")
      elif part.endswith("ь"):
        gen_parts.append(part[:-1] + "я")
        prep_parts.append(part[:-1] + "е")
      elif re.search(r"[бвгджзклмнпрстфхцчшщ]$", part, re.I):
        gen_parts.append(part + "а")
        prep_parts.append(part + "е")
      else:
        gen_parts.append(part)
        prep_parts.append(part)

    return "-".join(gen_parts), "-".join(prep_parts)

  gen_words, prep_words = [], []
  for word in words:
    gw, pw = process_word(word)
    gen_words.append(gw)
    prep_words.append(pw)

  genitive = " ".join(gen_words)
  prepositional = " ".join(prep_words)
  v_prep = f"{prep} {prepositional}"

  return genitive, prepositional, v_prep


def build_city_html(slug, city_name, pvz_count):
  city_genitive, city_prepositional, prep_v = get_city_cases(city_name)

  return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <!-- Yandex.Metrika counter -->
  <script type="text/javascript">
      (function(m,e,t,r,i,k,a){{
          m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
          m[i].l=1*new Date();
          for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }} }}
          k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
      }})(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=111090265', 'ym');

      ym(111090265, 'init', {{ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true}});
  </script>
  <noscript><div><img src="https://mc.yandex.ru/watch/111090265" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
  <!-- /Yandex.Metrika counter -->
  
  <!-- SEO: Заголовки и описания -->
  <title>СДЭК для селлеров {prep_v}: логистика FBS/DBS | Маркетплейсы</title>
  <meta name="description" content="Официальный договор со СДЭК для селлеров из {city_genitive}. Отгрузка через {pvz_count} ПВЗ {prep_v}. Интеграция с Wildberries, Ozon, Яндекс Маркетом и Авито. Скидки на логистику до 50%." />

  <!-- SEO: Верификация и OG теги -->
  <meta name="yandex-verification" content="f077a22013388718" />
  <meta name="yandex-verification" content="feb8f4adaa02427e" />
  <meta name="google-site-verification" content="b4CjmaWn0KRmnHjAm7abquUe5bkx0Colk-B61Fw698Y" />
  <meta name="theme-color" content="#8DE21A" />
  <link rel="canonical" href="https://cdek-marketplace.ru/geo/{slug}/" />
  
  <!-- OG теги для соцсетей -->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="СДЭК для маркетплейсов" />
  <meta property="og:locale" content="ru_RU" />
  <meta property="og:title" content="СДЭК для селлеров {prep_v}: логистика FBS/DBS" />
  <meta property="og:description" content="Официальный договор со СДЭК для селлеров из {city_genitive}. Отгрузка через {pvz_count} ПВЗ {prep_v}. Скидки до 50%." />
  <meta property="og:image" content="https://cdek-marketplace.ru/logo.png" />
  <meta property="og:url" content="https://cdek-marketplace.ru/geo/{slug}/" />
  <link rel="icon" type="image/png" href="/favicon.png" />

  <!-- 1. МИКРОРАЗМЕТКА ОРГАНИЗАЦИИ / ЛОКАЛЬНОГО БИЗНЕСА -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "СДЭК для маркетплейсов {prep_v}",
    "url": "https://cdek-marketplace.ru/geo/{slug}/",
    "logo": "https://cdek-marketplace.ru/logo.png",
    "telephone": "+7-993-322-15-20",
    "contactPoint": {{
      "@type": "ContactPoint",
      "telephone": "+7-993-322-15-20",
      "contactType": "customer service",
      "email": "sv.dudnik@cdek.ru",
      "availableLanguage": "Russian"
    }},
    "address": {{
      "@type": "PostalAddress",
      "addressLocality": "{city_name}",
      "addressCountry": "RU"
    }},
    "sameAs": [
      "https://t.me/cdek_marketplace",
      "https://wa.me/79933221520"
    ],
    "makesOffer": {{
      "@type": "Offer",
      "itemOffered": {{
        "@type": "Service",
        "name": "Подключение селлеров к логистике СДЭК (FBS/DBS) {prep_v}",
        "description": "Официальная логистика для продавцов Wildberries, Ozon, Яндекс Маркета и Авито через {pvz_count} ПВЗ {prep_v} со скидкой до 50%."
      }}
    }}
  }}
  </script>

  <!-- 2. МИКРОРАЗМЕТКА ХЛЕБНЫЕ КРОШКИ (3 уровня) -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{
        "@type": "ListItem",
        "position": 1,
        "name": "Главная",
        "item": "https://cdek-marketplace.ru/"
      }},
      {{
        "@type": "ListItem",
        "position": 2,
        "name": "Логистика для селлеров",
        "item": "https://cdek-marketplace.ru/geo/"
      }},
      {{
        "@type": "ListItem",
        "position": 3,
        "name": "{city_prepositional}",
        "item": "https://cdek-marketplace.ru/geo/{slug}/"
      }}
    ]
  }}
  </script>

  <!-- 3. МИКРОРАЗМЕТКА FAQ -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [{{
      "@type": "Question",
      "name": "Сколько времени занимает подключение к СДЭК для селлеров {prep_v}?",
      "@acceptedAnswer": {{
        "@type": "Answer",
        "text": "Подписание договора и настройка личного кабинета занимает от 15 минут. Вы сможете начать отгрузки {prep_v} в тот же день."
      }}
    }}, {{
      "@type": "Question",
      "name": "С какими маркетплейсами вы работаете {prep_v}?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "Мы доставляем заказы до складов и ПВЗ Wildberries, Ozon, Яндекс Маркет, Мегамаркет и Авито по схемам FBS и DBS {prep_v}."
      }}
    }}, {{
      "@type": "Question",
      "name": "Нужно ли платить за заключение договора {prep_v}?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "Нет, заключение договора абсолютно бесплатно. Селлеры {prep_v} получают скидку до 50% на логистику."
      }}
    }}]
  }}
  </script>

  <!-- Tailwind CSS через CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            cdek: '#8de21a',
            dark: {{ 900: '#0b101d' }}
          }}
        }}
      }}
    }}
  </script>

  <!-- Виджет СДЭК -->
  <script src="https://cdn.jsdelivr.net/npm/@cdek-it/widget@3" async></script>
</head>
<body class="bg-dark-900 text-slate-100 min-h-screen flex flex-col antialiased selection:bg-cdek selection:text-dark-900 pb-16 md:pb-0">

  <!-- Nginx: Подключение шапки -->
  <!--#include virtual="/src/components/header.html" -->

  <main class="flex-grow pt-8 pb-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- ВИЗУАЛЬНЫЕ ХЛЕБНЫЕ КРОШКИ -->
      <nav class="text-sm text-slate-400 mb-6">
        <a href="/" class="hover:text-cdek transition-colors">Главная</a>
        <span class="mx-2">/</span>
        <a href="/geo/" class="hover:text-cdek transition-colors">Логистика для селлеров</a>
        <span class="mx-2">/</span>
        <span class="text-white">{city_prepositional}</span>
      </nav>

      <!-- УНИКАЛЬНЫЙ ГЕО-ЗАГОЛОВОК И СТАТИСТИКА -->
      <div class="text-center max-w-3xl mx-auto mt-6 mb-12">
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 mb-6 rounded-full text-xs font-semibold tracking-wide uppercase transition-all border bg-cdek/10 text-cdek border-cdek/30">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cdek opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-cdek shadow-[0_0_8px_#8DE21A]"></span>
          </span>
          <span>Официальное подключение для бизнеса {prep_v}</span>
        </div>

        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white tracking-normal mb-5 leading-tight">
          Подключение селлеров к СДЭК в <span class="text-cdek">{city_prepositional}</span>
        </h1>
        <p class="text-base sm:text-lg text-slate-400 leading-relaxed">
          Специальные условия логистики для бизнеса из {city_genitive} при отгрузках на маркетплейсы. Бесплатный договор и скидки до 50% на доставку по моделям <b class="text-white">FBS и DBS</b>.
        </p>

        <!-- Динамическая статистика -->
        <div class="grid grid-cols-3 gap-4 max-w-xl mx-auto mt-8 pt-6 border-t border-slate-800">
          <div>
            <p class="text-2xl sm:text-3xl font-bold text-cdek drop-shadow-[0_0_8px_rgba(141,226,26,0.3)]">0 ₽</p>
            <p class="text-xs text-slate-500 font-medium mt-0.5">Договор бесплатно</p>
          </div>
          <div>
            <p class="text-2xl sm:text-3xl font-bold text-white">до 50%</p>
            <p class="text-xs text-slate-500 font-medium mt-0.5">Экономия на тарифах</p>
          </div>
          <div>
            <p class="text-2xl sm:text-3xl font-bold text-white">{pvz_count}</p>
            <p class="text-xs text-slate-500 font-medium mt-0.5">ПВЗ для отгрузки</p>
          </div>
        </div>
      </div>

      <!-- Калькулятор -->
      <section id="widget-section" class="mt-10">
        <!--#include virtual="/src/components/calculator-widget.html" -->
      </section>

      <!-- Блок маркетплейсов -->
      <div class="mt-16">
        <!--#include virtual="/src/components/platforms.html" -->
      </div>

      <!-- Форма заявки -->
      <section id="leadForm" class="mt-16 max-w-xl mx-auto">
        <div class="text-center mb-6">
          <h2 class="text-2xl font-bold text-white">Оставить заявку на договор {prep_v}</h2>
          <p class="text-sm text-slate-400 mt-1">Подключим за 15 минут без визита в офис</p>
        </div>
        <!--#include virtual="/src/components/leadform.html" -->
      </section>

      <!-- Секция блога -->
      <section class="py-16 mt-10">
        <!--#include virtual="/src/components/blog-latest.html" -->
      </section>

    </div>
  </main>

  <!-- Nginx: Подвал и мобильная кнопка -->
  <!--#include virtual="/src/components/footer.html" -->
  <!--#include virtual="/src/components/mobile-cta.html" -->

</body>
</html>"""


def main():
  geo_index_path = os.path.join("geo", "index.html")
  if not os.path.exists(geo_index_path):
    print(f"Ошибка: файл {geo_index_path} не найден!")
    return

  with open(geo_index_path, "r", encoding="utf-8") as f:
    content = f.read()

  pattern = (
      r'href="/geo/([^/]+)/".*?<span[^>]*>([^<]+)</span>\s*<span[^>]*>([^<]+)</span>'
  )
  matches = re.findall(pattern, content, re.DOTALL)

  if not matches:
    print("Города не найдены в geo/index.html")
    return

  print(f"Найдено {len(matches)} городов в каталоге geo/index.html...")

  count = 0
  for slug, city_name, pvz_str in matches:
    pvz_count = pvz_str.replace(" ПВЗ СДЭК", "").replace(" ПВЗ", "").strip()

    folder_path = os.path.join("geo", slug)
    os.makedirs(folder_path, exist_ok=True)

    html_content = build_city_html(slug, city_name.strip(), pvz_count)

    file_path = os.path.join(folder_path, "index.html")
    with open(file_path, "w", encoding="utf-8") as f:
      f.write(html_content)

    count += 1
    print(f"[{count}/{len(matches)}] Страница создана: {file_path}")

  print(
      f"\n ГОТОВО! Все {count} страниц городов успешно обновлены по новому"
      " шаблону!"
  )


if __name__ == "__main__":
  main()
