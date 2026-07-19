# Meet Core - Sprint 2 Retrospective (Geriye Bakış)

## 1. Neleri İyi Yaptık?

* **Asenkron İletişim ve Esneklik:** Takım üyelerinin dışarıda olma durumları veya program uyuşmazlıkları nedeniyle senkron toplantılar ayarlamakta zorlansak da, süreci WhatsApp üzerinden asenkron ve esnek bir şekilde başarıyla yönettik.
* **İnisiyatif Alma ve İş Birliği:** Sprint 1'de yaşanan "silo halinde çalışma" problemini aştık. Özellikle Frontend ve Backend'in bağlanması sürecinde geliştiriciler (Merve, Feyza) hızlıca inisiyatif alarak organize oldu ve entegrasyonu pürüzsüzce gerçekleştirdi.
* **Hızlı Problem Çözme:** Birleştirme sonrası testlerde Gemini modelinin toplantıda olmayan kişilere görev uydurma eğilimini fark edip, pratik ve yaratıcı bir çözümle (arayüze "toplantıdaki kişi sayısı" parametresi ekleyerek) hızlıca bu engeli ortadan kaldırdık.

## 2. Nerelerde Zorlandık? (Gelişim Alanlarımız)

* **Senkron Toplantı Ayarlama:** Üyelerin kişisel yoğunlukları ve program farklılıkları, planlanan bazı değerlendirme ve kod birleştirme toplantılarının ertelenmesine veya iptal edilmesine neden oldu. Süreci asenkron iletişimle kurtarmış olsak da, eşzamanlı çalışmanın getirebileceği hız avantajından zaman zaman mahrum kaldık.
* **Yapay Zeka Halüsinasyonları (Teknik Zorluk):** LLM'in (Gemini) metin dışına çıkarak kurgusal görev atamaları yapması, entegrasyon aşamasında beklenmedik bir teknik blokaj yarattı ve Backend mantığında ekstra bir revizyon yapılmasına sebep oldu.

## 3. Sprint 3 İçin Aksiyon Planımız (Neleri Değiştireceğiz?)

* **Gelişmiş (Advanced) Metriklerin Entegrasyonu:** Son sprintte yeni bir modül eklemek yerine, sistemde halihazırda var olan kelime ve frekans odaklı basit metrikleri daha oturaklı, elle tutulur ve analiz yeteneği yüksek metrik algoritmalarıyla değiştireceğiz.
* **Arayüz (UI) İyileştirmeleri:** Uçtan uca bağlanan ve sorunsuz çalışan sistemimizin kullanıcı deneyimini artırmak için Frontend tarafında tasarım iyileştirmelerine (son makyajlara) odaklanacağız.
* **Özellik Eklemeleri ve Geliştirmeleri:** Kullanıcı deneyimini ve verimliliği arttırmak adına yeni özellikler üzerinde çalışılacak ve hazır sisteme başarılı bir şekilde entegre etmeye odaklanacağız.
* **Final Sunumu ve Ürün Teslimi:** Projenin MVP gereksinimlerini çoktan aşmış olması sebebiyle, son haftayı projenin canlıya alınma (deployment) ihtimallerini değerlendirerek ve jüriye sunulacak final dokümantasyonlarını/videolarını hazırlayarak geçireceğiz.
