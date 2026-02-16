import requests
import json
import time
import os

# --- AYARLAR ---
# Kod çalıştığında bilgisayara/sunucuya "Bana bu şifreyi ver" diyecek.
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("DATABASE_ID")

# Eğer şifreleri bulamazsa hata verip dursun (Güvenlik önlemi)
if not NOTION_TOKEN or not DATABASE_ID:
    raise ValueError("HATA: Notion Token veya Database ID bulunamadı! Secrets ayarlarını kontrol et.")

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- FONKSİYON ---
def create_notion_page(data):
    url = "https://api.notion.com/v1/pages"
    
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "food": { "title": [{"text": {"content": data["name"]}}] },
            "kategori": { "select": {"name": data["kategori"]} },
            "porsiyon": { "rich_text": [{"text": {"content": str(data["porsiyon"])}}] },
            "Kalori (kcal)": { "number": data["kalori"] },
            "Protein (g)": { "number": data["protein"] },
            "Karbonhidrat (g)": { "number": data["karbonhidrat"] },
            "Yağ (g) (Number)": { "number": data["yag"] },
            "Vitaminler": { "multi_select": [{"name": v} for v in data["vitaminler"]] },
            "Mineraller": { "multi_select": [{"name": m} for m in data["mineraller"]] }
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"✅ Eklendi: {data['name']}")
    else:
        print(f"❌ Hata: {data['name']}")
        print(response.json())

# --- ÇALIŞTIRMA ---
if __name__ == "__main__":
    # GitHub'da dosya yolunu tam bulsun diye
    file_path = os.path.join(os.path.dirname(__file__), "data.json")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            food_list = json.load(f)
            
        print(f"🚀 İşlem başlıyor... {len(food_list)} veri var.")
        for food in food_list:
            create_notion_page(food)
            time.sleep(0.5)
        print("🎉 Bitti.")
        
    except FileNotFoundError:
        print("❌ Hata: data.json dosyası bulunamadı.")
