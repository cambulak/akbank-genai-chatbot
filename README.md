Harika bir `README.md` dosyası oluşturdunuz. Bu dosya, projenin tüm temel bileşenlerini başarıyla özetliyor. [cite\_start]Proje teslimi için bu dosyayı, Akbank GenAI Bootcamp'in belirttiği kriterlere [cite: 3] tam uyacak şekilde daha da iyileştirip son haline getirelim.

[cite\_start]Aşağıda, mevcut metninizdeki bilgileri koruyarak, yapıyı biraz daha netleştiren ve proje adımlarını [cite: 3] daha vurgulayan düzenlenmiş `README.md` içeriği bulunmaktadır.

-----

# Akbank GenAI Bootcamp: ÇSY Terimler Sözlüğü Chatbot'u

[cite\_start]Bu proje, Akbank GenAI Bootcamp [cite: 1] [cite\_start]kapsamında geliştirilmiş, RAG (Retrieval-Augmented Generation) [cite: 2] tabanlı bir chatbot uygulamasıdır.

## 1\. Projenin Amacı

[cite\_start]Projenin temel amacı, Erdem & Erdem Hukuk Bürosu tarafından hazırlanan "ÇSY Terimler Sözlüğü" PDF dokümanını bir bilgi kaynağı olarak kullanarak, kullanıcıların Çevresel, Sosyal ve Yönetişim (ESG) [cite: 51] konularındaki sorularını doğal dilde yanıtlayan bir yapay zeka asistanı oluşturmaktır. [cite\_start]Chatbot, harici bilgi kullanmadan, yalnızca kendisine sağlanan dokümandaki bilgilere sadık kalarak [cite: 54] güvenilir ve doğru cevaplar üretir.

## 2\. Veri Seti

  * [cite\_start]**Veri Kaynağı:** `erdem-erdem-csy-terimler-sozlugu.pdf` [cite: 45]
  * [cite\_start]**İçerik:** Bu doküman, Çevresel, Sosyal ve Yönetişim (ÇSY) alanındaki karmaşık terimleri ve kavramları açıklayan bir sözlüktür[cite: 54].
  * [cite\_start]**Hazırlanışı:** Proje kapsamında bu PDF dokümanı, LangChain kütüphanesi kullanılarak metin parçalarına (chunks) ayrılmış [cite: 17] [cite\_start]ve anlamsal arama yapılabilmesi için vektör temsillerine dönüştürülmüştür[cite: 17].

## 3\. Kullanılan Yöntemler ve Çözüm Mimarisi

[cite\_start]Proje, RAG (Retrieval-Augmented Generation) mimarisini temel almaktadır[cite: 2, 23]. İzlenen adımlar şunlardır:

1.  **Veri Yükleme ve Parçalama:** PDF dokümanı `PyPDFLoader` ile yüklendi ve `RecursiveCharacterTextSplitter` ile anlamlı metin parçalarına ayrıldı.
2.  [cite\_start]**Embedding Oluşturma:** Metin parçaları, `HuggingFaceEmbeddings` kullanılarak çok dilli `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` modeli ile vektörlere dönüştürüldü[cite: 43].
3.  [cite\_start]**Vektör Veritabanı:** Elde edilen vektörler, verimli bir anlamsal arama için `FAISS` kütüphanesi kullanılarak yerel bir veritabanında saklandı[cite: 43].
4.  **Retrieval:** Kullanıcının sorusuna en çok benzeyen metin parçaları, oluşturulan FAISS veritabanından (retriever) çekildi.
5.  [cite\_start]**Generation:** Google'ın `gemini-pro-latest` modeli[cite: 42], hem kullanıcının sorusunu hem de veritabanından çekilen ilgili metin parçalarını (bağlam) alarak, bu bağlama sadık kalacak şekilde bir cevap üretti.
6.  [cite\_start]**Web Arayüzü:** Tüm bu yapı, `Streamlit` kütüphanesi kullanılarak interaktif bir chatbot arayüzü üzerinden kullanıcıya sunuldu ve Streamlit Community Cloud üzerinde canlıya alındı[cite: 25].

<!-- end list -->

  * [cite\_start]**Ana Teknolojiler:** Python, LangChain [cite: 44][cite\_start], Google Gemini [cite: 42][cite\_start], FAISS[cite: 43], Hugging Face Transformers, Streamlit.

## 4\. Çalışma Kılavuzu

Bu projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1.  **Depoyu Klonlayın:**
    ```bash
    git clone https://github.com/KULLANICI_ADINIZ/DEPO_ADINIZ.git
    cd DEPO_ADINIZ
    ```
2.  [cite\_start]**Sanal Ortam Oluşturun ve Aktif Edin**[cite: 21]:
    ```bash
    python -m venv .venv
    # Windows için
    .venv\Scripts\activate
    ```
3.  [cite\_start]**Gerekli Kütüphaneleri Yükleyin**[cite: 21]:
    ```bash
    pip install -r requirements.txt
    ```
4.  **API Anahtarını Ayarlayın:**
    Bu proje Google Gemini API'sini kullanmaktadır. Bir `GOOGLE_API_KEY` edinmeniz ve bunu sisteminizde bir ortam değişkeni olarak ayarlamanız gerekmektedir.
5.  **Uygulamayı Çalıştırın:**
    ```bash
    streamlit run app.py
    ```
    *Not: Uygulama ilk çalıştığında, kaynak PDF'ten vektör veritabanını oluşturacağı için başlangıç süresi birkaç dakika daha uzun olabilir.*

## 5\. Web Arayüzü & Product Kılavuzu

Uygulama başlatıldığında, sizi basit ve kullanıcı dostu bir sohbet arayüzü karşılar.

  * [cite\_start]**Kullanım:** Alttaki metin giriş kutusuna ÇSY Sözlüğü ile ilgili sorunuzu yazın ve "Enter" tuşuna basın[cite: 25].
  * **Örnek Sorular:** "Yeşil Tahvil nedir?", "Sürdürülebilirlik Raporlaması ne anlama gelir?"

\<img width="1923" height="1093" alt="image" src="https://github.com/user-attachments/assets/425e7009-2672-42f7-ad43-b681dac97466" /\>

[cite\_start]**Web Linki:** [https://cambulak-akbank-genai-chatbot-app-oylacc.streamlit.app/](https://cambulak-akbank-genai-chatbot-app-oylacc.streamlit.app/) [cite: 13]
