# Akbank GenAI Bootcamp: Kurumsal Sürdürülebilirlik Asistanı

Bu proje, Akbank GenAI Bootcamp kapsamında geliştirilmiş, RAG (Retrieval-Augmented Generation) tabanlı bir chatbot uygulamasıdır. Asistan, sağlanan sürdürülebilirlik dokümanlarını bir bilgi kaynağı olarak kullanarak, kullanıcıların Çevresel, Sosyal ve Yönetişim (ÇSY/ESG) konularındaki sorularını doğal dilde yanıtlar.

## 🎯 1. Projenin Amacı

Projenin temel amacı, sürdürülebilirlik alanındaki karmaşık konuları güvenilir kaynaklardan yola çıkarak açıklamaktır. Chatbot, sadece kendisine sağlanan dokümanların (`ÇSY Terimler Sözlüğü` ve `Borsa İstanbul Sürdürülebilirlik Rehberi`) içeriğini kullanır ve harici bilgi kaynaklarına başvurmaz. Bu sayede, ÇSY terimlerinden sürdürülebilirlik stratejilerine, raporlama standartlarından risk yönetimine kadar geniş bir yelpazede doğru, tutarlı ve kaynakla uyumlu yanıtlar üretir.

## 📘 2. Veri Seti

  * **Veri Kaynakları:**
    1.  `Erdem & Erdem - ÇSY Terimler Sözlüğü.pdf`
    2.  `Borsa İstanbul - Sürdürülebilirlik Rehberi.pdf`
  * **İçerik:** Veri seti, ÇSY alanındaki temel terimleri açıklayan bir sözlük ile kurumsal sürdürülebilirlik stratejileri, raporlama standartları ve uygulama yöntemlerini detaylandıran kapsamlı bir rehberden oluşmaktadır.
  * **Hazırlık Süreci:**
      * PDF dokümanları, LangChain aracılığıyla anlamlı metin parçalarına (chunks) ayrılmıştır.
      * Sistem, `data/` klasörüne eklenen tüm PDF'leri otomatik olarak işleyecek şekilde tasarlanmıştır.
      * Metin parçaları, Hugging Face üzerindeki çok dilli `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` modeliyle vektör temsillerine (embeddings) dönüştürülmüştür.
      * Vektörler, `FAISS` tabanlı bir yerel veritabanında saklanarak anlamsal arama yapılabilir hale getirilmiştir.

## 🧩 3. Yöntem ve Mimarisi

Proje, RAG (Retrieval-Augmented Generation) mimarisiyle tasarlanmıştır. Sistem, kullanıcı sorusuna en uygun bilgiyi kendi doküman havuzundan bularak dil modeline sunar ve cevabın bu bilgiye dayalı üretilmesini sağlar.

  * **Veri Yükleme ve Parçalama:** `PyPDFLoader`, `data/` klasöründeki tüm PDF'leri yükler. `RecursiveCharacterTextSplitter` ile metinler anlamlı bloklara ayrılır.
  * **Embedding Oluşturma:** `HuggingFaceEmbeddings` kullanılarak metin vektörleri üretilir.
  * **Vektör Veritabanı:** `FAISS` kütüphanesiyle yerel bir vektör deposu oluşturulur.
  * **Retrieval (Bilgi Çekme):** Kullanıcının sorusuna en yakın metin parçaları FAISS veritabanından getirilir.
  * **Generation (Cevap Üretme):** Google'ın `gemini-pro-latest` modeli, hem kullanıcı sorusunu hem de ilgili metin parçalarını (bağlam) alarak cevabı oluşturur.
  * **Web Arayüzü:** `Streamlit` tabanlı interaktif bir sohbet arayüzüyle kullanıcıya sunulur ve Streamlit Community Cloud üzerinde canlıya alınmıştır.

**Kullanılan Temel Teknolojiler:**
Python • LangChain • Google Gemini • Hugging Face Transformers • FAISS • Streamlit

## ⚙️ 4. Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1.  **Depoyu Klonlayın:**
    ```bash
    git clone https://github.com/KULLANICI_ADINIZ/DEPO_ADINIZ.git
    cd DEPO_ADINIZ
    ```
2.  **Sanal Ortam Oluşturun ve Aktifleştirin:**
    ```bash
    python -m venv .venv
    # Windows için:
    .venv\Scripts\activate
    ```
3.  **Bağımlılıkları Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **API Anahtarını Tanımlayın:**
    Proje, Google Gemini API'sini kullanmaktadır. Bir `GOOGLE_API_KEY` oluşturun ve bunu sisteminizde bir ortam değişkeni olarak ayarlayın.
5.  **Uygulamayı Başlatın:**
    ```bash
    streamlit run app.py
    ```
    *Not: Uygulama ilk çalıştığında, `data` klasöründeki tüm PDF'lerden vektör veritabanı oluşturulacağı için başlangıç süresi birkaç dakika sürebilir.*

## 💬 5. Kullanım & Arayüz

Uygulama, sürdürülebilirlik konularında bilgi edinmenizi sağlayan sade bir sohbet arayüzü sunar.

  * **Kullanım:** Alttaki metin kutusuna sorunuzu yazın ve "Enter" tuşuna basın.
  * **Örnek Sorular:**
      * "Yeşil aklama (greenwashing) nedir?"
      * "Bir sürdürülebilirlik stratejisi nasıl hazırlanır?"
      * "TSRS nedir?"
      * "İklimle ilgili fiziksel riskler nelerdir?"

**Web Linki (Canlı Uygulama):** 🔗 [https://cambulak-akbank-genai-chatbot-app-oylacc.streamlit.app/](https://cambulak-akbank-genai-chatbot-app-oylacc.streamlit.app/)

## 🧱 6. Özet

Bu proje, RAG mimarisinin, belirli bir bilgi alanında uzmanlaşmış ve güvenilir yapay zeka asistanları oluşturmak için ne kadar güçlü bir yaklaşım olduğunu göstermektedir. Sistem, genişletilmiş bilgi tabanına dayalı yanıtlar üreterek, genel amaçlı chatbot'lara kıyasla doğruluk ve güvenilirlik açısından önemli bir avantaj sağlar.

## 🏷️ 7. Kaynaklar

  * Akbank GenAI Bootcamp
  * Erdem & Erdem Hukuk Bürosu – ÇSY Terimler Sözlüğü
  * Borsa İstanbul – Sürdürülebilirlik Rehberi
  * LangChain, Hugging Face, FAISS, Streamlit, Google Gemini dokümantasyonları
