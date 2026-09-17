# RAG Sözleşme Avukatı (Contract Lawyer AI) ⚖️🤖

Bu proje, **RAG (Retrieval-Augmented Generation)** teknolojisini kullanarak tasarlanmış bir "Sözleşme Asistanı"dır. Kullanıcıların yüklediği sözleşme belgelerini (PDF vb.) analiz eder, verileri anlamlı parçalara (chunk) böler, vektörel uzayda saklar ve doğal dil ile sorulan sorulara OpenAI API üzerinden akıllı yanıtlar verir.

## 🎯 Projenin Amacı
Uzun ve karmaşık sözleşme metinleri içerisinde manuel olarak bilgi aramak yerine;
1. Belgeden metin çıkarımı yapmak.
2. Bu metinleri bağlamsal olarak anlamlı küçük parçalara bölmek.
3. Bu parçaları **Sentence Transformers** kullanarak vektör veritabanında (**Faiss**) saklamak.
4. Kullanıcı sorularını alıp veritabanındaki en alakalı metin parçalarını bularak **GPT-3.5** aracılığıyla doğru, net ve bağlama uygun cevaplar üretmek.

## 🛠️ Kullanılan Teknolojiler
- **Python**: Temel programlama dili.
- **PyMuPDF**: PDF belgelerinden metin çıkarma.
- **Sentence Transformers (`all-MiniLM-L6-v2`)**: Metinleri vektörel temsillere (embedding) dönüştürme.
- **Faiss**: Yüksek performanslı vektör araması ve veritabanı yönetimi.
- **OpenAI API (GPT-3.5-turbo)**: İlgili bağlamı (context) yorumlayarak doğal dilde cevap üretme.
- **NumPy & Pickle**: Vektör işlemleri ve veri serileştirme.
- **Dotenv**: Güvenli ortam değişkenleri ve API anahtarı yönetimi.

## ⚙️ Kurulum (Installation)

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyebilirsiniz.

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/seydakaratekeli/NLP_Projects/RAG_sozlesme_avukati.git
cd RAG_sozlesme_avukati
```

### 2. Sanal Ortam Oluşturun (Opsiyonel ama Önerilir)
```bash
python -m venv venv
# Windows için
venv\Scripts\activate
# MacOS/Linux için
source venv/bin/activate
```

### 3. Gerekli Kütüphaneleri Yükleyin
```bash
pip install -r requirements.txt
```

### 4. `.env` Dosyası Oluşturun
Proje ana dizininde bir `.env` dosyası oluşturun ve OpenAI API anahtarınızı ekleyin:
```env
OPENAI_API_KEY=sk-sizin-api-anahtariniz-buraya
```

## 🚀 Kullanım (Usage)

Proje temel olarak iki adımdan oluşmaktadır:

### Adım 1: Vektör Veritabanının Oluşturulması
Öncelikle `data/` klasörünün içerisindeki sözleşme PDF'ini okutup veritabanını oluşturmanız gerekmektedir.
```bash
python build_vector_db.py
```
*Bu işlem sonucunda `data` klasörü altında `contract_index.faiss` ve `contract_chunks.pkl` dosyaları oluşacaktır.*

### Adım 2: Soru - Cevap Sisteminin Başlatılması
Veritabanı oluşturulduktan sonra sözleşme asistanına soru sormak için aşağıdaki dosyayı çalıştırın:
```bash
python ask_question.py
```
Program çalıştığında konsol üzerinden İngilizce (veya ayarlanan modele göre Türkçe) sorularınızı yöneltebilirsiniz:
```text
Sorunuzu giriniz: (Eng) What is the total fee mentioned in the contract?
AI Assistant: 
The total fee mentioned in the contract is $10,000.
```
*Çıkmak için `q`, `quit` veya `exit` yazabilirsiniz.*

## Terminal Ekran görüntüsü 

<img width="1231" height="588" alt="image" src="https://github.com/user-attachments/assets/e17db5bc-cff7-42c4-a370-be5505bcda8d" />



## 📂 Proje Yapısı

```text
RAG_sozlesme_avukati/
│
├── data/
│   ├── sample_contract_ucanble.pdf   # Örnek Sözleşme dosyası
│   ├── contract_chunks.pkl           # (Otomatik) Bölünmüş metin parçaları
│   └── contract_index.faiss          # (Otomatik) Vektör veritabanı
│
├── build_vector_db.py                # Veritabanı oluşturma ve embedding scripti
├── ask_question.py                   # Soru sorma ve GPT cevaplama scripti
├── requirements.txt                  # Proje bağımlılıkları
├── .env                              # Ortam değişkenleri (API anahtarları vb.)
└── README.md                         # Proje açıklama dosyası
```

