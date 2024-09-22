# -*- coding: utf-8 -*-
"""Dashboard Technical Test.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1M1aXYbgPJK7NyC7qmAMxlNUp-teO9WtB
"""

#!pip install streamlit babel

# Commented out IPython magic to ensure Python compatibility.
# %%writefile dashboard.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from matplotlib.colors import TwoSlopeNorm
sns.set(style='white')

df = pd.read_csv("https://raw.githubusercontent.com/AmrulFY/TechnicalTest-AnalisisData/refs/heads/main/dataset_final.csv")

with st.sidebar:
    st.image("https://github.com/AmrulFY/TechnicalTest-AnalisisData/blob/929cbfe54b1c4a2c37a65f456776d7099c3de3ad/logo_alfa.png")

    st.sidebar.title("Filter Data")
    selected_wilayah = st.sidebar.multiselect("Pilih Nama Cabang",
                                              options=df['NAMA_CABANG'].unique(),
                                              default=None)
    filtered_data = df[df['NAMA_CABANG'].isin(selected_wilayah)]

    st.title("Data Toko Berdasarkan Nama Cabang")
    st.dataframe(filtered_data)

st.header('Technical Test Dashboard :sparkles:')

st.subheader('Jumlah Cabang dan Divisi Tahun 2017')

kol1, kol2 = st.columns(2)

with kol1:
    total_cab = df["NAMA_CABANG"].nunique()
    st.metric("Total Cabang", value=total_cab)

with kol2:
    total_div = df["DIVISI"].nunique()
    st.metric("Total Divisi", value=total_div)

st.subheader('Persebaran Toko Pada Setiap Wilayah/Cabang Tahun 2017')

plt.figure(figsize=(8, 10))
order = df['NAMA_CABANG'].value_counts().index
sns.countplot(y='NAMA_CABANG', data=df, palette='viridis', order=order, legend=False)

plt.title('Persebaran Toko Berdasarkan Wilayah', fontsize=16)
plt.xlabel('Jumlah Toko', fontsize=12)
plt.ylabel('Wilayah', fontsize=12)
st.pyplot(plt)

st.subheader("Distribusi Penyebab Masalah Pada Setiap Divisi")

problem_distribution = df.groupby(['DIVISI', 'FAKTOR_PROBLEM']).size().unstack().fillna(0)
problem_distribution.plot(kind='bar', stacked=True, figsize=(10, 6), cmap='Set2')

plt.title('Distribusi Faktor Masalah pada Masing-masing Divisi', fontsize=16)
plt.xlabel('Divisi', fontsize=12)
plt.ylabel('Jumlah Kasus', fontsize=12)

plt.legend(title='Faktor Problem', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(plt)

st.subheader("Analisis Waktu Penyelesaian Masalah")

col1, col2 = st.columns(2)

with col1:
    plt.figure(figsize=(10, 6))
    sns.histplot(df['WAKTU_PENYELESAIAN'], bins=30, kde=True, color='navy')

    plt.title('Distribusi Waktu Penyelesaian Masalah', fontsize=16)
    plt.xlabel('Waktu Penyelesaian (hari)', fontsize=12)
    plt.ylabel('Frekuensi', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(plt)

with col2:
    batas_bin_wp = [-1,5,20,500]
    kategori_wp = ['0-5','6-20','21-500']
    df1 = (pd.cut(df['WAKTU_PENYELESAIAN'], bins=batas_bin_wp, labels=kategori_wp)).copy()

    plt.figure(figsize=(10, 6))
    sns.histplot(df1, bins=30, kde=True, color='navy')

    plt.title('Distribusi Waktu Penyelesaian Masalah (Setelah Proses Binning)', fontsize=16)
    plt.xlabel('Range (hari)', fontsize=12)
    plt.ylabel('Frekuensi', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(plt)

st.subheader("Identifikasi Penyebab Masalah")
plt.figure(figsize=(10, 6))

order = df['FAKTOR_PROBLEM'].value_counts().index
sns.countplot(y='FAKTOR_PROBLEM', data=df, palette='mako', order=order, legend=False)

plt.title('Data Penyebab Masalah', fontsize=16)
plt.xlabel('Frekuensi', fontsize=12)
plt.ylabel('Faktor Masalah', fontsize=12)
st.pyplot(plt)

st.subheader("Analisis Tingkat Kepuasan dan Pengaruh Faktor Masalah Terhadap Tingkat Kepuasan")

kolom1, kolom2 = st.columns(2)

with kolom1:
    labels = [4,3,2,1]
    sizes = df['TINGKAT_KEPUASAN'].value_counts()
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    explode = (0.1, 0, 0, 0)

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
       autopct='%1.1f%%', shadow=True, startangle=140)
    ax.axis('equal')
    plt.title('Tingkat Kepuasan Pelanggan')
    st.pyplot(fig)

with kolom2:
    total_fp = df["FAKTOR_PROBLEM"].nunique()
    st.metric("FAKTOR_PROBLEM", value=total_fp)

plt.figure(figsize=(12, 8))

sns.boxplot(x='TINGKAT_KEPUASAN', y='FAKTOR_PROBLEM', data=df, palette='Set2', showmeans=True, meanline=True)

plt.title('Distribusi Tingkat Kepuasan Berdasarkan Faktor Masalah', fontsize=16)
plt.xlabel('Tingkat Kepuasan', fontsize=12)
plt.ylabel('Faktor Masalah', fontsize=12)
st.pyplot(plt)

st.subheader("Korelasi Waktu Penyelesaian Masalah dengan Tingkat Kepuasan")
plt.figure(figsize=(10, 6))
correlation = df[['WAKTU_PENYELESAIAN', 'TINGKAT_KEPUASAN']].corr()
sns.heatmap(correlation, annot=True)
st.pyplot(plt)

st.subheader("Perbandingan Rata-Rata Tingkat Kepuasan Berdasarkan Wilayah dan Divisi")
ko1, ko2 = st.columns(2)

with ko1:
    plt.figure(figsize=(6, 10))
    mean_st = df.groupby('NAMA_CABANG')['TINGKAT_KEPUASAN'].mean().reset_index()
    mean_st = mean_st.sort_values(by='TINGKAT_KEPUASAN', ascending=False)
    sns.barplot(y='NAMA_CABANG', x='TINGKAT_KEPUASAN', data=mean_st, estimator='mean', palette='coolwarm')

    plt.title('Rata-rata Tingkat Kepuasan Berdasarkan Wilayah', fontsize=16)
    plt.ylabel('Wilayah', fontsize=12)
    plt.xlabel('Rata-rata Tingkat Kepuasan', fontsize=12)
    st.pyplot(plt)

with ko2:
    plt.figure(figsize=(6, 10))
    mean_st = df.groupby('DIVISI')['TINGKAT_KEPUASAN'].mean().reset_index()
    mean_st = mean_st.sort_values(by='TINGKAT_KEPUASAN', ascending=False)
    sns.barplot(y='DIVISI', x='TINGKAT_KEPUASAN', data=mean_st, estimator='mean', palette='coolwarm')

    plt.title('Rata-rata Tingkat Kepuasan Berdasarkan Divisi', fontsize=16)
    plt.ylabel('Divisi', fontsize=12)
    plt.xlabel('Rata-rata Tingkat Kepuasan', fontsize=12)
    st.pyplot(plt)

st.caption('Copyright (c)')

# !streamlit run dashboard.py & npx localtunnel --port 8501

