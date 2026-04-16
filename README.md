# 📊 DiaBites - Nutrition Label OCR Dataset

Dataset ini berisi potongan gambar (*cropped images*) dari "Informasi Nilai Gizi" pada kemasan makanan dan minuman di Indonesia. Dataset ini difokuskan untuk melatih model **Optical Character Recognition (OCR)** guna mengekstraksi 5 komponen gizi utama secara otomatis.

Dokumentasi ini ditujukan bagi tim **Data Science** (untuk pembuatan *Ground Truth* CSV) dan **AI Engineering** (untuk pengembangan model).

## 📈 Dataset Insights (Exploratory Data Analysis)

Visualisasi di bawah ini menunjukkan distribusi kelas, sebaran resolusi asli gambar, dan distribusi rasio aspek (lebar/tinggi) untuk acuan arsitektur model.

![images alt](https://github.com/ilmalyakinn/assets/blob/53b4a390e3d55519f4e4c39d6ce379aa2f1972d0/dataset_insight_dashboard.png)
```text
=== RINGKASAN STATISTIK ===
Total Gambar : 420
Rata-rata Tinggi : 87 px
Rata-rata Lebar  : 784 px
Dimensi Terkecil : 173x18 px
Dimensi Terbesar : 2515x242 px
```
-----

## ⚠️ Karakteristik & Kondisi Data (PENTING)

Dataset ini diambil dari kondisi dunia nyata (*real-world scenarios*) tanpa manipulasi kompresi atau *upscaling* buatan. Harap perhatikan 4 kondisi berikut sebelum memproses data:

### 1\. Variasi Visual Alami (Blur & Glare)

Foto diambil dari kemasan asli (plastik, kaleng, dll). Terdapat variasi pencahayaan, pantulan cahaya (*glare*), dan beberapa gambar tampak sedikit *blur*. **Tujuan:** Melatih ketahanan (*robustness*) model agar tidak *overfitting* pada gambar bersolusi sempurna.

### 2\. Teks Berdekatan (Overlap / Noise)

Karena jarak antar baris pada label gizi sangat rapat, beberapa hasil *crop* mungkin menyertakan potongan teks dari baris atas atau bawahnya. Ini sengaja **tidak dibuang** agar model belajar mengenali fitur utama dan mengabaikan *noise* (contoh: model harus fokus pada "Karbohidrat" meski ada potongan kata "Protein" di atasnya).

### 3\. Teks Multi-baris (Multiline)

Mayoritas komponen gizi terdiri dari 1 baris teks. Namun, khusus untuk kelas **Carbs (Karbohidrat)** dan **Sodium (Natrium)**, terdapat beberapa gambar yang teksnya terbagi menjadi **2 baris** karena ruang kemasan yang sempit.

### 4\. Distribusi Kelas (Slight Imbalance)

Terdapat sedikit ketidakseimbangan kelas akibat *human error* pada saat anotasi *bounding box* manual, dengan rincian total **420 gambar**:

  * `calories`: 84 gambar
  * `fat`: 84 gambar
  * `carbs`: 84 gambar
  * `sodium`: 84 gambar
  * `sugar`: 84 gambar

**Unduh Dataset (ZIP) di sini:** [Klik di Sini untuk Mengunduh](https://drive.google.com/file/d/1eXrfs0gX1kZnFk3LEZW41wfDIlgozdUI/view?usp=sharing)

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

---

### 💡 PRO TIP:
Untuk mempercepat proses pelabelan 400+ data, Gunakan bantuan *tools* ekstraksi teks (OCR) ringan agar Anda hanya perlu melakukan *copy-paste* dan mengoreksi kesalahan kecil (Proofreading).

**Rekomendasi Tools yang Bisa Digunakan:**
* **PowerToys Text Extractor (Windows):** Jika Anda pengguna Windows, instal Microsoft PowerToys. Tekan `Win + Shift + T`, blok gambar crop-nya, dan teks akan otomatis tercopy ke *clipboard*.
* **Browser Extensions:** Gunakan ekstensi Chrome seperti **Copyfish** atau **Project Naptha**. Buka gambar di *browser*, blok area teks, dan langsung *copy*.
* **Mac Live Text:** Jika menggunakan macOS, Anda bisa langsung menyeleksi dan menyalin teks dari dalam *preview* gambar.

Strategi terbaik: Ekstrak teks menggunakan *tools* tersebut -> *Paste* ke dalam kolom CSV -> Koreksi jika ada huruf/angka yang salah tebak -> Beri label `quality`.
