# app.py

import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# Veri işleme için ek kütüphaneler
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Veritabanının kaydedileceği yol
FAISS_INDEX_PATH = "faiss_index"


@st.cache_resource
def load_and_build_db():
    """
    Uygulama başladığında veritabanını yükler veya yoksa oluşturur.
    Bu fonksiyonun sonucu cache'lenir, böylece sadece bir kere çalışır.
    """
    print("Veritabanı kontrol ediliyor ve yükleniyor...")

    # Embedding modelini yükle
    model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    # Eğer veritabanı zaten oluşturulmuşsa, doğrudan yükle
    if os.path.exists(FAISS_INDEX_PATH):
        print("Mevcut veritabanı bulundu, yükleniyor.")
        db = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        # Eğer veritabanı yoksa, PDF'ten oluştur
        print("Veritabanı bulunamadı, PDF'ten oluşturuluyor. Bu işlem biraz zaman alabilir...")

        # --- DEĞİŞİKLİK BURADA ---
        pdf_path = "data/esg_dic.pdf"
        # -------------------------

        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)

        db = FAISS.from_documents(docs, embeddings)
        db.save_local(FAISS_INDEX_PATH)
        print("Veritabanı oluşturuldu ve kaydedildi.")

    # Retriever'ı oluştur
    retriever = db.as_retriever(search_kwargs={'k': 3})

    # Google Dil Modelini (LLM) Tanımla
    llm = ChatGoogleGenerativeAI(model="gemini-pro-latest", temperature=0.1, convert_system_message_to_human=True)

    print("Modeller ve veritabanı başarıyla hazırlandı.")
    return retriever, llm


def create_rag_chain(retriever, llm):
    """Verilen retriever ve llm ile RAG zincirini oluşturur."""
    template = """
    ### TALİMAT:
    Sadece sana verilen `BAĞLAM` bölümündeki bilgileri kullanarak `SORU` bölümündeki soruyu yanıtla. Cevabın dışarıdan bilgi içermemelidir. Eğer bağlamda sorunun cevabı yoksa, 'Bu konuda sağlanan dokümanda bir bilgi bulamadım.' de. Cevaplarını Türkçe ve anlaşılır bir dille yaz.

    ### BAĞLAM:
    {context}

    ### SORU:
    {question}

    ### CEVAP:
    """
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    return {"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()


# --- Ana Streamlit Uygulaması ---

st.title("📖 ÇSY Terimler Sözlüğü Chatbot'u")
st.write(
    "Bu chatbot, Erdem & Erdem tarafından hazırlanan ÇSY Terimler Sözlüğü'ndeki bilgileri kullanarak sorularınızı yanıtlar.")

# API anahtarını Streamlit Secrets'tan kontrol et
if 'GOOGLE_API_KEY' not in st.secrets:
    st.error("HATA: GOOGLE_API_KEY bulunamadı. Lütfen Streamlit Cloud ayarlarından 'Secrets' bölümüne ekleyin.")
    st.stop()

# Modelleri ve veritabanını yükle
try:
    retriever, llm = load_and_build_db()
    rag_chain = create_rag_chain(retriever, llm)
except Exception as e:
    st.error(f"Başlangıç sırasında bir hata oluştu: {e}")
    st.stop()

# Sohbet geçmişini yönet
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan girdi al ve sohbeti yürüt
if prompt := st.chat_input("ÇSY ile ilgili bir terim sorun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Düşünüyorum..."):
            response = rag_chain.invoke(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})