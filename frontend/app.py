import streamlit as st
import time
import pandas as pd

# 1. Sayfa Ayarları
st.set_page_config(page_title="Meet Core", page_icon="🎙️", layout="wide")

# 2. YAN MENÜ VE SAYFA YÖNLENDİRMESİ
with st.sidebar:
    st.header("📌 Menü")
    secilen_sayfa = st.radio(
        "Sayfa Seçin:", 
        ["Yeni Toplantı Analizi", "Risk Dashboard", "Geçmiş Toplantılar"]
    )
    st.divider()
    st.info("🤖 Agent Durumu: Hazır")

# ==========================================
# SAYFA 1: YENİ TOPLANTI ANALİZİ
# ==========================================
if secilen_sayfa == "Yeni Toplantı Analizi":
    st.title("🎙️ Meet Core: Yeni Toplantı Analizi")
    st.markdown("Toplantı ses kaydını yükleyin veya notları yapıştırın. Yapay zeka ajanları sizin için aksiyonları ve riskleri çıkarsın.")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("🎵 Ses Kaydı Yükle (Sürükle bırak)", type=["mp3", "wav", "m4a"])
    with col2:
        transcript = st.text_area("📝 Veya Transkript Yapıştır", height=110)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Yapay Zeka ile Analiz Et", use_container_width=True):
        if uploaded_file or transcript:
            with st.spinner("Agent'lar çalışıyor... Ses ayrıştırılıyor ve risk metrikleri hesaplanıyor..."):
                time.sleep(2) 
            
            st.success("✅ Toplantı başarıyla analiz edildi!")
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Toplam Süre", "45 Dk")
            m2.metric("Çıkarılan Görev", "5 Adet")
            m3.metric("Yüksek Riskli Görev", "2 Adet", "-Acil", delta_color="inverse")
            m4.metric("Genel Verimlilik", "%85", "+%5")
            
            st.divider()

            tab1, tab2, tab3 = st.tabs(["📝 Özet & Kararlar", "🎯 Görevler ve Risk Skorları", "🧠 Hafıza (Geçmiş Bağlantılar)"])
            
            with tab1:
                st.subheader("Toplantı Özeti")
                st.info("Bu toplantıda Q3 pazarlama stratejileri ve frontend arayüzünün agent'larla entegrasyonu konuşuldu.")
                
            with tab2:
                st.subheader("Aksiyon Maddeleri ve Risk Durumu")
                gorev_verileri = pd.DataFrame([
                    {"Sorumlu": "Feyza", "Görev": "Dashboard UI", "Deadline": "Yarın", "Risk Skoru": 85},
                    {"Sorumlu": "Merve", "Görev": "LLM Entegrasyonu", "Deadline": "Cuma", "Risk Skoru": 40},
                    {"Sorumlu": "Berke", "Görev": "Ses Modeli", "Deadline": "Haftaya", "Risk Skoru": 90},
                ])
                st.dataframe(gorev_verileri, use_container_width=True)
                
            with tab3:
                st.subheader("Önceki Toplantılarla Bağlantılar")
                st.warning("Geçen ayki toplantıda API gecikmeleri konuşulmuştu. Aksiyonlar kapanmamış!")
        else:
            st.error("Lütfen analiz için bir dosya yükleyin veya metin girin.")

# ==========================================
# SAYFA 2: RİSK DASHBOARD
# ==========================================
elif secilen_sayfa == "Risk Dashboard":
    st.title("📊 Risk ve Takip Dashboard'u")
    st.markdown("Tüm toplantılardaki görevlerin takım bazlı risk analizi ve verimlilik metrikleri.")
    st.divider()

    # Örnek Grafik Verileri
    risk_data = pd.DataFrame({
        "Takım Üyesi": ["Feyza", "Merve", "Berke", "Arda"],
        "Açık Görev Sayısı": [3, 2, 5, 1],
        "Yüksek Riskli Görev": [1, 0, 3, 0]
    }).set_index("Takım Üyesi")

    col_grafik1, col_grafik2 = st.columns(2)

    with col_grafik1:
        st.subheader("👤 Kişi Bazlı Toplam Görev Dağılımı")
        st.bar_chart(risk_data["Açık Görev Sayısı"])

    with col_grafik2:
        st.subheader("⚠️ Yüksek Riskli Görevler (Acil)")
        st.bar_chart(risk_data["Yüksek Riskli Görev"], color="#ff2b2b") # Kırmızı grafik

# ==========================================
# SAYFA 3: GEÇMİŞ TOPLANTILAR
# ==========================================
elif secilen_sayfa == "Geçmiş Toplantılar":
    st.title("🗂️ Geçmiş Toplantılar Arşivi")
    st.markdown("Önceki toplantıların analizlerine, kararlarına ve görev listelerine buradan ulaşabilirsiniz.")
    st.divider()

    # Geçmiş toplantıların listesi (Arama için)
    gecmis_toplantilar = {
        "Haftalık Senkronizasyon (10.07.2026)": {
            "tarih": "10.07.2026",
            "ozet": "Haftalık ilerlemeler değerlendirildi. Backend ve ML modellerinin API süreçleri konuşuldu.",
            "gorevler": [
                {"Sorumlu": "Arda", "Görev": "Gecikme Risk Metriklerinin Optimize Edilmesi", "Durum": "Devam Ediyor"},
                {"Sorumlu": "Meleksu", "Görev": "Agent Backlog Güncellemesi", "Durum": "Tamamlandı"}
            ]
        },
        "Sprint Planlama Toplantısı (03.07.2026)": {
            "tarih": "03.07.2026",
            "ozet": "Bootcamp projesi için MVP kapsamı belirlendi. Görev dağılımları yapıldı.",
            "gorevler": [
                {"Sorumlu": "Feyza", "Görev": "Streamlit Arayüz Tasarımı", "Durum": "Tamamlandı"},
                {"Sorumlu": "Merve", "Görev": "Prompt Yönetimi Altyapısı", "Durum": "Tamamlandı"}
            ]
        }
    }

    # Kullanıcının toplantı seçebileceği arama kutusu
    secilen_toplantı_adi = st.selectbox(
        "🔍 İncelemek istediğiniz toplantıyı seçin:", 
        list(gecmis_toplantilar.keys())
    )

    if secilen_toplantı_adi:
        veriler = gecmis_toplantilar[secilen_toplantı_adi]
        
        st.markdown(f"### 📅 Toplantı Tarihi: {veriler['tarih']}")
        
        # Detayları sekmelerle gösteriyoruz
        t1, t2 = st.tabs(["📝 Toplantı Özeti", "📋 Alınan Kararlar & Görevler"])
        
        with t1:
            st.info(veriler["ozet"])
            
        with t2:
            st.write("**Bu Toplantıda Dağıtılan Görevler:**")
            st.dataframe(pd.DataFrame(veriler["gorevler"]), use_container_width=True)
