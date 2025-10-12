# create_database.py

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

print("Gerekli kütüphaneler yüklendi.")

# 1. PDF'i Yükle
pdf_path = "data/esg_dic.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()
print(f"'{pdf_path}' dosyasından {len(documents)} sayfa doküman başarıyla yüklendi.")

# 2. Metinleri Parçalara Ayır (Chunking)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)
print(f"Dokümanlar toplam {len(docs)} adet metin parçasına (chunk) bölündü.")

# 3. Daha Güçlü Hugging Face Embedding Modelini Başlat
print("Daha güçlü Hugging Face embedding modeli başlatılıyor...")
# --- DEĞİŞİKLİK BURADA ---
model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
# -------------------------
embeddings = HuggingFaceEmbeddings(model_name=model_name)

# 4. Vektör Veritabanını Oluştur ve Kaydet
print("Vektör veritabanı yeni modelle oluşturuluyor. Bu işlem birkaç dakika sürebilir...")
db = FAISS.from_documents(docs, embeddings)

db.save_local("faiss_index_csy_hf_new") # Yeni model için yeni bir klasör adı
print("\nİşlem tamamlandı! Yeni veritabanı 'faiss_index_csy_hf_new' klasörüne kaydedildi.")