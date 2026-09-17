"""
Problem tanımı: gpt ile sesli sohbet 
    - kullanicinin mikrofona konusarak soru sormasi 
    - openai whisper modeli 
    - metnin gpt 3.5 turbo ile analiz etdilmesi
    - guvenlik mekanizmasi: zararli dil filtreleme

Kullanilan Teknolojiler:
    - ses kaydi
    - ses -> metin: openai whisper modeli
    - cevap üretimi: openai gpt 3.5 turbo
    - loglama: logging modülü
    - zararli içerik filtreleme: re

model tanıtımı: openai whisper ve gpt 3.5 turbo
    - çok dilli konuşma tanıma modeli
    - konuşmaları yazıya döker
    - birden çok dili destekler
    - otomatik dil algılama yapabilir
    - bu projede whisper 1 modeli kullanalim
    - whisper light: 
        * hafif, hızlı, offline ve açık kaynaklı

api tanimlama: digerleri ile ayni

plan/program:

install libraries: freeze 

import libraries

"""

# import libraries
from openai import OpenAI # openai api istemcisi sinifini iceriye aktarir
import sounddevice as sd # miktofon erisimi icin sound device modülü
from scipy.io.wavfile import write # ses kaydinin wav dosyasina yazma araci
import os # dosya islemleri icin os modülü
import uuid # benzersiz kimlik icin
import re # zararli icerek filtreleme
import json # json formati ile yasakli kelimeleri okumak icin
from datetime import datetime # tarih ve saat icin
from dotenv import load_dotenv # .env dosyasini yuklemek icin
import logging # loglama icin gerekli 

# log ayarlari
now = datetime.now().strftime("%Y%m%d_%H%M%S") # dosya adi icin suanki zamani al
log_file = f"logs/konusma_{now}.log" # log dosyasi adini olustur

# log klasoru yoksa olustur
os.makedirs("logs", exist_ok=True) # "logs" klasoru yoksa olustur varsa atla

# log formati ve seviyesini ayarlar: DEBUG, INFO, WARNING, ERROR, CRITICAL
logging.basicConfig(
    level = logging.INFO, # log seyiyesi info olarak ayarlandi, yani info ve info dan sonrasi (INFO, WARNING, ERROR, CRITICAL)
    format = "%(asctime)s [%(levelname)s] %(message)s", # zaman ve seviye iceren formatimiz
    handlers = [ #2 seviyeli yapılabilir
        logging.FileHandler(log_file, encoding='utf-8'), # log dosyasina yazma
        logging.StreamHandler() # konsola yazdirma
    ] # terminalin şişmemesi için log dosyasını yazdır
)

logger = logging.getLogger(__name__) # logger nesnesi olustur

# .env olustur ve yukle
load_dotenv() # .env dosyasi yuklenmis oldu
client = OpenAI() # openai istemcisi gidip .env dosyasindan api anahtarini alir

DURATION = 5 # tek seferde kac saniye kayit alacagimizin parametresi
FS = 44100 # ses kaydi icin kullanilacak frekans degeri

# zararli sozcuk filtrelemesi 
# Yasaklı kelimeleri JSON dosyasından dinamik olarak yükle
def load_banned_words(filepath="banned_words.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"{filepath} bulunamadı. Boş liste ile devam ediliyor.")
        return []
    except json.JSONDecodeError:
        logger.error(f"{filepath} formatı hatalı. Boş liste ile devam ediliyor.")
        return []

BANNED_WORDS = load_banned_words()
# Kelimeleri tek bir regex patterninde birleştirip derliyoruz
BANNED_PATTERN = re.compile(rf"\b({'|'.join(map(re.escape, BANNED_WORDS))})\b", flags=re.IGNORECASE) if BANNED_WORDS else None

def filter_bad_words(text):
    if not BANNED_PATTERN:
        return text

    def replacer(match):
        word = match.group(0)
        logger.warning(f"Zararli kelime tespiti yapildi: {word}")
        # Kelimenin uzunluğu kadar yıldız koyuyoruz
        return "*" * len(word)
        
    filtered_text, _ = BANNED_PATTERN.subn(replacer, text)
    return filtered_text 

# filter_bad_words("merhaba, zararlı bir kelime var mı?") # test et

# ses kaydi alma ve kaydet
def record_audio(filename = "recorded.wav", duration = DURATION): # mikrofon kaydi al
    logger.info("Mikrofondan ses kaydi baslatildi")
    recording = sd.rec(int(duration*FS), samplerate=FS, channels=1) # 
    sd.wait() # kayit bitene kadar bekle
    write(filename, FS, recording) # kaydi dosyaya yaz
    logger.info(f"Ses kaydi tamamlandi: {filename}")

# whisper ayarlari, sesi metne cevirme
def transcribe_with_whisper(audio_path): # wav dosyasini whisper ile metne donustur
    logger.info("Whisper ile ses yaziya cevriliyor")
    with open(audio_path, "rb") as audio_file: # ses dosyasini ac
        trasncript = client.audio.transcriptions.create(
            model = "whisper-1", # openai whisper modeli
            file=audio_file, 
            language="tr" # turkce dil ipucu
        )
    return trasncript.text # metin olarak dondur

# gpt 3.5 turbo ayarlari, dil modeli olusturma
def get_gpt_reponse(messages): # gonderilen mesaja gore yanit veren llm fonksiyonu
    logger.info("GPT yanit uretiyor")
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages= messages, # mesajlar listesi
    )
    return response.choices[0].message.content # ilk olsilik cevabı doner

# print(f"GPT Yanit test: {get_gpt_reponse([{"role":"user", "content": "Merhaba, nasılsın?"}])}") # test et

# hepsini birleştir ve çalıştır

if __name__ == "__main__":
    logger.info("--- --- GPT Sesli Chatbot Başladı --- ---")
    logger.info(f"Konuşma log dosyası: {log_file}")

    # mesaj gecmisini sistem mesajiyla baslat
    messages = [
        {"role": "system", "content": "Sen yardımserver bir sesli asistansın, konuşmalara uygun cevap ver."}
    ]

    while True: # kullanici cikana kadar sonsuz bir dongu olustur.
        uid = str(uuid.uuid4()) # her kayit icin unique bir id uret
        audio_file = f"record_{uid}.wav" # gecici wav dosyasi ismi
        #kullanıcının sesini metne çevirmek için önce bir waw dosyasına kayıt edip gptye gönderiyoruz
        record_audio(audio_file, DURATION) # mikrofon kaydi yap
        question = transcribe_with_whisper(audio_file) # wav dosyasini metne cevir
        logger.info(f"Kullanici (raw): {question}")

        filtered_question = filter_bad_words(question) # zararli kelimeleri filtrele
        if filtered_question != question: # yani filtreleme yapildiysa
            logger.info(f"Kullanici (filtreli): {filtered_question}")

        if "çık" in filtered_question.lower(): # kullanici cik derse
            logger.info("Çıkış komutu algılandı, program kapatılıyor")
            # döngüden çık ve programı bitir
            break

        messages.append({"role":"user", "content": filtered_question}) # kullanici mesajini ekle
        answer = get_gpt_reponse(messages) # gpt yanitini al

        logger.info(f"GPT: {answer}") # gpt yanitini logla

        if os.path.exists(audio_file):
            os.remove(audio_file) # olusturdugumuz gecici wav dosyasni sil
    
    logger.info("--- --- GPT Sesli Chatbot Bitti --- ---  ")
