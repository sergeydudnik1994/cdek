import os

target = "mobile-cta.html"
extensions = (".html", ".htm", ".php", ".py", ".txt")

cleaned_count = 0

for root, dirs, files in os.walk("."):
    # Пропускаем служебную папку git
    if ".git" in root:
        continue
        
    for file in files:
        if file.endswith(extensions):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                
                # Оставляем только те строки, где нет mobile-cta.html
                new_lines = [line for line in lines if target not in line]
                
                # Если что-то удалили — перезаписываем файл
                if len(new_lines) != len(lines):
                    with open(path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)
                    print(f"Очищен файл: {path}")
                    cleaned_count += 1
            except Exception as e:
                pass

print(f"\nГотово! Строка удалена из {cleaned_count} файлов.")
