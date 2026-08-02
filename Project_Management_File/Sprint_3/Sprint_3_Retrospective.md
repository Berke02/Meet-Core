# Meet Core - Sprint 3 Retrospective (Geriye Bakış)

## 1. Neleri İyi Yaptık?

* **Kriz Yönetimi ve Takım Dayanışması:** Teslim gününde (final günü) yaşanan beklenmedik bilgisayar çökmeleri, hastalık ve seyahat durumlarına rağmen ekip içi iletişim kopmadı. Üyeler durumu şeffafça paylaştı ve görevler anında yeniden dağıtılarak (örneğin Berke'nin inisiyatif alıp video çekimini üstlenmesi) teslimatın aksaması engellendi.
* **Pratik Çözüm Üretme (Çeviklik):** Backend altyapısını kısıtlı sürede bulutta canlıya almanın yaratacağı riskler son dakika fark edildiğinde, hızlı bir kararla uygulamanın Frontend kısmı GitHub entegrasyonuyla Streamlit üzerinden canlıya alındı. Bu manevra, projenin değerlendiricilere çalışır bir linkle sunulmasını sağladı.
* **Altyapı ve Konteynerizasyon:** Uygulamanın farklı bilgisayarlarda hatasız çalışabilmesi için Docker dosyalarının hazırlanıp repoya eklenmesi, ürünün profesyonel bir standartta paketlenmesini sağladı.

## 2. Nerelerde Zorlandık? (Gelişim Alanlarımız)

* **Son Gün Darboğazı (Bottleneck) ve Zaman Yönetimi:** Video çekimi, canlıya alma (deployment) ve form doldurma gibi kritik operasyonların son saatlere kalması, öngörülemeyen donanım aksaklıklarıyla birleşince büyük bir stres yarattı. Teslimat süreçleri için her zaman bir hata payı (buffer) süresi bırakılması gerektiği anlaşıldı.
* **Donanım ve Altyapı Sorunları:** Teslimat sürecinde bazı cihazlarda yaşanan performans sorunları (kasma, kapanma vb.), demo videosunun çekilmesinde ve uygulamanın son ayağa kaldırılma aşamasında operasyonel tıkanıklıklara yol açtı.
* **Kapsam Planlaması (Scope Reduction):** Sprint 2 sonunda hedeflenen "gelişmiş (advanced) metrikler" entegrasyonu, zaman kısıtı ve sistem stabilitesini bozma riski nedeniyle iptal edilmek zorunda kaldı.

## 3. Gelecek Aksiyonlarımız (Bootcamp Sonrası Vizyon)

* **Tam Kapsamlı Canlıya Alma (Full Deployment):** Şu an arayüzü Streamlit üzerinde çalışan projenin, hazırlanan Docker altyapısı kullanılarak Backend ve LLM API hizmetleriyle birlikte bulut platformlarında uçtan uca canlıya alınması.
* **Gelişmiş Analiz Metriklerinin Eklenmesi:** Zaman kısıtından dolayı kapsam dışı bırakılan daha oturaklı ve analitik metrik algoritmalarının, projenin sonraki sürümlerinde sisteme entegre edilmesi.
* **Proaktif Operasyon Yönetimi:** Gelecekteki çalışmalarda dokümantasyon, form teslimleri ve tanıtım videoları gibi geliştirme dışı süreçlerin son güne bırakılmadan tamamlanarak olası krizlere karşı önceden kalkan oluşturulması.
