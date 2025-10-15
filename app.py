# app.py

# Gerekli kütüphaneleri import ediyoruz
import os
import streamlit as st
import glob

# LangChain'in RAG mimarisi için temel bileşenleri
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.retrievers.multi_query import MultiQueryRetriever

# PDF okuma ve metin bölme işlemleri için kütüphaneler
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Vektör veritabanının diskte saklanacağı klasör adı
FAISS_INDEX_PATH = "faiss_index"


# --- RAG SİSTEMİNİN KURULUMU VE MODELLERİN YÜKLENMESİ ---

# @st.cache_resource, Streamlit'in bu fonksiyonu sadece bir kere çalıştırmasını sağlar.
# Bu, modellerin ve veritabanının her kullanıcı etkileşiminde yeniden yüklenmesini engelleyerek
# uygulamayı inanılmaz derecede hızlandıran bir optimizasyon yöntemidir.
@st.cache_resource
def load_and_build_db():
    """
    Uygulama başladığında modelleri ve vektör veritabanını yükler veya yoksa oluşturur.
    Bu fonksiyon, tüm ağır yükü (model indirme, PDF işleme, veritabanı oluşturma)
    sadece uygulamanın ilk açılışında bir kereliğine yapar.
    """
    print("Veritabanı kontrol ediliyor ve yükleniyor...")

    # 1. EMBEDDING MODELİ
    # Metinleri anlamsal vektörlere dönüştürmek için kullanılacak model.
    # 'paraphrase-multilingual-mpnet-base-v2' modeli, Türkçe dahil birçok dili
    # yüksek performansla anlama yeteneği sayesinde seçilmiştir. Bu, RAG sisteminin
    # "Retrieval" (Bilgi Getirme) adımının kalitesini doğrudan belirler.
    model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    # 2. VEKTÖR VERİTABANI
    # Eğer daha önce oluşturulmuş bir veritabanı diskte varsa, onu yükle.
    # Bu, uygulamanın yeniden başlatıldığında PDF'leri tekrar işlemesini engeller.
    if os.path.exists(FAISS_INDEX_PATH):
        print("Mevcut veritabanı bulundu, yükleniyor.")
        db = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        # Eğer veritabanı yoksa (örneğin ilk çalıştırma veya deploy sonrası)
        # 'data' klasöründeki tüm PDF'lerden yeni bir veritabanı oluştur.
        print("Veritabanı bulunamadı, PDF'lerden oluşturuluyor...")

        # 'data' klasöründeki tüm .pdf uzantılı dosyaları bul.
        pdf_files = glob.glob("data/*.pdf")
        if not pdf_files:
            st.error("HATA: 'data' klasöründe okunacak PDF dosyası bulunamadı.")
            st.stop()

        # Tüm PDF'lerden gelen dokümanları birleştirmek için bir liste oluştur.
        all_documents = []
        for pdf_path in pdf_files:
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            # Her bir dokümanın metadatasına, hangi dosyadan geldiği bilgisini ekliyoruz.
            # Bu, daha sonra cevap kaynaklarını gösterirken çok işe yarayacak.
            for doc in documents:
                doc.metadata["source"] = os.path.basename(pdf_path)
            all_documents.extend(documents)

        # Metinleri daha küçük ve yönetilebilir parçalara (chunks) böl.
        # chunk_overlap, parçalar arası anlam bütünlüğünü korumaya yardımcı olur.
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        docs = text_splitter.split_documents(all_documents)

        # Parçalanmış metinlerden ve embedding modelinden FAISS veritabanını oluştur.
        db = FAISS.from_documents(docs, embeddings)
        # Oluşturulan veritabanını diskte bir sonraki kullanım için kaydet.
        db.save_local(FAISS_INDEX_PATH)
        print("Veritabanı oluşturuldu ve kaydedildi.")

    # 3. DİL MODELİ (LLM)
    # Cevapları üretecek olan ana model. Google'ın Gemini Pro modelini kullanıyoruz.
    llm = ChatGoogleGenerativeAI(model="gemini-pro-latest", temperature=0.1, convert_system_message_to_human=True)

    # 4. RETRIEVER (BİLGİ GETİRİCİ)
    # Bu, RAG sisteminin en önemli optimizasyonlarından biridir.
    # Kullanıcının tek bir sorusunu alıp, LLM'i kullanarak o soruyu farklı açılardan
    # yeniden ifade eden birden çok alt sorgu üretir. Bu, cevabı dokümanların farklı
    # yerlerine yayılmış karmaşık sorular için bile ilgili tüm bilgi parçalarını toplama
    # başarısını büyük ölçüde artırır.
    base_retriever = db.as_retriever(search_kwargs={'k': 7})
    retriever = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)

    print("Modeller ve Multi-Query Retriever başarıyla hazırlandı.")
    return retriever, llm


def create_rag_chain(retriever, llm):
    """
    Verilen retriever ve llm ile RAG (Retrieval-Augmented Generation) zincirini oluşturur.
    Bu zincir, kullanıcı sorusundan nihai cevaba giden tüm adımları düzenler.
    """
    # 5. PROMPT ŞABLONU
    # LLM'e ne yapması gerektiğini söyleyen talimatlar bütünüdür.
    # {context} -> Retriever'dan gelen bilgi parçaları
    # {question} -> Kullanıcının orijinal sorusu
    # Bu şablon, modelin sadece kendisine verilen bağlama sadık kalmasını sağlayarak
    # "halüsinasyon" görmesini (bilgi uydurmasını) engeller.
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

    # 6. LANGCHAIN EXPRESSION LANGUAGE (LCEL) ZİNCİRİ
    # Boru (pipe |) operatörü ile adımları birbirine bağlarız:
    # 1. `retriever` ve `question` paralel olarak çalışır.
    # 2. Çıktıları `prompt` şablonuna beslenir.
    # 3. Doldurulan prompt `llm`'e gönderilir.
    # 4. LLM'in cevabı `StrOutputParser` ile temiz bir metne dönüştürülür.
    return {"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()


# --- STREAMLIT ARAYÜZÜ ---

# Sayfa konfigürasyonu (başlık, layout vb.)
st.set_page_config(page_title="Kurumsal Sürdürülebilirlik Asistanı", layout="wide", initial_sidebar_state="expanded")

# Kenar Çubuğu (Sidebar)
# Arayüzü temiz tutmak için bilgilendirici metinleri ve butonları buraya koyuyoruz.
with st.sidebar:
    st.title("🌱 Kurumsal Sürdürülebilirlik Asistanı")
    st.markdown("""
    Bu asistan, RAG mimarisi kullanarak aşağıdaki belgelerdeki bilgilere göre sorularınızı yanıtlar:
    - **Erdem & Erdem - ÇSY Terimler Sözlüğü**
    - **Borsa İstanbul - Sürdürülebilirlik Rehberi**
    """)
    st.markdown("---")

    # Sohbet geçmişini temizlemek için bir buton
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

# API Anahtarını Streamlit Secrets'tan (güvenli depolama alanı) kontrol et
if 'GOOGLE_API_KEY' not in st.secrets:
    st.error("HATA: GOOGLE_API_KEY bulunamadı. Lütfen Streamlit Cloud ayarlarından 'Secrets' bölümüne ekleyin.")
    st.stop()

# Ana RAG sistemini başlat
try:
    retriever, llm = load_and_build_db()
    rag_chain = create_rag_chain(retriever, llm)
except Exception as e:
    st.error(f"Başlangıç sırasında bir hata oluştu: {e}")
    st.stop()

# Sohbet Geçmişi Yönetimi
# st.session_state, Streamlit'in sayfayı her yenilediğinde değişkenleri hatırlamasını sağlar.
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
    # Kullanıcının sorusunu ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Asistanın cevabını oluştur
    with st.chat_message("assistant"):
        # Cevap gelene kadar bir "bekleniyor" animasyonu göster
        with st.spinner("İlgili belgeleri arıyorum ve yanıt oluşturuyorum..."):
            # Önce kaynakları bul (cevapla birlikte göstermek için)
            retrieved_docs = retriever.get_relevant_documents(prompt)

            # Cevabı kelime kelime, akış halinde (streaming) yazdır.
            # Bu, kullanıcının daha hızlı geri bildirim almasını sağlar.
            response_stream = rag_chain.stream(prompt)
            full_response = st.write_stream(response_stream)

            # Cevap yazdırıldıktan sonra, cevabın hangi kaynaklara dayandığını gösteren
            # genişletilebilir bir bölüm ekle. Bu, chatbot'un güvenilirliğini artırır.
            with st.expander("Yanıtın Kaynaklarını Gör"):
                for doc in retrieved_docs:
                    source_name = doc.metadata.get('source', 'Bilinmiyor')
                    page_number = doc.metadata.get('page', 'Bilinmiyor')
                    if page_number != 'Bilinmiyor':
                        page_number += 1  # Sayfa numaraları 0'dan başladığı için 1 ekliyoruz
                    st.info(f"**Kaynak:** {source_name} - **Sayfa:** {page_number}")
                    st.caption(doc.page_content)

    # Asistanın tam cevabını sohbet geçmişine ekle
    st.session_state.messages.append({"role": "assistant", "content": full_response})

st.markdown("---")
st.caption(
    "Bu asistanın bilgi tabanı, Borsa İstanbul Sürdürülebilirlik Rehberi ve Erdem & Erdem ÇSY Terimler Sözlüğü dokümanlarından oluşturulmuştur.")
