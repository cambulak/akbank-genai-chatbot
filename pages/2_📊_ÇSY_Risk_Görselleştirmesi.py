# pages/2_📊_ÇSY_Risk_Görselleştirmesi.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="ÇSY Risk Görselleştirmesi", layout="wide")

st.title("Kurumsal Sürdürülebilirlik (ÇSY) Risk Kategorileri")
st.write(
    "Bu interaktif görselleştirme, Borsa İstanbul Sürdürülebilirlik Rehberi'nde belirtilen ÇSY risklerini hiyerarşik olarak göstermektedir. Kutucukların üzerine gelerek detayları ve tanımlarını görebilirsiniz.")

# Tanımlar
definitions = {
    'Çevresel Riskler': 'Doğal çevrenin ve doğal sistemlerin kalitesi ile işleyişi ile ilgili konulardır.',
    'Sosyal Riskler': 'Bir işletmenin işgücü, insan hakları ve çevresindeki toplumu etkileyen eylemleriyle ilgili konulardır.',
    'Yönetişim Riskleri': 'Şirketlerin ve yatırım yapılan diğer kuruluşların yönetişimine ilişkin konulardır.',
    'İklim Değişikliği': 'İklim olaylarındaki değişimlerden kaynaklanan fiziksel ve düşük karbon ekonomisine geçişten kaynaklanan geçiş risklerini içerir.',
    'Doğal Kaynak Kullanımı': 'Malzeme döngülerinin geri dönüşümü, atık yönetimi, biyoçeşitliliğin korunması ve sürdürülebilir su yönetimi gibi konuları kapsar.',
    'İnsan Kaynakları Yönetimi': 'İş sağlığı ve güvenliği, yeteneklerin çekilmesi, elde tutulması ve kurum içinde çeşitlilik, eşit fırsatlar ve refah gibi konuları içerir.',
    'Ürün Sorumluluğu': 'Ürün güvenilirliği, kalite ve güvenlik yönetmeliklerine uygunluğun garanti edilmesiyle ilgilidir.',
    'Toplumsal Etkiler': 'Yerel alanlarda güven kaybı ve üretilen katma değerin dengeli yönetimi ve dağıtımı gibi konuları kapsar.',
    'İş Etiği ve Kurumsal Davranış': 'Yolsuzluk, rüşvet gibi hukuka aykırı davranışların önlenmesi ve sorumlu tedarik uygulamalarının benimsenmesidir.',
    'Politika ve Düzenleyici Değişiklikler': 'İklimle ilgili yeni veya değişen düzenlemeler nedeniyle ortaya çıkabilecek işletme maliyetleri veya varlık değer düşüklüğü riskleri.',
    'İnovasyon Geliştirme': 'Yenilikçi ve ekolojik açıdan sorumlu ürün ve teknolojilerin zamanında geliştirilmemesi riski.',
    'Karbon Ayak İzi Azaltma': 'Şirketin faaliyetleri sonucu ürettiği toplam sera gazı emisyonlarının (karbon ayak izi) etkili bir şekilde azaltılmasına yönelik çabalar.',
    'Fiziksel Riskler': 'Sıklığı ve şiddeti artan fırtına, sel, kuraklık gibi aşırı hava olaylarından kaynaklanan akut ve kronik riskler.',
    'Döngüsel Ekonomi': 'Atık oluşumunu en aza indirirken, ürün ve malzemelerin değerini mümkün olduğunca uzun süre korumayı amaçlayan sistem.',
    'Biyoçeşitlilik': 'Doğal habitatların bozulmasını azaltma, türlerin neslinin tükenmesini engelleme ve ekosistemleri koruma çabaları.',
    'Su Yönetimi': 'Şirketin su tüketimini yönetmesi, su tasarrufu için adımlar atması ve su kaynaklarının sürdürülebilir kullanımını sağlaması.',
    'İş Sağlığı ve Güvenliği': 'Şirketin en değerli varlığı olan insan kaynağını korumaya yönelik politikalar ve uygulamalar bütünü.',
    'Yetenek Yönetimi': 'Nitelikli yetenekleri şirkete çekme, elde tutma ve mesleki gelişimlerini sağlama faaliyetleri.',
    'Çeşitlilik ve Eşitlik': 'Kurum içinde çeşitlilik, eşit fırsatlar ve refah ortamının sağlanması; ırk, cinsiyet, köken ayrımı yapmaksızın adil muamele.',
    'Ürün Güvenilirliği': 'Ürünlerin kalite, güvenlik yönetmelikleri ve standartlarına uygunluğunun garanti edilmesi.',
    'Yerel Güven Kaybı': 'Şirket faaliyetlerinin yerel topluluklar üzerindeki olumsuz etkileri sonucu ortaya çıkan itibar ve güven riski.',
    'Katma Değer Dağıtımı': 'Şirketin ürettiği ekonomik değerin paydaşlar (çalışanlar, toplum vb.) arasında dengeli bir şekilde yönetilmesi ve dağıtılması.',
    'Hukuka Aykırı Davranışların Önlenmesi': 'Yolsuzluk, gasp ve rüşvet dahil olmak üzere hukuka aykırı davranışların önlenmesi, tespiti ve bunlarla mücadele edilmesi.',
    'Sorumlu Tedarik Zinciri': 'Küresel değer zincirinde etik ihlallerin önlenmesi ve sorumlu tedarik uygulamalarının benimsenmesi.'
}

# Veri yapısı
data = {
    'ids': [
        'ÇSY Riskleri', 'Çevresel Riskler', 'Sosyal Riskler', 'Yönetişim Riskleri',
        'İklim Değişikliği', 'Doğal Kaynak Kullanımı', 'İnsan Kaynakları Yönetimi', 'Ürün Sorumluluğu',
        'Toplumsal Etkiler',
        'İş Etiği ve Kurumsal Davranış', 'Politika ve Düzenleyici Değişiklikler', 'İnovasyon Geliştirme',
        'Karbon Ayak İzi Azaltma', 'Fiziksel Riskler',
        'Döngüsel Ekonomi', 'Biyoçeşitlilik', 'Su Yönetimi', 'İş Sağlığı ve Güvenliği', 'Yetenek Yönetimi',
        'Çeşitlilik ve Eşitlik',
        'Ürün Güvenilirliği', 'Yerel Güven Kaybı', 'Katma Değer Dağıtımı', 'Hukuka Aykırı Davranışların Önlenmesi',
        'Sorumlu Tedarik Zinciri'
    ],
    'parents': [
        '', 'ÇSY Riskleri', 'ÇSY Riskleri', 'ÇSY Riskleri',
        'Çevresel Riskler', 'Çevresel Riskler', 'Sosyal Riskler', 'Sosyal Riskler', 'Sosyal Riskler',
        'Yönetişim Riskleri', 'İklim Değişikliği', 'İklim Değişikliği', 'İklim Değişikliği', 'İklim Değişikliği',
        'Doğal Kaynak Kullanımı', 'Doğal Kaynak Kullanımı', 'Doğal Kaynak Kullanımı', 'İnsan Kaynakları Yönetimi',
        'İnsan Kaynakları Yönetimi', 'İnsan Kaynakları Yönetimi',
        'Ürün Sorumluluğu', 'Toplumsal Etkiler', 'Toplumsal Etkiler', 'İş Etiği ve Kurumsal Davranış',
        'İş Etiği ve Kurumsal Davranış'
    ],
    'labels': [
        'ÇSY Riskleri', 'Çevresel Riskler', 'Sosyal Riskler', 'Yönetişim Riskleri',
        'İklim Değişikliği', 'Doğal Kaynakların Kullanımı', 'İnsan Kaynakları Yönetimi', 'Ürün Sorumluluğu',
        'Toplum Üzerindeki Etkiler',
        'İş Etiği', 'Politika Değişiklikleri', 'Yenilik Geliştirme', 'Karbon Ayak İzini Azaltma', 'Fiziksel Riskler',
        'Döngüsel Ekonomi', 'Biyoçeşitlilik Korunması', 'Su Yönetimi', 'İş Sağlığı ve Güvenliği',
        'Yetenekleri Çekme/Tutma', 'Çeşitlilik ve Eşit Fırsatlar',
        'Ürün Güvenilirliği', 'Yerel Güven Kaybı', 'Katma Değer Dağıtımı', 'Yolsuzluğun Önlenmesi',
        'Sorumlu Tedarik Zinciri'
    ],
    'values': [
        0, 14, 10, 4, 4, 3, 3, 1, 2, 2,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
    ]
}

df = pd.DataFrame(data)
df['definitions'] = df['ids'].map(definitions)

fig = go.Figure(go.Treemap(
    ids=df['ids'],
    labels=df['labels'],
    parents=df['parents'],
    values=df['values'],
    root_color="lightgrey",
    textinfo="label",

    # --- DEĞİŞİKLİK: Metni ortalamak için parametre ekliyoruz ---
    textposition='middle center',

    customdata=df['definitions'],
    hovertemplate='<b>%{label}</b><br>Ana Kategori: %{parent}<br><br><b>Tanım:</b> %{customdata}<extra></extra>'
))

fig.update_layout(
    treemapcolorway=["#1f77b4", "#ff7f0e", "#2ca02c"],
    margin=dict(t=25, l=25, r=25, b=25)
)

st.plotly_chart(fig, use_container_width=True)
st.caption("Kaynak: Borsa İstanbul - Sürdürülebilirlik Rehberi (Sayfa 24) ve Erdem & Erdem - ÇSY Terimler Sözlüğü")