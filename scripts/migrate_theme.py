import os
import re

# Папки для массовой обработки
TARGET_DIRS = ["geo", "services", "solutions", "integrations", "blog", "calculator"]

# Замены стилей и палитры
REPLACEMENTS = [
    # 1. Мета-тег темы браузера
    ('content="#8DE21A"', 'content="#072624"'),
    ('content="#0b101d"', 'content="#072624"'),
    
    # 2. Tailwind Config (замена палитры на хвойную СДЭК)
    (
        r"colors:\s*\{\s*cdek:\s*['\"]#8de21a['\"],\s*dark:\s*\{\s*900:\s*['\"]#0b101d['\"]\s*\}\s*\}",
        "colors: { cdek: '#00b341', dark: { 900: '#072624', 950: '#041615' } }"
    ),
    (
        r"cdek:\s*['\"]#8de21a['\"]",
        "cdek: '#00b341'"
    ),

    # 3. Базовые классы тега <body> и селекшена
    (
        'class="bg-dark-900 text-slate-100 min-h-screen flex flex-col antialiased pb-16 md:pb-0"',
        'class="bg-dark-900 text-slate-100 min-h-screen flex flex-col antialiased selection:bg-[#00b341] selection:text-white pb-16 md:pb-0"'
    ),
    (
        'selection:bg-cdek selection:text-dark-900',
        'selection:bg-[#00b341] selection:text-white'
    ),

    # 4. Устранение неоновых теней (Glow)
    (r"drop-shadow-\[0_0_15px_rgba\(141,226,26,0\.35\)\]", ""),
    (r"drop-shadow-\[0_0_15px_rgba\(141,226,26,0\.3\)\]", ""),
    (r"drop-shadow-\[0_0_8px_rgba\(141,226,26,0\.3\)\]", ""),
    (r"shadow-\[0_0_8px_#8de21a\]", ""),
    (r"shadow-\[0_0_8px_#8DE21A\]", ""),

    # 5. Хлебные крошки и ссылки
    ('hover:text-cdek', 'hover:text-[#00b341]'),
    ('text-cdek hover:underline', 'text-[#00b341] hover:underline'),
    
    # 6. Бейджи первого экрана
    ('bg-cdek/10 text-cdek border-cdek/30', 'bg-[#0e3330] text-[#00b341] border-emerald-800/80'),
    ('bg-cdek/10 text-cdek border border-cdek/20', 'bg-[#0e3330] text-[#00b341] border border-emerald-800/80'),
    ('bg-cdek/10 text-cdek border-cdek/20', 'bg-[#0e3330] text-[#00b341] border-emerald-800/80'),
    
    # 7. Фоновые карточки и рамки контента
    ('bg-slate-900/60 border border-slate-800', 'bg-[#0b3330]/60 border border-emerald-800/60'),
    ('bg-slate-900/50 border border-slate-800', 'bg-[#0b3330]/60 border border-emerald-800/60'),
    ('bg-slate-800/40 border border-slate-700/50', 'bg-[#0b3330]/60 border border-emerald-800/60'),
    ('bg-slate-800/60 border border-slate-700', 'bg-[#0b3330]/60 border border-emerald-800/60'),
    ('bg-slate-800/30 p-6 rounded-xl border border-slate-700/50', 'bg-[#0e3330]/50 p-6 rounded-2xl border border-emerald-800/60'),
    ('border-slate-800', 'border-emerald-950'),
    ('border-slate-700', 'border-emerald-900'),
    
    # 8. Акцентные кнопки и маркеры
    ('bg-cdek hover:bg-cdek/90 text-[#0b101d]', 'bg-[#00b341] hover:bg-[#009c38] text-white'),
    ('bg-cdek hover:bg-cdek/90 text-dark-900', 'bg-[#00b341] hover:bg-[#009c38] text-white'),
    ('bg-cdek text-[#0b101d]', 'bg-[#00b341] text-white'),
    ('text-cdek font-black', 'text-[#00b341] font-black'),
    ('text-cdek font-bold', 'text-[#00b341] font-bold'),
]

def migrate_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    for pattern, replacement in REPLACEMENTS:
        if pattern.startswith("r'") or "\\" in pattern or "[" in pattern:
            content = re.sub(pattern, replacement, content)
        else:
            content = content.replace(pattern, replacement)

    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

def run_migration():
    total_scanned = 0
    total_updated = 0

    for directory in TARGET_DIRS:
        if not os.path.exists(directory):
            continue
        print(f"🔄 Обработка папки: {directory}...")
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".html"):
                    total_scanned += 1
                    full_path = os.path.join(root, file)
                    if migrate_html_file(full_path):
                        total_updated += 1

    print(f"\n Готово!")
    print(f"Всего проверено файлов: {total_scanned}")
    print(f"Обновлено файлов: {total_updated}")

if __name__ == "__main__":
    run_migration()
