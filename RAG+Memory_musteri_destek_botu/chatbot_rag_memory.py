"""
problem tanimi:Akıllı Müşteri Destek Sistemi
    - müşteriler sık sık benzer soruları sorarlar:
        - şifremi unuttum
        - fatura nereden alabilirim?
        - iade süresi kaç gün
        - yutdışına gönderim yapıyor musunuz?
    -çözüm: 
        - .pdf dosyasinı (sıkça sorulan sorular) vektör veri tabanina donustur.
        - kullanıcıdan gelen sorular veritabanına sorgulanır ve gpt türkçe ceaplar üretir

Kullanılan teknolojiler:
    - langchain: rag mimarisi kurmak için
    - faiss: embeddingleri saklamak için hızlı bir vektör veritabanı
    - openai: soru ecvap için llm
    - streamlit: web arayüzü, son kullanıcı ile interektif kullanıcı deneyimi

veri seti:chatbotun cevap verebilmesi için gerekli olan soru ve cevap seti

veri seti: chatgpt olusturdu
    - Soru: Yurdışı satışlarınız bulunuyor mu?
    - Cevap: Hayır

    - Faturamı nereden alabilirim?
    - Faturanız 3 iş günü içerisinde teslim edilecektir.

plan program
    - SSS bilgilerini içeren bir pdf
    - kullanıcı bu dosyayı arayüzden yukleyecek
    - pdf metni parçaya ayrılacak ve embeddingler çıkarılacak
    - kullanıcı soru sorduğu zaman vektor db den benzer içerikler getirilir, gpt ile cevap oluşuturulur
    - konuşma geçmişi memory ile saklanır ve sonraki yanıtlara bağlam oluştur.

install libraries: freeze



müşterinin soruları burdan okuyacağız ve bunu embedding hale getireceğiz
sonrasında bunu chatbota vererek memory altyapısı ekleyeceğiz


bunları yaptıktan sonra bunları bir arayüzden(streamlitten) kullanacağız
neden Rag yapısı?
pdf içeriğine dayalı güncel bilgileri bize sağlar,pdf güncellendikçe cevaplarda otomatik bir şekilde güncellenecektir
neden memory?
konuşmada bağlamı koruması açısından, kullanıcının chatbot arasında geçmiş konuşmaları hatırlamak için
neden gpt?
hem embedding hem de llm açısından türkçe dil desteği bulunuyor
neden streamlit?
hızlı prototipleme ve sunum imkanı veriyor

"""
from langchain_openai import ChatOpenAI # Openai destekli llm modelleri icin
from langchain_classic.chains import ConversationalRetrievalChain # RAG + sohbet zinciri
from langchain_community.vectorstores import FAISS # faiss vektor veritabani
from langchain_openai import OpenAIEmbeddings # metni vektorlestirmek icin openai embedding modeli
from langchain_classic.memory import ConversationBufferMemory # konuşma geçmişini tutan hafiza yapisi

from dotenv import load_dotenv
import os


load_dotenv() # ortam degiskenlerini .env dosyasindan yukle
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not found.")

os.environ["OPENAI_API_KEY"] = api_key

# embedding modelini başlat (text -> vektor donusumu)
embedding = OpenAIEmbeddings(model = "text-embedding-3-large")

# daha once olusturulmus vektor veritabani yukle (load_pdf_and_embed.py dosyasında)
# faiss, metin parcalarinin vektor temsillerini tutan bir vektör veritabanı 
vectordb = FAISS.load_local(
    "faq_vectorstore", # kaydedilmis faiss veritabani klasoru
    embedding,  # embedding modeli
    allow_dangerous_deserialization=True # pickle guvenlik uyarisi bastirma
)

# konusma gecmisi icin memory olusturma
memory = ConversationBufferMemory(
    memory_key="chat_history", # konusma gecmisi bu anahtar ile saklanir
    return_messages= True # gecmiş mesajlar tam haliyle geri döner, uzun bir konuşma olsaydı son 10 mesajıal şeklinde returnmessage parametresi ile ayarlanabilir
)

# sıfır rastlantısallık ile çalışır, sabit cevaplar verir
llm = ChatOpenAI(
    model_name = "gpt-4", # kullanilan dil modeli
    temperature = 0.8 # = 0 için deteministic (ayni girdiye ayni ciktiyi verir), 0.8-1.0 arası daha yaratıcı cevaplar verir
)


# rag + memory zincir olustur
# - llm
# - faiss retriever: en benzer 3 belge getirilsin (k=3)
# - memory
qa_chain = ConversationalRetrievalChain.from_llm(
    llm = llm,
    retriever = vectordb.as_retriever(search_kwargs = {"k" : 3}),
    memory = memory,
    verbose = True
)

print("Müşteri destek botuna hoş geldiniz")
while True:
    # 
    user_input = input("Siz: ")
    if user_input.lower() == "çık":
        break

    # kullanici sorusu llm + rag + memory zincirine verilir
    response = qa_chain.run(user_input)
    print("Müşteri Destek Botu: ", response)