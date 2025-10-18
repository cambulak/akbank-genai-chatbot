# ================================================================
#  Akbank GenAI Bootcamp - Kurumsal Sürdürülebilirlik Asistanı
#  ------------------------------------------------------------
#  Bu dosya, RAG (Retrieval-Augmented Generation) mimarisine
#  sahip bir Streamlit uygulamasıdır. Belgelerdeki sürdürülebilirlik
#  içeriklerini analiz edip kullanıcı sorularına bağlam temelli
#  yanıtlar üretir.
# ================================================================

# --- Gerekli kütüphanelerin import edilmesi ---
import os
import glob
import streamlit as st

# LangChain RAG bileşenleri
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers.multi_query import MultiQueryRetriever
# PDF yükleme ve metin bölme
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# FAISS veritabanı dizini (Streamlit Cloud'da /tmp klasörü yazılabilir olduğu için oraya alınabilir)
FAISS_INDEX_PATH = os.path.join(os.getenv("TMPDIR", "/tmp"), "faiss_index")

# ================================================================
#                  RAG SİSTEMİNİN YÜKLENMESİ
# ================================================================

@st.cache_resource
def load_and_build_db():
    """
    Tüm modelleri ve FAISS veritabanını yükler veya oluşturur.
    Bu işlem yalnızca ilk çalıştırmada yapılır, Streamlit tarafından cache'lenir.
    """

    print("Veritabanı kontrol ediliyor...")

    # --- 1. EMBEDDING MODELİ ---
    # Türkçe dahil çok dilli güçlü model: paraphrase-multilingual-mpnet-base-v2
    model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    # --- 2. FAISS VERİTABANI KONTROLÜ ---
    if os.path.exists(FAISS_INDEX_PATH):
        print("Mevcut FAISS veritabanı bulundu, yükleniyor...")
        db = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        print("Veritabanı bulunamadı. PDF'lerden yeni veritabanı oluşturuluyor...")

        # data klasöründeki tüm PDF’leri bul
        pdf_files = glob.glob("data/*.pdf")
        if not pdf_files:
            st.error("HATA: 'data' klasöründe PDF dosyası bulunamadı.")
            st.stop()

        all_documents = []
        for pdf_path in pdf_files:
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            for doc in documents:
                doc.metadata["source"] = os.path.basename(pdf_path)
            all_documents.extend(documents)

        # --- Metinleri parçalara ayırma ---
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        docs = text_splitter.split_documents(all_documents)

        # --- FAISS veritabanı oluşturma ---
        db = FAISS.from_documents(docs, embeddings)
        db.save_local(FAISS_INDEX_PATH)
        print("Yeni FAISS veritabanı oluşturuldu ve kaydedildi.")

    # --- 3. DİL MODELİ (LLM) ---
    # Gemini Pro kullanılıyor; düşük temperature değeri = daha tutarlı yanıtlar
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro-latest",
        temperature=0.1,
        convert_system_message_to_human=True
    )

    # --- 4. MULTIQUERY RETRIEVER ---
    # Kullanıcı sorgusunu LLM aracılığıyla farklı açılardan yeniden ifade ederek
    # daha kapsamlı bilgi getirimi sağlar.
    base_retriever = db.as_retriever(search_kwargs={'k': 7})
    retriever = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)

    print("Modeller ve retriever başarıyla hazırlandı.")
    return retriever, llm


# ================================================================
#               RAG ZİNCİRİNİN OLUŞTURULMASI
# ================================================================
def create_rag_chain(retriever, llm):
    """
    RAG zincirini oluşturur:
      - Kullanıcı sorusu alır
      - İlgili bağlamı retriever'dan çeker
      - LLM'e yönlendirir ve sonuç döner
    """

    # --- 5. PROMPT ŞABLONU ---
    # Türkçe açıklamalı, bağlama sadık kalan bir prompt.
    template = """
    ### TALİMAT:
    Sana verilen `BAĞLAM` bölümündeki bilgileri kullanarak `SORU` bölümündeki soruyu yanıtla.
    Cevap dışarıdan bilgi içermesin. Net, anlaşılır ve sohbet tarzında cevap ver.
    Eğer bağlamda yanıt yoksa, 'Bu konuda sağlanan dokümanlarda bilgi bulamadım.' de.
    Cevaplarını Türkçe ver.

    ### BAĞLAM:
    {context}

    ### SORU:
    {question}

    ### CEVAP:
    """
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    # --- 6. LANGCHAIN EXPRESSION LANGUAGE ZİNCİRİ ---
    # RAG akışını tanımlar.
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


# ================================================================
#                    STREAMLIT ARAYÜZÜ
# ================================================================

st.set_page_config(
    page_title="Kurumsal Sürdürülebilirlik Asistanı",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Kenar Çubuğu ---
with st.sidebar:
    st.image("assets/surdurulebilirlik_venn.png", use_container_width=True)
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

# --- Örnek Sorular ---
st.markdown("""
**Örnek Sorular:**
- Sürdürülebilir uygulamaların artırılması şirkete hangi katkıları sağlar?
- Sınırda karbon düzenlemesi nedir?
- Paris Anlaşması nedir?
- Kurumsal Yönetim nedir?
- Karbon tutma nedir?
""")
st.markdown("---")

# --- API ANAHTARI KONTROLÜ ---
# Streamlit Cloud'da secrets.toml içinde, lokal çalışmada ise os.environ'dan alınır.
api_key = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
if not api_key:
    st.error("HATA: GOOGLE_API_KEY bulunamadı. Lütfen secrets veya ortam değişkenine ekleyin.")
    st.stop()
os.environ["GOOGLE_API_KEY"] = api_key

# --- RAG Sisteminin Başlatılması ---
try:
    retriever, llm = load_and_build_db()
    rag_chain = create_rag_chain(retriever, llm)
except Exception as e:
    st.error(f"Başlatma sırasında hata oluştu: {e}")
    st.stop()

# --- Sohbet Geçmişi Yönetimi ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Merhaba! Sürdürülebilirlik veya ÇSY konularında nasıl yardımcı olabilirim?"}
    ]

# Geçmiş mesajları yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Yeni Kullanıcı Girdisi ---
if prompt := st.chat_input("Sürdürülebilirlik stratejisi, raporlama veya bir terim hakkında soru sorun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Belgeler analiz ediliyor ve yanıt hazırlanıyor..."):
            # Belge kaynaklarını getir (MultiQueryRetriever kullandığımız için base retriever üzerinden)
            try:
                retrieved_docs = retriever.retriever.get_relevant_documents(prompt)
            except:
                retrieved_docs = []

            # Cevabı stream halinde yazdır
            response_stream = rag_chain.stream(prompt)
            full_response = st.write_stream(response_stream)

            # Kaynakları göster
            with st.expander("Yanıtın Kaynaklarını Gör"):
                if retrieved_docs:
                    for doc in retrieved_docs:
                        source_name = doc.metadata.get('source', 'Bilinmiyor')
                        page_number = doc.metadata.get('page', None)
                        if page_number is not None:
                            page_number += 1
                        else:
                            page_number = 'Belirtilmemiş'
                        st.info(f"**Kaynak:** {source_name} - **Sayfa:** {page_number}")
                        st.caption(doc.page_content[:500] + "...")
                else:
                    st.warning("Kaynak bilgisi alınamadı.")

    st.session_state.messages.append({"role": "assistant", "content": full_response})

st.markdown("---")
st.caption("Bu asistanın bilgi tabanı, Borsa İstanbul Sürdürülebilirlik Rehberi ve Erdem & Erdem ÇSY Terimler Sözlüğü dokümanlarından oluşturulmuştur.")
