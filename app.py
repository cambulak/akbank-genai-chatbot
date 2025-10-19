# app.py

import os
import glob
import streamlit as st

from langchain_core.messages import HumanMessage

# --- LangChain & Embeddings ---

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

FAISS_INDEX_PATH = "faiss_index"


# --- Veritabanını yükle veya oluştur ---
@st.cache_resource
def load_and_build_db():
    print("Veritabanı kontrol ediliyor ve yükleniyor...")

    model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    if os.path.exists(FAISS_INDEX_PATH):
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

    # --- LLM ---
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro-latest",
        temperature=0.1,
        convert_system_message_to_human=True
    )

    print("Modeller başarıyla hazırlandı.")
    return db, llm


# --- Streamlit UI ---
st.set_page_config(
    page_title="Kurumsal Sürdürülebilirlik Asistanı",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.title("🌱 Kurumsal Sürdürülebilirlik Asistanı")
    st.markdown("""
    Bu asistan, PDF dokümanlarındaki bilgilere göre sorularınızı yanıtlar:
    - **Erdem & Erdem - ÇSY Terimler Sözlüğü**
    - **Borsa İstanbul - Sürdürülebilirlik Rehberi**
    """)
    st.markdown("---")

    if st.button("Sohbeti Temizle", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Akbank GenAI Bootcamp Projesi")

st.markdown("""
**Örnek Sorular:**
- Sürdürülebilir uygulamaların artırılması şirkete hangi katkıları sağlar?
- Sınırda karbon düzenlemesi nedir?
- Paris Anlaşması nedir?
- Kurumsal Yönetim nedir?
- Karbon tutma nedir?
""")
st.markdown("---")

if 'GOOGLE_API_KEY' not in st.secrets:
    st.error("HATA: GOOGLE_API_KEY bulunamadı. Lütfen Streamlit Cloud ayarlarından 'Secrets' bölümüne ekleyin.")
    st.stop()

try:
    db, llm = load_and_build_db()
except Exception as e:
    st.error(f"Başlangıç sırasında bir hata oluştu: {e}")
    st.stop()

# --- Chat geçmişi ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": "Merhaba! Sürdürülebilirlik veya ÇSY konularında size nasıl yardımcı olabilirim?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input ---
if prompt := st.chat_input("Sürdürülebilirlik stratejisi, raporlama veya bir terim hakkında soru sorun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("İlgili belgeleri arıyor ve yanıt oluşturuluyor..."):
            # --- FAISS ile similarity search ---
            docs = db.similarity_search(prompt, k=7)
            context_text = "\n\n".join([doc.page_content for doc in docs])

            # Prompt hazırla
            full_prompt = f"""
### BAĞLAM:
{context_text}

### SORU:
{prompt}

### CEVAP:
"""

            # LLM ile cevap üret
            response = llm.generate([[HumanMessage(content=full_prompt)]])
            answer = response.generations[0][0].text

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

st.markdown("---")
st.caption(
    "Bu asistanın bilgi tabanı, Borsa İstanbul Sürdürülebilirlik Rehberi ve Erdem & Erdem ÇSY Terimler Sözlüğü dokümanlarından oluşturulmuştur."
)
