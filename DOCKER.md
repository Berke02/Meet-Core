# Meet-Core Yerel Docker Kurulumu

Bu doküman, Meet-Core uygulamasının Docker Compose ile yerel geliştirme ortamında çalıştırılmasını açıklar.

Uygulama iki servisten oluşur:

- **backend:** FastAPI tabanlı analiz servisi
- **frontend:** Streamlit tabanlı kullanıcı arayüzü

## Gereksinimler

- Docker Desktop veya Docker Engine
- Docker Compose v2
- Gemini API anahtarı
- Ses analizi kullanılacaksa Hugging Face erişim tokenı

## Ortam değişkenleri

Proje kökündeki Compose ayarları hazırlanır:

```powershell
Copy-Item .env.example .env
```

Kök `.env` dosyasında portlar ve ses bağımlılıklarının kurulup kurulmayacağı belirlenir:

```dotenv
BACKEND_PORT=8000
FRONTEND_PORT=8501
INSTALL_AUDIO=true
```

Yalnızca metin ve doküman analizi için daha hafif bir imaj oluşturmak üzere `INSTALL_AUDIO=false` kullanılabilir.

Backend uygulama ayarları hazırlanır:

```powershell
Copy-Item backend/.env.example backend/.env
```

`backend/.env` dosyasında en az `GEMINI_API_KEY` tanımlanmalıdır. Konuşmacı ayrıştırma kullanılacaksa `HF_TOKEN` da eklenmelidir.

## Servislerin başlatılması

Proje kök dizininde aşağıdaki komut çalıştırılır:

```powershell
docker compose up -d --build
```

Servisler başladıktan sonra aşağıdaki adresler kullanılabilir:

- Frontend: `http://localhost:8501`
- Backend sağlık kontrolü: `http://localhost:8000/health`
- API dokümantasyonu: `http://localhost:8000/docs`

## Durum ve log kontrolü

```powershell
docker compose ps
docker compose logs -f backend
docker compose logs -f frontend
```

## Servislerin durdurulması

```powershell
docker compose down
```

## Ses analizi notu

Ses analizi etkinleştirildiğinde WhisperX ve Pyannote bağımlılıkları backend imajına eklenir. Bu nedenle imaj boyutu ve ilk kurulum süresi artabilir.