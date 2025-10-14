# pages/2_📊_ÇSY_Risk_Görselleştirmesi.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="ÇSY Risk Görselleştirmesi", layout="wide")

st.title("Kurumsal Sürdürülebilirlik (ÇSY) Risk Kategorileri")
st.write("Bu interaktif görselleştirme, Borsa İstanbul Sürdürülebilirlik Rehberi'nde belirtilen ÇSY risklerini hiyerarşik olarak göstermektedir. Kutucukların üzerine gelerek detayları görebilirsiniz.")

# "Sürdürülebilirlik Rehberi_2020.pdf" Sayfa 24'teki risk sınıflandırmasına dayalı veri
data = {
    'ids': [
        'ÇSY Riskleri',
        'Çevresel Riskler', 'Sosyal Riskler', 'Yönetişim Riskleri',
        'İklim Değişikliği', 'Doğal Kaynak Kullanımı',
        'İnsan Kaynakları Yönetimi', 'Ürün Sorumluluğu', 'Toplumsal Etkiler',
        'İş Etiği ve Kurumsal Davranış',
        'Politika ve Düzenleyici Değişiklikler', 'İnovasyon Geliştirme', 'Karbon Ayak İzi Azaltma', 'Fiziksel Riskler',
        'Döngüsel Ekonomi', 'Biyoçeşitlilik', 'Su Yönetimi',
        'İş Sağlığı ve Güvenliği', 'Yetenek Yönetimi', 'Çeşitlilik ve Eşitlik',
        'Ürün Güvenilirliği',
        'Yerel Güven Kaybı', 'Katma Değer Dağıtımı',
        'Hukuka Aykırı Davranışların Önlenmesi', 'Sorumlu Tedarik Zinciri'
    ],
    'parents': [
        '',
        'ÇSY Riskleri', 'ÇSY Riskleri', 'ÇSY Riskleri',
        'Çevresel Riskler', 'Çevresel Riskler',
        'Sosyal Riskler', 'Sosyal Riskler', 'Sosyal Riskler',
        'Yönetişim Riskleri',
        'İklim Değişikliği', 'İklim Değişikliği', 'İklim Değişikliği', 'İklim Değişikliği',
        'Doğal Kaynak Kullanımı', 'Doğal Kaynak Kullanımı', 'Doğal Kaynak Kullanımı',
        'İnsan Kaynakları Yönetimi', 'İnsan Kaynakları Yönetimi', 'İnsan Kaynakları Yönetimi',
        'Ürün Sorumluluğu',
        'Toplumsal Etkiler', 'Toplumsal Etkiler',
        'İş Etiği ve Kurumsal Davranış', 'İş Etiği ve Kurumsal Davranış'
    ],
    'labels': [
        'ÇSY Riskleri',
        'Çevresel Riskler', 'Sosyal Riskler', 'Yönetişim Riskleri',
        'İklim Değişikliği', 'Doğal Kaynakların Kullanımı',
        'İnsan Kaynakları Yönetimi', 'Ürün Sorumluluğu', 'Toplum Üzerindeki Etkiler',
        'İş Etiği ve Kurumsal Davranış',
        'Politika Değişiklikleri', 'Yenilik Geliştirme', 'Karbon Ayak İzini Azaltma', 'Fiziksel Riskler',
        'Döngüsel Ekonomi', 'Biyoçeşitlilik Korunması', 'Sürdürülebilir Su Yönetimi',
        'İş Sağlığı ve Güvenliği', 'Yetenekleri Çekme ve Elde Tutma', 'Çeşitlilik, Eşit Fırsatlar ve Refah',
        'Ürün Güvenilirliği ve Kalitesi',
        'Yerel Alanlarda Güven Kaybı', 'Katma Değerin Dengeli Dağıtımı',
        'Yolsuzluk ve Rüşvetin Önlenmesi', 'Sorumlu Tedarik Zinciri Uygulamaları'
    ],
    'values': [
        0,
        14, 10, 4, # Ana kategorilerin boyutu (alt öğelerin sayısı)
        4, 3,
        3, 1, 2,
        2,
        1, 1, 1, 1, # En alt dallar (her biri 1 birim)
        1, 1, 1,
        1, 1, 1,
        1,
        1, 1,
        1, 1
    ]
}

df = pd.DataFrame(data)

fig = go.Figure(go.Treemap(
    ids=df['ids'],
    labels=df['labels'],
    parents=df['parents'],
    root_color="lightgrey",
    textinfo="label+value",
    hoverinfo="label+value"
))

fig.update_layout(
    treemapcolorway=["#1f77b4", "#ff7f0e", "#2ca02c"], # Çevresel, Sosyal, Yönetişim için renkler
    margin = dict(t=25, l=25, r=25, b=25)
)

# Grafiği Streamlit arayüzünde göster
st.plotly_chart(fig, use_container_width=True)

st.caption("Kaynak: Borsa İstanbul - Sürdürülebilirlik Rehberi (Sayfa 24)")