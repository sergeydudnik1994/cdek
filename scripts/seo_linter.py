import os
import sys

# СПИСОК ИСКЛЮЧЕНИЙ: файлы и папки, которым не нужны строгие SEO-теги
IGNORE_LIST = [
    'src/components',
    'ping.html',
    'calculator',
    'policy'
]

def check_seo_tags(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read().lower()
        
        errors = []
        if '<title>' not in content or '</title>' not in content:
            errors.append("Отсутствует или сломан тег <title>")
        if 'name="description"' not in content:
            errors.append("Отсутствует тег <meta name=\"description\">")
        if '<h1' not in content or '</h1>' not in content:
            errors.append("Отсутствует или сломан тег <h1>")
            
        return errors

has_errors = False

for root, dirs, files in os.walk('.'):
    for filename in files:
        if filename.endswith('.html'):
            # Приводим путь к единому формату
            filepath = os.path.join(root, filename).replace('\\', '/')
            
            # Если файл или папка есть в списке исключений — пропускаем проверку
            if any(ignore_item in filepath for ignore_item in IGNORE_LIST):
                continue
                
            errors = check_seo_tags(filepath)
            
            if errors:
                print(f"❌ ОШИБКА В ФАЙЛЕ: {filepath}")
                for err in errors:
                    print(f"   - {err}")
                has_errors = True

if has_errors:
    print("\n🚨 Деплой остановлен! Исправьте SEO-ошибки в HTML.")
    sys.exit(1)
else:
    print("✅ Все файлы прошли строгую SEO-проверку! Ошибок нет.")
