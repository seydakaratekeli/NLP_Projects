# 🧭 AI Agent Kariyer Planlayıcısı

> **LangChain + GPT-4 destekli, kişiselleştirilmiş kariyer yol haritası üreten çok ajanlı bir NLP sistemi.**

---

## 🏗️ Sistem Mimarisi (Architecture Diagram)

```
┌─────────────────────────────────────────────────────────────────────┐
│                          KULLANICI (Terminal)                        │
│                    "Hedef mesleğim: Yapay Zeka Mühendisi"           │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           main.py  (Orkestratör)                     │
│    Bileşenleri başlatır, kullanıcı girdisini alır ve akışı yönetir  │
└───────┬─────────────────────┬──────────────────────┬────────────────┘
        │                     │                      │
        ▼                     ▼                      ▼
┌───────────────┐   ┌──────────────────┐   ┌─────────────────────┐
│  UserMemory   │   │ CareerGoalAgent  │   │  SuggestionTool     │
│ (memory.json) │   │  (LangChain +    │   │  (DuckDuckGo DDGS)  │
│               │   │    GPT-4 API)    │   │                     │
│ • Hedef kayıt │   │ • Prompt üret    │   │ • Web araması yapar │
│ • İlerleme    │   │ • JSON yol       │   │ • Kurs/makale/video │
│   takibi      │   │   haritası döndür│   │   önerileri döndür  │
└───────────────┘   └────────┬─────────┘   └─────────────────────┘
                             │
                             ▼
                   ┌──────────────────┐
                   │TaskSchedulerAgent│
                   │                  │
                   │ • Adımları hafta │
                   │   lara böler     │
                   │ • Tarih atar     │
                   │ • schedule.json  │
                   │   olarak kaydeder│
                   └──────────────────┘
```

**Veri Akışı:**
`Kullanıcı Girdisi` → `CareerGoalAgent (GPT-4)` → `JSON Adımlar` → `TaskSchedulerAgent` → `Haftalık Plan` + `Kaynak Önerileri`

---

## 🎯 Ne İşe Yarar?

Kariyer Planlayıcısı; kullanıcının terminal üzerinden belirttiği **hedef mesleğe** göre:

| Özellik | Açıklama |
|---|---|
| 📋 **Yol Haritası** | GPT-4 ile hedefe özel adım adım kariyer planı oluşturur |
| 📅 **Haftalık Program** | Görevleri haftalara böler ve başlangıç tarihleri atar |
| 🔍 **Kaynak Önerisi** | DuckDuckGo aracılığıyla kurs, makale ve video önerileri sunar |
| 💾 **Hafıza Sistemi** | Kullanıcının hedefini ve ilerleme durumunu JSON'da kalıcı olarak saklar |

---

## 🔍 Hangi Problemi Çözüyor?

Çoğu insan kariyer değiştirmek veya yeni bir alana girmek istediğinde **"Nereden başlamalıyım?"** sorusuyla karşılaşır. Bu sorunun cevabı kişiden kişiye çok farklıdır ve tek bir kaynaktan kapsamlı, yapılandırılmış ve takip edilebilir bir plan bulmak zordur.

Bu proje üç temel problemi çözer:
1. **Kişiselleştirme eksikliği** — Her kullanıcıya özel dinamik plan üretilir.
2. **Dağınık bilgi** — Kariyer adımları + takvim + kaynaklar tek akışta sunulur.
3. **Takip edilemezlik** — Hafıza sistemi ile ilerleme JSON'da saklanır, sonraki oturumda devam edilebilir.

---

## ⚙️ Nasıl Çalışır?

### Adım Adım Akış

```
1. Kullanıcı hedef mesleğini girer
        ↓
2. UserMemory hedefi memory.json'a kaydeder
        ↓
3. CareerGoalAgent, GPT-4'e system+human prompt gönderir
        ↓
4. GPT-4, {"adimlar": [...]} formatında JSON yol haritası döndürür
        ↓
5. TaskSchedulerAgent adımları N haftalık plana dönüştürür
   ve schedule.json'a kaydeder
        ↓
6. Kullanıcı bir beceri başlığı girer
        ↓
7. SuggestionTool, DuckDuckGo'da arama yaparak
   başlık + link + özet üçlüsünü döndürür
```

### Dosya Yapısı

```
AI_Agent_kariyer_planlayicisi/
│
├── main.py                     # Ana orkestratör — tüm akışı yönetir
│
├── agents/
│   ├── career_goal_agent.py    # GPT-4 ile kariyer yol haritası üretir
│   └── task_scheduler_agent.py # Yol haritasını haftalık takvime çevirir
│
├── tools/
│   └── suggestion_tool.py      # DuckDuckGo ile kaynak araması yapar
│
├── memory/
│   └── user_memory.py          # Hedef ve ilerleme bilgisini JSON'da saklar
│
├── memory.json                 # Kullanıcı hafıza dosyası (runtime, gitignore'd)
├── schedule.json               # Haftalık plan çıktısı (runtime, gitignore'd)
├── requirements.txt            # Tüm Python bağımlılıkları
└── .env                        # API anahtarları (gitignore'd, asla commit etme!)
```

---

## 🛠️ Kullanılan Teknolojiler & Seçilme Nedenleri

| Teknoloji | Versiyon | Neden Seçildi? |
|---|---|---|
| **Python** | 3.10+ | Hızlı prototipleme; NLP/AI ekosisteminin merkezi |
| **LangChain** | 1.4.x | LLM çağrılarını soyutlar; SystemMessage/HumanMessage ile temiz prompt yönetimi sağlar |
| **OpenAI GPT-4** | `gpt-4` | Türkçe'de yüksek kaliteli, yapılandırılmış JSON çıktısı üretebilen en güvenilir LLM |
| **DDGS (DuckDuckGo)** | 9.x | API key gerektirmez; gizlilik odaklı; ücretsiz web araması imkânı sunar |
| **python-dotenv** | 1.x | `.env` dosyasından API anahtarlarını güvenli şekilde yükler, hardcode'u önler |
| **JSON (stdlib)** | — | Hafıza ve takvim verisi için hafif, okunabilir, portatif depolama formatı |

---

## 🚀 Kurulum

### Ön Koşullar
- Python 3.10 veya üzeri
- Aktif bir [OpenAI API anahtarı](https://platform.openai.com/api-keys)

### 1. Repoyu Klonla

```bash
git clone https://github.com/seydakaratekeli/NLP_Projects.git
cd NLP_Projects/AI_Agent_kariyer_planlayicisi
```

### 2. Sanal Ortam Oluştur ve Aktifleştir

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### 4. Ortam Değişkenlerini Ayarla

`.env` adında bir dosya oluştur ve içine ekle:

```env
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
```


### 5. Uygulamayı Çalıştır

```bash
python main.py
```

### Beklenen Çıktı

```
Kariyer Planlayıcısı
Hedef mesleğiniz nedir? > Makine Öğrenmesi Mühendisi

Yol Haritanız:
{
  "adimlar": [
    "Python ve matematik temellerini pekiştir",
    "Scikit-learn ile ML algoritmalarını öğren",
    ...
  ]
}

 4 Haftalık Plan:
{
  "Hafta 1": [{"gorev": "...", "baslangic": "2026-09-22"}],
  ...
}

Bir beceri başlığı girin (kaynak önerisi için) > machine learning course

Kaynak Önerileri:
 - Coursera Machine Learning Specialization
   https://coursera.org/...
   Andrew Ng tarafından sunulan...

## Terminal Ekran Görüntüsü

<img width="808" height="890" alt="image" src="https://github.com/user-attachments/assets/0c1b2487-4f7d-425b-946c-4cec1bd090d8" />

<img width="993" height="560" alt="image" src="https://github.com/user-attachments/assets/9f7abe38-a313-4cdf-adf4-797de61b2961" />


## 📦 Bağımlılıklar (Özet)

```
langchain==1.4.2
langchain-openai==1.6.3
langchain-community==0.4.2
openai==3.17.0
ddgs==9.16.0
python-dotenv==1.2.3
```

> Tüm bağımlılıklar için [`requirements.txt`](./requirements.txt) dosyasına bakın.

---

## 🔮 Gelecek Geliştirmeler

- [ ] İlerleme takibi için interaktif CLI ekranı
- [ ] Çoklu kullanıcı profili desteği
- [ ] Web arayüzü (Streamlit veya Gradio)
- [ ] Daha fazla kaynak kaynağı (YouTube API, Udemy API)
- [ ] LangGraph ile çok-tur konuşma akışı

---

---

*NLP_Projects koleksiyonunun bir parçası — [@seydakaratekeli](https://github.com/seydakaratekeli)*
