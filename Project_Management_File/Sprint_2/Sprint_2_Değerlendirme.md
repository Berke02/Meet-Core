# Meet Core - Sprint 2 Değerlendirme

## 1. Sprint Hedefi (Sprint Goal)
Sprint 1'de bağımsız (silo halinde) geliştirilen Frontend (arayüz) ve Backend (LLM & ASR) modüllerinin uçtan uca entegrasyonunu sağlamak ve tam çalışan bir MVP (Minimum Viable Product) elde etmek.

## 2. Neleri Tamamladık? (Geliştirilen Özellikler)
Sprint 2 boyunca takım üyeleri, modüllerin birleştirilmesi ve sistemin iyileştirilmesi üzerine odaklanmıştır:

* **Genel Entegrasyon:** Frontend ve Backend API'leri başarıyla birbirine bağlandı. Sistem artık girdi alıp yapay zeka modelleriyle işleyerek sonuçları anlık olarak arayüze yansıtabiliyor.
* **Yapay Zeka & Backend (Merve, Meleksu, Arda):** Backend tarafında veri akışı güncellenerek, metin içerisindeki hitapların (isimlerin) LLM tarafından algılanması sağlandı. Sistem artık transkriptte yakaladığı isimlere göre doğrudan o kişiye spesifik görev ataması yapabilmektedir. Toplantı sırasında ismi geçmeyen konuşmacılar, sistemin bozulmaması için otomatik olarak "unknown" (örn. unknown01) şeklinde etiketlenecek formata getirildi. Backend, arayüzden gelen verilerle LLM'i sınırlandırarak doğruluk oranını artırdı.
* **Frontend (Feyza, Merve):** Kullanıcıların sisteme doğrudan metin/dosya girebilmesi için Frontend tarafına "Doküman Yükleme" alanı eklendi. Ayrıca Gemini modelinin toplantıda bulunmayan kurgusal kişilere görev atama eğilimini (halüsinasyon) çözmek amacıyla arayüze manuel bir "Toplantıdaki Kişi Sayısı" girdi alanı eklendi.
* **Veri Bilimi & Test (Berke):** Uçtan uca bağlanan sistemin testleri ve doğrulama süreçleri gerçekleştirildi. İlk etapta kelime ve frekans bazlı temel analiz metriklerinin arayüz bağlantısı sağlandı.

## 3. Ortaya Çıkan MVP Durumu
İkinci sprint itibarıyla projemiz; girdi alabilen, yapay zeka (ASR & LLM) ile metni işleyen, kişileri ayırt edip onlara görev atayan ve tüm bu sonuçları başarılı bir şekilde arayüzde sergileyen tam fonksiyonel (uçtan uca çalışan) bir MVP yapısına kavuşmuştur.

> **Teknik Not:** Sistemin uçtan uca çalışması ve LLM halüsinasyonlarının (manuel kişi sınırlandırması ile) önüne geçilmesi güvence altına alınmıştır. Sadece kelime esaslı temel metrikler yerine, sistemin analiz yeteneğini artıracak daha "advanced" (gelişmiş ve oturaklı) metrik algoritmalarının oluşturulması Sprint 3 planlamasına dahil edilmiştir.
