import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# kaydedilenleri yükle
model = load_model("lstm_model.keras")

with open("tokenizer.pickle", "rb") as f:
    tokenizer = pickle.load(f)

with open("max_sequence_length.pickle", "rb") as f:
    max_sequence_length = pickle.load(f)



def sample_with_temperature(predicted_probs, temperature=0.8):
    # predicted_probs: modelin urettigi olasilik dagilimi (toplam_kelime_sayisi kadar eleman)
    predicted_probs = np.asarray(predicted_probs).astype("float64")
 
    # sifira bolme / log(0) hatasini engellemek icin kucuk bir epsilon ekleniyor
    predicted_probs = np.log(predicted_probs + 1e-8) / temperature
    exp_probs = np.exp(predicted_probs)
    # yeniden normalize et (toplam olasilik 1 olsun)
    final_probs = exp_probs / np.sum(exp_probs)
 
    # olasiliklara gore AGIRLIKLI RASTGELE bir index sec (artik hep en
    # yuksek olasilikli index secilmiyor)
    predicted_index = np.random.choice(len(final_probs), p=final_probs)
    return predicted_index

def generate_text(seed_text, next_words, temperature=0.8):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0] # tokenization
        token_list = pad_sequences([token_list], maxlen = max_sequence_length - 1, padding= "pre") # padding
        predicted_probs = model.predict(token_list, verbose = 0)[0]
 
        # eskiden: predicted_index = np.argmax(predicted_probs, axis = -1)[0]
        predicted_index = sample_with_temperature(predicted_probs, temperature=temperature)
 
        # index 0, padding icin ayrilmisti; tokenizer.index_word icinde
        # karsiligi olmayabilir, bu durumda bu adimi atlayip devam ediyoruz
        predicted_word = tokenizer.index_word.get(predicted_index)
        if predicted_word is None:
            continue
 
        seed_text = seed_text + " " + predicted_word
 
        # YENI: uretilen kelime bir cumle sonu isareti iceriyorsa
        # (nokta, unlem, soru isareti), daha fazla kelime uretmeden dur.
        # Bu sayede next_words'e ulasilmamis olsa bile cumle "yarim" degil
        # "tamamlanmis" gibi bitiyor.
        if any(p in predicted_word for p in [".", "!", "?"]):
            break
 
    return seed_text


# kullanicidan konsol uzerinden baslangic kelimesini ve kac kelime
# uretilecegini al (train.py'daki eski hali ile ayni mantik)
seed_text = input("Başlangıç kelimesi/kelimeleri girin: ")
next_words = int(input("Kaç kelime üretilsin: "))
 
print(generate_text(seed_text, next_words))
 
"""
(1)
seed_text = bu sabah
predicted_word = okula
 
(2)
seed_text = bu sabah okula
predicted_word = geç
 
(return)
seed_text = bu sabah okula geç
"""