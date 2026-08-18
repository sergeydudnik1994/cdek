import os
from datetime import datetime

SERVICES_CATALOG = [
    ("services/fulfillment", "Фулфилмент для маркетплейсов", "15", "Комплексный фулфилмент для селлеров: приемка, хранение, комплектация, упаковка по регламентам маркетплейсов и отгрузка."),
    ("services/storage-services", "Ответственное хранение товаров", "5", "Складское хранение товаров селлеров на современных отапливаемых складах с круглосуточной охраной."),
    ("services/packaging-services", "Упаковка и маркировка товаров для маркетплейсов", "10", "Профессиональная упаковка, стикерование и подготовка товаров к отгрузке по стандартам Wildberries, Ozon и Яндекс Маркета."),
    ("services/cross-docking", "Кросс-докинг для селлеров", "50", "Быстрая перевалка и сортировка грузов без долгосрочного хранения с прямой отправкой на распределительные центры маркетплейсов."),
    ("services/returns-management", "Управление возвратами (Reverse Logistics)", "40", "Прием, проверка и оперативный возврат невыкупленных товаров со складов и ПВЗ обратно продавцу для повторной реализации."),
    ("services/labeling-chestny-znak", "Маркировка товаров в системе «Честный ЗНАК»", "5", "Нанесение кодов DataMatrix, ввод в оборот и полное сопровождение товаров, подлежащих обязательной маркировке."),
    ("services/fbs", "Доставка заказов по модели FBS", "136", "Логистика FBS для поставщиков маркетплейсов: ежедневный забор отправлений со склада продавца и передача в сортировочные центры."),
    ("services/dbs", "Доставка по схеме DBS и RealFBS", "150", "Доставка товаров покупателям от продавца напрямую через курьерскую службу и широкую сеть пунктов выдачи СДЭК."),
    ("wildberries", "Доставка СДЭК для селлеров Wildberries (FBS/DBS)", "136", "Логистика для продавцов Wildberries: спецтарифы от 136.5 ₽, отгрузка без очередей по реестру через ПВЗ СДЭК."),
    ("ozon", "Доставка СДЭК для продавцов Ozon (FBS/rFBS)", "136", "Официальная доставка для селлеров Ozon по моделям FBS и realFBS со скидками до 50% и сдачей в 4000+ ПВЗ."),
    ("yandex-market", "Доставка для продавцов Яндекс Маркета", "136", "Интеграция и доставка отправлений селлеров Яндекс Маркета по тарифам FBS и DBS по всей России.")
]

def generate_feed():
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    host = "https://cdek-marketplace.ru"
    brand = "СДЭК Маркетплейс"
    
    yml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!DOCTYPE yml_catalog SYSTEM "shops.dtd">',
        f'<yml_catalog date="{today}">',
        '  <shop>',
        f'    <name>{brand}</name>',
        f'    <company>{brand}</company>',
        f'    <url>{host}/</url>',
        '    <currencies><currency id="RUB" rate="1"/></currencies>',
        '    <categories><category id="1">Исполнители</category></categories>',
        '    <sets>'
    ]

    for idx, (path, name, price, desc ) in enumerate(SERVICES_CATALOG):
        yml_lines.append(f'      <set id="set_{idx+1}"><name>{name}</name><url>{host}/{path}/</url></set>')

    yml_lines.append('    </sets><offers>')

    for idx, (path, name, price, desc) in enumerate(SERVICES_CATALOG):
        yml_lines.append(f'      <offer id="offer_{idx+1}" available="true">')
        yml_lines.append(f'        <name>{brand}</name>')
        yml_lines.append(f'        <url>{host}/{path}/#executor</url>')
        yml_lines.append(f'        <price>{price}</price>')
        yml_lines.append('        <currencyId>RUB</currencyId><categoryId>1</categoryId>')
        yml_lines.append(f'        <set-ids>set_{idx+1}</set-ids>')
        yml_lines.append(f'        <picture>{host}/favicon.png</picture>')
        yml_lines.append(f'        <description>{desc}</description>')
        yml_lines.append('        <param name="Рейтинг">5.0</param>')
        yml_lines.append('        <param name="Число отзывов">150</param>')
        yml_lines.append('        <param name="Годы опыта">15</param>')
        yml_lines.append('        <param name="Регион">Россия</param>')
        yml_lines.append('      </offer>')

    yml_lines.append('    </offers></shop></yml_catalog>')

    with open('feed.yml', 'w', encoding='utf-8') as f:
        f.write("\n".join(yml_lines))
    print("✅ feed.yml обновлен: рейтинг 5.0 установлен.")

if __name__ == "__main__":
    generate_feed()
