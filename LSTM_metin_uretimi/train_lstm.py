"""
problem tanimi: LSTM ile metin uretme: verilen kelimelerden anlamli turkce scumleler olusturmasi
    - ben yarin ...

lstm: long short term memory


veri seti: motivasyon temali, 1000 adet Turkce cumleden olusuyor (motivasyon_cumleleri.txt)
 

plan/program:

install libraries (pip), requirements.txt

import libraries
"""

# import libraries
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout 
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping
import pickle


# YENI HALI: veri seti artik "motivasyon_cumleleri.txt" dosyasinda, her satirda
# bir cumle olacak sekilde tutuluyor. Asagidaki kod bu dosyayi acar, her satiri
# okur, basindaki/sonundaki bosluk ve satir sonu (\n) karakterlerini temizler
# (strip()) ve bos satirlari (varsa) atlayarak "data" listesini olusturur.
# Boylece "data" degiskeni, kodun geri kalaninda (tokenizer, n-gram uretimi vb.)
# TAMAMEN AYNI SEKILDE, bir Python string listesi olarak kullanilmaya devam eder.
# Yani kodun davranisi ve yapisi degismedi, sadece verinin kaynagi degisti.
with open("motivasyon_cumleleri.txt", "r", encoding="utf-8") as f:
    data = [line.strip() for line in f if line.strip()]
 
print(f"veri setindeki toplam cumle sayisi: {len(data)}")
 

# -- Preprocessing -- 
# Tokenization 
# kelimeleri indexlere (sayilar) cevir (tokenizer)
tokenizer = Tokenizer()
tokenizer.fit_on_texts(data)
total_words = len(tokenizer.word_index) + 1 # +1: padding icin yapiyoruz

print(f"total_words: {total_words}")

# elimizdeki tokenları dizilere bölüyoruz (n-gram dizileri olusturmak icin)
# n-gram dizileri olustur yani her cumleden kisa diziler olustur (embedding)
# 3-gram: kelimeleri indexlere (sayilar) cevir, ["kelimeleri indexlere (sayilar)", "indexlere (sayilar) cevir"]
input_sequences = []
for text in data:
    token_list = tokenizer.texts_to_sequences([text])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[: i+1]
        input_sequences.append(n_gram_sequence)

print(f"input_sequences: \n{input_sequences}")
"""
[1, 9], [1, 9, 97], [1, 9, 97, 98], [1, 9, 97, 98, 7], [1, 9, 97, 98, 7, 2], [1, 9, 97, 98, 7, 2, 10],

"Bugün(1) hava(9) top(97) oynamak(98) için(7) çok(2) güzel.(10)"
"""



# padding: farkli uzunluktaki dizileri sabitle
# bu sayede LSTM modeline girdi olarak verebiliriz
max_sequence_length = max(len(x) for x in input_sequences)
input_sequences = pad_sequences(input_sequences, maxlen = max_sequence_length, padding = "pre")

print(f"after padding input_sequences: \n{input_sequences}")
"""
[1, 9], [1, 9, 97], [1, 9, 97, 98],
[  0   0   0 ...   0   1   9]
 [  0   0   0 ...   1   9  97]
 [  0   0   0 ...   9  97  98]
"""
#padding yaptıktan sonraki amacımız buradaki her bir cümleyi aynı boyuta taşımak. Bu sayede LSTM modeline girdi olarak verebiliriz. Padding işlemi, dizilerin başına sıfır ekleyerek tüm dizileri aynı uzunluğa getirir. rnn e farklı boyutlarda girdi veremeyiz. Bu yüzden padding yapıyoruz.input sizeı belli olmalı. LSTM modeline girdi olarak verebilmek için dizilerin aynı boyutta olması gerekiyor.

# girdi (X) ve hedef degiskenler (y) ayir
# modele uygyn veri seti olusturmak icin n-gram dizilerinin son kelimesini hedef degisken olarak seciyoruz
X = input_sequences[:, :-1] # n - 1 kelimeyi giris olarak sec
y = input_sequences[:, -1] # n inci kelimeyi tahmin et
"""
 [  0   0   0 ...   1   9  97]
 X = [  0   0   0 ...   1   9]
 y = [97]
"""
# hedef degiskene one hot encoding
y = tf.keras.utils.to_categorical(y, num_classes = total_words)
print(f"hedef degisken: {y}")
"""
[1,2,3] -> 
1 -> [1, 0, 0]
2 -> [0, 1, 0]
3 -> [0, 0, 1]
"""

# -- LSTM Training -- 
# lstm modeli tanimla
model = Sequential()
model.add(Embedding(total_words, 50, input_length = X.shape[1])) # embedding katmani
model.add(LSTM(100))
model.add(Dropout(0.2)) 
model.add(Dense(total_words, activation = "softmax")) # output
"""
X = [bugün hava çok]
y = [güzel]

"""

# compile 
model.compile(optimizer = "adam", loss = "categorical_crossentropy", metrics = ["accuracy"])

print(model.summary())

early_stop = EarlyStopping(
    monitor='val_loss', 
    patience=5,                 # En iyi skordan sonra 5 epoch daha izle, gelişmezse durdur
    restore_best_weights=True   # Durduğunda otomatik olarak 13. epoch'taki en iyi haline geri dön
)

# egitimi baslat
# X = bagimsiz degiskenler
# y = bagimli degisken
# epoch verinin kac kere egitilecegi
# verbose = 1 ise egitim surecinin console da izlenmesi icin gerekli

history = model.fit(
    X, y,
    epochs = 100,
    batch_size = 64,
    validation_split = 0.2,  # verinin %20'sini dogrulama (validation) icin ayir
    # boylece egitim sirasinda training accuracy/loss ile birlikte
    # validation accuracy/loss de takip edilebiliyor
    callbacks=[early_stop], 
    verbose = 1
)





#Amac: modelin egitim (training) ve dogrulama (validation) verisi
# uzerindeki performansini gorsel olarak karsilastirmak.
#   - accuracy artiyor, loss azaliyorsa -> model iyi ogreniyor demektir
#   - training accuracy yukselirken validation accuracy dusuyorsa ->
#     model ezber yapiyor (overfitting) demektir
#   - training ve validation egrileri birbirine yakinsa -> model iyi
#     genelleme yapiyor demektir
# Bu fonksiyon sadece GOZLEM/ANALIZ amaclidir, modelin egitim davranisini
# (X, y, epochs, mimari vb.) degistirmez.
def plot_history(hist):
    plt.figure(figsize = (12, 4))
 
    # accuracy grafigi
    plt.subplot(1, 2, 1)  # 1 satir 2 sutun, 1. grafik
    plt.plot(hist.history["accuracy"], label = "Training")
    plt.plot(hist.history["val_accuracy"], label = "Validation")
    plt.title("Accuracy")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend()
 
    # loss grafigi
    plt.subplot(1, 2, 2)  # 1 satir 2 sutun, 2. grafik
    plt.plot(hist.history["loss"], label = "Training")
    plt.plot(hist.history["val_loss"], label = "Validation")
    plt.title("Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
 
    plt.tight_layout()
    plt.show()
 
plot_history(history)


# modeli kaydet
model.save("lstm_model.keras")

# tokenizer'ı kaydet
import pickle
with open("tokenizer.pickle", "wb") as f:
    pickle.dump(tokenizer, f)

# max_sequence_length'i kaydet
with open("max_sequence_length.pickle", "wb") as f:
    pickle.dump(max_sequence_length, f)

# veri sayımızı milyonlara çıkardığımızda veya lstm yerine transformer kullandığımızda daha iyi sonuçlar alabiliriz. LSTM, uzun dizilerdeki bağımlılıkları öğrenmekte zorlanabilir. Transformer mimarisi, özellikle dil modelleme görevlerinde daha iyi performans gösterebilir. Ayrıca, veri setini artırmak ve çeşitlendirmek, modelin genelleme yeteneğini artıracaktır.
