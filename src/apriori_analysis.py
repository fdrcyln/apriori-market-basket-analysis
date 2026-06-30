"""
Apriori Analizi Modulu
BMM4202 Veri Madenciligi Final Odevi
Apriori algoritmasi ile birliktelik kurallarini cikarir.
"""
import os
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")


def load_basket():
    """One-hot encoded transaction verisini yukler."""
    path = os.path.join(DATA_DIR, "processed_transactions.csv")
    if not os.path.exists(path):
        print("[HATA] processed_transactions.csv bulunamadi!")
        print("  Once data_preprocessing.py calistirin.")
        return None
    basket = pd.read_csv(path)
    print(f"[BILGI] Transaction verisi yuklendi: {basket.shape}")
    return basket


def run_apriori(basket, min_support=0.02, min_confidence=0.3):
    """
    Apriori algoritmasi ile sik oge kumeleri ve birliktelik kurallarini bulur.
    Eger hic kural cikmiyorsa min_support dusurulur.
    """
    print(f"\n[BILGI] === Apriori Analizi ===")
    print(f"[BILGI] min_support={min_support}, min_confidence={min_confidence}")

    # Sik oge kumelerini bul
    frequent_items = apriori(basket, min_support=min_support, use_colnames=True)

    if len(frequent_items) == 0:
        print("[UYARI] Hic sik oge kumesi bulunamadi! min_support dusurulecek...")
        for new_sup in [0.01, 0.005, 0.003, 0.002, 0.001]:
            frequent_items = apriori(basket, min_support=new_sup, use_colnames=True)
            if len(frequent_items) > 0:
                min_support = new_sup
                print(f"[BILGI] Yeni min_support={new_sup}, bulunan kume: {len(frequent_items)}")
                break
        if len(frequent_items) == 0:
            print("[HATA] Hicbir support degerinde sik kume bulunamadi!")
            return None, None, min_support

    print(f"[BILGI] Sik oge kumesi sayisi: {len(frequent_items)}")

    # Birliktelik kurallarini olustur
    rules = association_rules(frequent_items, metric="confidence",
                              min_threshold=min_confidence, num_itemsets=len(frequent_items))

    if len(rules) == 0:
        print("[UYARI] Hic kural bulunamadi! min_confidence dusurulecek...")
        for new_conf in [0.2, 0.15, 0.1, 0.05]:
            rules = association_rules(frequent_items, metric="confidence",
                                      min_threshold=new_conf, num_itemsets=len(frequent_items))
            if len(rules) > 0:
                min_confidence = new_conf
                print(f"[BILGI] Yeni min_confidence={new_conf}, bulunan kural: {len(rules)}")
                break

    if len(rules) == 0:
        print("[HATA] Hicbir confidence degerinde kural bulunamadi!")
        return frequent_items, None, min_support

    # Kurallari sirala (lift ve confidence'a gore)
    rules = rules.sort_values(by=["lift", "confidence"], ascending=False)

    # frozenset'leri okunabilir stringe cevir
    rules["antecedents_str"] = rules["antecedents"].apply(lambda x: ", ".join(list(x)))
    rules["consequents_str"] = rules["consequents"].apply(lambda x: ", ".join(list(x)))

    print(f"[BILGI] Toplam kural sayisi: {len(rules)}")
    print(f"[BILGI] Ortalama lift: {rules['lift'].mean():.2f}")
    print(f"[BILGI] Ortalama confidence: {rules['confidence'].mean():.2f}")

    return frequent_items, rules, min_support


def save_rules(rules):
    """Kurallari CSV dosyalarina kaydeder."""
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    if rules is None or len(rules) == 0:
        print("[UYARI] Kaydedilecek kural yok!")
        return

    # Tum kurallar
    save_cols = ["antecedents_str", "consequents_str", "support", "confidence",
                 "lift", "leverage", "conviction"]
    available = [c for c in save_cols if c in rules.columns]
    all_path = os.path.join(OUTPUTS_DIR, "association_rules.csv")
    rules[available].to_csv(all_path, index=False)
    print(f"[BILGI] Tum kurallar kaydedildi: {all_path} ({len(rules)} kural)")

    # En iyi 20 kural
    top_path = os.path.join(OUTPUTS_DIR, "top_rules.csv")
    rules[available].head(20).to_csv(top_path, index=False)
    print(f"[BILGI] En iyi kurallar kaydedildi: {top_path}")


def create_chart(rules, top_n=10):
    """Support, confidence ve lift degerleri icin grafik olusturur."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    if rules is None or len(rules) == 0:
        print("[UYARI] Grafik icin kural yok!")
        return

    top = rules.head(top_n).copy()
    top["label"] = top.apply(
        lambda r: f"{r['antecedents_str'][:20]} -> {r['consequents_str'][:20]}", axis=1
    )

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Confidence grafigi
    colors_conf = plt.cm.Blues(top["confidence"].values / top["confidence"].max())
    axes[0].barh(range(len(top)), top["confidence"].values, color=colors_conf)
    axes[0].set_yticks(range(len(top)))
    axes[0].set_yticklabels(top["label"].values, fontsize=7)
    axes[0].set_xlabel("Confidence")
    axes[0].set_title(f"Ilk {top_n} Kural - Confidence")
    axes[0].invert_yaxis()

    # Lift grafigi
    colors_lift = plt.cm.Oranges(top["lift"].values / top["lift"].max())
    axes[1].barh(range(len(top)), top["lift"].values, color=colors_lift)
    axes[1].set_yticks(range(len(top)))
    axes[1].set_yticklabels(top["label"].values, fontsize=7)
    axes[1].set_xlabel("Lift")
    axes[1].set_title(f"Ilk {top_n} Kural - Lift")
    axes[1].invert_yaxis()

    plt.tight_layout()
    chart_path = os.path.join(OUTPUTS_DIR, "support_confidence_lift_chart.png")
    plt.savefig(chart_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[BILGI] Grafik kaydedildi: {chart_path}")


def run_analysis():
    """Tum analiz adimlarini calistirir."""
    basket = load_basket()
    if basket is None:
        return None, None
    frequent_items, rules, final_support = run_apriori(basket)
    save_rules(rules)
    create_chart(rules)
    return frequent_items, rules


if __name__ == "__main__":
    run_analysis()
    print("\n[BASARILI] Apriori analizi tamamlandi!")
