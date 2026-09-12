"""
Problem tanimi: yorumlardan -> puan tahmini (1-5), regresyon problemi 
    - cok iyiydi cok memnun kaldim -> 4.5
    - berbatti, bir daha gelmem -> 1.2

Veri seti: yelp dataset, hugging face, (restoran, doktor, otel, araba yikama ...)
    - text: yorum metni
    - label: 0-4 arasinda ama biz bunu 1ile 5 e cekelim.
    - https://huggingface.co/datasets/Yelp/yelp_review_full

LSTM: bir yorumu bastan sona okur, sonrasinda yorumun genel anlamina karsilik gelen yildiz puanini cikarir

install libraries: freeze requirements.txt

Plan/program

import libraries
"""

# import libraries
import pandas as pd #veri yükleme için 
import numpy as np #numeric-sayısal işlemler için 
import matplotlib.pyplot as plt #görselleştirme için
import pickle # tokenizer'i diske kaydetmek icin kullanicaz

from sklearn.model_selection import train_test_split # veriyi egitim ve test olmak uzere 2 ye ayir
from sklearn.preprocessing import MinMaxScaler # normalization

from tensorflow.keras.preprocessing.text import Tokenizer # tokenization
from tensorflow.keras.preprocessing.sequence import pad_sequences # padding
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense 
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import MeanAbsoluteError # 5 -> 4 = 1, 4 -> 5 = 1

# load yelp dataset
# hugging face den yelp veri setini yukleme
splits = {"train": "yelp_review_full/train-00000-of-00001.parquet"}
train_path = "hf://datasets/Yelp/yelp_review_full/" + splits["train"]

# parquet formatindan veriyi pandas ile oku
df = pd.read_parquet(train_path)
print(df.head())

#veri setimizn içinde bulunan yorumların puanlarını değiştirdik 
# etiketleri 0-4 araligindan 1-5 araligina donustur
df["label"] = df["label"] + 1

# data preprocessing
texts = df["text"].values # yorum metinleri
labels = df["label"].values # puanlar 1-5 arasinda

# tokenizer: metni sayiya cevir
# num_words: en cok gecen ilk 10000 kelime
# OOV: bilinmeyen kelimeleri bu etiketle goster- kendimiz tokenzer oluşturduk
tokenizer = Tokenizer(num_words = 10000, oov_token = "<OOV>")

# metni sayilara donustur
tokenizer.fit_on_texts(texts)

#diske kaydetmemiz gerekiyor çünkü modelimizi kaydettikten sonra tekrar kullanmak istiyoruz, tokenizeri tekrar olusturmak istemiyoruz
#diğer dosyada dışarıdan gelen yorumları puanlamak için  metni sayılara çevirmek için tokenizeri kullanacağız, bu yüzden tokenizeri diske kaydetmemiz gerekiyor
# tokenizeri diske kaydet
with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

# yorumlari dizi haline getir
sequences = tokenizer.texts_to_sequences(texts)

# tum dizileri sabit uunluga getir yani padding uygula (kisa olnlari 0 ile doldur)
padded_sequences = pad_sequences(sequences, maxlen = 100, padding = "post", truncating = "post")

# şu an etiketler 1 ile 5 arasinda, normalization ile 0 iel 1 arasina alalim, cunku regresyon problemlerinde daha stabil bir ogrenme sagliyor
scaler = MinMaxScaler() # 1-5 - 1 = 0-4 sonra /4 = 0-1
labels_scaled = scaler.fit_transform(labels.reshape(-1, 1))

# egitim ve test verisini ayir
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels_scaled, test_size=0.2, random_state=42) #burada random_state=42 kullanmamizin sebebi, her seferinde ayni sekilde ayirmak icin, yoksa her calistirdigimizda farkli bir bolme yapar ve modelin performansi degisir ve test_size=0.2 -> %20 test verisi, %80 egitim verisi
print(f"X_train shape: {X_train.shape}") #burada şunu gösteriyor: 560000 yorum var, her bir yorum 100 kelime uzunlugunda olacak sekilde padding yapildi, yani 560000 x 100 boyutunda bir matris olustu
print(f"X_train: {X_train[:2]}") #burada ilk iki yorumun sayisal karsiliklarini gosteriyor, yani kelimeler sayilara donusturuldu ve padding yapildi
print(f"y_train shape: {y_train.shape}") #burada 560000 yorum var, her bir yorumun puani 1-5 arasinda, normalization ile 0-1 arasina alindi, yani 560000 x 1 boyutunda bir matris olustu
print(f"y_train: {y_train[:2]}") #burada ilk iki yorumun puanlarini gosteriyor, yani 1-5 arasinda olan puanlar normalization ile 0-1 arasina alindi

# LSTM tabanli regresyon modeli
model = Sequential()

#embedding yaptıktan sonra her bir kelime vektör uzayında 128 boyutlu bir vektörle temsil edilecek, LSTM katmanı bu vektörleri kullanarak yorumun genel anlamını öğrenmeye çalışacak.
# embedding katmani: kelime indekslerini vektor uzayina donusturur
# input_dim: 10000 -> kelime sayisi
# output_dim: 128 -> her bir kelime 128 boyutlu vektorle temsil edilecek
# input_length: 100 -> sabit dizi uzunlugu yani her bir metnimizin uzunlugu 
model.add(Embedding(input_dim = 10000, output_dim = 128, input_length = 100))

# LSTM katmani: sirali veride baglami ogrenecek olan katman
model.add(LSTM(128)) # 128: lstm de bulunan hucre sayisi yani daha fazla ogrenme kapasitesi

# tam bagli (dense) layer
model.add(Dense(64, activation = "relu"))

# output layer
model.add(Dense(1, activation = "linear")) # (relu, tanh genelde tam bağlı katmanlarda), (sigmoid-2sınıflı, softmax-çoksınıflı sınıflandırma için), linear -regresyonda

# model compile and training
model.compile(
    optimizer = "adam", # adaptif ogrenme algoritmasi
    loss = MeanSquaredError(), # mean squared error: regresyon icin uygun bir loss fonksiyonu
    metrics = [MeanAbsoluteError()] # modelin hata ortalamasi
    # burada seçilen metrikler loos fonksiyonlarında en çok kullanılan fonksiyonlar (MeanSquaredError, RootMeanSquaredError, R2Score) regresyon problemleri için uygun metriklerdir. MeanSquaredError ve MeanAbsoluteError en yaygın olarak kullanılan metriklerdir. MeanSquaredError, hataların karesini alarak büyük hataları daha fazla cezalandırır. MeanAbsoluteError ise hataların mutlak değerini alır ve daha az duyarlıdır. RootMeanSquaredError ise MeanSquaredError'un karekökünü alır ve aynı birimlerde sonuç verir. R2Score ise modelin açıklayıcılık oranını gösterir ve 1'e yakın olması iyi bir model olduğunu gösterir.
    # metrik olarak kullandığımızda skora ne kadar yakın olduğumuzu anlayamıyoruz AbsoluteError kullandığımmızda ise daha kolay anlıyoruz örn: AbsoluteError 1 ise 3 tahmin etmem gerekiyorsa 1 eksiği 2 veya 1 fazlası 4 tahmin ediyormuşum demek yorumlaması kolay bu nedenle bu metrikleri kullanıyoruz
)

history = model.fit(
    X_train, y_train,
    epochs = 3, # toplam egitim dongusu eğer 3 epoch yaparsak modelimiz 3 defa tum egitim verisini gormus olacak yetmezse epoch sayisini arttirabiliriz
    batch_size = 64, # her adimda islenecek ornek sayisi
    validation_split = 0.2 # egitim verisinin %20 si validasyon icin ayrilir 
    )


# egitim kayip grafigini gorsellestir ve modeli kaydet
plt.plot(history.history["loss"], label= "Training Loss")
plt.plot(history.history["val_loss"], label = "Validation Loss")
plt.title("Egitim sureci MSE")
plt.xlabel("Epoch")
plt.ylabel("Loss MSE")
plt.show()

# modeli kaydet
model.save("regression_lstm_yelp.h5")