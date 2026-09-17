"""
Vector Database Builder
Faiss is a library for efficient similarity search and clustering of dense vectors.
"""


# import libraries
import os
import pymupdf # PyMuPDF
from sentence_transformers import SentenceTransformer # embedding
import faiss # vektor veritabanı
import numpy as np
import pickle # for saving the vector database

# program icin dosya olarak .pdf yukleyelim
# .pdf den metin donusumu yapmamiz lazim
def extract_text_from_pdf(pdf_path):
    """
        pdf dosyasindan metin cikartma
    """
    doc = pymupdf.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    return text

# print(extract_text_from_pdf(".\data\sample_contract_ucanble.pdf"))
# pdfi texte çevirdik şimdi küçük chunklara bölmemiz gerekiyor

#gerçek projelerde paragraf veya başlık. ayrıca böldükten sonra chunklar arasında bağlamsal olanları ayrıca başka bir yerde birleştirip böllme yapılır
# uzun metni daha kucuk parcalara bol
def chunk_text(text, max_length=500):
    """
         metni belirtilen karakter uzunluguna gore bol
    """
    chunks = []
    current = ""
    for line in text.split("\n"):
        if len(current) + len(line) < max_length:
            current += " " + line.strip()
        else:
            chunks.append(current.strip())
            current = line.strip()
    if current:
        chunks.append(current.strip())
    
    return chunks

# text_dummy = extract_text_from_pdf(".\data\sample_contract_ucanble.pdf")
# print(chunk_text(text_dummy, max_length=500))

# sentence transformer ile embedding
# https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
model = SentenceTransformer("all-MiniLM-L6-v2")

# pdf yolunu belirt
pdf_file_path = ".\data\sample_contract_ucanble.pdf"

# pdf ten metin cikartalim
text = extract_text_from_pdf(pdf_file_path)

# metni chunklara bolelim
chunks = chunk_text(text, max_length=500)

# her chunk icin embedding (vektorel temsil) olusturalim
embeddings = model.encode(chunks)

print(f"embeddings shape: {embeddings.shape}")  # (n_chunks, embedding_dim)

# faiss index olustur
dimension = embeddings.shape[1]  # embedding (vektor) boyutu
index = faiss.IndexFlatL2(dimension) # L2 norm (Euclidean distance) kullanarak benzerlik arama
index.add(np.array(embeddings)) # embeddingleri indexe ekle 

# faiss indexi ve chunklari kaydet
faiss.write_index(index, "data/contract_index.faiss")
with open("data/contract_chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("faiss index ve chunklar kaydedildi.")