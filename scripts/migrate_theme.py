import os
import re

TARGET_DIRS = [".", "blog", "integrations", "solutions", "services", "geo", "calculator", "scripts", "src"]

CLEAN_TAILWIND_CONFIG = """<script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            cdek: '#00b341',
            dark: { 900: '#072624', 950: '#041615' }
          }
        }
      }
    }
  </script>"""

def fix_html_content(content):
    # 1. Восстанавливаем сломанный блок tailwind.config
    content = re.sub(r"<script>\s*tailwind\.config\s*=\s*\{[\s\S]*?\}?\s*\}?\s*\}?\s*</script>", CLEAN_TAILWIND_CONFIG, content)

    # 2. Гарантированный хвойный фон body (не зависит от конфига tailwind)
    content = content.replace("bg-dark-900", "bg-[#072624]")
    content = content.replace("bg-dark-950", "bg-[#041615]")
    content = content.replace("#0b101d", "#072624")
    content = content.replace("#0B101D", "#072624")
    content = content.replace("#8de21a", "#00b341")
    content = content.replace("#8DE21A", "#00b341")
    content = content.replace("#131b2c", "#0b3330")
    content = content.replace("#1e293b", "#0e3330")

    # 3. Карточки и блоки контента
    content = content.replace("bg-slate-900/60", "bg-[#0b3330]/60")
    content = content.replace("bg-slate-900/50", "bg-[#0b3330]/60")
    content = content.replace("bg-slate-900", "bg-[#072624]")
    content = content.replace("bg-slate-800/40", "bg-[#0b3330]/60")
    content = content.replace("bg-slate-800/50", "bg-[#0b3330]/60")
    content = content.replace("bg-slate-800/60", "bg-[#0b3330]/60")
    content = content.replace("bg-slate-800", "bg-[#0e3330]")

    # 4. Рамки
    content = content.replace("border-slate-800", "border-emerald-950")
    content = content.replace("border-slate-700", "border-emerald-900/80")

    # 5. Кнопки и плашки
    content = content.replace("bg-cdek text-[#0b101d]", "bg-[#00b341] text-white")
    content = content.replace("bg-cdek text-dark-900", "bg-[#00b341] text-white")
    content = content.replace("bg-cdek/10 text-cdek", "bg-[#0e3330] text-[#00b341]")
    content = content.replace("bg-cdek/20 text-cdek", "bg-[#0e3330] text-[#00b341]")

    return content

def main():
    scanned = 0
    updated = 0

    for folder in TARGET_DIRS:
        if not os.path.exists(folder):
            continue
        for root, _, files in os.walk(folder):
            if ".git" in root or ".github" in root:
                continue
            for file in files:
                if file.endswith(".html"):
                    scanned += 1
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8") as f:
                        old_text = f.read()

                    new_text = fix_html_content(old_text)

                    if new_text != old_text:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_text)
                        updated += 1

    print(f"✅ Проверено файлов: {scanned}")
    print(f"🔥 Исправлено файлов с контрастным фоном: {updated}")

if __name__ == "__main__":
    main()
