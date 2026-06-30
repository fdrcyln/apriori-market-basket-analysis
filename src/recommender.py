"""
Urun Oneri Modulu
BMM4202 Veri Madenciligi Final Odevi
Birliktelik kurallarina dayali urun onerisi yapar.
"""
import pandas as pd


def recommend_products(selected_product, rules, top_n=5):
    """
    Secilen urune gore birliktelik kurallarina dayali oneri yapar.

    Parametreler:
        selected_product (str): Kullanicinin sectigi urun adi
        rules (pd.DataFrame): Birliktelik kurallari
        top_n (int): Onerilecek urun sayisi

    Dondurur:
        pd.DataFrame: Onerilen urunler (urun, confidence, lift, support)
    """
    if rules is None or len(rules) == 0:
        return pd.DataFrame(columns=["Onerilen Urun", "Confidence", "Lift", "Support"])

    selected_upper = selected_product.strip().upper()

    # Antecedents icinde secilen urunu ara
    mask = rules["antecedents"].apply(lambda x: selected_upper in [i.upper() for i in x])
    filtered = rules[mask].copy()

    if len(filtered) > 0:
        # Lift ve confidence'a gore sirala
        filtered = filtered.sort_values(by=["lift", "confidence"], ascending=False)

        recommendations = []
        seen = set()
        for _, row in filtered.iterrows():
            for product in row["consequents"]:
                if product.upper() != selected_upper and product not in seen:
                    seen.add(product)
                    recommendations.append({
                        "Onerilen Urun": product,
                        "Confidence": round(row["confidence"], 4),
                        "Lift": round(row["lift"], 4),
                        "Support": round(row["support"], 4),
                    })
                    if len(recommendations) >= top_n:
                        break
            if len(recommendations) >= top_n:
                break

        if recommendations:
            return pd.DataFrame(recommendations)

    # Kural bulunamazsa consequents icinde de ara
    mask2 = rules["consequents"].apply(lambda x: selected_upper in [i.upper() for i in x])
    filtered2 = rules[mask2].copy()

    if len(filtered2) > 0:
        filtered2 = filtered2.sort_values(by=["lift", "confidence"], ascending=False)
        recommendations = []
        seen = set()
        for _, row in filtered2.iterrows():
            for product in row["antecedents"]:
                if product.upper() != selected_upper and product not in seen:
                    seen.add(product)
                    recommendations.append({
                        "Onerilen Urun": product,
                        "Confidence": round(row["confidence"], 4),
                        "Lift": round(row["lift"], 4),
                        "Support": round(row["support"], 4),
                    })
                    if len(recommendations) >= top_n:
                        break
            if len(recommendations) >= top_n:
                break

        if recommendations:
            return pd.DataFrame(recommendations)

    # Hicbir kural bulunamazsa genel en guclu kurallari oner
    print(f"[BILGI] '{selected_product}' icin kural bulunamadi, genel oneriler gosteriliyor")
    top_rules = rules.head(top_n)
    general = []
    seen = set()
    for _, row in top_rules.iterrows():
        for p in list(row["consequents"]) + list(row["antecedents"]):
            if p not in seen:
                seen.add(p)
                general.append({
                    "Onerilen Urun": p + " (genel oneri)",
                    "Confidence": round(row["confidence"], 4),
                    "Lift": round(row["lift"], 4),
                    "Support": round(row["support"], 4),
                })
                if len(general) >= top_n:
                    break
        if len(general) >= top_n:
            break

    return pd.DataFrame(general) if general else pd.DataFrame(
        columns=["Onerilen Urun", "Confidence", "Lift", "Support"]
    )


def interpret_lift(lift_value):
    """Lift degerini yorumlar."""
    if lift_value > 1:
        return "Pozitif iliski (birlikte alinma egilimi yuksek)"
    elif lift_value == 1:
        return "Bagimsiz (iliski yok)"
    else:
        return "Negatif iliski (birlikte alinma egilimi dusuk)"
