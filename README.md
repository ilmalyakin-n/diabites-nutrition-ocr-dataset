# 📊 DiaBites - Nutrition Label OCR Dataset

Dataset ini berisi potongan gambar (*cropped images*) dari "Informasi Nilai Gizi" pada kemasan makanan dan minuman di Indonesia. Dataset ini difokuskan untuk melatih model **Optical Character Recognition (OCR)** guna mengekstraksi 5 komponen gizi utama secara otomatis.

Dokumentasi ini ditujukan bagi tim **Data Science** (pembuatan *Ground Truth* CSV) dan **AI Engineering** (pengembangan model). 

*(Update: Proses pelabelan manual telah selesai. File CSV final tersedia di root folder dan lampiran Releases).*

## 📁 Struktur Direktori Repositori
```text
DiaBites_Dataset/
├── images/                         # [Hanya di ZIP/Release] 420 gambar hasil crop
├── EDA_CSV.ipynb                   # Skrip Google Colab untuk analisis teks & kualitas dari file label csv
├── EDA_croping_images.py           # Skrip untuk analisis gambar hasil croping
├── check.py                        # Skrip audit duplikasi bounding box
├── create_csv.py                   # Skrip pembuat template CSV 
├── croping.py                      # Skrip auto-crop (support polygon & lurus)
├── dataset_insight_dashboard.png   # Visualisasi resolusi gambar hasil croping
├── dataset_label.csv               # [DATA FINAL] Ground Truth teks gizi & kualitas
└── README.md                       # Dokumentasi ini\
```
-----
## 📈 Dataset Insights (Exploratory Data Analysis)

### 1\. Insight Visual (Dimensi Gambar/Dari file EDA_croping_images.py)
![images alt](https://github.com/ilmalyakinn/assets/blob/53b4a390e3d55519f4e4c39d6ce379aa2f1972d0/dataset_insight_dashboard.png)
Visualisasi di atas ini menunjukkan sebaran resolusi asli gambar dan distribusi rasio aspek (lebar/tinggi) untuk acuan pra-pemrosesan model.

```text
=== RINGKASAN STATISTIK VISUAL ===
Total Gambar     : 420
Rata-rata Tinggi : 87 px
Rata-rata Lebar  : 784 px
Dimensi Terkecil : 173x18 px
Dimensi Terbesar : 2515x242 px
```

### 2\. Insight Teks & Label (Dari `EDA_CSV.ipynb`)
Hasil analisis file CSV menunjukkan bahwa dataset memiliki tingkat kompleksitas dunia nyata.

```text
=== RINGKASAN TEKNIS UNTUK AI ENGINEER ===
Total Vocabulary Size : 60 karakter
Daftar Karakter (Map) : %(),./0123456789:CEFGKLNSTabcdefghiklmnorstuy... [Termasuk bbrp karakter Mandarin/Jepang]
Panjang Teks Rata-rata: 24.0 karakter
Panjang Teks Maksimal : 58 karakter
Distribusi Kualitas   : Didominasi oleh 'clear' dan 'overlap'.
```
-----

## ⚠️ Karakteristik & Kondisi Data (PENTING)

Dataset ini diambil dari kondisi dunia nyata (*real-world scenarios*) tanpa manipulasi kompresi atau *upscaling* buatan. Harap perhatikan 4 kondisi berikut sebelum memproses data:

### 1\. Variasi Visual Alami (Blur & Glare)

Foto diambil dari kemasan asli (plastik, kaleng, dll). Terdapat variasi pencahayaan, pantulan cahaya (*glare*), dan beberapa gambar tampak sedikit *blur*. **Tujuan:** Melatih ketahanan (*robustness*) model agar tidak *overfitting* pada gambar bersolusi sempurna.

### 2\. Teks Berdekatan (Overlap / Noise)

Karena jarak antar baris pada label gizi sangat rapat, beberapa hasil *crop* mungkin menyertakan potongan teks dari baris atas atau bawahnya. Ini sengaja **tidak dibuang** agar model belajar mengenali fitur utama dan mengabaikan *noise* (contoh: model harus fokus pada "Karbohidrat" meski ada potongan kata "Protein" di atasnya).

### 3\. Teks Multi-baris (Multiline)

Mayoritas komponen gizi terdiri dari 1 baris teks. Namun, khusus untuk kelas **Carbs (Karbohidrat)** dan **Sodium (Natrium)**, terdapat beberapa gambar yang teksnya terbagi menjadi **2 baris** karena panjang dan di campur dengann bahasa inggris.

### 4\. Distribusi Kelas

  * `calories`: 84 gambar
  * `fat`: 84 gambar
  * `carbs`: 84 gambar
  * `sodium`: 84 gambar
  * `sugar`: 84 gambar

**Unduh Dataset (ZIP V1 tanpa file label csv) di sini:** [Klik di Sini untuk Mengunduh](https://github.com/ilmalyakin-n/diabites-nutrition-ocr-dataset/releases/tag/v1.0.0)

**Unduh Dataset (ZIP V2 lengkap dengan file label csv ) di sini:** [Klik di Sini untuk Mengunduh](https://github.com/ilmalyakin-n/diabites-nutrition-ocr-dataset/releases/tag/v2.0.0)

-----
## 🤖 Rekomendasi untuk Tim AI Engineering

Berdasarkan hasil Exploratory Data Analysis (EDA), berikut adalah rekomendasi rancangan arsitektur model OCR:

1.  **Model Architecture:** Sangat disarankan menggunakan **CRNN (CNN + Bi-LSTM)** dipadukan dengan **Attention Mechanism**. Fitur Attention wajib ada untuk menangani 43% data bertipe `overlap` agar model fokus pada teks target di tengah.
2.  **Sequence Length:** Karena panjang teks maksimal mencapai 58 karakter, atur parameter *Sequence Length* minimum pada angka **64 atau 128**.
3.  **Data Augmentation:** Terdapat sejumlah data `blur` dan `glare`. Tambahkan augmentasi seperti *Gaussian Blur*, *Brightness/Contrast adjustment*, dan *Motion Blur* pada data yang `clear` untuk menyeimbangkan ketahanan model.
4.  **Vocabulary Mapping:** Pertimbangkan untuk melakukan *filtering* karakter non-latin (Mandarin/Jepang) pada CSV jika aplikasi DiaBites difokuskan murni untuk produk lokal, agar *output layer* (Softmax) model tidak terlalu besar.

Gambar dikelompokkan berdasarkan kategori kandungan gizi. Berikut adalah deskripsi setiap kategori (*field name*) beserta kemungkinan kata kunci (*keywords*) teks asli yang akan ditemukan oleh OCR di dalam gambar tersebut:
| Field Name | Possible Keywords | Deskripsi Gambar |
| :--- | :--- | :--- |
| `calories` | energi total, kalori, kkal, energy | Baris Energi Total / Kalori. |
| `fat_` | lemak, lemak total, total fat | Baris Lemak Total beserta satuannya (g). |
| `carbs_` | karbohidrat, karbohidrat total, total carbohydrate | Baris Karbohidrat Total beserta satuannya (g). |
| `sugar_` | gula, gula total, total sugar, sugars | Baris Gula / Sukrosa beserta satuannya (g). |
| `sodium_`| natrium, sodium | Baris Natrium / Garam beserta satuannya (mg). |

**Catatan: Penamaan file aktual di dalam folder mengikuti format 3 digit angka, contohnya `fat_001.png`, `sodium_001.png`, dst.**

-----
## 📝 Panduan untuk Data Scientist (Labeling CSV)
Dalam mengisi file `dataset_label_template.csv` yang telah disediakan. File ini sudah berisi daftar 420 nama file gambar (`file_name`). Anda hanya perlu mengisi kolom `text` dan `quality`.

### A. Aturan Pengisian Kolom `text` (Ground Truth)
* **Fokus pada Teks Utama:** Jika ada teks dari baris lain yang ikut terpotong masuk ke dalam gambar (*noise*), **abaikan teks tersebut**. Hanya tuliskan nilai gizi yang menjadi fokus utama kelas file tersebut.
* **Format Multi-baris:** Untuk kelas `carbs` dan `sodium` yang memiliki 2 baris teks dalam 1 gambar, gunakan spasi tunggal untuk menyambungnya (jangan gunakan *Enter* atau `\n`). 
    * *Contoh di gambar:* Baris 1 "Garam", Baris 2 "(Natrium) 20mg".
    * *Tulis di CSV:* `Garam (Natrium) 20mg`
* **Case & Symbol Sensitive:** Tulis sama persis seperti di gambar, termasuk huruf kapital dan satuannya (misal: `g`, `mg`, `kkal`).

### B. Aturan Pengisian Kolom `quality`
Untuk membantu tim AI Engineer melakukan *Error Analysis* nanti, mohon isi kolom `quality` dengan salah satu dari 4 label berikut berdasarkan kondisi visual gambar:
1. `clear` : Gambar sangat jelas, tajam, dan mudah dibaca.
2. `blur` : Gambar agak buram, resolusi pecah, namun masih bisa dibaca/ditebak oleh manusia.
3. `glare` : Terdapat pantulan cahaya (silau) yang menutupi sebagian teks.
4. `overlap` : Gambar cukup jelas, tetapi sangat berdempetan dengan teks dari baris lain.
