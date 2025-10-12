Akbank GenAI Bootcamp: ÇSY Terimler Sözlüğü Chatbot'u
Bu proje, Akbank GenAI Bootcamp kapsamında geliştirilmiş RAG (Retrieval-Augmented Generation) tabanlı bir chatbot uygulamasıdır.


1. Projenin Amacı 

Bu projenin temel amacı, Erdem & Erdem Hukuk Bürosu tarafından hazırlanan "ÇSY Terimler Sözlüğü" PDF dokümanını bir bilgi kaynağı olarak kullanarak, kullanıcıların Çevresel, Sosyal ve Yönetişim (ESG) konularındaki sorularını doğal dilde yanıtlayan bir yapay zeka asistanı oluşturmaktır. Chatbot, yalnızca kendisine sağlanan dokümandaki bilgilere sadık kalarak güvenilir ve doğru cevaplar üretir.


2. Veri Seti 

Veri Kaynağı: erdem-erdem-csy-terimler-sozlugu.pdf


İçerik: Bu doküman, Çevresel, Sosyal ve Yönetişim (ÇSY) alanındaki karmaşık ve genellikle detaylı terimleri ve kavramları açıklamayı amaçlamaktadır.

Hazırlanışı: Proje kapsamında bu PDF dokümanı, LangChain kütüphanesi kullanılarak metin parçalarına (chunks) ayrılmış ve anlamsal arama yapılabilmesi için vektör temsillerine dönüştürülmüştür.

3. Kullanılan Yöntemler ve Çözüm Mimarisi 


Proje, RAG (Retrieval-Augmented Generation) mimarisini temel almaktadır. İzlenen adımlar şunlardır:


Veri Yükleme ve Parçalama: PDF dokümanı PyPDFLoader ile yüklendi ve RecursiveCharacterTextSplitter ile anlamlı metin parçalarına ayrıldı.


Embedding Oluşturma: Metin parçaları, HuggingFaceEmbeddings kullanılarak çok dilli sentence-transformers/paraphrase-multilingual-mpnet-base-v2 modeli ile vektörlere dönüştürüldü.


Vektör Veritabanı: Elde edilen vektörler, verimli bir anlamsal arama için FAISS kütüphanesi kullanılarak yerel bir veritabanında saklandı.

Retrieval: Kullanıcının sorusuna en çok benzeyen metin parçaları, oluşturulan FAISS veritabanından (retriever) çekildi.


Generation: Google'ın gemini-pro-latest modeli, hem kullanıcının sorusunu hem de veritabanından çekilen ilgili metin parçalarını (bağlam) alarak, bu bağlama sadık kalacak şekilde bir cevap üretti.

Web Arayüzü: Tüm bu yapı, Streamlit kütüphanesi kullanılarak interaktif bir chatbot arayüzü üzerinden kullanıcıya sunuldu.


Ana Teknolojiler: Python, LangChain, Google Gemini, FAISS, Hugging Face Transformers, Streamlit.

4. Çalışma Kılavuzu 

Bu projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

Depoyu Klonlayın:

Bash

git clone https://github.com/KULLANICI_ADINIZ/DEPO_ADINIZ.git
cd DEPO_ADINIZ

Sanal Ortam Oluşturun ve Aktif Edin:

Bash

python -m venv .venv
# Windows için
.venv\Scripts\activate

Gerekli Kütüphaneleri Yükleyin:

Bash

pip install -r requirements.txt
API Anahtarını Ayarlayın:
Bu proje Google Gemini API'sini kullanmaktadır. Bir GOOGLE_API_KEY edinmeniz ve bunu sisteminizde bir ortam değişkeni olarak ayarlamanız gerekmektedir.


Uygulamayı Çalıştırın:

Bash

streamlit run app.py
5. Web Arayüzü & Product Kılavuzu 

Uygulama başlatıldığında, sizi basit ve kullanıcı dostu bir sohbet arayüzü karşılar.


Kullanım: Alttaki metin giriş kutusuna ÇSY Sözlüğü ile ilgili sorunuzu yazın ve "Enter" tuşuna basın.

Örnek Sorular: "Yeşil Tahvil nedir?", "Sürdürülebilirlik Raporlaması ne anlama gelir?"

<img width="1923" height="1093" alt="image" src="https://github.com/user-attachments/assets/425e7009-2672-42f7-ad43-b681dac97466" />


Web Linki: https://cambulak-akbank-genai-chatbot-app-oylacc.streamlit.app/ 
