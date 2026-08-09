import os
import sys

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

# Проверяем только index.html и главные страницы (чтобы не трогать компоненты)
files_to_check = ['index.html'] 
has_errors = False

for root, dirs, files in os.walk('.'):
    for filename in files:
        if filename.endswith('.html') and 'src/components' not in root:
            filepath = os.path.join(root, filename)
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
