import streamlit as st

from langchain_ollama import ChatOllama # ollama uzerinden llama cagirmak icin
from langchain_core.messages import SystemMessage, HumanMessage # sohbet mesajlari
from langchain_classic.memory import ConversationBufferMemory # hafiza yonetimi
from deep_translator import MyMemoryTranslator # ceviri kutuphanesi (MyMemory: ucretsiz REST API)

# streaming callbacks
# Streaming callbacks
from langchain_core.callbacks import (
    StreamingStdOutCallbackHandler,
    BaseCallbackHandler,
)
from typing import Any

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

# streamlit icin ozel streaming callback tanimi
class StreamHandler(BaseCallbackHandler):
    def __init__(self, placeholder):
        self.placeholder = placeholder # streamlit icindeki mesaj kutumuz
        self.final_text = ""

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        self.final_text += token # tokenlari birlestir
        self.placeholder.markdown(self.final_text + " ") # canli olarak yaz

# baslik ve aciklamalar
st.set_page_config(page_title = "Akıllı Turist Rehberi (Canlı)", page_icon = "🌍")
st.title("🌍 Akıllı Turist Rehberi (Streaming Modu)")
st.markdown("Türkiye'nin dört bir yanındaki turistik yerler hakkında bilgi almak için sorular sorabilirsiniz.")

# session state (streamlit de kullanici gecmisini tutmak icin)
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory( return_messages=True) # mesaj gecmisi

# mesaj kutusu: kullanicidan gelen mesaj
user_input = st.chat_input("Bir şehir, mekan, yemek ya da aktivite sorabilirsiniz...")

# sohbet gecmisini arayuzde goster
# tum mesajlari sirasiyla gezip ekrana bastiralim
for msg in st.session_state.memory.chat_memory.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("🧑‍💼 Kullanıcı"):
            st.markdown(msg.content)
    else: # ai ise 
        with st.chat_message("🧭 Akıllı Rehber"):
            st.markdown(msg.content)

if user_input:
    # yeni gelen kullanici mesajini ilk olarak memory e ekliyoruz
    st.session_state.memory.chat_memory.add_user_message(user_input)
    with st.chat_message("🧑‍💼 Kullanıcı"):
        st.markdown(user_input)

    with st.chat_message("🧭 Akıllı Rehber"):

        response_placeholder = st.empty()

        # LLM uretirken spinner goster (ingilizce tokenlar kullaniciya gosterilmesin)
        with st.spinner("Yanıt hazırlanıyor..."):
            llm = ChatOllama(model = "llama3.2:3b")

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

        # ceviri tamamlaninca turkce yaniti goster
        response_placeholder.markdown(response_tr)

        # turkce yaniti hafizaya kaydet (kullaniciya gosterilen dil)
        st.session_state.memory.chat_memory.add_ai_message(response_tr)