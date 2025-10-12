# app.py

import os
import streamlit as st  # Streamlit kütüphanesini import ediyoruz
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser


# --- Konfigurasyon ve Model Yükleme Fonksiyonları ---
# Bu fonksiyonlar sadece bir kere çalışacak ve sonuçları cache'lenecek.
# Bu sayede her kullanıcı girişi olduğunda modeller yeniden yüklenmeyecek.

@st.cache_resource
def load_models_and_db():
    """
    Uygulama başladığında modelleri ve veritabanını yükler.
    """
    print("Modeller ve veritabanı yükleniyor...")

    # Embedding Modelini Yükle
    model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    # Yerel Vektör Veritabanını Yükle
    db = FAISS.load_local("faiss_index_csy_hf_new", embeddings, allow_dangerous_deserialization=True)

    # Retriever'ı Oluştur
    retriever = db.as_retriever(search_kwargs={'k': 3})

    # Google Dil Modelini (LLM) Tanımla
    KULLANILACAK_MODEL = "gemini-pro-latest"
    llm = ChatGoogleGenerativeAI(model=KULLANILACAK_MODEL, temperature=0.1, convert_system_message_to_human=True)

    print("Modeller ve veritabanı başarıyla yüklendi.")
    return retriever, llm


def create_rag_chain(retriever, llm):
    """
    Verilen retriever ve llm ile RAG zincirini oluşturur.
    """
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

    rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )
    return rag_chain


# --- Ana Streamlit Uygulaması ---

# API anahtarını kontrol et (uygulama başlamadan önce)
if "GOOGLE_API_KEY" not in os.environ:
    st.error("HATA: GOOGLE_API_KEY ortam değişkeni bulunamadı. Lütfen ayarlayın.")
    st.stop()

# Başlık
st.title("📖 ÇSY Terimler Sözlüğü Chatbot'u")
st.write(
    "Bu chatbot, Erdem & Erdem tarafından hazırlanan ÇSY Terimler Sözlüğü'ndeki bilgileri kullanarak sorularınızı yanıtlar.")

# Modelleri ve veritabanını yükle
try:
    retriever, llm = load_models_and_db()
    rag_chain = create_rag_chain(retriever, llm)
except Exception as e:
    st.error(f"Modeller yüklenirken bir hata oluştu: {e}")
    st.stop()

# Sohbet geçmişini yönetmek için session state kullan
if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmiş mesajları ekrana yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan yeni bir girdi al
if prompt := st.chat_input("ÇSY ile ilgili bir terim sorun..."):
    # Kullanıcının mesajını sohbet geçmişine ekle ve ekrana yazdır
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Chatbot'un cevabını oluştur
    with st.chat_message("assistant"):
        with st.spinner("Düşünüyorum..."):
            response = rag_chain.invoke(prompt)
            st.markdown(response)

    # Chatbot'un cevabını sohbet geçmişine ekle
    st.session_state.messages.append({"role": "assistant", "content": response})