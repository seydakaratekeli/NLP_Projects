# RNN Duygu Dedektifi

IMDB film yorumlari uzerinde egitilmis bir RNN (SimpleRNN) modeli ile metinlerin pozitif veya negatif oldugunu tahmin eden bir duygu analizi projesi.

Bu repo iki temel parcadan olusur:
- `train_rnn_model.py`: IMDB veri seti ile modeli egitir ve `.h5` olarak kaydeder.
- `predict_rnn_review.py`: Egitilmis modeli yukleyip kullanici yorumlari uzerinde tahmin yapar.

## Proje Ozeti

- Problem: Binary text classification (pozitif/negatif)
- Veri seti: Keras IMDB dataset (50.000 yorum)
- Model: Embedding + SimpleRNN + Dense(sigmoid)
- Cikti: 0-1 arasi pozitif olasilik ve etiket

## Klasor Yapisi

```text
.
|-- predict_rnn_review.py
|-- README.md
|-- requirements.txt
|-- rnn_duygu_model.h5
`-- train_rnn_model.py
```

## Kullanilan Teknolojiler

- Python
- TensorFlow / Keras
- NLTK (stopwords)
- NumPy
- Matplotlib

## Kurulum

Asagidaki adimlar Windows PowerShell icin uygundur.

1. Depoyu klonlayin:

```powershell
git clone <repo-url>
cd RNN_duygu_dedektifi
```

2. (Onerilir) Sanal ortam olusturun ve aktif edin:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Bagimliliklari yukleyin:

```powershell
pip install -r requirements.txt
```

Not:
- Ilk calistirmada NLTK `stopwords` ve Keras IMDB dataset internet uzerinden indirilebilir.
- Internet yoksa indirme adimlarinda hata alinabilir.

## Modeli Egitme

Modeli sifirdan egitmek icin:

```powershell
python train_rnn_model.py
```

Egitim sonunda model su dosyaya kaydedilir:
- `rnn_duygu_model.h5`

Kodda tanimli temel hiperparametreler:
- `max_features = 10000`
- `maxlen = 500`
- `Embedding(output_dim=32)`
- `SimpleRNN(units=32)`
- `epochs = 2`
- `batch_size = 64`

## Tahmin Alma

Egitilmis model ile yorum tahmini yapmak icin:

```powershell
python predict_rnn_review.py
```

Program sizden bir film yorumu ister, sonra su bilgileri verir:
- Pozitif tahmin olasiligi (`0.0000 - 1.0000`)
- Nihai etiket (`Pozitif` veya `Negatif`)

Ornek:

```text
bir film yorumu girin : this movie was amazing and emotional
Pozitif Tahmin olasiligi: 0.9132
Pozitif
```

## On Isleme Yaklasimi

Her iki scriptte de benzer bir metin on isleme uygulanir:
- IMDB kelime indeks sozlugu kullanilir
- Metinler temizlenir (harf olmayanlar ayiklanir)
- Stopwords cikartilir
- Bilinmeyen kelimeler `<UNK>` indexine map edilir
- `pad_sequences` ile sabit uzunluga (`maxlen=500`) getirilir

Bu, modelin egitim ve tahmin sirasinda tutarli girdi bicimi gormesini saglar.


## Sik Karsilasilan Sorunlar

1. `ModuleNotFoundError` hatalari:
- Cozum: Sanal ortamin aktif oldugundan emin olun ve `pip install -r requirements.txt` komutunu tekrar calistirin.

2. Dataset/stopwords indirme hatasi:
- Cozum: Internet baglantisini kontrol edin, daha sonra komutu tekrar calistirin.

3. TensorFlow kurulum/surum sorunlari:
- Cozum: Python surumunuzun TensorFlow ile uyumlu oldugunu kontrol edin.

## Gelistirme Fikirleri

- SimpleRNN yerine LSTM/GRU denemek
- Dropout ve EarlyStopping ile overfitting azaltmak
- Farkli maxlen ve vocab boyutu denemeleri
- Sonuclarin confusion matrix ile detayli analizi
- Bir web arayuzu (Flask/FastAPI/Streamlit) eklemek


