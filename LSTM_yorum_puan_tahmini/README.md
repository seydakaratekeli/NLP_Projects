# LSTM Yorum Puan Tahmini

Bu proje, restoran, doktor, otel ve benzeri hizmetler hakkindaki yorumlardan 1-5 arasinda puan tahmini yapmak icin LSTM tabanli bir regresyon modeli kullanir.

## Proje Akisi

1. Yelp Review Full veri seti Hugging Face uzerinden yuklenir.
2. Yorum metinleri tokenize edilir ve 100 kelimelik dizilere donusturulur.
3. Puanlar normalize edilerek model egitilir.
4. Egitilen model ve tokenizer diske kaydedilir.
5. Ornek yorumlar icin tahmini puanlar uretilir.

## Dosyalar

- `lstm_regression.py`: Veri setini yukler, LSTM modelini egitir ve model ciktilarini kaydeder.
- `predict_review.py`: Kaydedilen model ile yorum puani tahmini yapar.
- `requirements.txt`: Python bagimliliklarini listeler.
- `.gitignore`: Sanal ortam, model ciktilari ve gecici dosyalarin Git'e eklenmesini engeller.

## Kurulum

Python 3.10 veya daha yeni bir surum onerilir.

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Linux/macOS:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Modeli Egitme

Proje klasorunde asagidaki komutu calistirin:

```bash
python lstm_regression.py
```

Ilk calistirmada Yelp veri seti Hugging Face'ten indirilir. Egitim tamamlandiginda su dosyalar olusturulur:

- `regression_lstm_yelp.h5`: Egitilmis LSTM modeli
- `tokenizer.pkl`: Metin tokenizer'i

Egitim grafigi ekranda gosterilir.

## Tahmin Yapma

Model egitildikten sonra:

```bash
python predict_review.py
```

Tahmin betigi icindeki `texts` listesine kendi yorumlarinizi ekleyerek farkli metinler icin puan tahmini alabilirsiniz.

## Model Mimarisi

- Embedding: 10.000 kelimelik sozluk, 128 boyutlu vektorler
- LSTM: 128 hucre
- Dense: 64 noron, ReLU aktivasyonu
- Cikis: 1 noron, lineer aktivasyon
- Loss: Mean Squared Error
- Metrik: Mean Absolute Error

## Notlar

- Veri setindeki etiketler 0-4 araligindan 1-5 araligina donusturulur.
- Yorumlar en fazla 100 token olacak sekilde kesilir; daha kisa yorumlar sifirlarla doldurulur.
- Model ve tokenizer dosyalari `.gitignore` ile Git takibinin disinda tutulur.
- `predict_review.py` calistirilmadan once model egitiminin tamamlanmis olmasi gerekir.
