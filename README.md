# Akbank GenAI Bootcamp: ÇSY Terimler Sözlüğü Chatbot'u

Bu proje, Akbank GenAI Bootcamp kapsamında geliştirilmiş RAG (Retrieval-Augmented Generation) tabanlı bir chatbot uygulamasıdır.

## [cite_start]1. Projenin Amacı [cite: 1418]

Bu projenin temel amacı, Erdem & Erdem Hukuk Bürosu tarafından hazırlanan "ÇSY Terimler Sözlüğü" PDF dokümanını bir bilgi kaynağı olarak kullanarak, kullanıcıların Çevresel, Sosyal ve Yönetişim (ESG) konularındaki sorularını doğal dilde yanıtlayan bir yapay zeka asistanı oluşturmaktır. Chatbot, sadece kendisine sağlanan dokümandaki bilgilere sadık kalarak güvenilir ve doğru cevaplar üretir.

## [cite_start]2. Veri Seti [cite: 1419]

* **Veri Kaynağı:** `erdem-erdem-csy-terimler-sozlugu.pdf`
* **İçerik:** Bu doküman, Çevresel, Sosyal ve Yönetişim (ÇSY) alanındaki karmaşık terimleri ve kavramları açıklayan bir sözlüktür.
* **Hazırlanışı:** Proje kapsamında bu PDF dokümanı, LangChain kütüphanesi kullanılarak metin parçalarına (chunks) ayrılmış ve anlamsal arama yapılabilmesi için vektör temsillerine dönüştürülmüştür.

## [cite_start]3. Kullanılan Yöntemler ve Çözüm Mimarisi [cite: 1420, 1439]

Proje, RAG (Retrieval-Augmented Generation) mimarisini temel almaktadır. İzlenen adımlar şunlardır:

1.  **Veri Yükleme ve Parçalama:** PDF dokümanı `PyPDFLoader` ile yüklendi ve `RecursiveCharacterTextSplitter` ile anlamlı metin parçalarına ayrıldı.
2.  **Embedding Oluşturma:** Metin parçaları, `HuggingFaceEmbeddings` kullanılarak çok dilli `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` modeli ile vektörlere dönüştürüldü.
3.  **Vektör Veritabanı:** Elde edilen vektörler, verimli bir anlamsal arama için `FAISS` kütüphanesi kullanılarak yerel bir veritabanında saklandı.
4.  **Retrieval:** Kullanıcının sorusuna en çok benzeyen metin parçaları, oluşturulan FAISS veritabanından (retriever) çekildi.
5.  **Generation:** Google'ın `gemini-pro-latest` modeli, hem kullanıcının sorusunu hem de veritabanından çekilen ilgili metin parçalarını (bağlam) alarak, bu bağlama sadık kalacak şekilde bir cevap üretti.
6.  **Web Arayüzü:** Tüm bu yapı, `Streamlit` kütüphanesi kullanılarak interaktif bir chatbot arayüzü üzerinden kullanıcıya sunuldu.

* **Ana Teknolojiler:** Python, LangChain, Google Gemini, FAISS, Hugging Face Transformers, Streamlit.

## [cite_start]4. Çalışma Kılavuzu [cite: 1438]

Bu projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1.  **Depoyu Klonlayın:**
    ```bash
    git clone [https://github.com/KULLANICI_ADINIZ/DEPO_ADINIZ.git](https://github.com/KULLANICI_ADINIZ/DEPO_ADINIZ.git)
    cd DEPO_ADINIZ
    ```
2.  **Sanal Ortam Oluşturun ve Aktif Edin:**
    ```bash
    python -m venv .venv
    # Windows için
    .venv\Scripts\activate
    ```
3.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **API Anahtarını Ayarlayın:**
    Bu proje Google Gemini API'sini kullanmaktadır. Bir `GOOGLE_API_KEY` edinmeniz ve bunu sisteminizde bir ortam değişkeni olarak ayarlamanız gerekmektedir.
5.  **Veritabanını Oluşturun (İlk Kurulum):**
    ```bash
    python create_database.py
    ```
6.  **Uygulamayı Çalıştırın:**
    ```bash
    streamlit run app.py
    ```

## [cite_start]5. Web Arayüzü & Product Kılavuzu [cite: 1440]

Uygulama başlatıldığında, sizi basit ve kullanıcı dostu bir sohbet arayüzü karşılar.

* **Kullanım:** Alttaki metin giriş kutusuna ÇSY Sözlüğü ile ilgili sorunuzu yazın ve "Enter" tuşuna basın.
* **Örnek Sorular:** "Yeşil Tahvil nedir?", "Sürdürülebilirlik Raporlaması ne anlama gelir?"

*<img width="1923" height="1093" alt="image" src="https://github.com/user-attachments/assets/425e7009-2672-42f7-ad43-b681dac97466" />*

[cite_start]**Web Linki:** [**(https://cambulak-akbank-genai-chatbot-app-oylacc.streamlit.app/)**] [cite: 1422]
