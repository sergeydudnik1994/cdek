import json
import os
from datetime import datetime

# Укажите точное юридическое наименование вашей организации/ИП:
COMPANY_LEGAL_NAME = "СДЭК Маркетплейс"  # Замените на ваше официальное ИП / ООО (например: "ИП Дудник С.В.")
BRAND_NAME = "СДЭК Маркетплейс"

SERVICES_CATALOG = [
    # 1. Складские услуги и фулфилмент (category id=4)
    {"slug": "fulfillment", "cat": "4", "name": "Фулфилмент для маркетплейсов", "price": "15", "desc": "Комплексный фулфилмент для селлеров: приемка, хранение, комплектация, упаковка по регламентам маркетплейсов и отгрузка."},
    {"slug": "storage-services", "cat": "4", "name": "Ответственное хранение товаров", "price": "5", "desc": "Складское хранение товаров селлеров на современных складах с круглосуточной охраной и видеонаблюдением."},
    {"slug": "packaging-services", "cat": "4", "name": "Упаковка и маркировка товаров для маркетплейсов", "price": "10", "desc": "Профессиональная упаковка, стикерование и подготовка товаров к отгрузке по стандартам Wildberries, Ozon и Яндекс Маркета."},
    {"slug": "cross-docking", "cat": "4", "name": "Кросс-докинг для селлеров", "price": "50", "desc": "Быстрая перевалка и сортировка грузов без долгосрочного хранения с прямой отправкой на распределительные центры маркетплейсов."},
    {"slug": "returns-management", "cat": "4", "name": "Управление возвратами (Reverse Logistics)", "price": "40", "desc": "Прием, проверка и оперативный возврат невыкупленных товаров со складов и ПВЗ обратно продавцу для повторной реализации."},
    {"slug": "labeling-chestny-znak", "cat": "4", "name": "Маркировка товаров в системе «Честный ЗНАК»", "price": "5", "desc": "Нанесение кодов DataMatrix, ввод в оборот и полное сопровождение товаров, подлежащих обязательной маркировке."},

    # 2. Курьерская доставка и модели отгрузки (category id=3)
    {"slug": "fbs", "cat": "3", "name": "Доставка заказов по модели FBS", "price": "136", "desc": "Логистика FBS для поставщиков маркетплейсов: ежедневный забор отправлений со склада продавца и передача в сортировочные центры."},
    {"slug": "dbs", "cat": "3", "name": "Доставка по схеме DBS и RealFBS", "price": "150", "desc": "Доставка товаров покупателям от продавца напрямую через курьерскую службу и широкую сеть пунктов выдачи СДЭК."},
    {"slug": "courier-for-shops", "cat": "3", "name": "Курьерская доставка для интернет-магазинов", "price": "190", "desc": "Быстрая доставка заказов до двери покупателя с возможностью примерки, частичного выкупа и согласования интервалов."},
    {"slug": "pudo-delivery", "cat": "3", "name": "Доставка заказов в пункты выдачи (ПВЗ)", "price": "136", "desc": "Выдача отправлений через разветвленную сеть отделений СДЭК по всей России с высоким клиентским рейтингом."},
    {"slug": "express-delivery", "cat": "3", "name": "Срочная экспресс-доставка для e-commerce", "price": "180", "desc": "Приоритетная доставка отправлений в минимальные сроки между городами и внутри регионов."},
    {"slug": "last-mile", "cat": "3", "name": "Доставка «Последняя миля»", "price": "120", "desc": "Финальный этап доставки посылок до двери покупателя или постамата с соблюдением временных слотов."},
    {"slug": "zabor-gruza", "cat": "3", "name": "Забор груза со склада поставщика", "price": "150", "desc": "Регулярный выезд курьера на склад селлера для забора партий посылок и доставки в распределительный центр."},
    {"slug": "cash-on-delivery", "cat": "3", "name": "Прием наложенного платежа и кассовое обслуживание", "price": "15", "desc": "Прием оплаты картами и наличными при вручении заказа с перечислением средств на расчетный счет продавца."},
    {"slug": "samozanyatye", "cat": "3", "name": "Логистика для самозанятых селлеров", "price": "136", "desc": "Специальные условия и тарифы доставки товаров для самозанятых предпринимателей на маркетплейсах."},

    # 3. Грузоперевозки и магистраль (category id=2)
    {"slug": "magistral-delivery", "cat": "2", "name": "Магистральные перевозки грузов", "price": "15", "desc": "Межрегиональная транспортировка сборных и генеральных грузов собственным и партнерским автопарком по всей стране."},
    {"slug": "ltl-shipping", "cat": "2", "name": "Доставка сборных грузов (LTL)", "price": "300", "desc": "Перевозка небольших и средних партий грузов в составе сборных машин с оплатой только за фактически занимаемый объем."},
    {"slug": "kgt-delivery", "cat": "2", "name": "Доставка крупногабаритных товаров (КГТ)", "price": "500", "desc": "Транспортировка тяжелых и объемных товаров для маркетплейсов и интернет-магазинов со специальными тарифами."},
    {"slug": "avia-shipping", "cat": "2", "name": "Авиадоставка грузов по России", "price": "120", "desc": "Сверхсрочная отправка коммерческих грузов регулярными авиарейсами в удаленные и труднодоступные регионы."},
    {"slug": "sorting-center", "cat": "2", "name": "Доставка до сортировочных центров маркетплейсов", "price": "100", "desc": "Прямая транспортировка партий товаров в распределительные хабы Wildberries, Ozon, Яндекс Маркет и Мегамаркет."},
    {"slug": "cis-delivery", "cat": "2", "name": "Международная доставка в страны СНГ", "price": "250", "desc": "Трансграничная логистика в Казахстан, Беларусь, Армению, Кыргызстан с полным таможенным сопровождением."},

    # 4. IT-сервисы и консалтинг (category id=2)
    {"slug": "dogovor-ip", "cat": "2", "name": "Заключение договора со СДЭК для ИП и ООО", "price": "500", "desc": "Оформление корпоративного договора со СДЭК для юридических лиц со скидками на логистику до 50%."},
    {"slug": "api-integration", "cat": "2", "name": "Интеграция со СДЭК по API и модулям", "price": "500", "desc": "Подключение CMS интернет-магазинов и учетных систем к логистическому шлюзу для автоматического создания накладных."},
    {"slug": "cargo-insurance", "cat": "2", "name": "Страхование грузов при доставке", "price": "75", "desc": "Комплексная финансовая защита отправлений от повреждений и утери с быстрым возмещением ущерба."},
    {"slug": "unit-economy", "cat": "2", "name": "Расчет стоимости доставки и юнит-экономики", "price": "500", "desc": "Экспертный аудит логистических затрат селлера и подбор оптимальных тарифов для повышения маржинальности."},
    {"slug": "logistics-analytics", "cat": "2", "name": "Логистический аудит и консалтинг для селлеров", "price": "500", "desc": "Анализ цепочек поставок, сроков выкупа и оптимизация расходов на хранение и транспортировку товаров."},

    # 5. Специализированные решения по площадкам (category id=3 / 4)
    {"slug": "fbs/ozon", "cat": "3", "name": "Логистика FBS для Ozon", "price": "136", "desc": "Доставка заказов селлеров Ozon по схеме FBS через пункты приема и сортировочные хабы СДЭК."},
    {"slug": "fbs/wildberries", "cat": "3", "name": "Логистика FBS для Wildberries", "price": "136", "desc": "Ежедневная доставка отправлений селлеров Wildberries (FBS) с соблюдением строгих тайм-слотов маркетплейса."},
    {"slug": "fbs/yandex-market", "cat": "3", "name": "Логистика FBS для Яндекс Маркета", "price": "136", "desc": "Интеграция и быстрая отгрузка заказов продавцов Яндекс Маркета через логистическую сеть СДЭК."},
    {"slug": "fbs/megamarket", "cat": "3", "name": "Логистика FBS для Мегамаркета", "price": "136", "desc": "Транспортировка заказов продавцов Мегамаркета с полным отслеживанием статусов и документооборотом."},
    {"slug": "fbs/avito", "cat": "3", "name": "Логистика для продавцов Авито", "price": "136", "desc": "Организация регулярных доставок товаров для магазинов на Авито с приемом платежей и забором грузов."},
    {"slug": "dbs/ozon", "cat": "3", "name": "Доставка RealFBS для Ozon", "price": "150", "desc": "Услуги доставки покупателям Ozon по схеме realFBS Express и realFBS Standard через курьеров и ПВЗ СДЭК."},
    {"slug": "dbs/yandex-market", "cat": "3", "name": "Доставка DBS для Яндекс Маркета", "price": "150", "desc": "Прямая доставка заказов покупателям Яндекс Маркета по схеме DBS с гарантией сроков и географией по всей РФ."},
    {"slug": "fulfillment/ozon", "cat": "4", "name": "Фулфилмент под ключ для Ozon", "price": "15", "desc": "Полный цикл обработки заказов для продавцов Ozon: хранение, сборка, упаковка и поставка на РЦ."},
    {"slug": "fulfillment/wildberries", "cat": "4", "name": "Фулфилмент под ключ для Wildberries", "price": "15", "desc": "Складская обработка товаров для селлеров WB в точном соответствии с регламентами маркетплейса."}
]

def generate_feed():
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    host = "https://cdek-marketplace.ru"
    
    yml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!DOCTYPE yml_catalog SYSTEM "shops.dtd">',
        f'<yml_catalog date="{today}">',
        '  <shop>',
        f'    <name>{BRAND_NAME}</name>',
        f'    <company>{COMPANY_LEGAL_NAME}</company>',
        f'    <url>{host}/</url>',
        '    <currencies>',
        '      <currency id="RUB" rate="1"/>',
        '    </currencies>',
        '    <categories>',
        '      <category id="1">Транспорт и логистика</category>',
        '      <category id="2" parentId="1">Грузоперевозки</category>',
        '      <category id="3" parentId="1">Курьерские услуги и доставка</category>',
        '      <category id="4" parentId="1">Складские услуги и фулфилмент</category>',
        '    </categories>',
        '    <sets>'
    ]

    for idx, s in enumerate(SERVICES_CATALOG):
        set_id = f"set_{idx + 1}"
        set_name = s['name']
        slug = s['slug']
        set_url = f"{host}/services/{slug}/"
        yml_lines.append(f'      <set id="{set_id}">')
        yml_lines.append(f'        <name>{set_name}</name>')
        yml_lines.append(f'        <url>{set_url}</url>')
        yml_lines.append('      </set>')

    yml_lines.append('    </sets>')
    yml_lines.append('    <offers>')

    for idx, s in enumerate(SERVICES_CATALOG):
        offer_id = f"offer_{idx + 1}"
        set_id = f"set_{idx + 1}"
        slug = s['slug']
        offer_url = f"{host}/services/{slug}/"
        price = s['price']
        cat_id = s['cat']
        desc = s['desc']
        picture = f"{host}/favicon.png"
        
        yml_lines.append(f'      <offer id="{offer_id}" available="true">')
        yml_lines.append(f'        <name>{BRAND_NAME}</name>')
        yml_lines.append(f'        <url>{offer_url}</url>')
        yml_lines.append(f'        <price>{price}</price>')
        yml_lines.append('        <currencyId>RUB</currencyId>')
        yml_lines.append(f'        <categoryId>{cat_id}</categoryId>')
        yml_lines.append(f'        <set-ids>{set_id}</set-ids>')
        yml_lines.append(f'        <picture>{picture}</picture>')
        yml_lines.append(f'        <description>{desc}</description>')
        yml_lines.append('        <param name="Тип исполнителя">Компания</param>')
        yml_lines.append('        <param name="Форма оплаты">Безналичный расчет, наличные, картой</param>')
        yml_lines.append('        <param name="Работа с юридическими лицами">Да</param>')
        yml_lines.append('        <param name="Заключение договора">Да</param>')
        yml_lines.append('        <param name="География услуг">Вся Россия и СНГ</param>')
        yml_lines.append('        <param name="Срок оказания услуг">от 1 дня</param>')
        yml_lines.append('        <param name="Опыт работы">15 лет</param>')
        yml_lines.append('        <param name="Рейтинг">4.9</param>')
        yml_lines.append('      </offer>')

    yml_lines.append('    </offers>')
    yml_lines.append('  </shop>')
    yml_lines.append('</yml_catalog>')

    with open('feed.yml', 'w', encoding='utf-8') as f:
        f.write("\n".join(yml_lines))
    
    print(f"✅ Фид сгенерирован: {len(SERVICES_CATALOG)} сетов под бренд {BRAND_NAME}.")

if __name__ == "__main__":
    generate_feed()
