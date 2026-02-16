import requests
import json
import time

# --- AYARLAR ---
NOTION_TOKEN = "SENIN_NOTION_TOKEN_BURAYA"
DATABASE_ID = "309a53bd113f801293d6d3d0ffaa03f1"  # Senin attığın linkten aldığım ID

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_notion_page(data):
    url = "https://api.notion.com/v1/pages"
    
    # JSON verisini Notion formatına çevirme
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
            "Yağ (g) (Number)": { 
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

# --- ÇALIŞTIRMA KISMI ---
if __name__ == "__main__":
    print("📂 data.json okunuyor...")
    
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            food_list = json.load(f)
            
        print(f"🚀 Toplam {len(food_list)} adet veri Notion'a gönderilecek...")
        
        for food in food_list:
            create_notion_page(food)
            # API'yi boğmamak için kısa bir bekleme
            time.sleep(0.5) 
            
        print("🎉 İşlem tamamlandı!")
        
    except FileNotFoundError:
        print("❌ Hata: data.json dosyası bulunamadı.")
