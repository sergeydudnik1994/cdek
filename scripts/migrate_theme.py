#!/usr/bin/env python3
import os
import re

# Папки для исключения
EXCLUDE_DIRS = {'.git', 'node_modules', '.github', '.astro'}

# Карта строгих строковых замен (палитры и фоны)
REPLACEMENTS = {
    # Цвета темы и мета-теги
    'content="#072624"': 'content="#060B11"',
    'content="#08221F"': 'content="#060B11"',
    'content="#031b14"': 'content="#060B11"',
    'content="#041615"': 'content="#060B11"',
    'content="#00b341"': 'content="#060B11"',
    
    # Фоны body и контейнеров
    'bg-[#072624]': 'bg-[#060B11]',
    'bg-[#041615]': 'bg-[#060B11]',
    'bg-[#08221F]': 'bg-[#060B11]',
    'bg-[#031b14]': 'bg-[#060B11]',
    'bg-market-bg': 'bg-[#060B11]',
    'bg-market-input': 'bg-[#060B11]',
    
    # Карточки и блоки (перевод в графитовое стекло)
    'bg-[#0b3330]': 'bg-[#0B131D]',
    'bg-[#07261e]': 'bg-[#0B131D]',
    'bg-[#062A30]': 'bg-[#0B131D]',
    'bg-[#0A3D36]': 'bg-[#0B131D]',
    'bg-market-card': 'bg-[#0B131D]',
    
    # Прозрачные подложки
    'bg-[#0b3330]/40': 'bg-[#0B131D]/80',
    'bg-[#0b3330]/50': 'bg-[#0B131D]/80',
    'bg-[#0b3330]/60': 'bg-[#0B131D]/80',
    'bg-[#041615]/90': 'bg-[#0B131D]/90',
    'bg-[#0e3330]': 'bg-white/[0.04]',
    
    # Границы блоков
    'border-emerald-800': 'border-white/[0.08]',
    'border-emerald-900': 'border-white/[0.08]',
    'border-emerald-950': 'border-white/[0.08]',
    'border-[#133E38]': 'border-white/[0.08]',
    'border-market-border': 'border-white/[0.08]',
    'border-emerald-800/60': 'border-white/[0.08]',
    'border-emerald-800/80': 'border-white/[0.08]',
    'border-emerald-800/50': 'border-white/[0.08]',
    'border-emerald-950/80': 'border-white/[0.06]',
    'border-emerald-900/60': 'border-white/[0.08]',
    'border-emerald-900/80': 'border-white/[0.08]',
    'border-emerald-500/20': 'border-white/[0.08]',
    'border-emerald-500/30': 'border-white/[0.08]',
    
    # Акценты и текст
    'text-[#00b341]': 'text-[#22E58B]',
    'text-cdek': 'text-[#22E58B]',
    'border-[#00b341]': 'border-[#22E58B]',
    'border-cdek': 'border-[#22E58B]',
    'bg-[#00b341]/15': 'bg-[#22E58B]/15',
    'bg-[#00b341]/20': 'bg-[#22E58B]/15',
    'border-[#00b341]/30': 'border-[#22E58B]/30',
    'border-cdek/30': 'border-[#22E58B]/30',
    
    # Выделение текста курсором
    'selection:bg-[#00b341]': 'selection:bg-[#22E58B] selection:text-slate-950',
    'selection:bg-[#1AB248]': 'selection:bg-[#22E58B] selection:text-slate-950',
    'selection:bg-cdek': 'selection:bg-[#22E58B] selection:text-slate-950',
}

def update_tailwind_config(content):
    """Обновляет цветовую палитру в script-теге tailwind.config"""
    sber_config = """tailwind.config = {
      theme: {
        extend: {
          colors: {
            cdek: '#00b341',
            neon: '#22E58B',
            obsidian: '#060B11',
            card: '#0B131D'
          }
        }
      }
    }"""
    pattern = r'tailwind\.config\s*=\s*\{[\s\S]*?theme[\s\S]*?\}\s*\}'
    if re.search(pattern, content):
        return re.sub(pattern, sber_config, content)
    return content

def process_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Применение карты замен
    for old_str, new_str in REPLACEMENTS.items():
        content = content.replace(old_str, new_str)

    # 2. Обновление Tailwind config
    content = update_tailwind_config(content)

    # 3. Сохранение изменений только при наличии правок
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    modified_count = 0
    total_count = 0

    print("🚀 Запуск миграции стилей репозитория в формат Sber AI / GigaChat UI...")

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith('.html') or file.endswith('.php'):
                total_count += 1
                full_path = os.path.join(root, file)
                if process_html_file(full_path):
                    modified_count += 1
                    print(f"  ✓ Обновлен: {full_path}")

    print(f"\n✨ Готово! Обработано файлов: {total_count}, успешно обновлено: {modified_count}")

if __name__ == '__main__':
    main()
