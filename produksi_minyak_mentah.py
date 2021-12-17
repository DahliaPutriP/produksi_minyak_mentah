'''
Aplikasi Streamlit untuk menggambarkan statistik produksi minyak mentah

Sumber data berasal dari “produksi_minyak_mentah.csv”
Referensi API Streamlit: https://docs.streamlit.io/library/api-reference
'''
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import streamlit as st
from PIL import Image

#Mengekstrak File json 
with open("kode_negara_lengkap.json") as f:
    dj = json.load(f)
#Mengekstrak File csv
df = pd.read_csv("produksi_minyak_mentah.csv")

############### TITLE #################
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Statistik Jumlah Produksi Minyak Mentah Dunia Tahun 1971-2015")
st.subheader("* Sumber data berasal dari  “produksi_minyak_mentah.csv” *")
st.caption("Dibuat oleh Dahlia Putri Permatasari (12220090)")
############### TITLE #################

############### SIDEBAR ###############
image = Image.open('pe_logo.png')
st.sidebar.image(image)
st.sidebar.title("Selamat Datang di Aplikasi Statistik Produksi Minyak Mentah Dunia")
st.sidebar.write('"Silakan Atur Data yang Ingin Ditampilkan"')
st.sidebar.caption("Pengaturan konfigurasi tampilan")
n_tampil = st.sidebar.slider("Jumlah Baris Tabel yang Ditampilkan", min_value=1, max_value=None, value=10)
jumlah_negara_pilihan = st.sidebar.slider("Jumlah Negara yang Ditampilkan", min_value=1, max_value=137, value=10)
tahun_pilihan = st.sidebar.slider("Tahun yang Ditampilkan", min_value=1971, max_value=2015)
############### SIDEBAR ###############

#Mengonversi Kode Negara pada File csv Menjadi Nama Negara dari File json
nama_negara={item['alpha-3']:item['name']for item in dj}
df.loc[:,'kode_negara']=df['kode_negara'].map(nama_negara)
df = df.rename(columns={'kode_negara':'nama_negara'})

#Menghapus Data Nama Negara yang Mengandung Nilai Missing Values (NaN)
df.dropna(subset=['nama_negara'], inplace=True)
#Membuat List Nama Negara Lengkap dan Menghapus Nama Negara Duplikat  
list_negara = df['nama_negara'].drop_duplicates().tolist()
#Membuat Select Box Pilihan Negara untuk Input User
negara = st.sidebar.selectbox("Pilih Negara", list_negara)

#Memfilter Data Frame File csv Sesuai Negara Pilihan User
filter_negara = df["nama_negara"]==negara
data_negara_pilihan = df[filter_negara]

c = st.container()
###FIRST COLUMNS###
#Membuat Tabel Representasi Data dari Negara Pilihan User
c.subheader(f"Representasi Data Jumlah Produksi Minyak Mentah di {negara}")
tabel = data_negara_pilihan.head(n_tampil)
c.write(tabel)
###FIRST COLUMNS###


###SECOND COLUMNS###
#Fitur 1 : Membuat Grafik Jumlah Produksi terhadap Tahun dari negara N; N pilihan user
c.subheader(f"Jumlah Produksi Minyak Mentah di {negara}")
cmap_name = 'tab20b'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(data_negara_pilihan)]
fig, ax = plt.subplots()
ax.bar(data_negara_pilihan["tahun"], data_negara_pilihan["produksi"], color=colors)
ax.set_title(f"Grafik Jumlah Produksi Minyak Mentah di {negara} Tahun 1971 - 2015")
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Jumlah Produksi", fontsize=12)
plt.tight_layout()

c.pyplot(fig)
###SECOND COLUMNS###


###THIRD COLUMNS###
left_col, right_col = st.columns(2)
############### THIRD LEFT COLUMN ###############
#Memfilter Data Frame File csv Sesuai Jumlah Negara dan Tahun Pilihan User
filter_tahun = df["tahun"]==tahun_pilihan
data_jumlah_pilihan = df[filter_tahun].sort_values(by=["produksi"], ascending=False).head(jumlah_negara_pilihan)
#Fitur 2 :Membuat Grafik B-besar Negara dengan Jumlah Produksi Terbesar pada Tahun T; B dan T pilihan User
left_col.subheader(f"{jumlah_negara_pilihan}-Besar Negara dengan Jumlah Produksi Terbesar pada Tahun {tahun_pilihan}")

cmap_name = 'tab20b'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(data_jumlah_pilihan)]
fig, ax = plt.subplots()
ax.barh(data_jumlah_pilihan["nama_negara"], data_jumlah_pilihan["produksi"], color=colors)
ax.set_title(f"Grafik {jumlah_negara_pilihan}-Besar Negara dengan Jumlah Produksi Terbesar pada Tahun {tahun_pilihan}")
ax.set_xlabel("Jumlah Produksi", fontsize=12)
plt.tight_layout()

left_col.pyplot(fig)
############### THIRD LEFT COLUMN ###############
############### THIRD RIGHT COLUMN ###############
#Memfilter Data Frame File csv Sesuai Jumlah Negara dan Tahun Pilihan User
df["produksi_kumulatif"] = df.groupby(["nama_negara"])["produksi"].transform("sum")
#Membuat Data Frame Baru dan Menghapus Nama Negara Duplikat  
df_negara = df.drop_duplicates(subset=["nama_negara"])
data_kumulatif_pilihan = df_negara.sort_values(by=["produksi_kumulatif"], ascending=False).head(jumlah_negara_pilihan)
#Fitur 3 : Grafik B-besar Negara dengan Jumlah Produksi Kumulatif Terbesar; B pilihan user
right_col.subheader(f"{jumlah_negara_pilihan}-Besar Negara dengan Jumlah Produksi Kumulatif Terbesar")

cmap_name = 'tab20b'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(data_kumulatif_pilihan)]
fig, ax = plt.subplots()
ax.barh(data_kumulatif_pilihan["nama_negara"], data_kumulatif_pilihan["produksi_kumulatif"], color=colors)
ax.set_title(f"Grafik {jumlah_negara_pilihan}-Besar Negara dengan Jumlah Produksi Kumulatif Terbesar")
ax.set_xlabel("Produksi Kumulatif (x10^7)", fontsize=12)
plt.tight_layout()

right_col.pyplot(fig)
############### THIRD RIGHT COLUMN ###############
###THIRD COLUMNS###


###FOURTH COLUMNS###
#Fitur 4 : SUMMARY Nama Lengkap Negara, Kode Negara, Region, dan Sub-Region
c = st.container()
c.subheader("SUMMARY")
#A1. Jumlah Produksi Terbesar pada Tahun T, T Pilihan User
#Memfilter Data Frame File csv Sesuai Tahun Pilihan User
filter_tahun = df["tahun"]==tahun_pilihan
max_tahun_pilihan = df[filter_tahun].sort_values(by=["produksi"], ascending=False).head(1)
produksi = np.asarray(max_tahun_pilihan["produksi"])
negara_max_tahun_pilihan = np.asarray(max_tahun_pilihan["nama_negara"])
for item in dj:
    if (item["name"]==negara_max_tahun_pilihan):
        kode = [item["alpha-3"]]
        region = [item["region"]]
        sub_region = [item ["sub-region"]]
kode = np.asarray(kode)
region = np.asarray(region)
sub_region = np.asarray(sub_region)
c.write (f"~ Negara dengan Jumlah Produksi Terbesar pada Tahun {tahun_pilihan} : {negara_max_tahun_pilihan} dengan Jumlah Produksi {produksi}, code country : {kode}, region: {region}, sub-region: {sub_region}")

#A2. Jumlah Produksi Terbesar pada Keseluruhan Tahun
max_total = df.sort_values(by=['produksi_kumulatif'], ascending=False).head(1)
produksi = np.asarray(max_total['produksi_kumulatif'])
negara_max_total = np.asarray(max_total['nama_negara'])
for item in dj:
    if (item['name'])==negara_max_total:
        kode = [item['alpha-3']]
        region = [item['region']]
        sub_region = [item['sub-region']]
kode = np.asarray(kode)
region = np.asarray(region)
sub_region = np.asarray(sub_region)
c.write(f"~ Negara dengan Jumlah Produksi Terbesar pada Keseluruhan Tahun : {negara_max_total} dengan Jumlah Produksi {produksi}, code country: {kode}, region: {region}, sub-region: {sub_region}")

#B1. Jumlah Produksi Terkecil (tidak sama dengan nol) pada Tahun T, T Pilihan User
filter1 = df['produksi']!=0
min_tahun_pilihan = df[filter1].sort_values(by=['produksi'], ascending=True)
filter2 = min_tahun_pilihan['tahun']==tahun_pilihan
min_pilihan = min_tahun_pilihan[filter2].sort_values(by=['produksi'], ascending=True).head(1)
produksi = np.asarray(min_pilihan['produksi'])
negara_min_tahun_pilihan = np.asarray(min_pilihan['nama_negara'])
for item in dj:
    if (item['name'])==negara_min_tahun_pilihan:
        kode = [item['alpha-3']]
        region = [item['region']]
        sub_region = [item['sub-region']]
kode = np.asarray(kode)
region = np.asarray(region)
sub_region = np.asarray(sub_region)
c.write(f"~ Negara dengan Jumlah Produksi Terkecil pada Tahun {tahun_pilihan} : {negara_min_tahun_pilihan} dengan Jumlah Produksi {produksi}, code country : {kode}, region: {region}, sub-region: {sub_region}")

#B2. Jumlah Produksi Terkecil (tidak sama dengan nol) pada Keseluruhan Tahun
filter3 = df["produksi_kumulatif"]!=0 
min_total = df[filter3].sort_values(by=['produksi_kumulatif'], ascending=True).head(1)
produksi = np.asarray(min_total["produksi_kumulatif"])
negara_min_total = np.asarray(min_total['nama_negara'])
for item in dj:
    if (item['name'])==negara_min_total:
        kode = [item['alpha-3']]
        region = [item['region']]
        sub_region = [item['sub-region']]
kode = np.asarray(kode)
region = np.asarray(region)
sub_region = np.asarray(sub_region)
c.write(f"~ Negara dengan Jumlah Produksi Terkecil pada Keseluruhan Tahun : {negara_min_total} dengan Jumlah Produksi {produksi}, code country: {kode}, region: {region}, sub-region: {sub_region}")

#C1. Jumlah Produksi = 0 pada Tahun T, T Pilihan User
c.write(f"~ Negara dengan Jumlah Produksi = 0 pada Tahun {tahun_pilihan}")
filter1 = df['produksi']==0
nol_data = df[filter1].sort_values(by=['produksi'])
filter2 = nol_data['tahun']==tahun_pilihan
nol_pil = nol_data[filter2].sort_values(by=['produksi']).drop(columns='produksi_kumulatif', axis=1).head(n_tampil)
negara_nol_pil = nol_pil['nama_negara'].values.tolist()
list_kode = []
list_region = []
list_subregion = []
for negara in negara_nol_pil:
    for item in dj:
        if (item['name'])==negara:
            kode = [(item['alpha-3'])]
            region = (item['region'])
            sub_region = (item['sub-region'])
            list_kode.append(kode)
            list_region.append(region)
            list_subregion.append(sub_region)
#Mengubah ke data frame agar mudah dibaca
nol_pil["kode_negara"] = list_kode
nol_pil["region"] = list_region
nol_pil["sub-region"] = list_subregion
c.write(nol_pil)

#C2. Jumlah Produksi = 0 pada Keseluruhan Tahun
c.write("~ Negara dengan Jumlah Produksi = 0 pada Keseluruhan Tahun")
filter3 = df['produksi_kumulatif']==0
nol_total = df[filter3].sort_values(by=['produksi_kumulatif']).drop(columns='produksi', axis=1).drop(columns='tahun',axis=1).drop_duplicates(subset=['nama_negara']).head(n_tampil)
negara_nol_total = nol_total['nama_negara'].values.tolist()
list_kode = []
list_region = []
list_subregion = []
for negara in negara_nol_total:
    for item in dj:
        if (item['name']) == negara:
            kode = [(item['alpha-3'])]
            region = (item['region'])
            sub_region = (item['sub-region'])
            list_kode.append(kode)
            list_region.append(region)
            list_subregion.append(sub_region)
#Mengubah ke data frame agar mudah dibaca
nol_total["kode_negara"] = list_kode
nol_total["region"] = list_region
nol_total["sub-region"] = list_subregion
st.write(nol_total)
###FOURTH COLUMNS###