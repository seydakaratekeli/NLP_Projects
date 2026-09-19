# AI Yatırım Uzmanı Ajanı 📈🤖

Yapay zeka destekli, doğal dil işleme tabanlı kişisel yatırım asistanı. Kullanıcıların doğal dilde sorduğu soruları anlar, gerekli durumlarda canlı verilere ulaşır, kur çevirisi yapar ve web üzerinden güncel haberleri araştırarak kapsamlı, tarafsız ve profesyonel yanıtlar üretir.

## Özellikler ✨

- **Doğal Dil Anlayışı:** Karmaşık yatırım ve finans sorularını algılar.
- **Canlı Hisse Senedi Verileri:** Finnhub API entegrasyonu ile (örneğin AAPL, TSLA) güncel hisse senedi fiyatlarını alır.
- **Canlı Kur Çevirisi:** CoinGecko API aracılığıyla ücretsiz ve anlık döviz çevirisi (USD -> TRY vb.) yapar.
- **Güncel Haber ve Analiz Taraması:** DuckDuckGo aracıyla finans dünyasındaki son dakika gelişmelerini (örneğin "altın fiyatları", "kripto analizleri") araştırır.
- **Gelişmiş AI Analizi:** Topladığı tüm bu verileri LangChain ve OpenAI (`gpt-3.5-turbo`) altyapısı kullanarak özetler ve profesyonel, tavsiye içermeyen bir dille kullanıcıya sunar.

## Kullanılan Teknolojiler 🛠️

- **Python 3.x**
- **LangChain:** Agent, Tools ve LLM orkestrasyonu.
- **OpenAI:** GPT-3.5-Turbo dil modeli.
- **Finnhub API:** Hisse senedi piyasa verileri.
- **CoinGecko API:** Kripto para ve kur verileri (Ücretsiz, anahtar gerektirmez).
- **DuckDuckGo Search:** Güncel veri ve haber araması.

## Kurulum ve Çalıştırma 🚀

Projenizi yerel ortamda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

1. **Depoyu Klonlayın:**
   ```bash
   git clone https://github.com/seydakaratekeli/NLP_Projects/AI_Agent_yatirim_uzmani.git
   cd AI_Agent_yatirim_uzmani
   ```

2. **Sanal Ortam (Virtual Environment) Oluşturun ve Aktif Edin:**
   ```bash
   python -m venv venv
   # Windows için:
   venv\Scripts\activate
   # macOS/Linux için:
   source venv/bin/activate
   ```

3. **Gerekli Kütüphaneleri Yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Çevre Değişkenlerini Ayarlayın:**
   Proje ana dizininde `.env` adında bir dosya oluşturun ve içerisine gerekli API anahtarlarınızı ekleyin:
   ```env
   OPENAI_API_KEY=sizin_openai_api_anahtariniz
   FINNHUB_API_KEY=sizin_finnhub_api_anahtariniz
   ```

5. **Ajanı Çalıştırın:**
   ```bash
   python agent_main.py
   ```

## Örnek Kullanım 💬

Ajanı çalıştırdıktan sonra terminal üzerinden sorularınızı sorabilirsiniz:

- *"Apple hissesi ne kadar?"*
- *"Dolar bugün kaç TL?"*
- *"Altın hakkında son haberler nedir?"*
- *"Tesla hissesi mi Apple hissesi mi daha karlı görünüyor?"*

Programdan çıkmak için `q` yazabilirsiniz.

## Gelecek Planları (Roadmap) 🗺️

- Bellek (Memory) eklenerek sohbet bağlamının hatırlanması.
- Streamlit veya FastAPI kullanılarak web/API tabanlı modern bir arayüz geliştirilmesi.
- *Plan and Execute* stratejisi ile karmaşık araştırma süreçlerinin daha optimize yürütülmesi.
- Retrieval-Augmented Generation (RAG) sistemi ile özel belgelere dayalı analiz yapma yeteneğinin kazandırılması.
