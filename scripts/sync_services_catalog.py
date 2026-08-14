import json
import os
import re

def update_services_page():
    seo_path = "scripts/seo_data.json"
    services_path = "services/index.html"
    
    if not os.path.exists(seo_path) or not os.path.exists(services_path):
        print("❌ Файлы не найдены. Убедитесь, что запускаете из корня репозитория.")
        return

    with open(seo_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    services = data.get("services", [])

    cards_html = ""
    for s in services:
        slug = s["slug"]
        title = s["h1_main"]
        desc = s["desc"]
        price = s.get("price", "")
        
        cards_html += f"""
      <a href="/services/{slug}/" class="group block bg-slate-800/50 border border-slate-700/50 rounded-2xl p-6 hover:bg-slate-800 hover:border-cdek/50 transition-all">
        <div class="flex items-center justify-between mb-4">
          <div class="h-12 w-12 bg-cdek/10 text-cdek rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path></svg>
          </div>
          {f'<span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-cdek/20 text-cdek">{price}</span>' if price else ''}
        </div>
        <h3 class="text-xl font-semibold text-white mb-2 group-hover:text-cdek transition-colors">{title}</h3>
        <p class="text-slate-400 text-sm">{desc}</p>
      </a>"""

    with open(services_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Заменяем содержимое внутри сетки услуг
    pattern = r'(<div class="grid[^>]*id="servicesGrid"[^>]*>).*?(</div>\s*</main>)'
    replacement = rf'\1\n{cards_html}\n    \2'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(services_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ Готово! Страница /services/index.html обновлена. Теперь там {len(services)} услуг.")

if __name__ == "__main__":
    update_services_page()
