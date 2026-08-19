"""


RNN ile Duygu Dedektifi (Sentiment Analysis)
Problem Tanimi: Bir yorumun olumlu mu olumsuz mu oldugunu anlamak (classification problem)
IMDB film yorumlari veri seti ile bir metnin duygusal analizini gerceklestirme:
- this movie is awesome -> pozitif
- it was terrible movie -> negatif

RNN: Tekrarlayan sinir aglari: sirali veriler uzerinde calisiyor, metin gibi verilerde onceki bilgileri hatirlayarak sonraki
tahminleri yapmaya calisirlar
Girdi: film -> cok -> kotuydu
Bellek:
Cikti: anlam anlam olumsuz

Veri Seti: IMDB veri seti: film yorumlari (olumlu ve olumsuz)
- 50000 adet film yorumu
- 0 negatif, 1 pozitif
- great = 65

plan /program

gerekli kurulumlar

import libraries


"""


# import libraries
import numpy as np
import nltk # natural language tool kit
import matplotlib.pyplot as plt
from nltk.corpus import stopwords # gereksiz kelime listesi
from tensorflow.keras.models import Sequential # base model
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense
from tensorflow.keras.datasets import imdb # veri seti IMDB yorumları gelir
from tensorflow.keras.preprocessing.sequence import pad_sequences

#Keras built-in dataset” kullanıyor. Dolayısıyla veri internet üzerinden veya Keras cache’inden indiriliyor; dosya içinde ayrı bir veri klasörü yok.
#eğitim verisi aslında “IMDB film yorumları + etiketleri” olan hazır bir veri setidir, proje içinde kendisi üretilmiyor.

# stopwords (gereksiz kelimeler) listesi belirle
nltk.download("stopwords") # nltk icinden ingilizce stopwords indriliyor
stop_words = set(stopwords.words("english")) # kucuk ve anlamsiz kelimeler ayiklanacak

# model parametreleri
max_features = 10000 # en cok kullanilan 10 bin kelime
maxlen = 500 # yorumlarin uzunlugu 500 kelime ile sinirli olacak

# load dataset
# imbd yorumları gelirken sayi dizisi olarak gelir. her sayi bir kelimeyi temsil eder. 0 bosluk, 1 cumle baslangici, 2 bilinmeyen kelime
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words = max_features) # train/test ayrilmis sekilde veri gelir

# ornek veri incelemesi
#kelimeler sayıların karşılığına çevrilmek için imdb.get_word_index() fonksiyonu kullanılır. Bu fonksiyon, kelimeleri sayılara dönüştüren bir sözlük döndürür. Örneğin, "great" kelimesi 65 sayısına karşılık gelir. Bu sayede model, metin verilerini sayısal formata dönüştürerek işleyebilir.
original_word_index = imdb.get_word_index()

# sayi kelime donusum sozlugu hazirlama
inv_word_index = {index +3: word for word, index in original_word_index.items()}
inv_word_index[0] = "<PAD>" # 0: bosluk padding
inv_word_index[1] ="<START>" # 1: cumle baslangici
inv_word_index[2] = "<UNK>" # 2: bilinmeyen kelime
# inv_word_index[3] -> great: 65

# sayi dizisini kelimelere ceviren fonksiyon
def decode_review(encoded_review):
    return " ".join([inv_word_index.get(i, "?") for i in encoded_review])


movie_index = 0
# ilk egitim verisini yazdiralim
print("ilk yorum: (sayi dizisi)")
print(X_train[movie_index])

print("ilk yorum: (kelimelerle)")
print(decode_review(X_train[movie_index]))

print(f"Label: {"Pozitif" if y_train[movie_index] == 1 else "Negatif"}")


# gerekli sozluklerin olusturulmasi: word to index ve index to word
word_index = imdb.get_word_index()
#+3 yapıyoruz çünkü ilk 3ü özel karakterler için ayırıyoruz. 0: padding, 1: start, 2: unknown
index_to_word = {index + 3: word for word, index in word_index. items()} # sayilardan kelimereler gecis
index_to_word[0] = "<PAD>"
index_to_word[1] = "<START>"
index_to_word[2] = "<UNK>"
word_to_index = {word: index for index, word in index_to_word.items()} # kelimelerden sayilara gecis


# data preprocessing (veri on isleme)

def preprocess_review(encoded_review):
    # sayilari kelimelere cevir
    words = [index_to_word.get(i, "") for i in encoded_review if i >= 3]

    # sadece harflerden olusan ve stop words olmayanlari al
    cleaned = [
        word.lower() for word in words if word.isalpha() and word.lower() not in stop_words
    ]

    # tekrardan temizlenmis metni sayilara cevir
    return [word_to_index.get(word, 2) for word in cleaned]

# veriyi temizle ve sabit uzunlugu pad et
X_train = [preprocess_review(review) for review in X_train]
X_test = [preprocess_review(review) for review in X_test]

# pad sequence
"""
merhaba bugun hava cok guzel
merhaba, naber, 0, 0, 0
"""
#bütün yorumlar aynı uzunlukta olmalı, bu yüzden pad_sequences kullanıyoruz. maxlen parametresi ile tüm yorumları 500 kelimeye tamamlıyoruz. Eğer yorum 500 kelimeden kısa ise başına 0 (padding) eklenir, eğer uzun ise kesilir.
X_train = pad_sequences(X_train, maxlen = maxlen)
X_test = pad_sequences(X_test, maxlen= maxlen)


# RNN Modeli olusturma
model = Sequential() # base model: katmanlari sirali olarak eklemek icin

# embedding katmani: kelime indexlerini 32 boyutlu bir vektore donusturur
model.add(Embedding(input_dim = max_features, output_dim = 32, input_length= maxlen))

# simplernn katmani: metni sirayla isler ve baglam iliskisini ogrenir
model.add(SimpleRNN(units = 32)) # cell (noron) sayisi 
# eğer overfit olursa units sayisini azaltabiliriz


# output katmani: binary classification: sigmoid, 1 noron
"""
negatif -> 0.7
"""
model.add(Dense(1, activation = "sigmoid"))
# sigmoid: 0-1 arasi deger verir

# model compile
model.compile(
    optimizer = "adam", # agirlik guncellemesi icin kullanilan algoritma
    loss = "binary_crossentropy", # kayip fonksiyonu
    metrics = ["accuracy"] # degerlendirme metrigi
)

print(model.summary())


# training
history = model.fit(
    X_train, y_train, # girdi ve cikti veri
    epochs = 2, # egitim tekrar sayisi yani tum veriyi 2 kere egit
    #bunun sebebi modelin daha iyi genelleme yapabilmesi icin veriyi birden fazla kez gormesi gerekir
    batch_size = 64, # torba, ayni anda islenecek ornek sayisi yani 64 lu paketler halinde isle
    #bunun sebebi GPU bellegi sinirli oldugu icin tum veriyi bir kerede isleyemeyiz küçük parçalar halinde isleriz
    validation_split = 0.2 # verilerin %20 yi dogrulama icin ayir

    #eğitim sırasında accuracy ve loss değerlerini takip etmek için validation_split kullanılır. Bu, modelin eğitim sırasında overfitting yapıp yapmadığını anlamamıza yardımcı olur.
    #eğer validation accuracy düşerse ve training accuracy artıyorsa, model overfitting yapıyor demektir. Bu durumda modelin karmaşıklığını azaltmak veya daha fazla veri eklemek gibi önlemler alınabilir.
    # eğer accuracy artıyor loss azalıyorsa, model iyi bir şekilde öğreniyor demektir. Bu durumda eğitim süresini artırabiliriz veya modelin karmaşıklığını artırabiliriz.
    #val accuracy ile train accuracy arasındaki farkı izleyerek modelin genelleme yeteneğini değerlendirebiliriz. birbirlerine yakınlarsa model iyi genelleme yapıyor demektir. aralarındaki fark büyükse model overfitting yapıyor demektir. bu durumda epochs sayısını azaltabiliriz veya modelin karmaşıklığını azaltabiliriz.
)

# model evaluation
def plot_history(hist):
    plt.figure(figsize = (12,4))

    # accuracy
    plt.subplot(1, 2, 1) # 1 satir 2 sutun 1. grafik
    plt.plot(hist.history["accuracy"], label = "Training") # burada hist.history["accuracy"] ile eğitim sırasında her epoch'ta elde edilen doğruluk değerlerini alıyoruz. Bu değerler, modelin eğitim verisi üzerindeki performansını gösterir.
    plt.plot(hist.history["val_accuracy"], label = "Validation") # burada hist.history["val_accuracy"] ile validation_split ile ayrılan doğrulama verisi üzerindeki doğruluk değerlerini alıyoruz. Bu değerler, modelin daha önce görmediği veriler üzerindeki performansını gösterir.
    plt.title("Accuracy")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend()

    # loss plot
    plt.subplot(1, 2, 2) # 1 satir 2 sutun 2. grafik
    plt.plot(hist.history["loss"], label = "Training") # burada hist.history["loss"] ile eğitim sırasında her epoch'ta elde edilen kayıp değerlerini alıyoruz. Bu değerler, modelin eğitim verisi üzerindeki performansını gösterir.
    plt.plot(hist.history["val_loss"], label = "Validation") # burada hist.history["val_loss"] ile validation_split ile ayrılan doğrulama verisi üzerindeki kayıp değerlerini alıyoruz. Bu değerler, modelin daha önce görmediği veriler üzerindeki performansını gösterir.
    plt.title("Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()

    plt.tight_layout()
    plt.show()
# burada 1. grafikte eğitim ve doğrulama doğruluk değerlerini, 2. grafikte ise eğitim ve doğrulama kayıp değerlerini görselleştiriyoruz. Bu grafikler, modelin eğitim sürecindeki performansını değerlendirmemize yardımcı olur. Eğer eğitim doğruluğu artarken doğrulama doğruluğu düşüyorsa, model overfitting yapıyor demektir. Bu durumda modelin karmaşıklığını azaltmak veya daha fazla veri eklemek gibi önlemler alınabilir.
plot_history(history)


# test verisiyle modeli degerlendirme
test_loss, test_acc = model.evaluate(X_test, y_test) # test
print(f"Test: {test_acc:.2f}")

# egitilen modelin kaydini yapalim
model.save("rnn_duygu_model.h5")
print(f"Model basariyla kaydedildi: rnn_duygu_model.h5")