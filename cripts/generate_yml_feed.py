import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timezone, timedelta

def generate_marketplace_feed():
    moscow_tz = timezone(timedelta(hours=3))
    now = datetime.now(moscow_tz).strftime("%Y-%m-%dT%H:%M:%S+03:00")

    yml_catalog = ET.Element("yml_catalog", date=now)
    shop = ET.SubElement(yml_catalog, "shop")

    ET.SubElement(shop, "name").text = "CDEK Marketplace"
    ET.SubElement(shop, "company").text = "СДЭК для Маркетплейсов"
    ET.SubElement(shop, "url").text = "https://cdek-marketplace.ru"

    currencies = ET.SubElement(shop, "currencies")
    ET.SubElement(currencies, "currency", id="RUB", rate="1")

    categories = ET.SubElement(shop, "categories")
    ET.SubElement(categories, "category", id="1").text = "Логистика для маркетплейсов"
    ET.SubElement(categories, "category", id="2", parentId="1").text = "Схемы доставки FBS и DBS"
    ET.SubElement(categories, "category", id="3", parentId="1").text = "Поставки на склады FBO"
    ET.SubElement(categories, "category", id="4", parentId="1").text = "Корпоративные B2B тарифы"

    offers_data = [
        {
            "id": "mp_fbs",
            "cat": "2",
            "name": "Прием и доставка отправлений по схеме FBS",
            "url": "https://cdek-marketplace.ru/",
            "price": "205",
            "desc": "Сдача готовых заказов селлеров в 5000+ ПВЗ без очередей по единому реестру. Сортировка и доставка отправлений до сортировочных центров маркетплейсов."
        },
        {
            "id": "mp_dbs",
            "cat": "2",
            "name": "Курьерская доставка и выдача в ПВЗ по схеме DBS",
            "url": "https://cdek-marketplace.ru/",
            "price": "205",
            "desc": "Доставка товаров покупателям со склада продавца. Автоматическая передача трек-номеров и статусов вручения в личные кабинеты Ozon, WB и Яндекс Маркет."
        },
        {
            "id": "mp_fbo",
            "cat": "3",
            "name": "Паллетная и коробочная доставка на склады FBO",
            "url": "https://cdek-marketplace.ru/",
            "price": "1500",
            "desc": "Транспортировка партий товаров на распределительные центры маркетплейсов. Забор с адреса селлера и сдача строго в назначенные тайм-слоты."
        },
        {
            "id": "mp_wb",
            "cat": "2",
            "name": "Логистическое обслуживание селлеров Wildberries",
            "url": "https://cdek-marketplace.ru/",
            "price": "205",
            "desc": "Прием заказов WB FBS в пунктах выдачи, маркировка грузовых мест и доставка отправлений на распределительные хабы с подтверждением в личном кабинете."
        },
        {
            "id": "mp_ozon",
            "cat": "2",
            "name": "Доставка заказов Ozon по схемам FBS и rFBS",
            "url": "https://cdek-marketplace.ru/",
            "price": "205",
            "desc": "Интеграция со шлюзами Ozon Rocket: автоматическое получение наклеек со штрихкодами, прием посылок в ПВЗ и соблюдение регламентных сроков площадки."
        },
        {
            "id": "mp_yamarket",
            "cat": "2",
            "name": "Доставка заказов Яндекс Маркета для продавцов",
            "url": "https://cdek-marketplace.ru/",
            "price": "205",
            "desc": "Транспортное обслуживание магазинов Яндекс Маркета по модели Экспресс и FBS с передачей координат отправлений и синхронизацией по API."
        },
        {
            "id": "mp_b2b_contract",
            "cat": "4",
            "name": "Оформление B2B-договора СДЭК для селлеров маркетплейсов",
            "url": "https://cdek-marketplace.ru/",
            "price": "205",
            "desc": "Корпоративное подключение юридических лиц, ИП и самозанятых. Доступ к тарифной линейке Посылка, ежемесячная постоплата и готовые модули интеграции."
        }
    ]

    offers = ET.SubElement(shop, "offers")

    for item in offers_data:
        offer = ET.SubElement(offers, "offer", id=item["id"], available="true")
        ET.SubElement(offer, "url").text = item["url"]
        ET.SubElement(offer, "price").text = item["price"]
        ET.SubElement(offer, "currencyId").text = "RUB"
        ET.SubElement(offer, "categoryId").text = item["cat"]
        ET.SubElement(offer, "picture").text = "https://cdek-marketplace.ru/og-image.png"
        ET.SubElement(offer, "name").text = item["name"]
        ET.SubElement(offer, "description").text = item["desc"]

    rough_string = ET.tostring(yml_catalog, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

    clean_xml_lines = [line for line in pretty_xml.splitlines() if line.strip()]
    final_xml = "\n".join(clean_xml_lines)

    with open("services.yml", "w", encoding="utf-8") as f:
        f.write(final_xml)

    print("Файл services.yml для cdek-marketplace.ru успешно сгенерирован!")

if __name__ == "__main__":
    generate_marketplace_feed()
