# Sprint 1 - LLM & Prompt Engineering Çalışması

Bu sprint kapsamında Meet Core projesi için toplantı metni analiz eden LLM tabanlı MVP akışı geliştirilmiştir.

## Yapılan İşler

- LLM sağlayıcısı olarak Gemini 2.5 Flash seçildi.
- Toplantı metninden özet, ana konular, katılımcılar, kararlar, aksiyon maddeleri ve açık sorular çıkaran yapı kuruldu.
- LLM çıktısı Pydantic schema ile doğrulanabilir JSON formatına alındı.
- Prompt dosyaları koddan ayrılarak yönetilebilir hale getirildi.
- Göreceli tarih ifadeleri için referans tarih ve gün bilgisi prompt'a eklendi.
- pazartesiye kadar, 5 Temmuz gibi tarih ifadelerinin normalize edilmesi test edildi.
- Gemini yoğunluk hataları için retry mekanizması eklendi.
- FastAPI endpoint oluşturuldu.

## Endpoint

POST /api/meetings/analyze

## Request Örneği

{
  "meeting_text": "Merve: LLM entegrasyonunu üstleneceğim. Berke: Metrik araştırmasını pazartesiye kadar paylaşacağım. Ekip: İlk demo için ses yükleme kapsam dışı bırakıldı."
}

## Response Alanları

- summary
- key_topics
- participants
- decisions
- action_items
- open_questions

## Durum

LLM + prompt engineering MVP akışı tamamlandı ve Swagger üzerinden test edildi.
