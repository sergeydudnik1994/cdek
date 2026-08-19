import json, os, random, re

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
    "Комсомольск-на-Амуре": ("Комсомольска-на-Амуре", "Комсомольске-на-Амуре", "в Комсомольске-на-Амуре"),
    "Славянск-на-Кубани": ("Славянска-на-Кубани", "Славянске-на-Кубани", "в Славянске-на-Кубани"),
    "Горячий Ключ": ("Горячего Ключа", "Горячем Ключе", "в Горячем Ключе"),
    "Сергиев Посад": ("Сергиева Посада", "Сергиевом Посаде", "в Сергиевом Посаде"),
    "Орехово-Зуево": ("Орехово-Зуева", "Орехово-Зуеве", "в Орехово-Зуеве"),
    "Переславль-Залесский": ("Переславля-Залесского", "Переславле-Залесском", "в Переславле-Залесском"),
    "Каменск-Уральский": ("Каменска-Уральского", "Каменске-Уральском", "в Каменске-Уральском"),
    "Каменск-Шахтинский": ("Каменска-Шахтинского", "Каменске-Шахтинском", "в Каменске-Шахтинском"),
    "Камень-на-Оби": ("Камня-на-Оби", "Камне-на-Оби", "в Камне-на-Оби"),
    "Новый Уренгой": ("Нового Уренгоя", "Новом Уренгое", "в Новом Уренгое"),
    "Великие Луки": ("Великих Лук", "Великих Луках", "в Великих Луках"),
    "Анжеро-Судженск": ("Анжеро-Судженска", "Анжеро-Судженске", "в Анжеро-Судженске"),
    "Аргун": ("Аргуна", "Аргуне", "в Аргуне"),
    "Химки": ("Химок", "Химках", "в Химках"),
    "Мытищи": ("Мытищ", "Мытищах", "в Мытищах"),
    "Чебоксары": ("Чебоксар", "Чебоксарах", "в Чебоксарах"),
    "Люберцы": ("Люберец", "Люберцах", "в Люберцах"),
    "Березники": ("Березников", "Березниках", "в Березниках"),
    "Шахты": ("Шахт", "Шахтах", "в Шахтах"),
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
            elif re.search(r"[бвгджзклмнпрстфхцчшщ]$", part, re.I):
                gen_parts.append(part + "а"); prep_parts.append(part + "е")
            else:
                gen_parts.append(part); prep_parts.append(part)
        return "-".join(gen_parts), "-".join(prep_parts)
    gen_words, prep_words = [], []
    for word in words:
        gw, pw = process_word(word)
        gen_words.append(gw); prep_words.append(pw)
    return " ".join(gen_words), " ".join(prep_words), f"{prep} {' '.join(prep_words)}"

def generate_pages():
    with open("scripts/seo_data.json", "r", encoding="utf-8") as f: data = json.load(f)
    with open("scripts/template.html", "r", encoding="utf-8") as f: template = f.read()
    with open("cities.json", "r", encoding="utf-8") as f: cities = json.load(f)

    platforms = [{"slug": "wildberries", "name": "Wildberries"}, {"slug": "ozon", "name": "Ozon"}, {"slug": "yandex-market", "name": "Яндекс Маркет"}]

    print(f"🚀 Полная регенерация гео-матрицы СДЭК...")

    for city in cities:
        slug, name = city["slug"], city["name"]
        gen, prep, prep_v = get_city_cases(name)
        rng = random.Random(name)
        dist = (len(slug) * 150) + (ord(slug[0]) * 5)
        
        unique = f"Город {name} является важным звеном в логистической цепочке. " \
                 f"Основные перевозки {prep_v} осуществляются через местные развязки. " \
                 f"Это позволяет нам доставлять заказы до Москвы (около {dist} км) в рекордные сроки."

        pvz_html = "<li class='flex items-center gap-2'><span class='text-cdek'>•</span> Адреса ПВЗ доступны на карте при оформлении.</li>"
        nearby = random.sample(cities, min(5, len(cities)))
        links_html = " ".join([f"<a href='/geo/{c['slug']}/' class='text-cdek hover:underline mr-3'>{c['name']}</a>" for c in nearby])

        for s in data["services"]:
            canonical_base = f"https://cdek-marketplace.ru/geo/{slug}/{s['slug']}/"
            
            sub_title = s.get("h1_sub", "")
            sub_block = f'<span class="block text-2xl sm:text-3xl mt-2 text-cdek">{sub_title}</span>' if sub_title else ""

            raw_h1 = s['h1_main'].split(' в ')[0].strip()
            h1_main_geo = f"{raw_h1} {prep_v}"

            # SEO: бренд СДЭК на первом месте и емкое описание
            seo_title = f"СДЭК {raw_h1} {prep_v} — Договор за 15 минут"
            seo_desc = f"Официальный B2B договор со СДЭК {prep_v}: {raw_h1.lower()}. Скидки на логистику до 50%, отгрузка через ПВЗ без очередей по реестру. Быстрое подключение."

            reps = {
                "{{SEO_TITLE}}": seo_title,
                "{{SEO_DESC}}": seo_desc,
                "{{H1_MAIN}}": h1_main_geo,
                "{{H1_SUB_BLOCK}}": sub_block,
                "{{DESC}}": s.get("desc", ""),
                "{{CITY_NAME}}": name,
                "{{CITY_PREP}}": prep,
                "{{CITY_GEN}}": gen,
                "{{PREP_V}}": prep_v,
                "{{UNIQUE_CONTENT}}": unique,
                "{{PVZ_LIST}}": pvz_html,
                "{{NEARBY_CITIES}}": links_html,
                "{{CITY_SLUG}}": slug,
                "{{SERVICE_SLUG}}": s["slug"],
                "{{CANONICAL_URL}}": canonical_base,
                "{{REVIEWS}}": str(random.randint(120, 350))
            }

            # 1. Базовая страница услуги
            html = template
            for tag, val in reps.items():
                html = html.replace(tag, str(val))
            
            path = os.path.join("geo", slug, s["slug"], "index.html")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f: f.write(html)

            # 2. Страницы маркетплейсов
            for p in platforms:
                p_canonical = f"https://cdek-marketplace.ru/geo/{slug}/{p['slug']}/{s['slug']}/"
                p_h1 = f"{raw_h1} {p['name']} {prep_v}"
                p_title = f"СДЭК для {p['name']} {prep_v} — {raw_h1}"
                p_desc = f"Официальная логистика СДЭК для селлеров {p['name']} {prep_v}: {raw_h1.lower()}. Скидка B2B до 50%, отгрузка через ПВЗ без очередей. Договор за 15 минут."
                
                p_html = html
                p_html = p_html.replace(reps["{{H1_MAIN}}"], p_h1)
                p_html = p_html.replace(reps["{{SEO_TITLE}}"], p_title)
                p_html = p_html.replace(reps["{{SEO_DESC}}"], p_desc)
                p_html = p_html.replace(canonical_base, p_canonical)
                
                p_path = os.path.join("geo", slug, p["slug"], s["slug"], "index.html")
                os.makedirs(os.path.dirname(p_path), exist_ok=True)
                with open(p_path, "w", encoding="utf-8") as f: f.write(p_html)

    print(f"✅ Гео-матрица перегенерирована: бренд СДЭК на 1-м месте, CTR-сниппеты настроены.")

if __name__ == "__main__":
    generate_pages()
