import streamlit as st
import pandas as pd
import os

st.title("Evcil Hayvan Sağlık Takip Uygulaması")

# CSV dosyalarının varlığını kontrol et, yoksa oluştur
if not os.path.exists("pet_kayitlari.csv"):
    df_pets = pd.DataFrame(columns=[
        "Pet Adı", "Tür", "Irk", "Yaş", "Cinsiyet", "Kısırlaştırma Durumu",
        "Mevcut Hastalıklar", "Geçirilmiş Hastalıklar", "Geçirilmiş Operasyonlar",
        "Kullanılan İlaçlar", "Hasta Sahibi", "Telefon"
    ])
    df_pets.to_csv("pet_kayitlari.csv", index=False)

if not os.path.exists("kilo_takibi.csv"):
    df_kilo = pd.DataFrame(columns=[
        "Pet Adı", "Tarih", "Kilo", "Verilen Mama (g)", "Toplam Enerji (kcal)"
    ])
    df_kilo.to_csv("kilo_takibi.csv", index=False)

# Verileri oku
df_pets = pd.read_csv("pet_kayitlari.csv")
df_kilo = pd.read_csv("kilo_takibi.csv")

# Basit bir veri girişi formu örneği
st.header("Yeni Evcil Hayvan Kaydı")

with st.form(key="pet_form"):
    pet_adi = st.text_input("Pet Adı")
    tur = st.text_input("Tür")
    irk = st.text_input("Irk")
    yas = st.number_input("Yaş", min_value=0, max_value=50, step=1)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Dişi"])
    kisirlastirma = st.selectbox("Kısırlaştırma Durumu", ["Evet", "Hayır"])
    mevcut_hastaliklar = st.text_area("Mevcut Hastalıklar")
    gecmis_hastaliklar = st.text_area("Geçirilmiş Hastalıklar")
    gecmis_operasyonlar = st.text_area("Geçirilmiş Operasyonlar")
    kullanilan_ilaclar = st.text_area("Kullanılan İlaçlar")
    hasta_sahibi = st.text_input("Hasta Sahibi Adı")
    telefon = st.text_input("Telefon")

    submit_button = st.form_submit_button(label="Kaydet")

if submit_button:
    yeni_kayit = {
        "Pet Adı": pet_adi,
        "Tür": tur,
        "Irk": irk,
        "Yaş": yas,
        "Cinsiyet": cinsiyet,
        "Kısırlaştırma Durumu": kisirlastirma,
        "Mevcut Hastalıklar": mevcut_hastaliklar,
        "Geçirilmiş Hastalıklar": gecmis_hastaliklar,
        "Geçirilmiş Operasyonlar": gecmis_operasyonlar,
        "Kullanılan İlaçlar": kullanilan_ilaclar,
        "Hasta Sahibi": hasta_sahibi,
        "Telefon": telefon
    }
    df_pets = pd.concat([df_pets, pd.DataFrame([yeni_kayit])], ignore_index=True)
    df_pets.to_csv("pet_kayitlari.csv", index=False)
    st.success("Yeni evcil hayvan kaydı başarıyla eklendi!")

# Varolan kayıtları göster
st.header("Kayıtlı Evcil Hayvanlar")
st.dataframe(df_pets)
