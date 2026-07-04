# Meet Core - Sprint 1 Değerlendirme 

---

## 1. Sprint Hedefi (Sprint Goal)
Takım yapısını oturtmak, "Meet Core" proje fikrinin MVP kapsamını belirlemek ve ürünün temel yapı taşlarını (Arayüz, LLM Entegrasyonu, Test Veri Setleri) bağımsız modüller halinde ayağa kaldırmak.

---

## 2. Neleri Tamamladık? (Geliştirilen Özellikler)
Sprint 1 boyunca farklı disiplinlerdeki takım üyeleri kendi alanlarındaki altyapı çalışmalarını tamamlamıştır:

*   **Proje Yönetimi ve Altyapı:** Takım iletişim kanalları, GitHub reposu ve Trello panosu kuruldu. Rol dağılımları netleştirildi.
*   **Veri Bilimi (Berke, Arda):** ASR (Sesten Metne Çeviri) ve konuşmacı ayrımı (Speaker Diarization) altyapısı için araştırmalar tamamlandı ve bu özelliğin MVP kapsamında tutulmasına karar verildi. Sistemin test edilebilmesi için örnek toplantı senaryolarını içeren `.txt` formatında model test veri setleri oluşturularak yapay zeka ekibine iletildi. Risk metriklerinin hesaplanması için altyapı dokümantasyonu çıkarıldı.
*   **Yapay Zeka & Backend (Meleksu, Merve):** LLM API entegrasyonu başarıyla sağlandı. Prompt Engineering süreçleri tamamlanarak, sisteme verilen ham toplantı transkriptlerinden kararları, görev listelerini ve sorumlu kişileri yapılandırılmış formatta geri döndüren agentic arka plan mimarisi kuruldu. Geliştirilen backend kodları `main/backend` dizinine pushlandı.
*   **Frontend (Feyza):** Kullanıcıların verileri sisteme girebileceği ve LLM çıktılarını görebileceği temel (base) kullanıcı arayüzü oluşturuldu.

---

## 3. Ortaya Çıkan MVP Durumu
Bu sprint sonunda, ürünün çalışması için gereken temel bileşenler (Test Verisi, Backend/LLM İşleyişi ve Frontend Taslağı) üretilmiştir.

> **Teknik Not:** İlk sprintin kısıtlı süresi içerisinde modüller ayrı ayrı ayağa kaldırılmış olup, henüz uçtan uca birbirleriyle tam entegre çalışmamaktadır. Arayüz, backend API'si ve sistemin karar çıktıları bağımsız olarak test edilebilir durumdadır. Modüllerin entegrasyonu Sprint 2 planlamasına dahil edilmiştir.
