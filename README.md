# Kurumsal Sürdürülebilirlik Asistanı (Akbank GenAI Bootcamp Projesi)

Bu proje, **Akbank GenAI Bootcamp** kapsamında geliştirilmiş, **RAG (Retrieval-Augmented Generation)** tabanlı çok sayfalı bir Streamlit web uygulamasıdır. Uygulama, kurumsal sürdürülebilirlik ve ESG (Çevresel, Sosyal, Yönetişim) konularında bilgi sağlayan bir **Sohbet Asistanı** ve ilgili riskleri görselleştiren bir **Veri Görselleştirme** panelinden oluşmaktadır.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://akbank-genai-chatbot-h8apfoq5vnx3xrc9yavmnk.streamlit.app/)

## 🎯 Projenin Amacı

Projenin temel amacı, sürdürülebilirlik alanındaki karmaşık konuları, sağlanan güvenilir PDF kaynaklarına dayanarak açıklığa kavuşturmaktır. Bu amaçla iki ana bileşen sunulmaktadır:

1.  **Sohbet Asistanı:** Kullanıcıların doğal dilde sorduğu sorulara, yalnızca yüklenen dokümanların içeriğini kullanarak, harici bilgi kaynaklarına başvurmadan, doğru ve bağlamsal yanıtlar üretir.
2.  **Veri Görselleştirme:** Borsa İstanbul Sürdürülebilirlik Rehberi'ndeki ESG risk sınıflandırmasını interaktif bir treemap grafiği ile sunar.

## ✨ Öne Çıkan Özellikler

* **Güvenilir Bilgi:** Yanıtlar yalnızca sağlanan PDF dokümanlarına dayanır (RAG).
* **Kaynak Gösterimi:** Sohbet Asistanı, yanıtlarını oluştururken kullandığı kaynak doküman ve sayfa numarasını belirtir.
* **Etkileşimli Görselleştirme:** ESG risk kategorileri, tanımları ve hiyerarşisi Plotly treemap ile keşfedilebilir.
* **Çok Sayfalı Arayüz:** Streamlit'in çok sayfalı uygulama yapısı kullanılarak farklı işlevler (sohbet, görselleştirme) ayrı sayfalarda sunulur.
* **Gelişmiş Anlamsal Arama:** `MultiQueryRetriever` kullanarak kullanıcı soruları alt sorgulara bölünür ve daha isabetli sonuçlar elde edilir.

## 📘 Veri Seti ve Hazırlık

* **Veri Kaynakları:**
    * `Erdem & Erdem - ÇSY Terimler Sözlüğü.pdf`
    * `Borsa İstanbul - Sürdürülebilirlik Rehberi.pdf`
* **İçerik:** ÇSY alanındaki temel terimler sözlüğü ve kurumsal sürdürülebilirlik stratejileri, raporlama standartları ve uygulama yöntemlerini içeren rehber.
* **Hazırlık Süreci:**
    1.  PDF dosyaları proje içindeki `data/` klasörüne yerleştirilir.
    2.  Uygulama ilk çalıştığında (veya vektör veritabanı bulunamadığında), bu PDF'ler `PyPDFLoader` ile yüklenir.
    3.  Metinler `RecursiveCharacterTextSplitter` ile anlamlı parçalara ayrılır.
    4.  Parçalar, `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` modeli kullanılarak `HuggingFaceEmbeddings` ile vektör temsillerine (embeddings) dönüştürülür.
    5.  Oluşturulan vektörler, `FAISS` kullanılarak lokal bir vektör veritabanına kaydedilir (`faiss_index` dosyası). Sonraki çalıştırmalarda bu hazır veritabanı kullanılır.

## 🧩 Mimari (RAG Akışı)

Proje, gelişmiş bir **RAG (Retrieval-Augmented Generation)** mimarisi üzerine kuruludur:

1.  **Veri Yükleme & İşleme:** `PyPDFLoader` PDF'leri yükler, `RecursiveCharacterTextSplitter` metinleri böler.
2.  **Vektörleştirme & Depolama:** `HuggingFaceEmbeddings` metinleri vektöre çevirir, `FAISS` bu vektörleri verimli arama için indeksler ve lokalde saklar.
3.  **Sorgu Anlama & Arama (Retrieval):** Kullanıcının sorusu alınır. `MultiQueryRetriever`, LLM (Gemini Pro) kullanarak orijinal sorudan birden fazla alt sorgu türetir. Bu alt sorgular FAISS veritabanında çalıştırılarak ilgili doküman parçaları bulunur.
4.  **Yanıt Üretme (Generation):** Bulunan ilgili doküman parçaları ve orijinal kullanıcı sorusu, bir prompt şablonu ile birleştirilerek `Google Gemini Pro` modeline gönderilir. Model, sağlanan bağlama dayanarak nihai yanıtı üretir.

## 🛠️ Kullanılan Teknolojiler

* **Programlama Dili:** Python
* **Web Framework:** Streamlit
* **LLM Orkestrasyon:** LangChain
* **Dil Modeli (LLM):** Google Gemini Pro (`langchain-google-genai`)
* **Embedding Modeli:** Hugging Face Sentence Transformers (`sentence-transformers/paraphrase-multilingual-mpnet-base-v2`)
* **Vektör Veritabanı:** FAISS (Facebook AI Similarity Search)
* **PDF İşleme:** PyPDF (`PyPDFLoader`)
* **Veri Görselleştirme:** Plotly

## ⚙️ Kurulum ve Çalıştırma (Lokal)

1.  **Depoyu Klonlayın:**
    ```bash
    git clone [https://github.com/cambulak/akbank-genai-chatbot.git](https://github.com/cambulak/akbank-genai-chatbot.git)
    cd akbank-genai-chatbot
    ```

2.  **Sanal Ortam Oluşturun ve Aktifleştirin:**
    ```bash
    # Sanal ortamı oluştur (Windows/Linux/macOS)
    python -m venv .venv

    # Sanal ortamı aktifleştir
    # Windows PowerShell:
    .\.venv\Scripts\Activate.ps1
    # Windows CMD:
    # .\.venv\Scripts\activate.bat
    # Linux/macOS (bash/zsh):
    # source .venv/bin/activate
    ```
    *(Not: PowerShell'de `Activate.ps1` betiğini çalıştırmak için önce `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` komutunu çalıştırmanız gerekebilir.)*

3.  **Gerekli Paketleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **API Anahtarını Güvenli Bir Şekilde Tanımlayın:**
    * Proje ana dizininde `.streamlit` adında bir klasör oluşturun: `mkdir .streamlit`
    * Bu klasörün içine `secrets.toml` adında bir dosya oluşturun.
    * Dosyanın içeriğini aşağıdaki gibi düzenleyin ve kendi Google API anahtarınızı (Gemini API erişimi olan) ekleyin:
        ```toml
        # .streamlit/secrets.toml
        GOOGLE_API_KEY = "SIZIN_GOOGLE_API_ANAHTARINIZ"
        ```
    * **ÖNEMLİ:** `.streamlit/` klasörünün `.gitignore` dosyanızda olduğundan emin olun! Bu, gizli anahtarınızın yanlışlıkla Git geçmişine ve GitHub'a gönderilmesini engeller.

5.  **PDF Dosyalarının Konumunu Kontrol Edin:**
    * Kullanılacak PDF dosyalarının (`Erdem & Erdem - ÇSY Terimler Sözlüğü.pdf`, `Borsa İstanbul - Sürdürülebilirlik Rehberi.pdf`) proje ana dizinindeki `data/` klasöründe bulunduğundan emin olun.

6.  **Uygulamayı Başlatın:**
    ```bash
    streamlit run app.py
    ```
    * Uygulama varsayılan tarayıcınızda `http://localhost:8501` adresinde açılacaktır.
    * **Not:** İlk çalıştırmada, `data` klasöründeki PDF'lerden vektör veritabanı (`faiss_index`) oluşturulacağı için bu işlem birkaç dakika sürebilir. Sonraki çalıştırmalar daha hızlı olacaktır.

## 💬 Web Arayüzü & Kullanım Kılavuzu

Uygulama detayları aşağıdadır;

### 🧠 Sohbet Asistanı

* **Kullanım:** "Sorunuzu buraya yazın..." alanına ESG veya sürdürülebilirlik ile ilgili sorunuzu yazın ve Enter'a basın.
* **Yanıt:** Asistan, `data/` klasöründeki PDF'lere dayanarak bir yanıt üretecektir.
* **Kaynak Gösterimi:** Üretilen yanıtın altında, bilginin hangi dokümandan ve hangi sayfa numarasından alındığına dair referanslar gösterilir (eğer LangChain tarafından bulunabildiyse).
* **Örnek Sorular:**
    * `Sürdürülebilir uygulamaların artırılması şirkete hangi katkıları sağlar?`
    * `Sınırda karbon düzenlemesi nedir?`
    * `Paris Anlaşması nedir?`
    * `Kurumsal Yönetim nedir?`
    * `Karbon tutma nedir?`


## ☁️ Canlı Uygulama

Uygulamanın Streamlit Cloud üzerinde yayınlanmış versiyonuna aşağıdaki linkten erişebilirsiniz:

[https://akbank-genai-chatbot-h8apfoq5vnx3xrc9yavmnk.streamlit.app/](https://akbank-genai-chatbot-h8apfoq5vnx3xrc9yavmnk.streamlit.app/)

<img width="1899" height="747" alt="image" src="https://github.com/user-attachments/assets/101f791b-3b6c-48a7-96c8-fbb96935dbfe" />


## 🧱 Özet

Bu proje, RAG mimarisinin belirli bir bilgi alanında (kurumsal sürdürülebilirlik) uzmanlaşmış, güvenilir ve kaynak gösterebilen yapay zekâ asistanları geliştirmede etkinliğini göstermektedir. `MultiQueryRetriever` kullanımı sorgu çeşitliliğini artırarak daha kapsamlı sonuçlar bulunmasına yardımcı olurken, Streamlit tabanlı çok sayfalı yapı hem sohbet arayüzünü hem de veri görselleştirmesini kullanıcı dostu bir şekilde sunmaktadır.

## 🏷️ Kaynaklar ve Teşekkür

* Bu proje **Akbank GenAI Bootcamp** kapsamında hazırlanmıştır.
* **Veri Kaynakları:**
    * Erdem & Erdem Hukuk Bürosu – ÇSY Terimler Sözlüğü
    * Borsa İstanbul – Sürdürülebilirlik Rehberi
* **Kullanılan Teknolojilerin Belgeleri:**
    * [LangChain](https://python.langchain.com/docs/get_started/introduction)
    * [Streamlit](https://docs.streamlit.io/)
    * [Google AI for Developers (Gemini)](https://ai.google.dev/)
    * [Hugging Face Transformers & Sentence Transformers](https://huggingface.co/sentence-transformers)
    * [FAISS](https://github.com/facebookresearch/faiss)
    * [Plotly](https://plotly.com/python/)
