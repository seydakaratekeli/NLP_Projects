"""
problem tanimi: kullanicilar yazili olarak soru soracak, gercek zamanli ve dogal selilde yanitlar alabilecek
    - akilli turizm rehberi
    - Türkiye özelinde: tarihi yerler, kültürel etkinlikler, yemekler, ulaşım ...
    - llama 3.2 3b parametreli modeli ile cevaplari streamlit uzerinden gercek zamanli olarak gorsellestirelim

model tanitimi: LLAMA (Large Language Model Meta AI) (llama 3.2 3B) 
    -llama aynı gpt gibi içinde bir çok parametreye sahip büyük bir dil modelidir
    - acik kaynak: akademik ve ticari kullanimlar icin uygundur
    - verimli: daha az parametre ile ayni performansi sergiliyor
    - moduler: 1B, 3B, 8B, 70B paremetreye sahip modelleri var
    - lokal de calisabilir.
    
    -streamlit ile web arayuzu olusturabiliriz

langchain : llm uygulamalarını yapılandırmak, hafıza ve mesaj yönetimi gibi özellikleri kolayca eklemek için kullanılan bir kütüphanedir.
ollama: lama gibi uygulamları lokalde calistirmak icin kullandigimiz bir sunucu. 
streamlit: python ile web arayuzu olusturmak icin kullandigimiz kutuphane kullanıcı arayüzü ve görselleştirme için kullanılır.  
Plan/Program

install libraries: freeze 

ollama indir ve llama kur
    - ollama: https://ollama.com/download
    - llama 3.2 3b: https://ollama.com/library/llama3.2:3b

import libraries

ilk olarak terminal uzerinden calistirip test edelim, sonra streamlit ile web arayuzu olusturalim
"""

# import libraries
from langchain_ollama import ChatOllama # ollama llm arayuzu
from langchain_core.messages import SystemMessage, HumanMessage # chat mesaj siniflari
from langchain_classic.memory import ConversationBufferMemory # konusma gecmisi icin basit bir hafiza
from deep_translator import MyMemoryTranslator # ceviri kutuphanesi (MyMemory: ucretsiz REST API)

# ---- Çeviri yardımcı fonksiyonları ----
def _split_text(text: str, max_chars: int = 490) -> list:
    """Metni max_chars uzunluğunda parçalara böler, kelime sınırlarına göre."""
    if len(text) <= max_chars:
        return [text]
    chunks = []
    while text:
        if len(text) <= max_chars:
            chunks.append(text)
            break
        split_at = text.rfind(" ", 0, max_chars)  # son bosluktan kes
        if split_at == -1:
            split_at = max_chars  # boslu bulamazsa zorla kes
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip()
    return chunks

def translate_to_en(text: str) -> str:
    """Türkçe metni İngilizceye çevirir."""
    return MyMemoryTranslator(source="tr-TR", target="en-US").translate(text)

def translate_to_tr(text: str) -> str:
    """İngilizce metni Türkçeye çevirir. 500 kar. limitini otomatik yönetir."""
    translator = MyMemoryTranslator(source="en-US", target="tr-TR")
    chunks = _split_text(text)
    return " ".join(translator.translate(chunk) for chunk in chunks)
# ----------------------------------------

# llama model
llm = ChatOllama(model = "llama3.2:3b")

# hafiza ekleme, konusma gecmisi takip etme
memory = ConversationBufferMemory(return_messages=True) # return_messages = True -> mesajlar formatli doner bizim okuyabileceğimiz şekilde

# welcome message
print("Akıllı Turizm Rehberine Hoş Geldiniz")
print("Size gezilecek yerler, tatil önerileri ve ulaşım bilgileri gibi konularda yardımcı olabilirim.")

# terminal uzerinden llama ile konusma
while True:

    user_input = input("Siz: ")

    if user_input.lower() == "quit":
        print("Program sonlandirildi")
        break

# bu ikisini de yapabiliriz yazılım tasarım tercihidir
# 1) user inputu memorye atalim m? bunu yaparsak modelin hafizasi daha iyi olur, once memorye atayip sonra modelle konusmak daha mantikli
# 1 için lamayı ve memory bileşenlerini ayrı ayrı kullanabiliriz, 2 için ise memory ve lamayı tek bir bileşen olarak kullanabiliriz.
# 2) once llama ile konusup sonra memorye atalim? bunu yapabiliriz ama modelin hafizasi daha zayif olur. once memorye atamak daha mantikli
# langchaini içeri  aktarıp lama ve memory birleştiriyoduk chain ile sonra tek bir bileşen olarak kullanabiliriz. sonra zaten 2yi kendiliğinden yapıyordu
    # kullanicinin mesajlarini hafizaya kaydediyoruz
    memory.chat_memory.add_user_message(user_input)

    # kullanici mesajini ingilizceye cevir (model ingilizce dusunecek)
    user_input_en = translate_to_en(user_input)

    # model icin gerekli olan tum mesajlari olustur: sistem mesajı + memory + human mesajı
    messages = [
        SystemMessage(content = "You are a smart tourism guide for Turkey. "
                      "Help users with information about cities, historical sites, local cuisine, transportation and holiday recommendations in Turkey. "
                      "Always respond in English.")
    ] + memory.load_memory_variables({})["history"] + [HumanMessage(content=user_input_en)]

    # modelden yanit alma
    response = llm.invoke(messages)

    # modelin ingilizce cevabini turkceye cevir
    response_tr = translate_to_tr(response.content)

    # modelin cevabini hafizaya ekle
    memory.chat_memory.add_ai_message(response.content)

    print(f"Rehber: {response_tr}")

    #websearch özelliği eklenebilir. Websearch: internette aranan konularla ilgili güncel bilgi almak için kullanılabilir. Örneğin, bir şehirdeki güncel etkinlikler veya restoranlar hakkında bilgi almak için websearch kullanılabilir. Bu sayede modelin yanıtları daha güncel ve doğru olabilir.    