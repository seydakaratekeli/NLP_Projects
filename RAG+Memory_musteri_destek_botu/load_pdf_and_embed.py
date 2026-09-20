from langchain_openai import OpenAIEmbeddings # langchainin openai tabanlı vektör temsili modeli
from langchain_community.vectorstores import FAISS # vektör database
from langchain_community.document_loaders import PyPDFLoader # pdf dosyasından metin çıkarma işlemi için gerekli
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter # metni daha kucuk parcalara bolme (chunk)


from dotenv import load_dotenv 
import os

load_dotenv() # api key yukleme

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is not found")

# openai api anahtarini sistem ortam degiskenlerine tanimliyoruz
os.environ["OPENAI_API_KEY"] = api_key

# sık sorulan sorular dosyasını yukle
loader = PyPDFLoader("musteri_destek_faq.pdf")

# langchain documents objesi olustur
documents = loader.load()

# metinleri parçalamak için 
# splitter, metni anlamlı parçalara ayırırken cümle veya paragraf bütünlüğünü korumaya çalışıyor
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500, # her parça maksimum 500 karakter içerecek demek, bunu soruların uzunluğuna göre değiştirebiliriz soru ve cevabı alacak şekilde optimumu seç gerçek projelerde
    chunk_overlap = 50 # her parça bir öncekinden 50 karakter alabilir, bağlam kaybını önlemek için
)

# chunklari olustur
docs = text_splitter.split_documents(documents)
#chunklar şu an metin şeklinde, bunlari vektore donusturecegiz

# openai embedding modeli
# text embedding 3 large modeli kaliteli ve turkce destegi cok iyi
embedding = OpenAIEmbeddings(model = "text-embedding-3-large")

# faiss vektor veritabanı, parçalara ayrılmış metni embedding ile vektör haline getirir ve indeks oluşturur
vectordb = FAISS.from_documents(docs, embedding)

# olusturulan vektor veritabanını yerel disske kaydet
vectordb.save_local("faq_vectorstore")

print("Embedding ve vektör veri tabanı başarılı bir şekilde oluşturuldu")

#burada oluşturduğumuz vektör veritabanını kullanarak LLM ile akıllı bir şekilde soru yanıtlanacak bir sistem olusturacagız
#bu sistemde