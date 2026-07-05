import re
from typing import Dict, List, Any

class TaskMetricsCalculator:
    
    def __init__(self):
        # 1. Hazırlık: Belirsizlik kelimeleri
        # Görevde muğlaklık yaratan ifadeleri bu sözlükte tutuyoruz.
        self.ambiguity_words = [
            "belki", "bakarız", "sanırım", "gibi", "çalışırız", 
            "duruma göre", "halletmeye çalış", "bir ara", "inşallah",
            "kısmetse", "dur bakalım", "vakit bulursam", "boşluğumda",
            "şöyle bir", "kabaca", "hemen hemen", "yaklaşık", "aşağı yukarı",
            "umut ediyorum", "zannedersem", "tahminen", "ihtimalle"
        ]
        
        # Hazırlık: Aciliyet kelimeleri ve ağırlıkları
        # Cümlede geçen zaman bildiren kelimelerin önem derecesine göre puanları.
        self.urgency_words = {
            "acil": 50, "hemen": 50, "bugün": 50, "ivedi": 50,
            "şimdi": 50, "derhal": 50, "mesai bitimine kadar": 50, "çok acil": 50,
            "yarın": 30, "bu hafta içi": 30, "cumaya kadar": 30, 
            "yakın zamanda": 30, "birkaç güne": 30, "haftaya": 30, "en kısa sürede": 30,
            "önümüzdeki hafta": 10, "ay sonu": 10, "önümüzdeki ay": 10, 
            "daha sonra": 10, "ilerleyen zamanda": 10, "gelecek ay": 10, "yıl sonu": 10
        }

    def _clean_text(self, text: str) -> str:
        """
        2. Metin Temizleme: 
        Hesaplamalarda noktalama işaretleri ya da büyük/küçük harf farkı 
        sorun yaratmasın diye metni temizliyoruz (Örn: 'Acil!' -> 'acil').
        """
        text = re.sub(r'[^\w\s]', '', text.lower())
        return text

    def calculate_ambiguity_score(self, task_sentence: str) -> float:
        """
        3. Belirsizlik Skorunun Hesaplanması
        Mantık: Cümledeki muğlak kelimelerin (U), toplam kelime sayısına (N) oranını hesaplar.
        Formül: (U / N) * 100
        """
        cleaned_text = self._clean_text(task_sentence)
        words = cleaned_text.split()
        if not words:
            return 0.0
            
        N = len(words) # Toplam kelime sayısı
        U = 0          # Cümlede bulunan muğlak kelime sayısı
        
        for ambiguity_word in self.ambiguity_words:
            if ambiguity_word in cleaned_text:
                U += 1
                
        score = (U / N) * 100
        return min(score, 100.0)

    def calculate_urgency_score(self, task_sentence: str, has_date_entity: bool = False) -> float:
        """
        4. Aciliyet Skorunun Hesaplanması
        Mantık: Toplam puan havuzu mantığıyla çalışır. Cümlede yakalanan aciliyet kelimelerinin puanları toplanır.
        
        Parametre Notu (has_date_entity): NLP analizinde (NER) cümlede net bir tarih ('15 Ağustos' vb.) 
        yakalanırsa, bu parametre True olarak gönderilmeli. Skora ekstra +40 puan ekler.
        """
        cleaned_text = self._clean_text(task_sentence)
        total_score = 0
        
        # Sözlükteki kelimeleri cümlede ara, bulursan ağırlığını skora ekle
        for word, weight in self.urgency_words.items():
            if word in cleaned_text:
                total_score += weight
                
        # NLP tarafında tarih bulunmuşsa ekstra puan ekle
        if has_date_entity:
            total_score += 40
            
        return min(total_score, 100.0)

    def calculate_action_density_score(self, task_sentence: str, verb_count: int) -> float:
        """
        5. Aksiyon/Eylem Yoğunluğu Skoru
        Mantık: İyi bir görev cümlesi net fiiller barındırmalıdır. Gönderilen fiil sayısını toplam kelime sayısına böler.
        
        Parametre Notu (verb_count): NLP tarafında (Zemberek/spaCy vb.) 
        bulunan toplam fiil sayısı bu parametre ile gönderilmeli.
        """
        cleaned_text = self._clean_text(task_sentence)
        words = cleaned_text.split()
        if not words:
            return 0.0
            
        N = len(words)
        # Formül: (Fiil Sayısı / Toplam Kelime) * 100
        score = (verb_count / N) * 100
        return min(score, 100.0)

    def get_all_metrics(self, task_sentence: str, has_date_entity: bool = False, verb_count: int = 1) -> Dict[str, float]:
        """
        6. Tek Tuşla Tüm Sonuçları Alma (Ana Metod)
      
        """
        return {
            "ambiguity_score": round(self.calculate_ambiguity_score(task_sentence), 2),
            "urgency_score": round(self.calculate_urgency_score(task_sentence, has_date_entity), 2),
            "action_density_score": round(self.calculate_action_density_score(task_sentence, verb_count), 2)
        }

if __name__ == "__main__":
    # Örnek test kullanımı
    calculator = TaskMetricsCalculator()
    
    test_task = "Yarın Ahmet ile görüşüp onay aldıktan sonra duruma göre raporu acil halletmeye çalış"
    is_date_found = True
    detected_verbs = 3
    
    metrics = calculator.get_all_metrics(test_task, has_date_entity=is_date_found, verb_count=detected_verbs)
    print(f"Görev: '{test_task}'")
    print(f"Metrikler: {metrics}")
