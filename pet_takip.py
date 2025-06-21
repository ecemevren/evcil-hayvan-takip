# -*- coding: utf-8 -*-
"""
Created on Sat Jun 21 18:33:09 2025

@author: evren
"""
import os
import pandas as pd

# Boş CSV dosyalarını oluştur (uygulama ilk defa açıldığında)
if not os.path.exists("pet_kayitlari.csv"):
    df = pd.DataFrame(columns=[
        "Pet Adı", "Tür", "Irk", "Yaş", "Cinsiyet", "Kısırlaştırma Durumu",
        "Mevcut Hastalıklar", "Geçirilmiş Hastalıklar", "Geçirilmiş Operasyonlar",
        "Kullanılan İlaçlar", "Hasta Sahibi", "Telefon"
    ])
    df.to_csv("pet_kayitlari.csv", index=False)

if not os.path.exists("kilo_takibi.csv"):
    df = pd.DataFrame(columns=[
        "Pet Adı", "Tarih", "Kilo", "Verilen Mama (g)", "Toplam Enerji (kcal)"
    ])
df.to_csv("kilo_takibi.csv", index=False)
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Evcil Hayvan Sağlık Takip", layout="wide")

st.title("🐾 Evcil Hayvan Sağlık ve Kilo Takip Sistemi")

# --- Hayvan Kayıt Bölümü ---
st.sidebar.header("Yeni Evcil Hayvan Kaydı")

pet_adi = st.sidebar.text_input("Pet Adı")
tur = st.sidebar.selectbox("Tür", ["Kedi", "Köpek", "Diğer"])
irk = st.sidebar.text_input("Irk")
yas = st.sidebar.number_input("Yaş", min_value=0)
cinsiyet = st.sidebar.radio("Cinsiyet", ["Dişi", "Erkek"])
kisir = st.sidebar.radio("Kısırlaştırma Durumu", ["Evet", "Hayır"])
mevcut_hastaliklar = st.sidebar.text_area("Mevcut Hastalıklar (virgülle ayır)")
gecirilen_hastaliklar = st.sidebar.text_area("Geçirilmiş Hastalıklar (virgülle ayır)")
gecirilen_operasyonlar = st.sidebar.text_area("Geçirilmiş Operasyonlar (virgülle ayır)")
kullanilan_ilaclar = st.sidebar.text_area("Kullanılan İlaçlar (virgülle ayır)")
sahip = st.sidebar.text_input("Hasta Sahibi Adı")
telefon = st.sidebar.text_input("Hasta Sahibi Telefon")

if st.sidebar.button("Yeni Hayvanı Kaydet"):
    yeni_pet = {
        "Pet Adı": pet_adi,
        "Tür": tur,
        "Irk": irk,
        "Yaş": yas,
        "Cinsiyet": cinsiyet,
        "Kısırlaştırma Durumu": kisir,
        "Mevcut Hastalıklar": mevcut_hastaliklar,
        "Geçirilmiş Hastalıklar": gecirilen_hastaliklar,
        "Geçirilmiş Operasyonlar": gecirilen_operasyonlar,
        "Kullanılan İlaçlar": kullanilan_ilaclar,
        "Hasta Sahibi": sahip,
        "Telefon": telefon
    }
    try:
        df_pets = pd.read_csv("pet_kayitlari.csv")
    except FileNotFoundError:
        df_pets = pd.DataFrame()
    df_pets = pd.concat([df_pets, pd.DataFrame([yeni_pet])], ignore_index=True)
    df_pets.to_csv("pet_kayitlari.csv", index=False)
    st.sidebar.success(f"{pet_adi} başarıyla kaydedildi!")

# --- Ana Gösterim Alanı ---
st.header("📊 Evcil Hayvan Seçimi ve Takibi")

try:
    df_pets = pd.read_csv("pet_kayitlari.csv")
    pet_list = df_pets["Pet Adı"].tolist()
except:
    st.warning("Henüz hayvan kaydı yok. Lütfen yan taraftan yeni hayvan kaydedin.")
    pet_list = []

secili_pet = st.selectbox("Takip Edilecek Hayvanı Seç", pet_list)

if secili_pet:
    df_pet = df_pets[df_pets["Pet Adı"] == secili_pet].iloc[0]

    # Hayvan Detaylarını Göster
    st.subheader(f"{secili_pet} - Temel Bilgiler")
    st.write(f"Tür: {df_pet['Tür']}")
    st.write(f"Irk: {df_pet['Irk']}")
    st.write(f"Yaş: {df_pet['Yaş']}")
    st.write(f"Cinsiyet: {df_pet['Cinsiyet']}")
    st.write(f"Kısırlaştırma: {df_pet['Kısırlaştırma Durumu']}")
    st.write(f"Mevcut Hastalıklar: {df_pet['Mevcut Hastalıklar']}")
    st.write(f"Geçirilmiş Hastalıklar: {df_pet['Geçirilmiş Hastalıklar']}")
    st.write(f"Geçirilmiş Operasyonlar: {df_pet['Geçirilmiş Operasyonlar']}")
    st.write(f"Kullanılan İlaçlar: {df_pet['Kullanılan İlaçlar']}")
    st.write(f"Hasta Sahibi: {df_pet['Hasta Sahibi']}")
    st.write(f"Telefon: {df_pet['Telefon']}")

    # Kilo Takip Girişi
    st.subheader(f"{secili_pet} için Kilo ve Mama Takibi")

    kilo = st.number_input("Güncel Kilo (kg)", min_value=0.0, format="%.2f")
    tarih = st.date_input("Tarih", datetime.today())
    verilen_mama = st.number_input("Verilen Mama Miktarı (g)", min_value=0)
    mama_kcal = st.number_input("Mama Enerjisi (kcal/g)", min_value=0.0, format="%.2f")

    if st.button("Kilo ve Mama Kaydet"):
        yeni_kilo = {
            "Pet Adı": secili_pet,
            "Tarih": tarih.strftime("%Y-%m-%d"),
            "Kilo": kilo,
            "Verilen Mama (g)": verilen_mama,
            "Toplam Enerji (kcal)": verilen_mama * mama_kcal
        }
        try:
            df_kilo = pd.read_csv("kilo_takibi.csv")
        except FileNotFoundError:
            df_kilo = pd.DataFrame()
        df_kilo = pd.concat([df_kilo, pd.DataFrame([yeni_kilo])], ignore_index=True)
        df_kilo.to_csv("kilo_takibi.csv", index=False)
        st.success("Kilo ve mama bilgileri kaydedildi!")

    # --- Grafik ve İdeal Kilo Analizi ---
    st.subheader("Aylık Kilo Takibi ve İdeal Kilo")

    try:
        df_kilo = pd.read_csv("kilo_takibi.csv")
        df_pet_kilo = df_kilo[df_kilo["Pet Adı"] == secili_pet]
        df_pet_kilo["Tarih"] = pd.to_datetime(df_pet_kilo["Tarih"])
        df_pet_kilo = df_pet_kilo.sort_values("Tarih")

        # İdeal kilo basit örnek:
        if df_pet["Tür"] == "Kedi":
            ideal_min, ideal_max = 3, 5
        elif df_pet["Tür"] == "Köpek":
            ideal_min, ideal_max = 5, 30
        else:
            ideal_min, ideal_max = 1, 10

        fig = px.line(df_pet_kilo, x="Tarih", y="Kilo", title=f"{secili_pet} Aylık Kilo Takibi")
        fig.add_hline(y=ideal_min, line_dash="dot", line_color="green", annotation_text="İdeal Min")
        fig.add_hline(y=ideal_max, line_dash="dot", line_color="red", annotation_text="İdeal Max")

        st.plotly_chart(fig)

        if not df_pet_kilo.empty:
            son_kilo = df_pet_kilo["Kilo"].iloc[-1]
            if son_kilo < ideal_min:
                st.warning("⚠️ Kilo düşük, veteriner önerisi alın.")
            elif son_kilo > ideal_max:
                st.warning("⚠️ Kilo yüksek, diyet önerilir.")
            else:
                st.success("✅ Kilo ideal aralıkta.")

        # Mama Miktarı Önerisi (Basit Formül Örnek)
        ideal_mama_kcal = son_kilo * 50  # Örnek: kilo x 50 kcal
        if mama_kcal > 0:
            ideal_mama_g = ideal_mama_kcal / mama_kcal
            st.info(f"💡 Tavsiye edilen mama miktarı: {ideal_mama_g:.1f} gram/gün")
        else:
            st.info("Mama kalori bilgisini giriniz.")

    except Exception as e:
        st.error("Kilo verisi bulunamadı veya hata oluştu.")

    # --- Hayvanlar Arası Karşılaştırma ---
    st.subheader("🐕🐈 Tüm Hayvanların Kilo Karşılaştırması")

    try:
        df_kilo = pd.read_csv("kilo_takibi.csv")
        df_pets = pd.read_csv("pet_kayitlari.csv")
        df_merge = pd.merge(df_kilo, df_pets[["Pet Adı", "Tür"]], on="Pet Adı", how="left")
        if not df_merge.empty:
            fig2 = px.box(df_merge, x="Tür", y="Kilo", points="all", title="Türlere Göre Kilo Dağılımı")
            st.plotly_chart(fig2)
        else:
            st.info("Henüz kilo verisi yok.")
    except:
        st.info("Henüz kilo verisi yok.")
else:
    st.info("Lütfen bir hayvan seçin veya yeni hayvan kaydedin.")


