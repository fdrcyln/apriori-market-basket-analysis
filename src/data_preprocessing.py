"""
Veri On Isleme Modulu
BMM4202 Veri Madenciligi Final Odevi
"""
import os, sys
import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")


def load_dataset(filepath=None):
    """Veri setini yukler. CSV veya Excel formatini destekler."""
    if filepath is None:
        csv_path = os.path.join(DATA_DIR, "online_retail.csv")
        xlsx_path = os.path.join(DATA_DIR, "Online Retail.xlsx")
        if os.path.exists(csv_path):
            filepath = csv_path
        elif os.path.exists(xlsx_path):
            filepath = xlsx_path
        else:
            print("[HATA] Veri seti bulunamadi!")
            print(f"  Beklenen konum: {csv_path}")
            print("  Kaggle: https://www.kaggle.com/datasets/vijayuv/onlineretail")
            sys.exit(1)
    print(f"[BILGI] Veri seti yukleniyor: {filepath}")
    try:
        if filepath.endswith((".xlsx", ".xls")):
            df = pd.read_excel(filepath)
        else:
            try:
                df = pd.read_csv(filepath, encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(filepath, encoding="latin1")
    except Exception as e:
        print(f"[HATA] Veri seti okunamadi: {e}")
        sys.exit(1)
    print(f"[BILGI] Boyut: {df.shape[0]} satir, {df.shape[1]} sutun")
    print(f"[BILGI] Sutunlar: {list(df.columns)}")
    return df


def detect_columns(df):
    """Veri setindeki sutun adlarini otomatik algilar."""
    columns = {}
    col_lower = {c.lower().strip(): c for c in df.columns}
    mappings = {
        "invoice": ["invoiceno", "invoice", "invoice_no", "transaction_id", "order_id"],
        "description": ["description", "product_name", "productname", "item", "itemname"],
        "quantity": ["quantity", "qty", "amount", "count"],
        "customer_id": ["customerid", "customer_id", "customer", "member_number"],
        "date": ["invoicedate", "date", "invoice_date", "order_date"],
        "country": ["country"],
    }
    for key, candidates in mappings.items():
        for c in candidates:
            if c in col_lower:
                columns[key] = col_lower[c]
                break
    if "invoice" not in columns:
        columns["invoice"] = df.columns[0]
    if "description" not in columns and len(df.columns) > 1:
        columns["description"] = df.columns[1]
    print(f"[BILGI] Algilanan sutunlar: {columns}")
    return columns


def clean_data(df, columns):
    """Veri temizleme: eksik degerler, iptaller, negatif miktar, standardizasyon."""
    original_size = len(df)
    print(f"\n[BILGI] === Veri Temizleme ===")
    desc_col = columns.get("description")
    inv_col = columns.get("invoice")
    qty_col = columns.get("quantity")
    # 1. Eksik urun adlarini temizle
    if desc_col:
        df = df.dropna(subset=[desc_col]).copy()
    # 2. Iptal edilen siparisleri cikar (C ile baslayanlar)
    if inv_col:
        df.loc[:, inv_col] = df[inv_col].astype(str)
        df = df[~df[inv_col].str.startswith("C")].copy()
    # 3. Quantity <= 0 olanlari cikar
    if qty_col:
        df = df[df[qty_col] > 0]
    # 4. Urun adlarini standartlastir
    if desc_col:
        df[desc_col] = df[desc_col].astype(str).str.strip().str.upper()
        df[desc_col] = df[desc_col].str.replace(r'\s+', ' ', regex=True)
        exclude = ["?", "POSTAGE", "DOTCOM POSTAGE", "MANUAL", "BANK CHARGES", "AMAZONFEE"]
        for pat in exclude:
            df = df[df[desc_col] != pat]
    print(f"[BILGI] {original_size} -> {len(df)} satir ({original_size - len(df)} silindi)")
    return df


def create_transactions(df, columns, min_product_freq=5):
    """Siparis bazli one-hot encoded transaction verisi olusturur."""
    from mlxtend.preprocessing import TransactionEncoder
    inv_col = columns.get("invoice")
    desc_col = columns.get("description")
    if not inv_col or not desc_col:
        print("[HATA] Fatura ve urun sutunlari gerekli!")
        sys.exit(1)
    # Siparis bazli urun listesi
    grouped = df.groupby(inv_col)[desc_col].apply(lambda x: list(set(x))).reset_index()
    grouped.columns = ["InvoiceNo", "Products"]
    print(f"[BILGI] Toplam siparis: {len(grouped)}")
    # Urun frekanslari
    all_products = df[desc_col].value_counts()
    print(f"[BILGI] Toplam benzersiz urun: {len(all_products)}")
    # Nadir urunleri filtrele
    frequent = all_products[all_products >= min_product_freq].index.tolist()
    print(f"[BILGI] Min frekans={min_product_freq}, sik urun={len(frequent)}")
    grouped["Products"] = grouped["Products"].apply(lambda p: [x for x in p if x in frequent])
    grouped = grouped[grouped["Products"].apply(len) > 0]
    # One-hot encoding
    te = TransactionEncoder()
    te_array = te.fit(grouped["Products"].tolist()).transform(grouped["Products"].tolist())
    basket = pd.DataFrame(te_array, columns=te.columns_)
    # Cok buyuk veri seti icin sinirla
    if basket.shape[1] > 500:
        top_cols = basket.sum().sort_values(ascending=False).head(500).index.tolist()
        basket = basket[top_cols]
    print(f"[BILGI] One-hot encoded boyut: {basket.shape}")
    return basket, list(basket.columns), grouped


def save_processed_data(basket):
    """Islenmis verileri kaydeder."""
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, "processed_transactions.csv")
    basket.to_csv(path, index=False)
    print(f"[BILGI] Kaydedildi: {path}")


def run_preprocessing():
    """Tum on isleme adimlarini calistirir."""
    df = load_dataset()
    columns = detect_columns(df)
    df_clean = clean_data(df, columns)
    basket, unique_products, transactions = create_transactions(df_clean, columns)
    save_processed_data(basket)
    stats = {
        "total_transactions": len(basket),
        "total_unique_products": len(unique_products),
        "original_rows": len(df),
        "cleaned_rows": len(df_clean),
    }
    print(f"\n[BASARILI] On isleme tamam: {stats['total_transactions']} siparis, {stats['total_unique_products']} urun")
    return basket, unique_products, stats


if __name__ == "__main__":
    run_preprocessing()
