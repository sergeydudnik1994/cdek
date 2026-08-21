<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

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
  
  <!-- SEO: Заголовки и описания -->
  <title>{{SEO_TITLE}}</title>
  <meta name="description" content="{{SEO_DESC}}" />

  <!-- SEO: Верификация и канонический адрес -->
  <meta name="yandex-verification" content="f077a22013388718" />
  <meta name="yandex-verification" content="feb8f4adaa02427e" />
  <meta name="google-site-verification" content="b4CjmaWn0KRmnHjAm7abquUe5bkx0Colk-B61Fw698Y" />
  <meta name="theme-color" content="#00b341" />
  <link rel="canonical" href="{{CANONICAL_URL}}" />
  
  <!-- Автообнаружение LLMs.txt для ИИ-агентов -->
  <link rel="alternate" type="text/markdown" title="LLM Information" href="https://cdek-marketplace.ru/llms.txt" />
  <link rel="alternate" type="text/markdown" title="LLM Full Documentation" href="https://cdek-marketplace.ru/llms-full.txt" />

  <!-- OG теги для соцсетей -->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="СДЭК для маркетплейсов" />
  <meta property="og:locale" content="ru_RU" />
  <meta property="og:title" content="{{SEO_TITLE}}" />
  <meta property="og:description" content="{{SEO_DESC}}" />
  <meta property="og:image" content="https://cdek-marketplace.ru/logo.png" />
  <meta property="og:url" content="{{CANONICAL_URL}}" />

  <!-- Favicons -->
  <link rel="icon" href="/favicon.ico" sizes="any" />
  <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="apple-touch-icon" href="/favicon.png" />

  <!-- 1. МИКРОРАЗМЕТКА ОРГАНИЗАЦИИ / LOCAL BUSINESS -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "СДЭК {{CITY_PREP}}",
    "url": "{{CANONICAL_URL}}",
    "logo": "https://cdek-marketplace.ru/logo.png",
    "telephone": "+7-993-322-15-20",
    "priceRange": "₽₽",
    "openingHours": "Mo-Su 09:00-18:00",
    "contactPoint": {
      "@type": "ContactPoint",
      "telephone": "+7-993-322-15-20",
      "contactType": "customer service",
      "email": "sv.dudnik@cdek.ru",
      "availableLanguage": "Russian"
    },
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "{{CITY_NAME}}",
      "addressCountry": "RU"
    },
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.9",
      "reviewCount": "{{REVIEWS}}"
    },
    "sameAs": [
      "https://t.me/cdek_marketplace",
      "https://wa.me/79933221520",
      "https://max.ru/u/f9LHodD0cOIzaS1qORDXcJzrkKFof3ACzehNo6cFxOcrfwa6KtVgohy-Pxo"
    ],
    "makesOffer": {
      "@type": "Offer",
      "itemOffered": {
        "@type": "Service",
        "name": "{{H1_MAIN}}",
        "description": "{{SEO_DESC}}"
      }
    }
  }
  </script>

  <!-- 2. МИКРОРАЗМЕТКА ХЛЕБНЫЕ КРОШКИ -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "Главная",
        "item": "https://cdek-marketplace.ru/"
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": "{{CITY_NAME}}",
        "item": "https://cdek-marketplace.ru/geo/{{CITY_SLUG}}/"
      },
      {
        "@type": "ListItem",
        "position": 3,
        "name": "{{H1_MAIN}}",
        "item": "{{CANONICAL_URL}}"
      }
    ]
  }
  </script>

  <!-- 3. МИКРОРАЗМЕТКА FAQ ДЛЯ ИИ-ПОИСКОВИКОВ -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "Как подключить {{H1_MAIN}}?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Подайте заявку онлайн через форму на странице. Оформление B2B-договора СДЭК занимает 15 минут дистанционно через СМС или ЭДО."
        }
      },
      {
        "@type": "Question",
        "name": "Сколько стоит заключение договора?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Подключение бесплатно (0 ₽). Скидки на логистику маркетплейсов составляют до 50% от базовых тарифов."
        }
      }
    ]
  }
  </script>

  <!-- Tailwind CSS -->
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

  <!-- Виджет СДЭК -->
  <script src="https://cdn.jsdelivr.net/npm/@cdek-it/widget@3" async></script>
</head>
<body class="bg-[#072624] text-slate-100 min-h-screen flex flex-col antialiased selection:bg-[#00b341] selection:text-white pb-16 md:pb-0">

  <!-- Шапка сайта -->
  <!--#include virtual="/src/components/header.html" -->

  <main class="flex-grow pt-8 pb-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- Хлебные крошки -->
      <nav class="text-sm text-slate-400 mb-6">
        <a href="/" class="hover:text-cdek transition-colors">Главная</a>
        <span class="mx-2">/</span>
        <a href="/geo/{{CITY_SLUG}}/" class="hover:text-cdek transition-colors">{{CITY_NAME}}</a>
        <span class="mx-2">/</span>
        <span class="text-white">{{H1_MAIN}}</span>
      </nav>

      <!-- Главный заголовок и уникальное гео-описание -->
      <div class="text-center max-w-3xl mx-auto mt-6 mb-12">
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 mb-6 rounded-full text-xs font-semibold tracking-wide uppercase transition-all border bg-[#0e3330] text-[#00b341] border border-emerald-800/80">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cdek opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-cdek"></span>
          </span>
          <span>Официальный B2B сервис {{PREP_V}}</span>
        </div>

        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white tracking-normal mb-5 leading-tight">
          {{H1_MAIN}}
        </h1>
        {{H1_SUB_BLOCK}}
        
        <p class="text-base sm:text-lg text-slate-400 leading-relaxed mt-4">
          {{DESC}}
        </p>

        <!-- Динамическая статистика -->
        <div class="grid grid-cols-3 gap-4 max-w-xl mx-auto mt-8 pt-6 border-t border-emerald-950">
          <div>
            <p class="text-2xl sm:text-3xl font-bold text-cdek">0 ₽</p>
            <p class="text-xs text-slate-500 font-medium mt-0.5">Договор бесплатно</p>
          </div>
          <div>
            <p class="text-2xl sm:text-3xl font-bold text-white">до 50%</p>
            <p class="text-xs text-slate-500 font-medium mt-0.5">Скидка B2B</p>
          </div>
          <div>
            <p class="text-2xl sm:text-3xl font-bold text-white">15 мин</p>
            <p class="text-xs text-slate-500 font-medium mt-0.5">Подключение онлайн</p>
          </div>
        </div>
      </div>

      <!-- Уникальный блок логистики города -->
      <div class="max-w-4xl mx-auto my-10 p-6 rounded-2xl bg-[#0a2f2c] border border-emerald-900/60 text-slate-300 text-sm leading-relaxed">
        <p>{{UNIQUE_CONTENT}}</p>
        <ul class="mt-4 space-y-2">
          {{PVZ_LIST}}
        </ul>
      </div>

      <!-- Калькулятор тарифов -->
      <section id="widget-section" class="mt-10">
        <!--#include virtual="/src/components/calculator-widget.html" -->
      </section>

      <!-- Блок платформ и маркетплейсов -->
      <div class="mt-16">
        <!--#include virtual="/src/components/platforms.html" -->
      </div>

      <!-- Форма онлайн-заявки -->
      <section id="contract-form-container" class="mt-16 max-w-xl mx-auto">
        <div class="text-center mb-6">
          <h2 class="text-2xl font-bold text-white">Оформить B2B-договор {{PREP_V}}</h2>
          <p class="text-sm text-slate-400 mt-1">Активация за 15 минут без визита в офис</p>
        </div>
        <!--#include virtual="/src/components/leadform.html" -->
      </section>

      <!-- Ближайшие города для перелинковки -->
      <div class="max-w-4xl mx-auto mt-16 pt-8 border-t border-emerald-950/80 text-xs text-slate-400">
        <span class="font-semibold text-slate-300 mr-2">Другие города региона:</span>
        {{NEARBY_CITIES}}
      </div>

      <!-- Блог -->
      <section class="py-16 mt-10">
        <!--#include virtual="/src/components/blog-latest.html" -->
      </section>

    </div>
  </main>

  <!-- Подвал сайта -->
  <!--#include virtual="/src/components/footer.html" -->

</body>
</html>
