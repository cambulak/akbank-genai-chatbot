# 💼 Akbank GenAI Bootcamp: Kurumsal Sürdürülebilirlik Asistanı

Bu proje, **Akbank GenAI Bootcamp** kapsamında geliştirilmiş **RAG (Retrieval-Augmented Generation)** tabanlı çok sayfalı bir web uygulamasıdır.  
Uygulama; bir **Sohbet Asistanı** ve bir **Veri Görselleştirme Paneli** olmak üzere iki ana bileşenden oluşmaktadır.

---

## 🎯 1. Projenin Amacı

Projenin temel amacı, **sürdürülebilirlik alanındaki karmaşık kavramları** güvenilir kaynaklara dayalı olarak açıklayabilen, etkileşimli bir **yapay zeka destekli asistan** geliştirmektir.  
Sistem yalnızca kendisine yüklenen dokümanlardan yararlanır; harici bilgi kaynaklarına başvurmaz. Böylece yanıtların **doğruluğu, tutarlılığı ve kaynak izlenebilirliği** sağlanır.

---

## 📘 2. Veri Seti

### Veri Kaynakları
1. *Erdem & Erdem – ÇSY Terimler Sözlüğü.pdf*  
2. *Borsa İstanbul – Sürdürülebilirlik Rehberi.pdf*

### İçerik  
Veri seti, Çevresel, Sosyal ve Yönetişim (ÇSY) kavramlarını açıklayan bir terimler sözlüğü ile kurumsal sürdürülebilirlik stratejilerini, raporlama standartlarını ve uygulama yöntemlerini anlatan kapsamlı bir rehberden oluşmaktadır.

### Hazırlık Süreci
- `data/` klasörüne eklenen tüm PDF’ler uygulamanın ilk çalıştırılmasında otomatik olarak işlenir.  
- Metinler, **`sentence-transformers/paraphrase-multilingual-mpnet-base-v2`** modeliyle vektör temsillerine dönüştürülür.  
- Vektörler, **FAISS** tabanlı bir yerel veritabanında saklanır ve anlamsal arama için kullanılır.  

---

## 🧩 3. Yöntem ve Mimari

Proje, gelişmiş bir **RAG (Retrieval-Augmented Generation)** mimarisiyle tasarlanmıştır.  
Sistem, kullanıcı sorularını dokümanlardan çekilen en alakalı bilgiyle ilişkilendirir ve modelin bağlama dayalı yanıt üretmesini sağlar.

### Süreç Adımları
- **Veri Yükleme ve Parçalama:**  
  `PyPDFLoader` dokümanları yükler, `RecursiveCharacterTextSplitter` metinleri anlamlı bloklara ayırır.  
- **Embedding Oluşturma:**  
  `HuggingFaceEmbeddings` ile her metin parçası vektörel olarak temsil edilir.  
- **Vektör Veritabanı:**  
  `FAISS` ile yerel bir veri deposu oluşturulur.  
- **Bilgi Çekme (Retrieval):**  
  `MultiQueryRetriever`, tek bir soruyu çok sayıda alt sorguya dönüştürerek farklı bölümlerdeki ilgili bilgileri bir araya getirir.  
- **Cevap Üretme (Generation):**  
  `Google Gemini-Pro` modeli, kullanıcı sorusunu ve ilgili bağlamı birlikte işleyerek cevabı üretir.  
- **Web Arayüzü:**  
  `Streamlit` ile oluşturulan çok sayfalı arayüz, **Sohbet Asistanı** ve **Veri Görselleştirme Paneli** bölümlerinden oluşur.

### Kullanılan Teknolojiler
> Python • LangChain • Google Gemini • Hugging Face Transformers • FAISS • Streamlit • Plotly

---

## ⚙️ 4. Kurulum ve Çalıştırma

Yerel ortamda uygulamayı çalıştırmak için şu adımları izleyin:

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/KULLANICI_ADINIZ/DEPO_ADINIZ.git
cd DEPO_ADINIZ
