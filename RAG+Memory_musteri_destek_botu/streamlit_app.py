import streamlit as st # web arayuzu olusturmak icin bir python kutuphanesi

from langchain_openai import ChatOpenAI, OpenAIEmbeddings # langchain openai modulleri: chat llm ve embedding modeli
from langchain_community.vectorstores import FAISS # faiss vektor db
from langchain_community.document_loaders import PyPDFLoader
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter # metni daha kucuk parcalara bolme (chunk)
from langchain_classic.chains import ConversationalRetrievalChain # RAG + sohbet zinciri
from langchain_classic.memory import ConversationBufferMemory # konusma gecmisini tutan hafiza yapisi

from dotenv import load_dotenv
import os
import tempfile # gecici dosya islemleri icin

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# streamlit sayfa başlığını ve ikonunu ayarla
st.set_page_config(page_title="Müşteri Destek Botu", page_icon="📄")
st.title("Müşteri Destek Botu (RAG + Memory)")
st.write("Bir pdf yükleyin, içeriğine dair sorular sorun. Türkçe desteklidir.")

# pdf yukleme bileseni
uploaded_file = st.file_uploader("PDF dosyanızı yükleyin.", type = "pdf", key = "pdf_uploader")

# eger kullanici yeni bir pdf yuklediyse ve daha once yuklenen ile aynı degilse
if uploaded_file is not None:
    if "last_uploaded_name" not in st.session_state or uploaded_file.name != st.session_state.last_uploaded_name:
        # kullaniciya isnleniyor bilgisi gonderelim
        with st.spinner("PDF işleniyor..."):
            # yuklenen pdf i gecici bir dosyaya yazdir
            with tempfile.NamedTemporaryFile(delete=False, suffix =".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name # gecici dosyanın yolu

            # PyPDFLoaader ile PDF içeriğini yukle
            loader = PyPDFLoader(tmp_path)
            documents = loader.load()

            # metinleri parcala yani chunklara bol
            splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
            docs = splitter.split_documents(documents)

            # openai embedding ile metin vektorlestirme
            embedding = OpenAIEmbeddings(model = "text-embedding-3-large")

            # FAISS ile vector veri tabani
            vectordb = FAISS.from_documents(docs, embedding)

            # memory ve gpt 4 ile llm olusturma
            memory = ConversationBufferMemory(memory_key = "chat_history", return_messages=True)
            llm = ChatOpenAI(model_name = "gpt-4", temperature=0) # temperature=0 için deteministic (ayni girdiye ayni ciktiyi verir)

            # rag + memory zincirini olusturma
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever = vectordb.as_retriever(search_kwargs = {"k":3}),
                memory = memory
            )

            st.session_state.qa_chain = qa_chain
            st.session_state.chat_history = []
            st.session_state.last_uploaded_name = uploaded_file.name # aynı dosyanın yeniden işlenmesini engellemek için
        
        st.success("PDF başarıyla işlendi.")

if "qa_chain" in st.session_state: # eger pdf islendiyse
    # kullanicinin sorusu alinir
    user_question = st.text_input("👤 Sorunuzu yaziniz:" )

    if user_question:
        response = st.session_state.qa_chain.invoke(user_question) # langchain zinciriene soruyu gonder
        st.session_state.chat_history.append(("👤", user_question)) # kullanici mesajibi gecmişe ekleme
        st.session_state.chat_history.append(("🤖", response["answer"])) # model yanitini historye ekleme
    
    if st.session_state.chat_history:
        st.subheader("🗂 Sohbet Geçmişi")
        for sender, msg in st.session_state.chat_history:
            st.markdown(f"**{sender}**: {msg}")
