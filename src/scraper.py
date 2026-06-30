"""
Web Scraping Modulu
BMM4202 Veri Madenciligi Final Odevi
E-pazaryeri urun bilgilerini cekmek icin kullanilir.
Etik ve basit bir scraping ornegi.
"""
import os
import csv
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")


def scrape_products():
    """
    Web scraping ile e-pazaryeri urun bilgilerini ceker.
    Basarisiz olursa ornek veri olusturur.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    output_path = os.path.join(DATA_DIR, "scraped_products.csv")
    products = []
    today = datetime.now().strftime("%Y-%m-%d")

    # Gercek scraping denemesi
    try:
        import requests
        from bs4 import BeautifulSoup

        print("[BILGI] Web scraping denemesi basliyor...")
        print("[BILGI] Hedef: books.toscrape.com (izin verilen test sitesi)")

        url = "https://books.toscrape.com/"
        headers = {"User-Agent": "Mozilla/5.0 (Educational Project)"}

        # robots.txt kontrol
        try:
            robots_resp = requests.get(url + "robots.txt", timeout=5)
            print(f"[BILGI] robots.txt durumu: {robots_resp.status_code}")
        except Exception:
            print("[UYARI] robots.txt kontrol edilemedi")

        # Ana sayfayi cek
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Urun bilgilerini parse et (en fazla 20 urun)
        articles = soup.find_all("article", class_="product_pod")[:20]

        for article in articles:
            try:
                title_tag = article.find("h3").find("a")
                name = title_tag.get("title", title_tag.text.strip())
                category = "Book"
                products.append({
                    "product_name": name,
                    "category": category,
                    "source": "books.toscrape.com",
                    "scraped_date": today,
                })
            except Exception:
                continue

        if products:
            print(f"[BILGI] {len(products)} urun basariyla cekildi!")
        else:
            print("[UYARI] Urun cekilemedi, ornek veri olusturulacak")

    except ImportError:
        print("[UYARI] requests/beautifulsoup4 yuklu degil")
    except Exception as e:
        print(f"[UYARI] Scraping basarisiz: {e}")
        print("[BILGI] Site erisim engellenmis olabilir.")

    # Bos kaldiysa ornek veri olustur
    if not products:
        print("[BILGI] Ornek scraped_products.csv olusturuluyor...")
        sample_items = [
            ("Wireless Mouse", "Electronics"),
            ("USB-C Charging Cable", "Electronics"),
            ("Laptop Stand", "Electronics"),
            ("Mechanical Keyboard", "Electronics"),
            ("Bluetooth Headphones", "Electronics"),
            ("Phone Case", "Accessories"),
            ("Screen Protector", "Accessories"),
            ("Notebook Set", "Stationery"),
            ("Ballpoint Pen Pack", "Stationery"),
            ("Desk Organizer", "Home Office"),
            ("LED Desk Lamp", "Home Office"),
            ("Coffee Mug", "Kitchen"),
            ("Water Bottle", "Kitchen"),
            ("Backpack", "Bags"),
            ("Tote Bag", "Bags"),
        ]
        for name, cat in sample_items:
            products.append({
                "product_name": name,
                "category": cat,
                "source": "manual_sample",
                "scraped_date": today,
            })
        print("[BILGI] Site engellenirse bu ornek veri kullanilabilir.")

    # CSV kaydet
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["product_name", "category", "source", "scraped_date"])
        writer.writeheader()
        writer.writerows(products)

    print(f"[BILGI] Kaydedildi: {output_path} ({len(products)} urun)")
    return products


if __name__ == "__main__":
    scrape_products()
    print("\n[BASARILI] Web scraping tamamlandi!")
