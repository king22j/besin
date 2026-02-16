import requests
import os
from dotenv import load_dotenv

# .env dosyasındaki tokeni al
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def list_databases():
    url = "https://api.notion.com/v1/search"
    payload = {
        "filter": {
            "value": "database",
            "property": "object"
        }
    }
    
    print("🔍 Notion taranıyor...")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        results = response.json()["results"]
        if not results:
            print("❌ HATA: Bot çalışıyor ama HİÇBİR veritabanını göremiyor.")
            print("LÜTFEN ŞUNU YAP: Notion'da o sayfaya git, sağ üstteki '...' -> 'Add connections' -> Botunu seç.")
        else:
            print(f"✅ Bot şu veritabanlarını görüyor ({len(results)} adet):")
            print("-" * 50)
            for db in results:
                db_name = db['title'][0]['plain_text'] if db['title'] else "İsimsiz Veritabanı"
                db_id = db['id']
                print(f"📌 İsim: {db_name}")
                print(f"🔑 GERÇEK ID: {db_id}")
                print("-" * 50)
            print("☝️ Yukarıdaki 'GERÇEK ID'yi kopyalayıp kodundaki/env dosyanındaki ile değiştir.")
    else:
        print("❌ Token Hatası! Secret Key yanlış olabilir.")
        print(response.text)

if __name__ == "__main__":
    list_databases()
