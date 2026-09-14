"""
web uzerinde calisan chatbot ekrani gelistirme 
streamlit framework: machine learning ve yapay zeka uygulamalarini web uzerinde gorsellestirmek icin kullanilan bir kutuphane.
"""

import streamlit as st # streamlit ile web arayuzu olusturma kutuphanesi
from langchain_ollama import ChatOllama # ollama uzerinden llama cagirmak icin
from langchain_core.messages import SystemMessage, HumanMessage # sohbet mesajlari
from langchain_classic.memory import ConversationBufferMemory # hafiza yonetimi
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
        split_at = text.rfind(" ", 0, max_chars)
        if split_at == -1:
            split_at = max_chars
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

# baslik ve aciklamalar
st.set_page_config(page_title = "Akıllı Turist Rehberi", page_icon = "🌍")
st.title("🌍 Akıllı Turist Rehberi")
st.markdown("Türkiye'nin dört bir yanındaki turistik yerler hakkında bilgi almak için sorular sorabilirsiniz.")

# session state (streamlit de kullanici gecmisini tutmak icin)
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory( return_messages=True) # mesaj gecmisi

# ollama ile llama 3.2 3B parametreli modeli yukleyelim
llm = ChatOllama(model = "llama3.2:3b")

# mesaj kutusu: kullanicidan gelen mesaj
user_input = st.chat_input("Bir şehir, mekan, yemek ya da aktivite sorabilirsiniz...")

if user_input:
    # yeni gelen kullanicinin mesajini ilk olarak memory e ekliyoruz
    st.session_state.memory.chat_memory.add_user_message(user_input)

    # kullanici mesajini ingilizceye cevir (model ingilizce dusunecek)
    user_input_en = translate_to_en(user_input)

    # tum konusmayi modele verecek sekilde mesajlari olusturalim: sistem mesaji + memory + human message
    messages = [
        SystemMessage(content = "You are a smart tourism guide for Turkey. "
                      "Help users with information about cities, historical sites, local cuisine, transportation and holiday recommendations in Turkey. "
                      "Always respond in English.")
    ] + st.session_state.memory.load_memory_variables({})["history"] + [HumanMessage(content = user_input_en)]

    # modelden yanit al (ingilizce gelir)
    response = llm.invoke(messages)

    # ingilizce yaniti turkceye cevir
    response_tr = translate_to_tr(response.content)

    # turkce yaniti hafizaya kaydet
    st.session_state.memory.chat_memory.add_ai_message(response_tr)

# sohbet gecmisini arayuzde goster
# tum mesajlari sirasiyla gezip ekrana bastiralim
for msg in st.session_state.memory.chat_memory.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("🧑‍💼 Kullanıcı"):
            st.markdown(msg.content)
    else: # ai ise 
        with st.chat_message("🧭 Akıllı Rehber"):
            st.markdown(msg.content)