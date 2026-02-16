import requests
import json
import time
import os

# --- AYARLAR ---
# GitHub Secrets'tan şifreleri alıyoruz
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("DATABASE_ID")

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- KONTROL FONKSİYONU (DUPLICATE ENGELLEYİCİ) ---
def check_if_exists(food_name):
    """
    Notion veritabanına sorar: Bu isimde bir yiyecek var mı?
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    
    # "food" sütununda ismi arıyoruz
    payload = {
        "filter": {
            "property": "food",
            "title": {
                "equals": food_name
            }
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        results = response.json().get("results")
        # Eğer sonuç listesi boş değilse (>0), demek ki kayıt var.
        return len(results) > 0
    else:
        print(f"⚠️ Arama hatası: {response.text}")
        return False

# --- EKLEME FONKSİYONU ---
def create_notion_page(data):
    # ADIM 1: Önce kontrol et
    if check_if_exists(data["name"]):
        print(f"⏩ Pas geçildi (Zaten var): {data['name']}")
        return # Fonksiyondan çık, ekleme yapma!

    # ADIM 2: Yoksa ekle
    url = "https://api.notion.com/v1/pages"
    
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "food": { 
                "title": [{"text": {"content": data["name"]}}] 
            },
            "kategori": { 
                "select": {"name": data["kategori"]} 
            },
            "porsiyon": { 
                "rich_text": [{"text": {"content": str(data["porsiyon"])}}] 
            },
            "Kalori (kcal)": { 
                "number": data["kalori"] 
            },
            "Protein (g)": { 
                "number": data["protein"] 
            },
            "Karbonhidrat (g)": { 
                "number": data["karbonhidrat"] 
            },
            "Yağ (g) (Number)": { # Senin tablodaki sütun ismiyle birebir aynı
                "number": data["yag"] 
            },
            "Vitaminler": { 
                "multi_select": [{"name": v} for v in data["vitaminler"]] 
            },
            "Mineraller": { 
                "multi_select": [{"name": m} for m in data["mineraller"]] 
            }
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"✅ Eklendi: {data['name']}")
    else:
        print(f"❌ Hata: {data['name']}")
        print(response.json())

# --- ANA MOTOR ---
if __name__ == "__main__":
    # Dosya yolunu bul
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "data.json")
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            food_list = json.load(f)
            
        print(f"🚀 İşlem başlıyor... {len(food_list)} veri taranacak.")
        
        for food in food_list:
            create_notion_page(food)
            # Notion API'yi yormamak için çok kısa bekleme
            time.sleep(0.3)
            
        print("🎉 İşlem bitti.")
        
    except FileNotFoundError:
        print("❌ Hata: data.json dosyası bulunamadı.")
