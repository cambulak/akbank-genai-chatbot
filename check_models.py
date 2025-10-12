# check_models.py

import os
import google.generativeai as genai

# Adım 1'de ayarladığımız ortam değişkenini oku
api_key = os.environ.get('GOOGLE_API_KEY')

if not api_key:
    print("HATA: GOOGLE_API_KEY ortam değişkeni bulunamadı.")
    print(
        "Lütfen Windows ortam değişkenlerini ayarladığınızdan ve terminali/IDE'yi yeniden başlattığınızdan emin olun.")
else:
    try:
        genai.configure(api_key=api_key)

        print("API Anahtarı başarıyla yapılandırıldı.")
        print("-" * 30)
        print("Hesabınızla kullanabileceğiniz uyumlu modeller:")

        for model in genai.list_models():
            # Sadece 'generateContent' metodunu destekleyen, yani sohbet/metin üretimi
            # yapabilen modelleri listeliyoruz.
            if 'generateContent' in model.supported_generation_methods:
                print(f"- {model.name}")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")