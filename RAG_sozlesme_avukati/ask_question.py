"""
problem tanımı: sozlesme asistanı-herhangi bir dosya ile konuşmak,kullanıcının yüklediği dosyadan içerik çıkarmak
    - kullanicinin yukledigi bir sozlesme dosyasindan icerik cikarmak
    - bu icerigi vektorel olarak temsil edelim yani (embedding)
    - faiss kullanarak hizli arama yapabilen bir vektor veri tabani olustur
    - kullanicisorularini al, sonra git db den bilgiyi getir, sonra gpt 3.5 ile cevapla

# elimizdeki pdften gelen metinleri dbde metin olarak saklamak yerine vektör uzatına taşıyıp  (embedding) saklıyoruz çünkü saklaması,erimi,bilgi çıkarımı daha kolay

user->soru sorgu->db(faiss)->llm(gpt)->cevap olayi

kullanılan teknolojiler:
    - embedding: metni vektorlestirme
    - faiss: hizli benzerlik aramasi icin vektor veri tabani
    - gpt 3.5: metin uretimi ve cevaplama

RAG: Retrieval Augmented Generation: dil modellerine bilgi destegi saglayan bir teknik
    - kullanici sorularini al, ilgili bilgiyi veritabanindan getir, sonra gpt ile cevapla
    - retrieval: kullanici sorusu embedding e donusturulur, faiss(db) uzerinden en alakalı icerik (chunk) getiriliyor
    - augmentation: zenginlestirme, bulunan metin parcalari llm'in anlayabilecegi bir formata donusturuluyor
    - generation: dil modeli bu bilgiler ile mantikli yanit uretir
        - 1) tarih
        - 2) ücret
        - 3) taraflar Ucanble Teknoloji - KCY

Plan/program
    - sozlesme belgesinin hazirlanmasi
    - metin cikarma ve parcalama
    - embedding ve faiss ile vector db olusturma
    - soru cevap sistemi

install libraries: freeze

#Ragde bir vektör databsei var verileri sayısal.vektörel olarak depolama. bunun için bir db oluştur
#vektör dbden aldığımız bilgileri işleyebilmek için ask_ques dosyasını kullanacağız


"""
# import libaries
import os
import pickle
import faiss # databastende veri cekmek icin
import numpy as np # numpy
from sentence_transformers import SentenceTransformer #embedding yapılacak kütüphane
from dotenv import load_dotenv #env dosyasından ortam degiskenlerini yuklemek icin

from openai import OpenAI #openai apı kullanmak için

# .env dosyasindan ortam degiskenlerini yukle
load_dotenv()

# openai api anhatarinin ortam degiskeninden alinmasi
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key) # oepnai istemcisi

# sentence transformers modelimiz, kucuk ve hizli bir embedding modeli
model = SentenceTransformer("all-MiniLM-L6-v2")

# faiss index dosyasini yukle (onceden olusturulmus vektor veritabanimiz)
index = faiss.read_index(".\data\contract_index.faiss")

# chunklanmis metin verisini yukle
with open("data/contract_chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

# kullanicidan gelen sorulari al
while True:

    # kullanicidan soru al
    #vektör dbyi ingilizce oluşturduk soruyu ingilizce girmelisin contract ingilizce olduğu için
    #türkçe dilinde embedding yapabilecek modeller ve çok dilli modeller var 
    question = input("\n Sorunuzu giriniz: (Eng)")

    # cikmak istersek donguyu sonlandir
    if question.lower() in ["exit", "quit", "q"]:
        print("Cikisi yapiliyor...")
        break

    # kullanicinin sorularini vektore cevirmemiz lazim yani embedding
    question_embedding = model.encode([question])

    # faiss veri tabanindan en yakin 3 chunk i ara
    k = 3 # en yakin 3 chunk
    distances, indices = index.search(np.array(question_embedding), k)

    # bulunan chunklari birlestirerek bagalm yani contexxt olustur
    retrieved_chunks = [chunks[i] for i in indices[0]]  # ilk satirdaki chunklar
    context = "\n ---- \n".join(retrieved_chunks)

    # llm'e gonderielcek bir sistem prompt u yaz
    prompt = f"""
            You are a contract lawyer AI assistant. Based on the contract context below, 
            answer the user's question clearly.

            Context: 
            {context}

            Question:
            {question}

            Answer:
    """

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [{"role":"user", "content":prompt}],
        temperature=0.2 # daha kararki cevaplar icin dusuk deger,yüksek değer yazılırsa halüsinasyon gorur
    )

    print("AI Assistant: \n", response.choices[0].message.content.strip())