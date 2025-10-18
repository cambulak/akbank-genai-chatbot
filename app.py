# app.py

import os
import streamlit as st
import glob

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.retrievers.multi_query import MultiQueryRetriever

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

FAISS_INDEX_PATH = "faiss_index"


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

    llm = ChatGoogleGenerativeAI(model="gemini-pro-latest", temperature=0.1, convert_system_message_to_human=True)

    base_retriever = db.as_retriever(search_kwargs={'k': 7})
    retriever = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)

    print("Modeller ve Multi-Query Retriever başarıyla hazırlandı.")
    return retriever, llm


def create_rag_chain(retriever, llm):
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
    return {"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()


# --- Ana Streamlit Uygulaması ---
st.set_page_config(page_title="Kurumsal Sürdürülebilirlik Asistanı", layout="wide", initial_sidebar_state="expanded")

# --- DEĞİŞİKLİK BURADA: Sidebar'a fotoğrafı ekliyoruz ---
with st.sidebar:
    # Fotoğrafı ekle
    st.image("assets/surdurulebilirlik_venn.png", use_column_width=True)

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
# ----------------------------------------------------

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
    retriever, llm = load_and_build_db()
    rag_chain = create_rag_chain(retriever, llm)
except Exception as e:
    st.error(f"Başlangıç sırasında bir hata oluştu: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": "Merhaba! Sürdürülebilirlik veya ÇSY konularında size nasıl yardımcı olabilirim?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sürdürülebilirlik stratejisi, raporlama veya bir terim hakkında soru sorun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("İlgili belgeleri arıyorum..."):
            retrieved_docs = retriever.get_relevant_documents(prompt)

        response_stream = rag_chain.stream(prompt)
        full_response = st.write_stream(response_stream)

        with st.expander("Yanıtın Kaynaklarını Gör"):
            for doc in retrieved_docs:
                source_name = doc.metadata.get('source', 'Bilinmiyor')
                page_number = doc.metadata.get('page', 'Bilinmiyor')
                if page_number != 'Bilinmiyor':
                    page_number += 1
                st.info(f"**Kaynak:** {source_name} - **Sayfa:** {page_number}")
                st.caption(doc.page_content)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

st.markdown("---")
st.caption(
    "Bu asistanın bilgi tabanı, Borsa İstanbul Sürdürülebilirlik Rehberi ve Erdem & Erdem ÇSY Terimler Sözlüğü dokümanlarından oluşturulmuştur.")