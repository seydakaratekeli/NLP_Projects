"""
problem tanimi: kullanicinin saglikla ilgili sorularini anlayan ve yanitlayan bir GPT tabanli doktor asistani chatbot
    - kullanicinin "yasini" ve "adini" dikkate alan cevaplar uretsin
    - mejsa gecmisini hatirlayarak diyalogu ona gore surdurmeli "memory"
    - Langchain ve OPENAI GPT teknolojisi kullanılacak
    - ilk olarak terminalde calisan bir versiyon ardindan FastAPI tabanli bir web servisi olsuturalim
    - client tarafini yazip test edelim- python request kütüphansiyle APIde test edildeck

veri seti: veri seti yok onun yerine hazir gpt modelini kullanarak prompt ayarlamasi yapalim.
GPT ye bir Fine-tuningyapıp onun doktor asistanıymışa çevirebilirdik veya bunu veriyl de yapabilirdik ama bunlar zor ve zaman alıcı işlemler. Bunun yerine hazır GPT modelini kullanıp prompt ayarlaması yapacağız.
model tanitimi: GPT (Generative Pre-Trained Transformer) ile olusturulan modeli kullanalim, gpt 3.5 turbo(sorulara mantıklı cevap üretiyor,öneride bulunuyor, tavsiye veriyor) 
    - API uzerinden iletisim kurarak gercek zamanli saglik onerilerini alalim.

    langchain tensorflow , keras gibi düşünebilirsiniz büyük dil modelleri ile bir çalışma için kullanılabilecek bir kütüphanedir. 
Langchain: llm kutuphanesi
    - prompt yonetimi 
    - memory
    - tool entegrayonu: ai agents icin tool kullanimi
    - chain yapisi- çok adımlı konuşma ve işleemleri zincir halinde yönetebiliyoruz multirag,multitool, multichain gibi.LLM modelinin arka tarafında çalıştığı birbiri ile iletişim kurabilen iş yaptıkları zincirlerdir.

plan/program

install libraries
    - fastapi: web api gelistirmek icin bir framework (asenkron)
    - uvicorn: fastapi calistirmak icin gereken bir sunucu
    - langchain
    - openai 
    - python-dotenv: .env dosyasindan api anahatini almak icin kullanicaz
    - langchain_community

import libraries

LLM   +    Memory
    |        |
         Chain
         Langchainde bulunan conversationschain ile yapıyoruz

ilk olarak temrinalde calisan bir versiyonunu yazalim, ardindan FastAPI tabanli bir web servisi olusturalim.

"""

# import libraries
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI 
from langchain_classic.chains import ConversationChain 
from langchain_classic.memory import ConversationBufferMemory

import warnings
warnings.filterwarnings("ignore")


# ortam degiskenlerini tanimla (openai api key tanimla)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY bulunamadı. Proje kök dizininde .env oluşturup anahtarınızı ekleyin."
    )

# LLM + memeory
# buyuk dil modeli 
llm = ChatOpenAI(
    model = "gpt-3.5-turbo", # hangi gpt yi kullandigimiz
    temperature = 0.7, # 0-1, 0 a yakinsa garanti cevap verir, 1 e yakinsa dusunerek cevap verir. 1 e yaklastikca halusinasyon riski artar
    openai_api_key = api_key
)

# hafiza
memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(llm = llm, memory = memory, verbose = True)

# kullanici bilgilerini al isim ve yas
name = input("Adiniz: ")
age = input("Yasiniz: ")

intro = (
    f"Sen bir doktor asistanısın. Hasta {name}, {age} yaşında. "
    "Sağlık sorunları hakkında konuşmak istiyor. "
    "Yaşına uygun dikkatli ve nazik tavsiyeler ver; ismiyle hitap et."
)

memory.chat_memory.add_user_message(intro)
print("Merhaba ben bir doktor asistaniyim, size nasil yardimci olabilirim. ")

# chatbot dongusu tanimlama
while True:
    # hasta soru sordu
    user_msg = input(f"{name}: ")
    if user_msg.lower() == "quit": # konusmayi sonlandir
        print("Sana yardımcı olabildiysem ne mutlu bana, görüşmek üzere")
        break 

    # doktor asistani cevap verdi ve hafizaya atildi
    reply = conversation.predict(input = user_msg) # llm cevabi
    print(f"Doktor Asistanı: {reply}")

    # verilen cevaplari memory e kaydet
    print("\nHafiza: ")
    for idx, m in enumerate(memory.chat_memory.messages, start = 1):
        print(f"{idx:02d}. {m.type.upper()}: {m.content}")
    print("------------------\n")


