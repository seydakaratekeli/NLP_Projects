"""
yorum yazalim, lstm bu yoruma gore bir tahmin ortaya cikarsin

"""
import numpy as np
import pickle
from tensorflow.keras.models import load_model 
from tensorflow.keras.preprocessing.sequence import pad_sequences

# modeli yukle
model = load_model("regression_lstm_yelp.h5", compile = False) #false  -> modelin compile edilmesini engeller, bu sayede modeli daha hızlı yükleyebiliriz

# biz metin giriyoruz ama o bizden sayı bekliyor bu yüzden metini sayılara çevirmemiz gerekiyor, bunun için tokenizeri diske kaydetmiştik, şimdi tekrar yükleyelim
# tokenizeri yukle
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# ornek input "ben bir doktora gittim ve bu doktoru cok sevdim."
# 1 star - 5 star örnek yorumlar
texts = [
    "Terrible. Preordered my tires and when I arrived they couldn't find the order anywhere. Once we got through that process I waited over 2 hours for them to be put on... I was originally told it would take 30 mins. Slow, over priced, I'll go elsewhere next time.",
    "BEST DINER IN THE COUNRTY!!! We've been to many famous diners across the country and we still give Gab and Eat the best rating !! I was a little intimidated when I first walked in and there was like 2 pounds of butter just sitting on top of the homefires on the grill. If you are looking for a healthy breakfast they probably can accomodate you, but Everything I ate was clearly the opposite of healthy. After trying like every meal they have I would recommend the mix grill(half unless you are sharing) adding cajun seasoning with the texas toast. Burgers are great too.\n\nIt's hard to find a place that makes a better breakfast than you could make by yourself at home, but this place does it. The atmosphere is classy, old school Americana.",
    "best experience ever",
    "worst experience ever"
]

# PREPROCESSING
# Tokenizer "0 1 2 3 4 5 6 7 8"
# padding: "0 1 2 3 4 5 6 7 8 0 0 0 0 0 ... 0" boyu 100 olacak
# text i sayilara cevir ve padding islemini gerceklestir
sequences = tokenizer.texts_to_sequences(texts)
padded = pad_sequences(sequences,  maxlen = 100, padding = "post") #daha önce yaptığımızın aynısını yapmamız gerekiyor
# modelin inputunu 100 yapmıştık, o yüzden padding ile 100 boyutuna getirdik, eğer boyut 100 den kucukse 0 ile doldurduk, eğer buyukse 100 e kadar kesip attık

# LSTM predicton
predictions = model.predict(padded)

# POST PROCESSING
#yeniden ölçeklendirme yaptık çünkü modelimiz 0-1 arasında tahmin yapıyor, biz ise 1-5 arasında skor istiyoruz
predictions_scaled = predictions * 5

# sonuclari yazdir
for i, comment in enumerate(texts):
    print(f"Yorum: \n{comment}")
    print(f"Tahmini skor degeri: {predictions_scaled[i][0]:.2f}")