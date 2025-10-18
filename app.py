# app.py

import os
import glob
import streamlit as st

# .env dosyasından ortam değişkenlerini yüklemek için
from dotenv import load_dotenv
try:
    from langchain.retrievers.multi_query import MultiQueryRetriever
except ImportError:
    from langchain.retrievers import MultiQueryRetriever
# LangChain'in RAG mimarisi için temel bileşenleri
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers.multi_query import MultiQueryRetriever

# PDF okuma ve metin bölme işlemleri için kütüphaneler
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# LOKAL ÇALIŞMA İÇİN .env DOSYASINI YÜKLÜYORUZ
# Bu satır, .env dosyasındaki değişkenleri os.environ'a yükler
load_dotenv()

# Vektör veritabanının diskte saklanacağı klasör adı
FAISS_INDEX_PATH = 'faiss_index_csy_hf_new'  # (İlk koddaki isme döndürdüm, sizinkiyle aynı olması için)


# --- RAG SİSTEMİNİN KURULUMU VE MODELLERİN YÜKLENMESİ ---

@st.cache_resource
def load_and_build_db():
    """
    Uygulama başladığında modelleri ve vektör veritabanını yükler veya yoksa oluşturur.
    """
    print("Veritabanı kontrol ediliyor ve yükleniyor...")

    # --- 1. EMBEDDING MODELİ ---
    model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    # --- 2. VEKTÖR VERİTABANI ---
    if os.path.exists(FAISS_INDEX_PATH):
        print("Mevcut veritabanı bulundu, yükleniyor.")
        db = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        print("Veritabanı bulunamadı, PDF'lerden oluşturuluyor...")
        pdf_files = glob.glob("data/*.pdf")
        if not pdf_files:
            st.error("HATA: 'data' klasöründe okunacak PDF dosyası bulunamadı.")
            st.stop()

        all_documents = []
        for pdf_path in pdf_files:
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            for doc in documents:
                doc.metadata["source"] = os.path.basename(pdf_path)
            all_documents.extend(documents)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        docs = text_splitter.split_documents(all_documents)

        db = FAISS.from_documents(docs, embeddings)
        db.save_local(FAISS_INDEX_PATH)
        print("Veritabanı oluşturuldu ve kaydedildi.")

    # --- 3. DİL MODELİ (LLM) ---
    # ChatGoogleGenerativeAI, load_dotenv() sayesinde API anahtarını
    # otomatik olarak ortam değişkenlerinden (os.environ) bulacaktır.
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro", temperature=0.1, convert_system_message_to_human=True)
    # Not: Model adını "gemini-pro-latest" yerine "gemini-pro" olarak değiştirdim,
    # "latest" bazen sorun çıkarabiliyor. İsterseniz geri değiştirebilirsiniz.

    # --- 4. RETRIEVER (BİLGİ GETİRİCİ) ---
    base_retriever = db.as_retriever(search_kwargs={'k': 20})
    retriever = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)

    print("Modeller ve Multi-Query Retriever başarıyla hazırlandı.")
    return retriever, llm


def create_rag_chain(retriever, llm):
    """
    Verilen retriever ve llm ile RAG (Retrieval-Augmented Generation) zincirini oluşturur.
    """
    # --- 5. PROMPT ŞABLONU ---
    template = """
    ### TALİMAT:
    Sana verilen `BAĞLAM` bölümündeki bilgileri kullanarak `SORU` bölümündeki soruyu yanıtla. Cevabın dışarıdan bilgi içermemelidir. Cevabın net, anlaşılır ve sohbet formatında olsun. Eğer bağlamda sorunun cevabı yoksa, 'Bu konuda sağlanan dokümanlarda bir bilgi bulamadım.' de. Cevaplarını Türkçe ver.

    ### BAĞLAM:
    {context}

    ### SORU:
    {question}

    ### CEVAP:
    """
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    # --- 6. LANGCHAIN EXPRESSION LANGUAGE (LCEL) ZİNCİRİ ---
    return {"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()


# --- STREAMLIT ARAYÜZÜ ---

# Sayfa konfigürasyonu
st.set_page_config(page_title="Kurumsal Sürdürülebilirlik Asistanı", layout="wide", initial_sidebar_state="expanded")

# Kenar Çubuğu (Sidebar)
with st.sidebar:
    #st.image("assets/surdurulebilirlik_venn.png", use_container_width=True)  # Bu dosyanın olduğundan emin olun
    st.title("🌱 Kurumsal Sürdürülebilirlik Asistanı")
    st.markdown("""
    Bu asistan, RAG mimarisi kullanarak aşağıdaki belgelerdeki bilgilere göre sorularınızı yanıtlar:
    - **Erdem & Erdem - ÇSY Terimler Sözlüğü**
    - **Borsa İstanbul - Sürdürülebilirlik Rehberi**
    """)
    st.markdown("---")

    if st.button("Sohbeti Temizle", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Akbank GenAI Bootcamp Projesi")

# Örnek Sorular Bölümü
st.markdown("""
**Örnek Sorular:**
- Sürdürülebilir uygulamaların artırılması şirkete hangi katkıları sağlar?
- Sınırda karbon düzenlemesi nedir?
- Paris Anlaşması nedir?
- Kurumsal Yönetim nedir?
- Karbon tutma nedir?
""")
st.markdown("---")

# --- LOKAL API ANAHTARI KONTROLÜ ---
# Artık st.secrets yerine os.environ'u (ortam değişkenlerini) kontrol ediyoruz
if not os.environ.get("GOOGLE_API_KEY"):
    st.error("HATA: GOOGLE_API_KEY bulunamadı. Lütfen `.env` dosyanıza anahtarınızı ekleyin.")
    st.stop()
# --- KONTROL TAMAMLANDI ---

# Ana RAG sistemini başlat
try:
    retriever, llm = load_and_build_db()
    rag_chain = create_rag_chain(retriever, llm)
except Exception as e:
    st.error(f"Başlangıç sırasında bir hata oluştu: {e}")
    st.info(
        "Lütfen GOOGLE_API_KEY anahtarınızın doğru olduğundan ve 'Vertex AI' API'sinin Google Cloud projenizde etkinleştirildiğinden emin olun.")
    st.stop()

# Sohbet Geçmişi Yönetimi
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": "Merhaba! Sürdürülebilirlik veya ÇSY konularında size nasıl yardımcı olabilirim?"}
    ]

# Geçmiş mesajları ekrana yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan yeni girdi al ve sohbeti yürüt
if prompt := st.chat_input("Sürdürülebilirlik stratejisi, raporlama veya bir terim hakkında soru sorun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Asistanın cevabını oluştur
    with st.chat_message("assistant"):
        with st.spinner("İlgili belgeleri arıyorum ve yanıt oluşturuyorum..."):
            try:
                # Önce kaynakları bul
                retrieved_docs = retriever.get_relevant_documents(prompt)

                # Cevabı akış halinde (streaming) yazdır
                response_stream = rag_chain.stream(prompt)
                full_response = st.write_stream(response_stream)

                # Kaynakları göster
                with st.expander("Yanıtın Kaynaklarını Gör"):
                    for doc in retrieved_docs:
                        source_name = doc.metadata.get('source', 'Bilinmiyor')
                        page_number = doc.metadata.get('page', 'Bilinmiyor')
                        if page_number != 'Bilinmiyor':
                            page_number += 1  # Sayfa numaraları 0'dan başladığı için
                        st.info(f"**Kaynak:** {source_name} - **Sayfa:** {page_number}")
                        st.caption(doc.page_content)

                # Asistanın tam cevabını sohbet geçmişine ekle
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"Yanıt oluşturulurken bir hata oluştu: {e}")

st.markdown("---")
st.caption(
    "Bu asistanın bilgi tabanı, Borsa İstanbul Sürdürülebilirlik Rehberi ve Erdem & Erdem ÇSY Terimler Sözlüğü dokümanlarından oluşturulmuştur.")