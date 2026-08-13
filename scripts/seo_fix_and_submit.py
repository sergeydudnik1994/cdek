import os
import urllib.request
import json
import xml.etree.ElementTree as ET

HOST = "cdek-marketplace.ru"
KEY = "cdek-index-key" # Имя вашего ключа из файла cdek-index-key.txt
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"

def fix_blog_canonicals():
    print("🛠 1. Автоматическое исправление тегов canonical в Блоге...")
    fixed_count = 0
    
    if not os.path.exists('blog'):
        print("  [-] Папка 'blog' не найдена. Пропуск.")
        return

    # Обходим все HTML файлы в папке blog
    for root, _, files in os.walk('blog'):
        for file in files:
            if file == 'index.html':
                file_path = os.path.join(root, file)
                
                # Формируем правильный URL (например: https://cdek-marketplace.ru/blog/post-name/)
                relative_path = root.replace('\\', '/')
                correct_url = f"https://{HOST}/{relative_path}/"
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                wrong_canonical = f'<link rel="canonical" href="https://{HOST}/" />'
                correct_canonical = f'<link rel="canonical" href="{correct_url}" />'
                
                if wrong_canonical in content:
                    content = content.replace(wrong_canonical, correct_canonical)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixed_count += 1
                    print(f"  [+] Исправлено: {file_path} -> {correct_url}")
                    
    print(f"✅ Готово. Исправлено битых страниц блога: {fixed_count}\n")

def submit_to_indexnow():
    print("🚀 2. Массовая отправка sitemap в Яндекс (API IndexNow)...")
    if not os.path.exists('sitemap.xml'):
        print("  [-] Ошибка: файл sitemap.xml не найден в корне!")
        return

    urls = []
    try:
        tree = ET.parse('sitemap.xml')
        root_xml = tree.getroot()
        for url in root_xml.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            if loc is not None and loc.text:
                urls.append(loc.text)
    except Exception as e:
        print(f"  [-] Ошибка чтения sitemap.xml: {e}")
        return
        
    print(f"  [i] Собрано ссылок для принудительной индексации: {len(urls)}")
    
    data = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls
    }
    
    req = urllib.request.Request(
        'https://yandex.com/indexnow', 
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.getcode() in [200, 202]:
                print(f"✅ УСПЕШНО! {len(urls)} страниц отправлено на переобход в Яндекс.")
            else:
                print(f"⚠️ Ответ Яндекса: {response.getcode()}")
    except Exception as e:
        print(f"❌ Ошибка отправки запроса в Яндекс: {e}")

if __name__ == "__main__":
    fix_blog_canonicals()
    submit_to_indexnow()
