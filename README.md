# Akbank GenAI Bootcamp: Kurumsal Sürdürülebilirlik Asistanı

Bu proje, **Akbank GenAI Bootcamp** kapsamında geliştirilmiş, **RAG (Retrieval-Augmented Generation)** tabanlı çok sayfalı bir web uygulamasıdır.  
Uygulama, bir **Sohbet Asistanı** ve bir **Veri Görselleştirme** panelinden oluşmaktadır.

---

## 🎯 1. Projenin Amacı

Projenin temel amacı, sürdürülebilirlik alanındaki karmaşık konuları güvenilir kaynaklardan yola çıkarak hem interaktif bir sohbet arayüzüyle açıklamak hem de veri görselleştirmesiyle sunmaktır.  
Chatbot, yalnızca kendisine sağlanan dokümanların içeriğini kullanarak, harici bilgi kaynaklarına başvurmadan, doğru ve tutarlı yanıtlar üretir.

---

## 📘 2. Veri Seti

**Veri Kaynakları:**
1. *Erdem & Erdem - ÇSY Terimler Sözlüğü.pdf*
2. *Borsa İstanbul - Sürdürülebilirlik Rehberi.pdf*

**İçerik:** Veri seti, ÇSY alanındaki temel terimleri açıklayan bir sözlük ile kurumsal sürdürülebilirlik stratejileri, raporlama standartları ve uygulama yöntemlerini detaylandıran kapsamlı bir rehberden oluşmaktadır.

**Hazırlık Süreci:**
- `data/` klasörüne eklenen PDF’ler otomatik olarak işlenir.
- Metinler, `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` modeliyle embedding’e dönüştürülür.
- Embedding’ler, `FAISS` tabanlı yerel bir vektör veritabanında saklanır.

---

## 🧩 3. Yöntem ve Mimarisi

Proje, gelişmiş bir **RAG (Retrieval-Augmented Generation)** mimarisiyle tasarlanmıştır.

### Sistem Akışı
1. **Veri Yükleme:** `PyPDFLoader` PDF’leri yükler.  
2. **Parçalama:** `RecursiveCharacterTextSplitter` ile metinler anlamlı bloklara ayrılır.  
3. **Embedding:** `HuggingFaceEmbeddings` modeliyle metin vektörleri oluşturulur.  
4. **Depolama:** `FAISS` kullanılarak vektör tabanı oluşturulur.  
5. **Retrieval:** `MultiQueryRetriever` bir soruyu çoklu alt sorgulara dönüştürür.  
6. **Cevap Üretimi:** `Google Gemini Pro` modeli yanıt üretir.

**Kullanılan Teknolojiler:**  
Python • LangChain • Google Gemini • Hugging Face • FAISS • Streamlit • Plotly

---

## ⚙️ 4. Kurulum ve Çalıştırma

### 1️⃣ Depoyu Klonlayın
```bash
git clone https://github.com/KULLANICI_ADINIZ/DEPO_ADINIZ.git
cd DEPO_ADINIZ
```

### 2️⃣ Sanal Ortam Oluşturun
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
```

### 3️⃣ Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4️⃣ API Anahtarını Tanımlayın
```bash
set GOOGLE_API_KEY=YOUR_API_KEY
```

### 5️⃣ Uygulamayı Başlatın
```bash
streamlit run app.py
```

> *Not:* İlk çalıştırmada `data` klasöründeki PDF’lerden vektör veritabanı oluşturulacağı için birkaç dakika sürebilir.

---

## 💬 5. Web Arayüzü & Product Kılavuzu

### 🧠 Sohbet Asistanı
- **Kullanım:** Sorunuzu yazın, Enter’a basın.
- **Kaynak Gösterimi:** Yanıtın dayandığı doküman ve sayfa bilgisi görünür.
- **Örnek Sorular:**
  - Sürdürülebilir uygulamaların artırılması şirkete hangi katkıları sağlar?
  - Sınırda karbon düzenlemesi nedir?
  - Paris Anlaşması nedir?
  - Kurumsal Yönetim nedir?
  - Karbon tutma nedir?

### 📊 ÇSY Risk Görselleştirmesi
- **İçerik:** Borsa İstanbul Sürdürülebilirlik Rehberi’nden alınan risk sınıflandırması.
- **Özellik:** Treemap grafiği ile etkileşimli risk keşfi.
- **Kullanım:** Fareyle kategori üzerine gelin, tanım ve üst kategori bilgisi görünür.

<img width="1882" height="804" alt="image" src="https://github.com/user-attachments/assets/3a7bf4a1-da92-4179-864e-5f3bf9130496" />


**Canlı Uygulama:**  
🔗 [https://cambulak-akbank-genai-chatbot-app-oylacc.streamlit.app/](https://cambulak-akbank-genai-chatbot-app-oylacc.streamlit.app/)

---

## 🧱 6. Özet

Bu proje, RAG mimarisinin belirli bir bilgi alanında uzmanlaşmış yapay zekâ asistanları geliştirmede ne kadar güçlü olduğunu göstermektedir.  
`MultiQueryRetriever` ve Streamlit tabanlı çok sayfalı yapı sayesinde hem teknik derinlik hem kullanıcı dostu deneyim sağlanmıştır.

---

## 🏷️ 7. Kaynaklar

- Akbank GenAI Bootcamp  
- Erdem & Erdem Hukuk Bürosu – ÇSY Terimler Sözlüğü  
- Borsa İstanbul – Sürdürülebilirlik Rehberi  
- LangChain, Hugging Face, FAISS, Streamlit, Google Gemini belgeleri
