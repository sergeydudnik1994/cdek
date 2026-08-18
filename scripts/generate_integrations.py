import os
import random

MODULES = [
    # -------------------------------------------------------------
    # 1. CMS И КОНСТРУКТОРЫ ИНТЕРНЕТ-МАГАЗИНОВ
    # -------------------------------------------------------------
    {
        "slug": "1c-bitrix",
        "name": "1С-Битрикс",
        "category": "CMS платформы",
        "title": "Интеграция СДЭК с 1С-Битрикс — Официальный модуль доставки",
        "desc": "Готовый модуль доставки СДЭК для 1С-Битрикс: «Управление сайтом». Расчет тарифов в корзине онлайн, интерактивная карта ПВЗ, автоматическое создание накладных и печать штрихкодов.",
        "features": ["Расчет тарифов «Посылка» и DBS в чекауте", "Выбор ПВЗ и постаматов на интерактивной карте", "Автоматическое создание накладных и вызов курьера", "Передача статусов и трек-номеров в заказы Битрикс"],
        "setup_steps": ["Установите модуль из каталога Marketplace 1C-Битрикс", "Укажите Account и Secure password из официального договора СДЭК", "Настройте правила отгрузки, габариты по умолчанию и доступные типы доставки"]
    },
    {
        "slug": "tilda",
        "name": "Tilda Publishing",
        "category": "Конструкторы сайтов",
        "title": "Интеграция СДЭК с Tilda — Доставка в корзину ST100",
        "desc": "Официальный сервис доставки СДЭК для сайтов на Tilda. Автоматический расчет стоимости в корзине ST100, виджет выбора пунктов выдачи и моментальная передача заказов по API v2.0.",
        "features": ["Встроенный расчет тарифа в блоке корзины ST100", "Интерактивная карта пунктов выдачи заказов для покупателей", "Спецтарифы для юрлиц и самозанятых от 136.5 ₽", "Автоматическая выгрузка данных получателя в систему СДЭК"],
        "setup_steps": ["Подключите сервис доставки СДЭК в панели сайта Tilda", "Введите ключи интеграции API v2.0 из личного кабинета СДЭК", "Активируйте службу доставки в блоке корзины ST100 и задайте габариты товаров"]
    },
    {
        "slug": "insales",
        "name": "InSales",
        "category": "CMS платформы",
        "title": "Интеграция СДЭК с InSales — Модуль доставки интернет-магазина",
        "desc": "Официальный модуль СДЭК для платформы InSales. Синхронизация статусов заказов, автоформирование накладных, печать этикеток со штрихкодами и расчет стоимости доставки.",
        "features": ["Полная интеграция с бэк-офисом InSales", "Отображение карты ПВЗ и постаматов при оформлении заказа", "Массовая печать квитанций и актов приема-передачи", "Поддержка наложенного платежа и фискализации"],
        "setup_steps": ["Установите приложение «СДЭК» из магазина InSales AppStore", "Авторизуйтесь по API-ключам официального договора СДЭК", "Активируйте курьерскую доставку и самовывоз из пунктов выдачи"]
    },
    {
        "slug": "woocommerce-wordpress",
        "name": "WooCommerce (WordPress)",
        "category": "CMS платформы",
        "title": "Плагин СДЭК для WooCommerce — Доставка WordPress",
        "desc": "Официальный плагин доставки СДЭК для интернет-магазинов на WordPress WooCommerce. Калькулятор стоимости, выбор ПВЗ на карте, синхронизация статусов и автосоздание накладных.",
        "features": ["Поддержка актуального протокола CDEK API 2.0", "Интерактивная карта ПВЗ в стандартном и кастомном чекауте", "Автоматический пересчет веса и габаритов посылки", "Смена статусов заказа в WordPress при вручении посылки"],
        "setup_steps": ["Скачайте и активируйте плагин СДЭК в консоли WordPress", "Внесите Client ID и Client Secret в настройках WooCommerce", "Сконфигурируйте зоны доставки и разрешенные тарифы"]
    },
    {
        "slug": "opencart",
        "name": "OpenCart / ocStore",
        "category": "CMS платформы",
        "title": "Модуль СДЭК для OpenCart 2.x / 3.x и ocStore — Доставка заказов",
        "desc": "Официальный модуль СДЭК для OpenCart и ocStore. Выбор ПВЗ на карте, наложенный платеж, печать актов приема-передачи, генерация штрихкодов и трекинг посылок.",
        "features": ["Совместимость с модулями Simple, QuickCheckout и стандартным заказом", "Поддержка тарифов «Посылка склад-склад» и «склад-дверь»", "Автоматическая генерация штрихкодов для коробок", "Прямая отправка реестров на отгрузку курьеру"],
        "setup_steps": ["Установите модификатор через установщик OpenCart", "Вставьте API-ключи из корпоративного договора СДЭК", "Настройте привязку статусов заказов к трекингу СДЭК"]
    },
    {
        "slug": "cs-cart",
        "name": "CS-Cart & Multi-Vendor",
        "category": "CMS платформы",
        "title": "Интеграция СДЭК с CS-Cart — Модуль для интернет-магазинов и маркетплейсов",
        "desc": "Официальный модуль доставки СДЭК для CS-Cart и Multi-Vendor. Раздельный расчет логистики для разных поставщиков, карта ПВЗ, выгрузка реестров и B2B-скидки.",
        "features": ["Поддержка мультивендорных маркетплейсов", "Раздельный расчет стоимости для каждого продавца витрины", "Автоматический вызов курьера на склад отгрузки", "Поддержка международных отправок в страны ЕАЭС"],
        "setup_steps": ["Установите модуль через панель администратора CS-Cart", "Настройте тарифные зоны и внесите авторизационные данные СДЭК", "Проверьте вывод карты отделений на странице оформления заказа"]
    },
    {
        "slug": "shop-script-webasyst",
        "name": "Shop-Script (Webasyst)",
        "category": "CMS платформы",
        "title": "Плагин СДЭК для Webasyst Shop-Script — Доставка интернет-магазина",
        "desc": "Официальный плагин интеграции СДЭК для Webasyst Shop-Script. Автоматический расчет стоимости, карта пунктов выдачи, печать наклеек и синхронизация статусов заказов.",
        "features": ["Расчет стоимости с учетом индивидуальной B2B-скидки", "Печать термоэтикеток прямо из админки Webasyst", "Передача точных габаритов каждого артикула в заказе", "СМС-уведомление покупателя при поступлении заказа в ПВЗ"],
        "setup_steps": ["Установите плагин из магазина приложений Webasyst", "Введите логин и пароль интеграции API СДЭК", "Настройте правила наценки/скидки и габариты товаров по умолчанию"]
    },
    {
        "slug": "advantshop",
        "name": "AdvantShop",
        "category": "CMS платформы",
        "title": "Интеграция СДЭК с AdvantShop — Модуль доставки и ПВЗ",
        "desc": "Встроенный модуль СДЭК для интернет-магазинов на AdvantShop. Расчет сроков доставки, выбор пункта выдачи, создание накладных и вызов курьера на склад.",
        "features": ["Интерактивная карта пунктов выдачи в чекауте AdvantShop", "Генерация квитанций к заказу в 1 клик", "Автоматический вызов курьера на забор груза", "Синхронизация трек-номеров и уведомление клиентов"],
        "setup_steps": ["Активируйте метод доставки СДЭК в панели AdvantShop", "Введите параметры интеграции из личного кабинета", "Укажите адрес склада для корректного расчета забора груза"]
    },
    {
        "slug": "ecwid",
        "name": "Ecwid",
        "category": "Конструкторы сайтов",
        "title": "Интеграция СДЭК с Ecwid — Виджет доставки в корзину",
        "desc": "Официальное приложение СДЭК для платформы Ecwid. Онлайн-калькулятор тарифов в корзине, интерактивная карта пунктов выдачи и автоматическая генерация накладных.",
        "features": ["Точный расчет тарифов для физических и юридических лиц", "Интерактивный виджет выбора ПВЗ для покупателей", "Поддержка мультиязычных и кроссбордерных продаж", "Автоматическое создание накладных в личном кабинете"],
        "setup_steps": ["Установите приложение СДЭК из Ecwid App Market", "Внесите ключи доступа API из договора СДЭК", "Сконфигурируйте поддерживаемые способы отправки"]
    },
    {
        "slug": "prestashop",
        "name": "PrestaShop",
        "category": "CMS платформы",
        "title": "Модуль СДЭК для PrestaShop — Официальная доставка",
        "desc": "Модуль интеграции курьерской службы СДЭК для PrestaShop 1.7 / 8.x. Авторасчет стоимости доставки, выбор ПВЗ на карте Яндекс, печать наклеек и трекинг посылок.",
        "features": ["Поддержка тарифов доставки до двери и до склада", "Выбор терминалов самовывоза на интерактивной карте", "Создание накладных прямо из панели управления заказом", "Автоматическое отслеживание трек-номеров"],
        "setup_steps": ["Загрузите архив модуля через раздел «Модули» PrestaShop", "Укажите Account и Password из договора со СДЭК", "Задайте соответствие статусов заказа статусам доставки"]
    },
    {
        "slug": "magento",
        "name": "Magento 2 (Adobe Commerce)",
        "category": "CMS платформы",
        "title": "Модуль СДЭК для Magento 2 — Доставка для крупных eCommerce проектов",
        "desc": "Высоконагруженный модуль интеграции СДЭК для Magento 2 / Adobe Commerce. Расчет доставки, карта ПВЗ, выгрузка реестров и поддержка мультивалютности.",
        "features": ["Высокая скорость ответа API при больших каталогах", "Гибкая настройка правил расчета стоимости и наценок", "Интерактивная карта ПВЗ на странице OneStepCheckout", "Массовое создание накладных СДЭК"],
        "setup_steps": ["Установите расширение через Composer в корень Magento 2", "Активируйте модуль в Stores -> Configuration -> Sales -> Shipping Methods", "Укажите реквизиты API v2.0 и настройте складские адреса"]
    },
    {
        "slug": "drupal-commerce",
        "name": "Drupal Commerce",
        "category": "CMS платформы",
        "title": "Модуль СДЭК для Drupal Commerce — Логистический шлюз",
        "desc": "Интеграционный модуль СДЭК для интернет-магазинов на Drupal 8 / 9 / 10 Commerce. Расчет тарифов, выбор пункта выдачи и передача данных получателя.",
        "features": ["Полная интеграция с чекаутом Drupal Commerce", "Поддержка выбора пунктов выдачи на карте", "Создание отправлений в кабинете СДЭК по событию оплаты", "Гибкая архитектура и открытый исходный код"],
        "setup_steps": ["Подключите модуль через Composer и включите в админке Drupal", "Внесите учетные данные CDEK API в настройках способов доставки", "Настройте правила маппинга полей адреса покупателя"]
    },
    {
        "slug": "nethouse",
        "name": "Nethouse",
        "category": "Конструкторы сайтов",
        "title": "Интеграция СДЭК с Nethouse — Подключение доставки в интернет-магазин",
        "desc": "Готовая интеграция со СДЭК для сайтов на конструкторе Nethouse. Авторасчет стоимости доставки для покупателей, выбор ПВЗ и передача заказов.",
        "features": ["Быстрое подключение без привлечения программистов", "Отображение точек выдачи СДЭК по всей России", "Экономия на логистике со спецтарифами СДЭК", "Уведомление клиентов о статусах отправки"],
        "setup_steps": ["Откройте раздел «Настройки» -> «Доставка» в панели Nethouse", "Выберите «СДЭК» и введите реквизиты договора", "Укажите параметры отгрузки и сохраните изменения"]
    },
    {
        "slug": "moguta-cms",
        "name": "Moguta.CMS",
        "category": "CMS платформы",
        "title": "Плагин СДЭК для Moguta.CMS — Доставка для интернет-магазина",
        "desc": "Официальный плагин интеграции СДЭК для Moguta.CMS. Интерактивная карта ПВЗ, расчет тарифов с учетом скидок, автосоздание накладных и печать этикеток.",
        "features": ["Расчет тарифов курьерской доставки и самовывоза", "Выбор терминала СДЭК на карте прямо в корзине", "Генерация трек-номеров и накладных из админки", "Синхронизация статусов доставки"],
        "setup_steps": ["Установите плагин из маркетплейса Moguta", "Вставьте логин и пароль интеграции СДЭК", "Настройте типы отправлений и габариты по умолчанию"]
    },
    {
        "slug": "umi-cms",
        "name": "UMI.CMS",
        "category": "CMS платформы",
        "title": "Модуль СДЭК для UMI.CMS — Автоматизация доставки заказов",
        "desc": "Модуль СДЭК для системы управления сайтом UMI.CMS. Расчет стоимости, выбор ПВЗ на интерактивной карте, формирование накладных и выгрузка трек-кодов.",
        "features": ["Встроенный калькулятор стоимости для покупателя", "Интерактивный выбор ПВЗ на карте", "Создание накладных в 1 клик из списка заказов", "Поддержка B2B-договоров СДЭК"],
        "setup_steps": ["Активируйте модуль доставки СДЭК в расширениях UMI.CMS", "Внесите учетные данные из договора со СДЭК", "Сконфигурируйте правила расчета доставки"]
    },
    {
        "slug": "diafan-cms",
        "name": "Diafan.CMS",
        "category": "CMS платформы",
        "title": "Модуль СДЭК для Diafan.CMS — Доставка и пункты выдачи",
        "desc": "Интеграция доставки СДЭК для Diafan.CMS. Отображение актуальных тарифов в корзине, выбор пунктов выдачи на карте и передача заказов в СДЭК.",
        "features": ["Автоматический расчет стоимости по тарифам договора", "Выбор ПВЗ на карте при оформлении заказа", "Передача габаритов и веса корзины в СДЭК", "Отслеживание статусов выполнения заказов"],
        "setup_steps": ["Подключите модуль СДЭК в панели администрирования Diafan", "Укажите Account и Password из личного кабинета СДЭК", "Настройте методы доставки (дверь/склад)"]
    },
    {
        "slug": "hostcms",
        "name": "HostCMS",
        "category": "CMS платформы",
        "title": "Модуль СДЭК для HostCMS — Официальный логистический плагин",
        "desc": "Официальный модуль доставки СДЭК для HostCMS. Калькуляция стоимости посылок, выбор отделений на карте и печать сопроводительных документов.",
        "features": ["Расчет тарифов «Посылка» по всей территории РФ", "Интерактивная карта ПВЗ в чекауте HostCMS", "Создание накладных из панели управления интернет-магазином", "Экспорт реестров отгрузки"],
        "setup_steps": ["Установите модуль через систему обновлений HostCMS", "Внесите авторизационные данные API", "Настройте параметры расчета стоимости"]
    },
    {
        "slug": "vigbo",
        "name": "Vigbo",
        "category": "Конструкторы сайтов",
        "title": "Интеграция СДЭК с Vigbo — Доставка для креативного бизнеса",
        "desc": "Подключение доставки СДЭК к интернет-магазинам на платформе Vigbo. Автоматический расчет стоимости доставки, выбор пунктов самовывоза и спецтарифы.",
        "features": ["Простая настройка без программирования", "Спецтарифы на легкие отправления от 136.5 ₽", "Выбор ПВЗ СДЭК по всей России для покупателей", "Сдача посылок без очередей по реестру"],
        "setup_steps": ["Подключите СДЭК в разделе интеграций интернет-магазина Vigbo", "Авторизуйтесь по API-ключам B2B-договора СДЭК", "Проверьте работу калькулятора в корзине сайта"]
    },

    # -------------------------------------------------------------
    # 2. CRM, ERP И СКЛАДСКОЙ УЧЕТ
    # -------------------------------------------------------------
    {
        "slug": "moysklad",
        "name": "МойСклад",
        "category": "Складской учет и ERP",
        "title": "Интеграция СДЭК с МойСклад — Автоматизация отгрузок и накладных",
        "desc": "Официальная интеграция СДЭК и облачного сервиса МойСклад. Автоматическое создание накладных из заказов покупателей, печать штрихкодов, трекинг и списание остатков.",
        "features": ["Создание отгрузки СДЭК в 1 клик из документа заказа", "Массовая печать маркировок и актов приема-передачи", "Автоматическое обновление статусов доставки в МойСклад", "Списание остатков со склада при передаче курьеру"],
        "setup_steps": ["Подключите приложение «СДЭК» в разделе «Приложения» МойСклад", "Введите Account и Password из договора со СДЭК", "Настройте соответствие статусов заказа статусам доставки"]
    },
    {
        "slug": "1c-predpriyatie",
        "name": "1С:Предприятие (УТ, УНФ, ERP, КА)",
        "category": "Складской учет и ERP",
        "title": "Модуль СДЭК для 1С — Интеграция с УТ 11, УНФ и ERP",
        "desc": "Официальная внешняя обработка и расширение СДЭК для 1C:Управление торговлей, УНФ, Комплексной автоматизации и 1C:ERP. Прямой обмен по CDEK API 2.0.",
        "features": ["Прямое формирование накладных СДЭК без сторонних сервисов", "Печать термоэтикеток со штрихкодами прямо из 1С", "Пакетная передача реестров заказов на отгрузку", "Учет стоимости доставки в себестоимости и расчетах с клиентами"],
        "setup_steps": ["Подключите внешнее расширение СДЭК в конфигураторе или базе 1С", "Укажите ключи авторизации CDEK API", "Свяжите справочники складов и номенклатурных групп"]
    },
    {
        "slug": "retailcrm",
        "name": "RetailCRM",
        "category": "CRM системы",
        "title": "Интеграция СДЭК с RetailCRM — Логистический шлюз",
        "desc": "Интеграция службы доставки СДЭК с RetailCRM. Маршрутизация заказов, автоматический расчет тарифов, печать сопроводительных документов и трекинг посылок.",
        "features": ["Авторасчет тарифа и сроков доставки при оформлении заявки менеджером", "Подбор оптимального ПВЗ по адресу покупателя", "Печать полного пакета складских документов и стикеров", "Триггерные SMS/WhatsApp уведомления по статусам СДЭК"],
        "setup_steps": ["Активируйте модуль СДЭК в Маркетплейсе RetailCRM", "Введите API-ключи учетной записи СДЭК", "Сконфигурируйте способы доставки и правила отгрузки"]
    },
    {
        "slug": "bitrix24",
        "name": "Битрикс24",
        "category": "CRM системы",
        "title": "Интеграция СДЭК с Битрикс24 — Доставка из сделок CRM",
        "desc": "Приложение доставки СДЭК для Битрикс24 CRM. Создание накладных из лидов и сделок, выбор ПВЗ на карте, печать документов и автоматические роботы движения по воронке.",
        "features": ["Оформление доставки прямо из карточки сделки Битрикс24", "Автоматическая смена стадий сделки по статусам вручения СДЭК", "Виджет интерактивной карты для менеджеров отдела продаж", "Формирование трек-ссылки для отправки клиенту в чат"],
        "setup_steps": ["Установите приложение из Маркетплейса Битрикс24", "Авторизуйтесь по API-ключам договора СДЭК", "Настройте роботов на смену стадий по событиям доставки"]
    },
    {
        "slug": "amocrm",
        "name": "amoCRM",
        "category": "CRM системы",
        "title": "Виджет СДЭК для amoCRM — Доставка и отслеживание в сделках",
        "desc": "Интеграция СДЭК с amoCRM. Авторасчет стоимости доставки, выбор пункта выдачи, создание накладной и отображение статуса вручения клиенту прямо в воронке продаж.",
        "features": ["Создание отправлений внутри цифровой воронки amoCRM", "Отображение текущего местоположения посылки в ленте сделки", "Автоматический перенос сделки на этап «Доставлено / Оплачено»", "Контроль наложенных платежей и возвратов"],
        "setup_steps": ["Установите виджет СДЭК из каталога интеграций amoCRM", "Внесите авторизационные данные договора", "Настройте Digital Pipeline для автоматизации логистики"]
    },
    {
        "slug": "megaplan",
        "name": "Мегаплан",
        "category": "CRM системы",
        "title": "Интеграция СДЭК с Мегаплан — Автоматизация доставки в CRM",
        "desc": "Интеграция CRM Мегаплан со службой доставки СДЭК. Создание накладных из заказов и сделок, расчет стоимости доставки и отслеживание статуса посылок.",
        "features": ["Оформление отправки СДЭК из карточки клиента или сделки", "Расчет стоимости тарифов с учетом B2B-скидок", "Печать квитанций и маркировок", "Автоматическое обновление статусов доставки в CRM"],
        "setup_steps": ["Подключите интеграцию СДЭК в центре приложений Мегаплана", "Внесите логин и пароль API из официального договора", "Настройте правила создания отгрузок"]
    },
    {
        "slug": "leadvertex",
        "name": "LeadVertex",
        "category": "CRM системы",
        "title": "Интеграция СДЭК с LeadVertex — CRM для товарного бизнеса",
        "desc": "Официальная интеграция LeadVertex со СДЭК. Массовая генерация накладных, печать термоэтикеток, контроль статусов доставки и наложенных платежей.",
        "features": ["Массовая генерация накладных СДЭК в один клик", "Автоматический трекинг статусов доставки и возвратов", "Контроль движения наложенных платежей", "Печать термоэтикеток для маркировки коробок"],
        "setup_steps": ["Перейдите в «Настройки» -> «Интеграции» -> «СДЭК» в LeadVertex", "Вставьте авторизационные ключи Account / Secure password", "Свяжите статусы заказов со статусами доставки СДЭК"]
    },
    {
        "slug": "lp-crm",
        "name": "LP-CRM",
        "category": "CRM системы",
        "title": "Интеграция СДЭК с LP-CRM — Доставка для одностраничников и лендингов",
        "desc": "Модуль доставки СДЭК для LP-CRM. Автоматическое создание накладных, расчет стоимости, печать реестров и контроль забора груза курьером.",
        "features": ["Быстрое создание накладных из входящих лидов", "Автоматический расчет тарифов по всей России", "Пакетная печать наклеек на посылки", "СМС-информирование покупателей о трек-номере"],
        "setup_steps": ["Активируйте модуль СДЭК в настройках служб доставки LP-CRM", "Укажите данные учетной записи CDEK API", "Задайте склад отгрузки по умолчанию"]
    },

    # -------------------------------------------------------------
    # 3. МАРКЕТПЛЕЙСЫ, ВИДЖЕТЫ И АГРЕГАТОРЫ
    # -------------------------------------------------------------
    {
        "slug": "flowwow",
        "name": "Flowwow",
        "category": "Маркетплейсы",
        "title": "Интеграция СДЭК для продавцов Flowwow — Доставка DBS",
        "desc": "Логистика СДЭК для селлеров Flowwow. Срочная доставка цветов, подарков и кондитерских изделий по схемам DBS и Express с B2B-скидками до 50%.",
        "features": ["Срочная курьерская доставка день в день по городу", "Особые регламенты бережной перевозки цветов и подарков", "Спецтарифы на легкие отправления от 136.5 ₽", "Автоматическая интеграция трек-номеров"],
        "setup_steps": ["Заключите официальный B2B договор СДЭК за 15 минут", "Выберите модель DBS доставки в кабинете селлера Flowwow", "Передавайте трек-номера СДЭК для отслеживания покупателями"]
    },
    {
        "slug": "avito-dostavka",
        "name": "Авито Доставка",
        "category": "Маркетплейсы",
        "title": "СДЭК для магазинов на Авито — Доставка и наложенный платеж",
        "desc": "Официальная доставка СДЭК для продавцов и интернет-магазинов на Авито. Доставка через 4000+ ПВЗ, курьерский забор и прием оплаты при вручении.",
        "features": ["Отгрузка партий заказов без очередей по реестру", "Безопасная оплата и наложенный платеж с переводом на р/с", "Экономия до 50% на тарифах для юрлиц и ИП", "Доставка крупногабаритных товаров (КГТ)"],
        "setup_steps": ["Оформите договор СДЭК для ИП, юрлиц или самозанятых", "Настройте передачу заказов через личный кабинет или API", "Сдавайте посылки в ближайший ПВЗ или вызывайте курьера на склад"]
    },
    {
        "slug": "apiship",
        "name": "ApiShip",
        "category": "Логистические агрегаторы",
        "title": "Интеграция СДЭК через ApiShip — Единый логистический протокол",
        "desc": "Подключение СДЭК через интеграционную платформу ApiShip. Единый API для работы со всеми тарифами, складами, пунктами выдачи и статусами доставки СДЭК.",
        "features": ["Единый стандартизированный API для интернет-магазинов", "Поддержка всех типов тарифов СДЭК (дверь, склад, постамат)", "Автоматическое получение актуальных списков ПВЗ", "Единая маршрутизация заказов и возвратов"],
        "setup_steps": ["Зарегистрируйте личный кабинет на платформе ApiShip", "Подключите провайдера «СДЭК», указав реквизиты официального договора", "Настройте правила тарификации и сопоставление складов"]
    },
    {
        "slug": "cdek-widget",
        "name": "Официальный виджет СДЭК (JS SDK)",
        "category": "Виджеты и SDK",
        "title": "Виджет СДЭК 3.0 для любого сайта — Карта ПВЗ и калькулятор",
        "desc": "Официальный интерактивный JavaScript-виджет СДЭК 3.0 для любого самописного сайта или фреймворка (React, Vue, HTML). Расчет стоимости и выбор ПВЗ на карте.",
        "features": ["Быстрое встраивание в любой чекаут за 3 строчки кода", "Интерактивная карта ПВЗ с поиском и фильтрацией", "Автоматический расчет сроков и стоимости по договору", "Полная адаптивность под мобильные устройства"],
        "setup_steps": ["Подключите скрипт виджета @cdek-it/widget на страницу оформления заказа", "Инициализируйте виджет с вашим API-ключом и адресом отправки", "Получайте данные о выбранном ПВЗ в callback-функции при оформлении"]
    }
]

def generate_catalog_hub(host="https://cdek-marketplace.ru"):
    categories = ["CMS платформы", "Конструкторы сайтов", "CRM системы", "Складской учет и ERP", "Маркетплейсы", "Логистические агрегаторы", "Виджеты и SDK"]
    
    sections_html = []
    for cat in categories:
        cat_modules = [m for m in MODULES if m["category"] == cat]
        if not cat_modules:
            continue
        
        cards = []
        for m in cat_modules:
            cards.append(f"""
            <a href="/integrations/{m['slug']}/" class="group flex flex-col justify-between bg-slate-900/60 border border-slate-800 hover:border-cdek/50 rounded-2xl p-5 sm:p-6 transition-all duration-300 backdrop-blur-sm shadow-md">
              <div>
                <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 mb-3 rounded-md text-[10px] font-extrabold uppercase tracking-wider bg-slate-800 text-cdek border border-slate-700">
                  {m['category']}
                </div>
                <h3 class="text-lg sm:text-xl font-bold text-white mb-2 group-hover:text-cdek transition-colors">{m['name']}</h3>
                <p class="text-slate-400 text-xs sm:text-sm leading-relaxed mb-4">{m['desc']}</p>
              </div>
              <div class="flex items-center justify-between pt-4 border-t border-slate-800/80 text-xs">
                <span class="text-slate-500 font-medium">Готовый модуль</span>
                <span class="text-cdek font-bold group-hover:translate-x-1 transition-transform">Подключить →</span>
              </div>
            </a>""")
            
        sections_html.append(f"""
        <div class="mb-14">
          <div class="flex items-center gap-3 mb-6 pb-2 border-b border-slate-800">
            <span class="w-2.5 h-2.5 rounded-full bg-cdek shadow-[0_0_8px_#8de21a]"></span>
            <h2 class="text-xl sm:text-2xl font-black text-white uppercase tracking-wide">{cat}</h2>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 sm:gap-6">
            {''.join(cards)}
          </div>
        </div>
        """)

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <!-- Yandex.Metrika counter -->
  <script type="text/javascript">
    (function(m,e,t,r,i,k,a){{
        m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }}}}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    }})(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=111090265', 'ym' );
    ym(111090265, 'init', {{ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", accurateTrackBounce:true, trackLinks:true}});
  </script>
  <noscript><div><img src="https://mc.yandex.ru/watch/111090265" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
  <!-- /Yandex.Metrika counter -->

  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Модули интеграции СДЭК — Официальный каталог готовых решений для CMS, CRM и маркетплейсов</title>
  <meta name="description" content="Полный каталог официальных модулей интеграции СДЭК: 1C-Битрикс, Tilda, InSales, WooCommerce, МойСклад, 1С, RetailCRM, Битрикс24, amoCRM, OpenCart и 20+ других систем." />
  <meta name="theme-color" content="#8DE21A" />
  <link rel="canonical" href="{host}/integrations/" />
  
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="СДЭК Маркетплейсы" />
  <meta property="og:title" content="Модули интеграции СДЭК — 30 готовых решений" />
  <meta property="og:description" content="Официальное подключение логистики СДЭК к любой CMS, CRM и учетной системе за 15 минут со скидкой до 50%." />
  <meta property="og:url" content="{host}/integrations/" />
  <meta property="og:image" content="{host}/logo.png" />
  <link rel="icon" type="image/png" href="/favicon.png" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Главная", "item": "{host}/" }},
      {{ "@type": "ListItem", "position": 2, "name": "Интеграции", "item": "{host}/integrations/" }}
    ]
  }}
  </script>

  <script src="https://cdn.tailwindcss.com"></script>
  <script>tailwind.config={{theme:{{extend:{{colors:{{cdek:'#8de21a',dark:{{900:'#0b101d'}}}}}}}}}}</script>
</head>
<body class="bg-dark-900 text-slate-100 min-h-screen flex flex-col antialiased pb-16 md:pb-0">
  <!--#include virtual="/src/components/header.html" -->

  <main class="flex-grow max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-10 pb-20 w-full">
    <div class="mb-14 text-center">
      <div class="inline-flex items-center gap-2 px-3.5 py-1.5 mb-4 rounded-full text-xs font-semibold uppercase tracking-wider bg-cdek/10 text-cdek border border-cdek/20">
        Ready-to-use API & CMS Modules
      </div>
      <h1 class="text-4xl md:text-5xl lg:text-6xl font-black text-white mb-4 tracking-tight">
        Модули интеграции <span class="text-cdek">СДЭК</span>
      </h1>
      <p class="text-slate-400 text-base md:text-lg max-w-3xl mx-auto">
        Официальные модули и плагины для автоматического расчета тарифов, интерактивной карты ПВЗ и пакетного создания накладных в вашей системе за 15 минут.
      </p>
    </div>

    {''.join(sections_html)}

    <div class="mt-16">
      <!--#include virtual="/src/components/calculator-widget.html" -->
    </div>
  </main>

  <!--#include virtual="/src/components/footer.html" -->
  <!--#include virtual="/src/components/mobile-cta.html" -->
</body>
</html>"""

def generate_module_page(mod, all_mods, host="https://cdek-marketplace.ru"):
    slug = mod["slug"]
    name = mod["name"]
    category = mod["category"]
    title = mod["title"]
    desc = mod["desc"]
    features = mod["features"]
    steps = mod["setup_steps"]
    canonical_url = f"{host}/integrations/{slug}/"

    other_mods = [m for m in all_mods if m["slug"] != slug]
    cross_links = random.sample(other_mods, min(4, len(other_mods)))
    cross_links_html = "".join([
        f'<a href="/integrations/{m["slug"]}/" class="p-4 rounded-xl bg-slate-800/40 border border-slate-700/50 hover:border-cdek/50 transition-all flex flex-col justify-between group">'
        f'  <span class="text-white font-bold text-sm group-hover:text-cdek transition-colors">{m["name"]}</span>'
        f'  <span class="text-[11px] text-slate-400 mt-1">{m["category"]}</span>'
        f'</a>'
        for m in cross_links
    ])

    features_html = "".join([
        f'<li class="flex items-start gap-3 text-sm text-slate-300">'
        f'  <span class="text-cdek text-base font-bold shrink-0">✓</span>'
        f'  <span>{f}</span>'
        f'</li>'
        for f in features
    ])

    steps_html = "".join([
        f'<div class="flex items-start gap-4 p-4 rounded-xl bg-slate-800/30 border border-slate-700/40">'
        f'  <div class="w-8 h-8 rounded-lg bg-cdek/10 border border-cdek/30 text-cdek font-black flex items-center justify-center shrink-0 text-sm">{idx+1}</div>'
        f'  <div>'
        f'    <p class="text-sm text-slate-200 leading-relaxed">{step}</p>'
        f'  </div>'
        f'</div>'
        for idx, step in enumerate(steps)
    ])

    faq_items = [
        {
            "q": f"Как получить ключи доступа к API для интеграции с {name}?",
            "a": f"Ключи доступа (Account и Secure password) генерируются автоматически после заключения официального B2B-договора со СДЭК в течение 15 минут."
        },
        {
            "q": f"Какая скидка предоставляется на доставку при работе через {name}?",
            "a": "При работе по официальному договору СДЭК для юридических лиц, ИП и самозанятых действуют сниженные оптовые тарифы со скидкой до 50% по сравнению с отправками физлиц."
        },
        {
            "q": f"Поддерживает ли модуль {name} выбор ПВЗ на интерактивной карте?",
            "a": "Да, официальный модуль и виджет СДЭК позволяют покупателям выбирать ближайший пункт выдачи или постамат на интерактивной карте прямо в корзине при оформлении заказа."
        }
    ]

    faq_json_entities = ",".join([
        f'{{"@type": "Question", "name": "{item["q"]}", "acceptedAnswer": {{"@type": "Answer", "text": "{item["a"]}"}}}}'
        for item in faq_items
    ])

    faq_visual_html = "".join([
        f'<details class="group p-5 bg-slate-800/30 rounded-2xl border border-slate-700/50 open:border-cdek/50 transition-all">'
        f'  <summary class="flex justify-between items-center font-bold text-sm sm:text-base text-white cursor-pointer list-none select-none">'
        f'    <span>{item["q"]}</span>'
        f'    <span class="text-cdek transition-transform duration-300 group-open:rotate-180">▼</span>'
        f'  </summary>'
        f'  <p class="mt-3 text-xs sm:text-sm text-slate-400 leading-relaxed">{item["a"]}</p>'
        f'</details>'
        for item in faq_items
    ])

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <!-- Yandex.Metrika counter -->
  <script type="text/javascript">
    (function(m,e,t,r,i,k,a){{
        m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }}}}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    }})(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=111090265', 'ym' );
    ym(111090265, 'init', {{ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", accurateTrackBounce:true, trackLinks:true}});
  </script>
  <noscript><div><img src="https://mc.yandex.ru/watch/111090265" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
  <!-- /Yandex.Metrika counter -->

  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="theme-color" content="#8DE21A" />
  <link rel="canonical" href="{canonical_url}" />
  
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="СДЭК Маркетплейсы" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:image" content="{host}/logo.png" />
  <link rel="icon" type="image/png" href="/favicon.png" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Главная", "item": "{host}/" }},
          {{ "@type": "ListItem", "position": 2, "name": "Интеграции", "item": "{host}/integrations/" }},
          {{ "@type": "ListItem", "position": 3, "name": "{name}", "item": "{canonical_url}" }}
        ]
      }},
      {{
        "@type": "SoftwareApplication",
        "name": "Модуль интеграции СДЭК для {name}",
        "operatingSystem": "All",
        "applicationCategory": "BusinessApplication",
        "provider": {{
          "@type": "Organization",
          "name": "СДЭК Маркетплейсы",
          "url": "{host}/"
        }},
        "description": "{desc}"
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [{faq_json_entities}]
      }}
    ]
  }}
  </script>

  <script src="https://cdn.tailwindcss.com"></script>
  <script>tailwind.config={{theme:{{extend:{{colors:{{cdek:'#8de21a',dark:{{900:'#0b101d'}}}}}}}}}}</script>
</head>
<body class="bg-dark-900 text-slate-100 min-h-screen flex flex-col antialiased pb-16 md:pb-0">
  <!--#include virtual="/src/components/header.html" -->
  
  <main class="flex-grow">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 pb-12 sm:pt-10 sm:pb-16">
      
      <!-- Хлебные крошки -->
      <nav class="text-xs sm:text-sm text-slate-400 mb-6 flex flex-wrap items-center gap-1.5">
        <a href="/" class="hover:text-cdek transition-colors">Главная</a> <span>/</span>
        <a href="/integrations/" class="hover:text-cdek transition-colors">Интеграции</a> <span>/</span>
        <span class="text-white">{name}</span>
      </nav>

      <div class="grid lg:grid-cols-[1.1fr_0.9fr] gap-10 items-start">
        
        <!-- Левая колонка -->
        <section class="flex flex-col items-start">
          <div class="inline-flex items-center gap-2 px-3.5 py-1.5 mb-6 rounded-full text-xs font-semibold tracking-wide uppercase border bg-cdek/10 text-cdek border-cdek/30">
            <span>{category} • Готовое решение</span>
          </div>

          <h1 class="text-3xl sm:text-4xl lg:text-5xl font-black text-white leading-tight mb-5">
            Интеграция СДЭК с <span class="text-cdek">{name}</span>
          </h1>

          <p class="text-slate-300 text-base sm:text-lg leading-relaxed mb-8">
            {desc}
          </p>

          <!-- Метрики -->
          <div class="grid grid-cols-3 gap-4 py-6 border-y border-slate-800 w-full mb-8">
            <div>
              <p class="text-xl sm:text-2xl font-black text-cdek">до 50%</p>
              <p class="text-xs text-slate-400">Скидка B2B</p>
            </div>
            <div>
              <p class="text-xl sm:text-2xl font-black text-white">15 мин</p>
              <p class="text-xs text-slate-400">Настройка API</p>
            </div>
            <div>
              <p class="text-xl sm:text-2xl font-black text-white">4 000+</p>
              <p class="text-xs text-slate-400">ПВЗ на карте</p>
            </div>
          </div>

          <!-- Возможности -->
          <div class="w-full mb-10">
            <h2 class="text-xl font-bold text-white mb-4">Возможности модуля для {name}</h2>
            <ul class="space-y-3 bg-slate-800/30 p-6 rounded-2xl border border-slate-700/40">
              {features_html}
            </ul>
          </div>

          <!-- Инструкция -->
          <div class="w-full mb-10">
            <h2 class="text-xl font-bold text-white mb-4">Как подключить интеграцию за 3 шага</h2>
            <div class="space-y-3">
              {steps_html}
            </div>
          </div>

          <!-- FAQ -->
          <div class="w-full mb-8">
            <h2 class="text-xl font-bold text-white mb-4">Частые вопросы</h2>
            <div class="space-y-3">
              {faq_visual_html}
            </div>
          </div>
        </section>

        <!-- Правая колонка: Форма захвата -->
        <section class="relative w-full max-w-xl mx-auto lg:ml-auto sticky top-24" id="leadForm">
          <!--#include virtual="/src/components/leadform.html" -->
        </section>
      </div>

      <!-- Калькулятор тарифов -->
      <section class="mt-14">
        <!--#include virtual="/src/components/calculator-widget.html" -->
      </section>

      <!-- Другие интеграции -->
      <section class="mt-16 pt-10 border-t border-slate-800">
        <h3 class="text-lg font-bold text-white mb-4">Другие модули и платформы</h3>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {cross_links_html}
        </div>
      </section>

    </div>
  </main>

  <!--#include virtual="/src/components/footer.html" -->
</body>
</html>"""

def generate_all():
    print(f"🚀 Генерация полного каталога СДЭК ({len(MODULES)} официальных модулей интеграции)...")
    
    os.makedirs("integrations", exist_ok=True)
    with open("integrations/index.html", "w", encoding="utf-8") as f:
        f.write(generate_catalog_hub())
    print("✅ Сформирован хаб /integrations/index.html")

    count = 0
    for m in MODULES:
        out_dir = os.path.join("integrations", m["slug"])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(generate_module_page(m, MODULES))
        count += 1

    print(f"✅ Успешно сгенерировано {count} посадочных страниц модулей интеграции СДЭК.")

if __name__ == "__main__":
    generate_all()
