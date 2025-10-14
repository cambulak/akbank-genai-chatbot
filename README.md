
# Akbank GenAI Bootcamp: Kurumsal Sürdürülebilirlik Asistanı

Bu proje, Akbank GenAI Bootcamp kapsamında geliştirilmiş, RAG (Retrieval-Augmented Generation) tabanlı çok sayfalı bir web uygulamasıdır. Uygulama, bir **Sohbet Asistanı** ve bir **Veri Görselleştirme** panelinden oluşmaktadır.

## 🎯 1. Projenin Amacı

Projenin temel amacı, sürdürülebilirlik alanındaki karmaşık konuları güvenilir kaynaklardan yola çıkarak hem interaktif bir sohbet arayüzüyle açıklamak hem de veri görselleştirmesiyle sunmaktır. Chatbot, yalnızca kendisine sağlanan dokümanların içeriğini kullanarak, harici bilgi kaynaklarına başvurmadan, doğru ve tutarlı yanıtlar üretir.

## 📘 2. Veri Seti

  * **Veri Kaynakları:**
    1.  [cite\_start]`Erdem & Erdem - ÇSY Terimler Sözlüğü.pdf` [cite: 45]
    2.  [cite\_start]`Borsa İstanbul - Sürdürülebilirlik Rehberi.pdf` [cite: 1454]
  * [cite\_start]**İçerik:** Veri seti, ÇSY alanındaki temel terimleri açıklayan bir sözlük ile kurumsal sürdürülebilirlik stratejileri, raporlama standartları ve uygulama yöntemlerini detaylandıran kapsamlı bir rehberden oluşmaktadır[cite: 54, 1465].
  * **Hazırlık Süreci:**
      * [cite\_start]Uygulama, `data/` klasörüne eklenen tüm PDF'leri ilk çalıştırmada otomatik olarak işler[cite: 2].
      * Metin parçaları, Hugging Face üzerindeki çok dilli `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` modeliyle vektör temsillerine (embeddings) dönüştürülmüştür.
      * [cite\_start]Vektörler, `FAISS` tabanlı bir yerel veritabanında saklanarak anlamsal arama yapılabilir hale getirilmiştir[cite: 43].

## 🧩 3. Yöntem ve Mimarisi

Proje, gelişmiş bir RAG (Retrieval-Augmented Generation) mimarisiyle tasarlanmıştır. Sistem, kullanıcı sorusuna en uygun bilgiyi kendi doküman havuzundan bularak dil modeline sunar ve cevabın bu bilgiye dayalı üretilmesini sağlar.

  * **Veri Yükleme ve Parçalama:** `PyPDFLoader`, `data/` klasöründeki tüm PDF'leri yükler. `RecursiveCharacterTextSplitter` ile metinler anlamlı bloklara ayrılır.
  * **Embedding Oluşturma:** `HuggingFaceEmbeddings` kullanılarak metin vektörleri üretilir.
  * **Vektör Veritabanı:** `FAISS` kütüphanesiyle yerel bir vektör deposu oluşturulur.
  * **Retrieval (Bilgi Çekme):**
      * Kullanıcının sorduğu tek bir soruyu, arka planda LLM kullanarak birden çok alt sorguya dönüştüren **`MultiQueryRetriever`** tekniği kullanılmıştır.
      * Bu yöntem, cevabı dokümanların farklı yerlerine yayılmış karmaşık sorular için bile ilgili tüm bilgi parçalarını toplama başarısını artırır.
  * [cite\_start]**Generation (Cevap Üretme):** Google'ın `gemini-pro-latest` modeli, hem kullanıcı sorusunu hem de ilgili metin parçalarını (bağlam) alarak cevabı oluşturur[cite: 42].
  * **Web Arayüzü:** `Streamlit` ile geliştirilen çok sayfalı uygulama, bir sohbet arayüzü ve interaktif bir `Plotly` veri görselleştirmesi sunar.

**Kullanılan Temel Teknolojiler:**
Python • LangChain • Google Gemini • Hugging Face Transformers • FAISS • Streamlit • Plotly

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

## 💬 5. Web Arayüzü & Product Kılavuzu

Uygulama, soldaki menüden geçiş yapabileceğiniz iki ana bölümden oluşur:

### Sohbet Asistanı

  * **Kullanım:** Alttaki metin kutusuna sorunuzu yazın ve "Enter" tuşuna basın. Chatbot, cevabını oluştururken hangi kaynak dokümanın hangi sayfasından yararlandığını gösteren bir kaynakça bölümü sunar.
  * **Örnek Sorular:**
      * Sürdürülebilir uygulamaların artırılması şirkete hangi katkıları sağlar?
      * Sınırda karbon düzenlemesi nedir?
      * Paris Anlaşması nedir?
      * Kurumsal Yönetim nedir?
      * Karbon tutma nedir?

### ÇSY Risk Görselleştirmesi

  * **İçerik:** Bu sayfa, Borsa İstanbul Sürdürülebilirlik Rehberi'nden alınan ÇSY risk sınıflandırmasını interaktif bir Treemap grafiği ile sunar.
  * **Kullanım:** Fare ile her bir risk kategorisinin üzerine gelerek o riskin tanımını ve ait olduğu ana kategoriyi görebilirsiniz.

**Web Linki (Canlı Uygulama):** 🔗 [https://cambulak-akbank-genai-chatbot-app-oylacc.streamlit.app/](https://cambulak-akbank-genai-chatbot-app-oylacc.streamlit.app/)

<img width="1890" height="811" alt="image" src="https://github.com/user-attachments/assets/25ea9e26-ffef-4faf-a7cc-c3cb67c02d85" />

## 🧱 6. Özet

Bu proje, RAG mimarisinin, belirli bir bilgi alanında uzmanlaşmış ve güvenilir yapay zeka asistanları oluşturmak için ne kadar güçlü bir yaklaşım olduğunu göstermektedir. Sistemin `MultiQueryRetriever` gibi gelişmiş tekniklerle optimize edilmesi ve Streamlit ile çok sayfalı, interaktif bir arayüzle sunulması, projenin hem teknik derinliğini hem de kullanıcı dostu bir ürün olma potansiyelini ortaya koymaktadır.

## 🏷️ 7. Kaynaklar

  * Akbank GenAI Bootcamp
  * Erdem & Erdem Hukuk Bürosu – ÇSY Terimler Sözlüğü
  * Borsa İstanbul – Sürdürülebilirlik Rehberi
  * LangChain, Hugging Face, FAISS, Streamlit, Google Gemini dokümantasyonları
