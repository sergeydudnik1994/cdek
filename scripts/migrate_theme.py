import os
import re

# Папки для массовой обработки (включая корень)
TARGET_DIRS = [".", "blog", "integrations", "solutions", "services", "geo", "calculator", "scripts", "src"]

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # 1. Замена цветов палитры СДЭК
    content = content.replace("#8de21a", "#00b341")
    content = content.replace("#8DE21A", "#00b341")
    content = content.replace("#0b101d", "#072624")
    content = content.replace("#0B101D", "#072624")
    content = content.replace("#131b2c", "#0b3330")
    content = content.replace("#0f172a", "#072624")
    content = content.replace("#1e293b", "#0e3330")

    # 2. Tailwind Config (гарантированная изумрудная палитра)
    content = re.sub(
        r"colors:\s*\{[^\}]+\}",
        "colors: { cdek: '#00b341', dark: { 900: '#072624', 950: '#041615' } }",
        content
    )

    # 3. Карточки статей, решений и модулей (убираем темно-синий slate)
    content = content.replace("bg-slate-900/60", "bg-[#0b3330]/60")
    content = content.replace("bg-slate-900/50", "bg-[#0b3330]/60")
    content = content.replace("bg-slate-900/90", "bg-[#0b3330]/90")
    content = content.replace("bg-slate-900", "bg-[#072624]")
    content = content.replace("bg-slate-800/40", "bg-[#0b3330]/60")
    content = content.replace("bg-slate-800/50", "bg-[#0b3330]/60")
    content = content.replace("bg-slate-800/60", "bg-[#0b3330]/60")
    content = content.replace("bg-slate-800/70", "bg-[#0e3330]")
    content = content.replace("bg-slate-800", "bg-[#0e3330]")

    # 4. Рамки и разделители
    content = content.replace("border-slate-800/80", "border-emerald-950")
    content = content.replace("border-slate-800/60", "border-emerald-950")
    content = content.replace("border-slate-800", "border-emerald-950")
    content = content.replace("border-slate-700/50", "border-emerald-900/80")
    content = content.replace("border-slate-700/80", "border-emerald-900/80")
    content = content.replace("border-slate-700", "border-emerald-900/80")

    # 5. Бейджи и плашки
    content = content.replace("bg-cdek/10 text-cdek border-cdek/30", "bg-[#0e3330] text-[#00b341] border border-emerald-800/80")
    content = content.replace("bg-cdek/10 text-cdek border border-cdek/20", "bg-[#0e3330] text-[#00b341] border border-emerald-800/80")
    content = content.replace("bg-cdek/10 text-cdek border-cdek/20", "bg-[#0e3330] text-[#00b341] border border-emerald-800/80")
    content = content.replace("bg-cdek/20 text-cdek", "bg-[#0e3330] text-[#00b341]")
    content = content.replace("bg-cdek text-[#0b101d]", "bg-[#00b341] text-white")
    content = content.replace("bg-cdek text-dark-900", "bg-[#00b341] text-white")

    # 6. Удаление ядовитого неонового свечения (Glow)
    content = re.sub(r"drop-shadow-\[[^\]]+\]", "", content)
    content = re.sub(r"shadow-\[0_0_8px_[^\]]+\]", "", content)
    content = re.sub(r"shadow-\[0_0_15px_[^\]]+\]", "", content)
    content = re.sub(r"shadow-\[0_0_25px_[^\]]+\]", "", content)

    # 7. Выделение текста
    content = content.replace("selection:bg-cdek selection:text-dark-900", "selection:bg-[#00b341] selection:text-white")

    if content != original:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

def main():
    updated = 0
    scanned = 0
    for folder in TARGET_DIRS:
        if not os.path.exists(folder):
            continue
        for root, _, files in os.walk(folder):
            # Пропускаем служебные папки git
            if ".git" in root or ".github" in root:
                continue
            for file in files:
                if file.endswith(".html") or file.endswith(".py"):
                    scanned += 1
                    if process_file(os.path.join(root, file)):
                        updated += 1

    print(f"✅ Проверено файлов: {scanned}")
    print(f"🔥 Обновлено файлов в стиль СДЭК: {updated}")

if __name__ == "__main__":
    main()
