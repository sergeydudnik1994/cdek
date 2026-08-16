import json
import os
from datetime import datetime

def generate_feed():
    # Загружаем данные об услугах (их у нас 26)
    try:
        with open('scripts/seo_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Ошибка чтения seo_data.json: {e}")
        return

    services = data.get('services', [])
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    host = "https://cdek-marketplace.ru"
    
    # Заголовок YML-фида
    yml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE yml_catalog SYSTEM "shops.dtd">
<yml_catalog date="{today}">
  <shop>
    <name>СДЭК Маркетплейсы</name>
    <company>СДЭК для бизнеса</company>
    <url>{host}/</url>
    <currencies><currency id="RUB" rate="1"/></currencies>
    <categories><category id="1">Логистика для маркетплейсов</category></categories>
    <offers>
"""
    # Генерируем карточку для каждой услуги
    for idx, s in enumerate(services ):
        # Очищаем цену (оставляем только цифры)
        price = ''.join(filter(str.isdigit, s.get('price', '0')))
        if not price: price = "0"
        
        # Используем favicon.png, так как он точно есть в корне
        picture = f"{host}/favicon.png"
        
        # Описание из JSON
        desc = s.get('desc', 'Профессиональная логистика для селлеров маркетплейсов.')
        
        yml += f"""      <offer id="{idx+1}" available="true">
        <name>{s['h1_main']}</name>
        <url>{host}/services/{s['slug']}/</url>
        <price>{price}</price>
        <currencyId>RUB</currencyId>
        <categoryId>1</categoryId>
        <picture>{picture}</picture>
        <description>{desc}</description>
        <param name="рейтинг">4.9</param>
        <param name="регион">Россия</param>
      </offer>
"""
    yml += "    </offers>\n  </shop>\n</yml_catalog>"

    with open('feed.yml', 'w', encoding='utf-8') as f:
        f.write(yml)
    print(f"✅ Фид успешно сгенерирован: {len(services)} услуг добавлено в feed.yml")

if __name__ == "__main__":
    generate_feed()
