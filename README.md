🧠 Akbank GenAI Bootcamp: ÇSY Terimler Sözlüğü Chatbot’u

Bu proje, Akbank GenAI Bootcamp kapsamında geliştirilmiş, RAG (Retrieval-Augmented Generation) tabanlı bir chatbot uygulamasıdır.
Amaç, Erdem & Erdem Hukuk Bürosu tarafından hazırlanan “ÇSY Terimler Sözlüğü” dokümanını bilgi kaynağı olarak kullanarak, kullanıcıların Çevresel, Sosyal ve Yönetişim (ESG/ÇSY) konularındaki sorularına doğal dilde yanıt verebilen bir yapay zekâ asistanı geliştirmektir.

🎯 1. Projenin Amacı

Proje, ÇSY alanındaki kavram ve terimleri güvenilir bir kaynaktan açıklayarak, kullanıcıların ESG konusunda farkındalığını artırmayı hedefler.
Chatbot, yalnızca kendisine sağlanan doküman (ÇSY Terimler Sözlüğü) içeriğini kullanır; harici bilgi kaynaklarından yararlanmaz.
Böylece yanıtlar doğru, tutarlı ve kaynakla uyumlu şekilde üretilir.

📘 2. Veri Seti

Veri Kaynağı: erdem-erdem-csy-terimler-sozlugu.pdf

İçerik: Çevresel, Sosyal ve Yönetişim alanındaki kavram ve tanımların açıklandığı sözlük formatında metin.

Hazırlık Süreci:

PDF dokümanı LangChain aracılığıyla anlamlı metin parçalarına (chunks) ayrılmıştır.

Parçalar, Hugging Face üzerindeki çok dilli sentence-transformers/paraphrase-multilingual-mpnet-base-v2 modeliyle vektör temsillerine (embeddings) dönüştürülmüştür.

Vektörler, FAISS tabanlı bir yerel veritabanında saklanarak anlamsal arama yapılabilir hale getirilmiştir.

🧩 3. Yöntem ve Mimarisi

Proje, RAG (Retrieval-Augmented Generation) mimarisiyle tasarlanmıştır.
Aşağıda sistemin ana bileşenleri yer almaktadır:

Veri Yükleme ve Parçalama:

PyPDFLoader ile PDF yüklenir.

RecursiveCharacterTextSplitter ile anlamlı metin bloklarına ayrılır.

Embedding Oluşturma:

HuggingFaceEmbeddings kullanılarak metin vektörleri üretilir.

Vektör Veritabanı:

FAISS kütüphanesiyle yerel vektör deposu oluşturulur.

Retrieval:

Kullanıcının sorusuna en yakın metin parçaları FAISS veritabanından getirilir.

Generation:

Google Gemini (gemini-pro-latest) modeli, hem kullanıcı sorusunu hem de ilgili metin parçalarını kullanarak cevap oluşturur.

Web Arayüzü:

Streamlit tabanlı bir sohbet arayüzüyle kullanıcıya sunulur.

Uygulama, Streamlit Community Cloud üzerinde çevrimiçi olarak erişilebilir hale getirilmiştir.

Kullanılan Temel Teknolojiler:

Python • LangChain • Google Gemini • Hugging Face Transformers • FAISS • Streamlit

⚙️ 4. Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

Depoyu Klonlayın

git clone https://github.com/KULLANICI_ADINIZ/DEPO_ADINIZ.git
cd DEPO_ADINIZ


Sanal Ortam Oluşturun ve Aktifleştirin

python -m venv .venv
# Windows için:
.venv\Scripts\activate


Bağımlılıkları Yükleyin

pip install -r requirements.txt


API Anahtarını Tanımlayın
Proje, Google Gemini API kullanmaktadır.
Bir GOOGLE_API_KEY oluşturun ve sistem değişkeni olarak ayarlayın:

setx GOOGLE_API_KEY "YOUR_API_KEY_HERE"


Uygulamayı Başlatın

streamlit run app.py


İlk çalıştırmada PDF’ten vektör veritabanı oluşturulacağı için başlangıç süresi birkaç dakika sürebilir.

💬 5. Kullanım & Arayüz

Uygulama başlatıldığında, sizi sade bir sohbet arayüzü karşılar.

Kullanım:
Alttaki metin kutusuna ÇSY Sözlüğü ile ilgili sorunuzu yazın ve Enter tuşuna basın.

Örnek Sorular:

“Yeşil Tahvil nedir?”

“Sürdürülebilirlik Raporlaması ne anlama gelir?”

Web Linki (Canlı Uygulama):
🔗 https://cambulak-akbank-genai-chatbot-app-oylacc.streamlit.app/

<img width="100%" alt="Chatbot Görseli" src="https://github.com/user-attachments/assets/425e7009-2672-42f7-ad43-b681dac97466" />
🧱 6. Özet

Bu proje, yapay zekâ tabanlı bilgi asistanlarının yerel verilerle eğitilerek nasıl güvenilir bir şekilde çalıştırılabileceğini göstermektedir.
RAG yaklaşımı sayesinde, model genel bilgiye değil, kendi doküman tabanına dayalı yanıtlar üretir — bu da doğruluk ve güvenilirlik açısından büyük avantaj sağlar.

🏷️ 7. Kaynaklar

Akbank GenAI Bootcamp

Erdem & Erdem Hukuk Bürosu – ÇSY Terimler Sözlüğü

LangChain, Hugging Face, FAISS, Streamlit, Google Gemini
