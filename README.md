# E-Pazaryeri Sepet Verilerinden Apriori Algoritması ile Birliktelik Kurallarının Çıkarılması

**BMM4202 Veri Madenciliği Final Ödevi**  
Balıkesir Üniversitesi - Bilgisayar Mühendisliği Bölümü  
202213709053 Furkan Dürceylan

## Proje Hakkında

Bu proje, e-ticaret sepet verilerinden **Apriori algoritması** kullanarak ürünler arasındaki birliktelik kurallarını çıkarır. Kullanıcı Streamlit arayüzünden bir ürün seçtiğinde, o ürünle birlikte alınma eğilimi yüksek ürünler önerilir.

## Kurulum

### 1. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

### 2. Veri setini indirin:

Kaggle'dan [Online Retail Dataset](https://www.kaggle.com/datasets/vijayuv/onlineretail) veri setini indirip `data/` klasörüne `online_retail.csv` adıyla kaydedin.

### 3. Web Scraping (opsiyonel):

```bash
python src/scraper.py
```

### 4. Veri ön işleme ve analizi çalıştırın:

```bash
python src/data_preprocessing.py
python src/apriori_analysis.py
```

### 5. Streamlit arayüzünü başlatın:

```bash
streamlit run app.py
```

### 6. Rapor oluşturun:

```bash
python src/report_generator.py
```

## Proje Yapısı

```
202213709053_Furkan_Durceylan/
├── data/
│   ├── online_retail.csv
│   ├── scraped_products.csv
│   └── processed_transactions.csv
├── src/
│   ├── data_preprocessing.py
│   ├── apriori_analysis.py
│   ├── scraper.py
│   ├── recommender.py
│   └── report_generator.py
├── outputs/
│   ├── association_rules.csv
│   ├── top_rules.csv
│   ├── support_confidence_lift_chart.png
│   └── final_report.docx
├── app.py
├── requirements.txt
└── README.md
```

## Kullanılan Teknolojiler

- Python, pandas, numpy
- mlxtend (Apriori, Association Rules)
- matplotlib
- Streamlit
- requests, BeautifulSoup
- python-docx

## Lisans

Bu proje eğitim amaçlıdır.
