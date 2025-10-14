# pages/2_📊_ÇSY_Risk_Görselleştirmesi.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="ÇSY Riskleri", layout="wide")

st.title("Kurumsal Sürdürülebilirlik (ÇSY) Risk Kategorileri")
st.write("Bu interaktif görselleştirme, Borsa İstanbul Sürdürülebilirlik Rehberi'nde belirtilen ÇSY risklerini hiyerarşik olarak göstermektedir. Kutucukların üzerine gelerek detayları ve tanımlarını görebilirsiniz.")

# --- DEĞİŞİKLİK 1: Tanımları ekliyoruz ---
definitions = {
    'Çevresel Riskler': 'Doğal çevrenin ve doğal sistemlerin kalitesi ve işleyişi ile ilgili konular.',
    'Sosyal Riskler': 'Bir işletmenin işgücü, insan hakları ve çevresindeki toplumu etkileyen eylemleriyle ilgili konular.',
    'Yönetişim Riskleri': 'Şirketlerin ve yatırım yapılan diğer kuruluşların yönetişimine ilişkin konular.',
    'İklim Değişikliği': 'Sıklığı ve şiddeti artan fırtına, sel, kuraklık gibi olaylara bağlı akut fiziksel riskler ve iklim olaylarındaki uzun vadeli değişimlerden kaynaklanan kronik fiziksel riskler.',
    'Doğal Kaynak Kullanımı': 'Malzeme döngülerinin geri dönüşümü, atık yönetimi, biyoçeşitliliğin korunması ve sürdürülebilir su yönetimi gibi konuları kapsar.',
    'İnsan Kaynakları Yönetimi': 'İş sağlığı ve güvenliği, yeteneklerin çekilmesi, elde tutulması ve kurum içinde çeşitlilik, eşit fırsatlar ve refah gibi konuları içerir.',
    'Ürün Sorumluluğu': 'Ürün güvenilirliği, kalite ve güvenlik yönetmeliklerine uygunluğun garanti edilmesi.',
    'Toplumsal Etkiler': 'Yerel alanlarda güven kaybı ve üretilen katma değerin dengeli yönetimi ve dağıtımı.',
    'İş Etiği ve Kurumsal Davranış': 'Çalışanların hukuka aykırı davranışlarının (yolsuzluk, rüşvet) önlenmesi ve sorumlu tedarik uygulamalarının benimsenmesi.'
}

# Veri yapısını oluşturma
data = {
    'ids': [
        'ÇSY Riskleri', 'Çevresel Riskler', 'Sosyal Riskler', 'Yönetişim Riskleri',
        'İklim Değişikliği', 'Doğal Kaynak Kullanımı', 'İnsan Kaynakları Yönetimi', 'Ürün Sorumluluğu', 'Toplumsal Etkiler',
        'İş Etiği ve Kurumsal Davranış', 'Politika ve Düzenleyici Değişiklikler', 'İnovasyon Geliştirme', 'Karbon Ayak İzi Azaltma', 'Fiziksel Riskler',
        'Döngüsel Ekonomi', 'Biyoçeşitlilik', 'Su Yönetimi', 'İş Sağlığı ve Güvenliği', 'Yetenek Yönetimi', 'Çeşitlilik ve Eşitlik',
        'Ürün Güvenilirliği', 'Yerel Güven Kaybı', 'Katma Değer Dağıtımı', 'Hukuka Aykırı Davranışların Önlenmesi', 'Sorumlu Tedarik Zinciri'
    ],
    'parents': [
        '', 'ÇSY Riskleri', 'ÇSY Riskleri', 'ÇSY Riskleri',
        'Çevresel Riskler', 'Çevresel Riskler', 'Sosyal Riskler', 'Sosyal Riskler', 'Sosyal Riskler',
        'Yönetişim Riskleri', 'İklim Değişikliği', 'İklim Değişikliği', 'İklim Değişikliği', 'İklim Değişikliği',
        'Doğal Kaynak Kullanımı', 'Doğal Kaynak Kullanımı', 'Doğal Kaynak Kullanımı', 'İnsan Kaynakları Yönetimi', 'İnsan Kaynakları Yönetimi', 'İnsan Kaynakları Yönetimi',
        'Ürün Sorumluluğu', 'Toplumsal Etkiler', 'Toplumsal Etkiler', 'İş Etiği ve Kurumsal Davranış', 'İş Etiği ve Kurumsal Davranış'
    ],
    'labels': [
        'ÇSY Riskleri', 'Çevresel Riskler', 'Sosyal Riskler', 'Yönetişim Riskleri',
        'İklim Değişikliği', 'Doğal Kaynakların Kullanımı', 'İnsan Kaynakları Yönetimi', 'Ürün Sorumluluğu', 'Toplum Üzerindeki Etkiler',
        'İş Etiği', 'Politika Değişiklikleri', 'Yenilik Geliştirme', 'Karbon Ayak İzini Azaltma', 'Fiziksel Riskler',
        'Döngüsel Ekonomi', 'Biyoçeşitlilik Korunması', 'Su Yönetimi', 'İş Sağlığı ve Güvenliği', 'Yetenekleri Çekme/Tutma', 'Çeşitlilik ve Eşit Fırsatlar',
        'Ürün Güvenilirliği', 'Yerel Güven Kaybı', 'Katma Değer Dağıtımı', 'Yolsuzluğun Önlenmesi', 'Sorumlu Tedarik Zinciri'
    ],
    'values': [
        0, 14, 10, 4, 4, 3, 3, 1, 2, 2,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
    ]
}

df = pd.DataFrame(data)
# Tanımları DataFrame'e ekle
df['definitions'] = df['ids'].map(definitions).fillna('Detaylı alt kategoridir.')

fig = go.Figure(go.Treemap(
    ids=df['ids'],
    labels=df['labels'],
    parents=df['parents'],
    values=df['values'],
    root_color="lightgrey",
    textinfo="label",
    # --- DEĞİŞİKLİK 2: Hovertemplate'i tanımları içerecek şekilde güncelle ---
    customdata=df['definitions'],
    hovertemplate='<b>%{label}</b><br>Ana Kategori: %{parent}<br>Tanım: %{customdata}<extra></extra>'
))

fig.update_layout(
    treemapcolorway=["#1f77b4", "#ff7f0e", "#2ca02c"],
    margin=dict(t=25, l=25, r=25, b=25)
)

st.plotly_chart(fig, use_container_width=True)
st.caption("Kaynak: Borsa İstanbul - Sürdürülebilirlik Rehberi (Sayfa 24) ve Erdem & Erdem - ÇSY Terimler Sözlüğü")