# Gemini Akıllı Asistan 🤖

Google DeepMind'ın güçlü **Gemini API'sini (gemini-3.6-flash)** kullanan, doğal dildeki komutlarınızı anlayabilen, kişisel notlarınızı ve etkinliklerinizi yönetebileceğiniz terminal tabanlı akıllı bir yapay zeka asistanıdır.

## 🚀 Özellikler

- **Niyet Algılama (Intent Detection):** Serbest metinle yazdığınız mesajın sohbet mi, not özeti talebi mi yoksa etkinlik özeti talebi mi olduğunu otomatik olarak anlar.
- **Kişisel Not Yönetimi:** Hızlıca notlar ekleyebilir, kayıtlı notlarınızı listeleyebilirsiniz.
- **Takvim ve Etkinlik Yönetimi:** Gelecekteki etkinliklerinizi ve toplantılarınızı tarihleriyle birlikte kaydedebilirsiniz.
- **Yapay Zeka Destekli Özetleme:** Kaydettiğiniz tüm notları veya yaklaşan etkinlikleri yapay zekaya yorumlatabilir ve özetletebilirsiniz.
- **Esnek Sohbet:** Belirli bir komut olmadan, genel konularda Gemini yapay zekası ile sohbet edebilirsiniz.
- **Hata Yönetimi (Retry Mekanizması):** Sunucu yoğunluğuna (503 Service Unavailable) karşı otomatik tekrar deneme mekanizmasına sahiptir.

## 🛠️ Kullanılan Teknolojiler

- **Python 3.x**
- **SQLite3** (Yerel Veritabanı)
- **Google Gemini API**
- **dotenv** (Çevresel değişken yönetimi)
- **requests** (HTTP istekleri)

## 📦 Kurulum

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

1. **Projeyi indirin (Klonlayın):**
   ```bash
   git clone https://github.com/seydakaratekeli/Gemini_akilli_asistan.git
   cd Gemini_akilli_asistan
   ```

2. **Gerekli Kütüphaneleri Yükleyin:**
   Eğer kullanıyorsanız sanal ortamınızı (virtual environment) aktif edin, ardından `requirements.txt` dosyasındaki kütüphaneleri kurun:
   ```bash
   pip install -r requirements.txt
   ```

3. **API Anahtarını Yapılandırın:**
   Ana dizinde `.env` adında bir dosya oluşturun ve Google AI Studio'dan aldığınız Gemini API anahtarınızı içine ekleyin. Veritabanı yolunu da belirtebilirsiniz:
   ```env
   GEMINI_API_KEY = "Sizin-Api-Anahtariniz-Buraya"
   DB_PATH = "data/assistant.db"
   ```

## 🎮 Kullanım

Uygulamayı başlatmak için terminalde aşağıdaki komutu çalıştırın:
```bash
python main.py
```

### Desteklenen Komutlar
Uygulama açıldığında "Komut girin:" uyarısı ile karşılaşacaksınız. Aşağıdaki komutları kullanabilirsiniz:

- `not ekle` : Sisteme yeni bir not kaydeder.
- `etkinlik ekle` : Sisteme tarihli bir etkinlik/toplantı kaydeder.
- `notları göster` : Veritabanındaki tüm notlarınızı listeler.
- `etkinlikleri göster` : Yaklaşan etkinlikleri listeler.
- `sohbet et` : Yapay zeka ile etkileşime girer. (Örn: "Notlarımı benim için özetle", "Yarınki etkinliklerim neler?", veya "Bana bir fıkra anlat")
- `çıkış` : Asistandan çıkar.

## 📂 Proje Yapısı

- `main.py` : Uygulamanın ana giriş noktasıdır. Menü döngüsünü ve komut yönetimini üstlenir.
- `assistant.py` : Gemini API ile olan tüm iletişimi (istek atma, niyet algılama, hata yönetimi) sağlar.
- `database.py` : Notların ve etkinliklerin tutulduğu SQLite veritabanının (CRUD işlemleri) kodlarını barındırır.
- `data/assistant.db` : Uygulama çalıştığında otomatik olarak oluşan SQLite yerel veritabanı dosyasıdır. (GitHub'a yüklenmez).

## 📝 Notlar
- Proje eğitim amaçlı geliştirilmiş olup yerel olarak (terminal üzerinden) çalışmaktadır. 
- İlerleyen süreçlerde bu projeye bir kullanıcı arayüzü (Arayüz / UI) eklenebilir veya veritabanı yapısı ORM araçlarıyla (SQLAlchemy) büyütülebilir.
