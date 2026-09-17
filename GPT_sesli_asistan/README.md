# GPT Sesli Asistan 🎙️🤖

Bu proje, OpenAI'nin **Whisper** ve **GPT-3.5 Turbo** modellerini kullanarak geliştirilmiş yapay zeka destekli, sesten metne (speech-to-text) ve karşılıklı sohbet özelliklerine sahip bir sesli asistandır.

Kullanıcı mikrofonu aracılığıyla asistanla konuşur, asistan sesi metne çevirir, olası zararlı kelimeleri dinamik bir JSON dosyası üzerinden filtreler ve OpenAI API'si üzerinden yapay zeka destekli yanıtlar üretir.

## 🚀 Özellikler

- **Sesli Etkileşim:** Mikrofondan ses kaydı alarak doğrudan asistan ile konuşma imkanı.
- **Sesten Metne (Speech-to-Text):** OpenAI Whisper modeli ile yüksek doğruluk oranına sahip ses tanıma ve yazıya çevirme.
- **Akıllı Sohbet:** OpenAI GPT-3.5 Turbo dil modeli kullanılarak anlamlı ve bağlama uygun cevaplar üretilmesi.
- **Dinamik Zararlı Kelime Filtresi:** Düzenli ifadeler (Regex) ve `banned_words.json` dosyası kullanılarak küfür veya zararlı kelimelerin anında tespit edilip sansürlenmesi (örn: `****`).
- **Gelişmiş Loglama:** Uygulama içindeki tüm sohbet geçmişi ve hatalar `logs/` klasörü altına tarih damgasıyla detaylı olarak kaydedilir.
- **Sesli Çıkış Komutu:** Asistanla olan konuşmayı bitirmek için sadece "çık" demeniz yeterlidir.

## 🛠️ Kullanılan Teknolojiler

- **[Python](https://www.python.org/)**
- **[OpenAI API](https://platform.openai.com/)** (Whisper-1 & GPT-3.5-turbo)
- **[SoundDevice](https://python-sounddevice.readthedocs.io/) & SciPy:** Ses kaydetme ve `.wav` formatında işleme.
- **[python-dotenv](https://pypi.org/project/python-dotenv/):** Çevresel değişkenleri (`.env`) güvenli bir şekilde yönetme.

## ⚙️ Kurulum

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

1. **Depoyu Klonlayın:**
   ```bash
   git clone https://github.com/seydakaratekeli/NLP_Projects/GPT_sesli_asistan.git
   cd gpt-sesli-asistan
   ```

2. **Gerekli Kütüphaneleri Yükleyin:**
    `requirements.txt` dosyası ile bağımlılıkları doğrudan kurabilirsiniz:
   ```bash
   pip install -r requirements.txt
   ```
   *(Not: Eğer requirements dosyasına ulaşamazsanız şu komutla paketleri indirebilirsiniz: `pip install openai sounddevice scipy python-dotenv`)*

3. **API Anahtarını Ayarlayın:**
   Proje dizininde bir `.env` dosyası oluşturun ve OpenAI API anahtarınızı ekleyin:
   ```env
   OPENAI_API_KEY="sk-proj-sizin-api-anahtariniz"
   ```

4. **Yasaklı Kelimeleri Yapılandırın (Opsiyonel):**
   Filtrelenmesini istediğiniz zararlı kelimeleri `banned_words.json` dosyasına ekleyebilirsiniz.

## 🖥️ Kullanım

Uygulamayı başlatmak için terminal veya komut satırında aşağıdaki komutu çalıştırın:

```bash
python gpt_voice_chat.py
```

- Program çalıştığında otomatik olarak mikrofonunuzdan ses kaydı almaya başlar.
- Konuştuğunuz cümle yazıya dökülür ve terminalde/loglarda gösterilir.
- Yapay zeka size uygun bir cevap üretir ve bu cevap ekrana yazılır.
- Sistem bu döngüyü, siz **"Çık"** kelimesini barındıran bir cümle kurana kadar sonsuz döngüde devam ettirir.

## 📝 Güvenlik ve Gizlilik
Bu depo `.gitignore` ile yapılandırılmıştır. 


