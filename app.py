"""
Streamlit Arayuzu
BMM4202 Veri Madenciligi Final Odevi
E-Pazaryeri Sepet Verilerinden Apriori ile Birliktelik Kurallari
"""
import os
import sys
import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Proje dizinini path'e ekle
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from src.data_preprocessing import run_preprocessing, load_dataset, detect_columns, clean_data, create_transactions
from src.apriori_analysis import run_apriori, create_chart, save_rules
from src.recommender import recommend_products, interpret_lift

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")


@st.cache_data
def load_and_analyze():
    """Veri yukler, on isler ve Apriori analizini calistirir (cache'li)."""
    # On isleme
    basket, unique_products, stats = run_preprocessing()
    # Apriori
    frequent_items, rules, final_support = run_apriori(basket)
    # Grafik ve dosyalari kaydet
    if rules is not None and len(rules) > 0:
        save_rules(rules)
        create_chart(rules)
    return basket, unique_products, stats, rules


def main():
    # Sayfa ayarlari
    st.set_page_config(
        page_title="E-Pazaryeri Birliktelik Analizi",
        page_icon="🛒",
        layout="wide",
    )

    # ===== Baslik =====
    st.title("🛒 E-Pazaryeri Sepet Verilerinden Birliktelik Kuralları")
    st.markdown("""
    **BMM4202 Veri Madenciliği Final Ödevi**  
    Bu uygulama, e-ticaret sepet verilerinden **Apriori algoritması** ile birliktelik 
    kurallarını çıkarır ve seçilen ürüne göre öneri yapar.
    """)
    st.divider()

    # ===== Veri Yukle ve Analiz Et =====
    try:
        basket, unique_products, stats, rules = load_and_analyze()
    except Exception as e:
        st.error(f"Veri yüklenirken hata oluştu: {e}")
        st.info("Lütfen data/ klasörüne online_retail.csv dosyasını koyun.")
        st.stop()

    if rules is None or len(rules) == 0:
        st.warning("Birliktelik kuralı bulunamadı. Lütfen veri setini kontrol edin.")
        st.stop()

    # ===== Istatistikler =====
    st.subheader("📊 Veri Seti Bilgileri")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Toplam Sipariş", f"{stats['total_transactions']:,}")
    col2.metric("Benzersiz Ürün", f"{stats['total_unique_products']:,}")
    col3.metric("Çıkarılan Kural", f"{len(rules):,}")
    col4.metric("Ort. Lift", f"{rules['lift'].mean():.2f}")

    st.divider()

    # ===== Urun Secimi ve Oneri =====
    st.subheader("🔍 Ürün Seçin ve Önerileri Görün")

    sorted_products = sorted(unique_products)
    selected = st.selectbox(
        "Bir ürün seçin:",
        sorted_products,
        index=0,
        help="Seçtiğiniz ürünle birlikte alınma eğilimi yüksek ürünleri gösterir."
    )

    if selected:
        recommendations = recommend_products(selected, rules, top_n=5)

        if len(recommendations) > 0:
            st.markdown(f"**'{selected}'** için önerilen ürünler:")

            for i, row in recommendations.iterrows():
                product = row["Onerilen Urun"]
                conf = row["Confidence"]
                lift = row["Lift"]
                interp = interpret_lift(lift)

                col_a, col_b = st.columns([3, 2])
                with col_a:
                    st.markdown(f"**{i+1}. {product}**")
                with col_b:
                    lift_color = "🟢" if lift > 1 else "🔴"
                    st.markdown(f"Confidence: `{conf:.4f}` | Lift: `{lift:.4f}` {lift_color} _{interp}_")

            # Tablo olarak da goster
            st.dataframe(recommendations, use_container_width=True, hide_index=True)
        else:
            st.info("Bu ürün için spesifik öneri bulunamadı.")

    st.divider()

    # ===== En Guclu Kurallar =====
    st.subheader("🏆 En Güçlü Birliktelik Kuralları")

    top_n = st.slider("Gösterilecek kural sayısı:", 5, 50, 15)
    top_rules = rules.head(top_n)[
        ["antecedents_str", "consequents_str", "support", "confidence", "lift"]
    ].copy()
    top_rules.columns = ["Öncül (Antecedent)", "Sonuç (Consequent)", "Support", "Confidence", "Lift"]

    st.dataframe(
        top_rules.style.format({
            "Support": "{:.4f}",
            "Confidence": "{:.4f}",
            "Lift": "{:.2f}",
        }).background_gradient(subset=["Lift"], cmap="YlOrRd"),
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # ===== Grafik =====
    st.subheader("📈 Support - Confidence - Lift Grafiği")

    chart_path = os.path.join(OUTPUTS_DIR, "support_confidence_lift_chart.png")
    if os.path.exists(chart_path):
        st.image(chart_path, use_container_width=True)
    else:
        # Grafigi burada olustur
        top10 = rules.head(10).copy()
        if len(top10) > 0:
            top10["label"] = top10.apply(
                lambda r: f"{r['antecedents_str'][:18]}→{r['consequents_str'][:18]}", axis=1
            )
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            axes[0].barh(range(len(top10)), top10["confidence"].values, color="#4A90D9")
            axes[0].set_yticks(range(len(top10)))
            axes[0].set_yticklabels(top10["label"].values, fontsize=7)
            axes[0].set_xlabel("Confidence")
            axes[0].set_title("İlk 10 Kural - Confidence")
            axes[0].invert_yaxis()

            axes[1].barh(range(len(top10)), top10["lift"].values, color="#E8913A")
            axes[1].set_yticks(range(len(top10)))
            axes[1].set_yticklabels(top10["label"].values, fontsize=7)
            axes[1].set_xlabel("Lift")
            axes[1].set_title("İlk 10 Kural - Lift")
            axes[1].invert_yaxis()

            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

    st.divider()

    # ===== Yorum =====
    st.subheader("💡 Yorum")
    st.markdown("""
    - **Support**: Bir kuralın veri setinde ne kadar sık geçtiğini gösterir.
    - **Confidence**: Öncül ürünü alan müşterinin sonuç ürününü de alma olasılığıdır.
    - **Lift > 1**: İki ürün arasında pozitif bir ilişki vardır; birlikte alınma eğilimi yüksektir.
    - **Lift = 1**: Ürünler bağımsızdır, aralarında özel bir ilişki yoktur.
    - **Lift < 1**: Negatif ilişki; ürünler birlikte alınma eğiliminde değildir.
    
    Bu analiz, e-pazaryeri platformlarında ürün öneri sistemleri, çapraz satış stratejileri 
    ve kampanya planlaması için kullanılabilir.
    """)

    # Footer
    st.divider()
    st.caption("BMM4202 Veri Madenciliği Final Ödevi | 202213709053 Furkan Dürceylan | Balıkesir Üniversitesi")


if __name__ == "__main__":
    main()
