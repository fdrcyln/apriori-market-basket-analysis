<h1 align="center">🛒 E-Pazaryeri Market Basket Analizi & Ürün Öneri Sistemi</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Machine%20Learning-Apriori-orange?style=for-the-badge" alt="Apriori">
</p>

## 📝 Proje Hakkında

Bu proje, veri madenciliği kapsamında geliştirilmiş bir **Birliktelik Kuralı Çıkarımı (Association Rule Mining)** ve **Ürün Öneri Sistemi** uygulamasıdır. 

Büyük bir çevrimiçi perakende mağazasının (Online Retail) gerçek işlem (sepet) verileri kullanılarak, **Apriori algoritması** yardımıyla müşterilerin birlikte satın alma alışkanlıkları analiz edilmiştir. Elde edilen güçlü birliktelik kuralları, kullanıcı dostu bir **Streamlit web arayüzü** ile etkileşimli bir ürün öneri sistemine (Recommender System) dönüştürülmüştür.

> **Bağlam:** Bu çalışma, Balıkesir Üniversitesi - Bilgisayar Mühendisliği Bölümü **BMM4202 Veri Madenciliği** dersi final ödevi kapsamında hazırlanmıştır. 
> 
> **Öğrenci:** Furkan Dürceylan (202213709053)

---

## 🌟 Temel Özellikler

- **Veri Ön İşleme (Data Preprocessing):** Eksik verilerin temizlenmesi, iadelerin (negatif miktarlar) filtrelenmesi, veri standardizasyonu ve nadir ürünlerin ayıklanması.
- **Apriori Algoritması:** Binlerce işlem içerisinden *Support*, *Confidence* ve *Lift* metriklerine dayalı gizli satın alma örüntülerinin çıkarılması.
- **Web Scraping Modülü (Bonus):** `BeautifulSoup` kullanılarak etik kurallar çerçevesinde e-ticaret sitelerinden deneme amaçlı veri çekme özelliği.
- **Dinamik Öneri Arayüzü:** Kullanıcının seçtiği bir ürüne göre, diğer müşterilerin alışkanlıklarından yola çıkarak en mantıklı yan ürünleri öneren interaktif **Streamlit** dashboard'u.
- **Otomatik Raporlama:** `python-docx` ile bulguların ve oluşturulan kuralların akademik standartlarda MS Word dokümanına dökülmesi.

---

## 🏗️ Proje Yapısı

```bash
apriori-market-basket-analysis/
│
├── data/                            # Veri setlerinin bulunduğu klasör (Git'te yoksayıldı)
│   ├── online_retail.csv            # Orijinal Kaggle/UCI veri seti
│   ├── scraped_products.csv         # Scraping ile çekilen örnek veri
│   └── processed_transactions.csv   # Apriori için One-Hot formatlı matris
│
├── src/                             # Ana Kaynak Kodları
│   ├── data_preprocessing.py        # Veri temizleme ve dönüştürme scripti
│   ├── apriori_analysis.py          # Kural çıkarımı ve metrik hesabı
│   ├── scraper.py                   # Web scraping scripti
│   ├── recommender.py               # Ürün önerme algoritmaları
│   └── report_generator.py          # .docx formatında rapor hazırlama
│
├── outputs/                         # Analiz Çıktıları
│   ├── association_rules.csv        # Bulunan tüm kurallar
│   ├── top_rules.csv                # En yüksek Lift'e sahip ilk 20 kural
│   ├── support_confidence_lift_chart.png # Kuralların görselleştirmesi
│   └── final_report.docx            # Otomatik üretilen proje raporu
│
├── app.py                           # 🚀 Streamlit web uygulaması (Arayüz)
├── requirements.txt                 # Bağımlılıklar
└── .gitignore
```

---

## 💻 Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla izleyin:

### 1. Repoyu Klonlayın
```bash
git clone https://github.com/fdrcyln/apriori-market-basket-analysis.git
cd apriori-market-basket-analysis
```

### 2. Gerekli Kütüphaneleri Yükleyin
Sanal bir ortam (virtual environment) oluşturmanız tavsiye edilir.
```bash
pip install -r requirements.txt
```

### 3. Veri Setini İndirin
Kaggle'dan [Online Retail Dataset](https://www.kaggle.com/datasets/vijayuv/onlineretail) (veya UCI ML Repository) verisini indirip, `data/` klasörünün içine `online_retail.csv` veya `Online Retail.xlsx` ismiyle yerleştirin. (Proje her iki formatı da otomatik tanır).

### 4. Analiz ve Ön İşlemeyi Çalıştırın
Tüm veri ardışık düzenini (pipeline) çalıştırmak için (bu işlem veri boyutuna göre birkaç dakika sürebilir):
```bash
python src/data_preprocessing.py
python src/apriori_analysis.py
```

*(İsteğe bağlı)* Otomatik akademik Word raporunu oluşturmak veya veri çekme (scraping) denemesini test etmek için:
```bash
python src/report_generator.py
python src/scraper.py
```

### 5. Streamlit Arayüzünü Başlatın
Uygulamayı tarayıcıda görüntülemek için:
```bash
python -m streamlit run app.py
```
*Otomatik açılmazsa, terminalde beliren `http://localhost:8501` adresine tarayıcınızdan gidebilirsiniz.*

---

## 📊 Analiz Sonuçları ve Çıktılar

541.909 ham satış kaydı üzerinde yapılan temizleme sonrası yaklaşık **19.887 sipariş** ve **500 popüler ürün** ile analiz gerçekleştirilmiştir.

**Örnek Güçlü Birliktelik Kuralı:**
- **Öncül Ürün (Antecedent):** `PINK REGENCY TEACUP AND SAUCER` & `ROSES REGENCY TEACUP AND SAUCER`
- **Sonuç Ürün (Consequent):** `GREEN REGENCY TEACUP AND SAUCER`
- **Confidence (Güven):** `%90.4` -> Öncül ürünleri alanların %90'ı sonuç ürününü de almıştır.
- **Lift (Kaldıraç):** `17.7` -> Bu ürünlerin birlikte alınma ihtimali, rastgele alınma ihtimallerinden 17.7 kat daha fazladır.

Bu bulgular, e-ticaret platformlarında **"Birlikte Al" (Bundle) kampanyaları**, **Sepet sayfasında çapraz satış (Cross-sell)** ve **Raf dizilimi optimizasyonu** gibi kritik iş kararlarında doğrudan kullanılabilir.

---

## 🛠️ Kullanılan Teknolojiler

- **Veri İşleme & Algoritma:** `pandas`, `numpy`, `mlxtend` (TransactionEncoder, apriori, association_rules)
- **Veri Görselleştirme:** `matplotlib`
- **Web Scraping:** `requests`, `BeautifulSoup4`
- **Arayüz (Frontend):** `Streamlit`
- **Raporlama:** `python-docx`

---

> **Not:** Bu repo akademik bir ödev kapsamında oluşturulmuştur ve açık kaynak kodludur. Veri madenciliği ve birliktelik kuralı öğrenmek isteyen herkes örnek olarak inceleyebilir.
