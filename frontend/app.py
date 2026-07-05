import streamlit as st

# 1. Sayfa Ayarları (Geniş ekran modunu açtık)
st.set_page_config(page_title="Meet Core", page_icon="🎙️", layout="wide")

# 2. YAN MENÜ (SIDEBAR) TASARIMI
with st.sidebar:
    st.header("📌 Menü")
    st.button("Yeni Toplantı Analizi", use_container_width=True, type="primary")
    st.button("Geçmiş Toplantılar", use_container_width=True)
    st.button("Risk Dashboard", use_container_width=True)
    st.divider()
    st.info("🤖 Agent Durumu: Hazır")

# 3. ANA EKRAN TASARIMI
st.title("🎙️ Meet Core: Yeni Toplantı")
st.markdown("Toplantı ses kaydını yükleyin veya notları yapıştırın. Yapay zeka ajanları sizin için aksiyonları ve riskleri çıkarsın.")
st.divider()

# Ekranı iki sütuna bölüyoruz (Yükleme ve Metin alanı yan yana dursun diye)
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎵 Ses Kaydı Yükle")
    # Berke ve Arda'nın ses ayırma modeli için dosya alma alanı
    uploaded_file = st.file_uploader("Sürükle bırak veya dosya seç", type=["mp3", "wav", "m4a"])
    if uploaded_file is not None:
        st.success("Dosya başarıyla yüklendi!")

with col2:
    st.subheader("📝 Veya Transkript Yapıştır")
    transcript = st.text_area("Metni buraya girin...", height=150)

# Analiz Butonu
st.markdown("<br>", unsafe_allow_html=True) # Araya biraz boşluk koyuyoruz
if st.button("🚀 Yapay Zeka ile Analiz Et", use_container_width=True):
    if uploaded_file or transcript:
        # Meleksu ve Merve'nin LLM Agent'larına veri gidecek kısım
        st.info("Agent'lar çalışıyor... Görevler ve risk metrikleri çıkarılıyor. Lütfen bekleyin...")
    else:
        st.warning("Lütfen analiz için bir dosya yükleyin veya metin girin.")
