import os
import json

def scan():
    cities_in_geo = [d for d in os.listdir('geo') if os.path.isdir(os.path.join('geo', d))]
    with open('scripts/seo_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        cities_in_json = [c['slug'] for c in data['cities']]
    
    missing = [c for c in cities_in_geo if c not in cities_in_json]
    print(f"📁 Города в папке geo, но отсутствуют в JSON: {missing}")

if __name__ == "__main__":
    scan()
