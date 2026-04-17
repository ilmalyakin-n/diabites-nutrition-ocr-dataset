import os
import pandas as pd

# Konfigurasi Direktori (Sesuaikan dengan folder Anda)
input_dir = r'C:\Users\ilmal\OneDrive\Dokumen\KODING\kodebaru\hasil_crop_ocr'
output_csv = r'C:\Users\ilmal\OneDrive\Dokumen\KODING\kodebaru\dataset_label_template.csv'

print("=== MEMBUAT TEMPLATE DATASET CSV ===")

# Mengambil semua nama file gambar
files = [f for f in os.listdir(input_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Membuat struktur data (DataFrame) dengan 3 kolom
df = pd.DataFrame({
    'file_name': files,
    'text': '',       # Dikosongkan untuk diisi teks gizi
    'quality': ''     # Dikosongkan untuk diisi status kualitas gambar
})

# Menyimpan ke format CSV
df.to_csv(output_csv, index=False)

print(f"✅ Sukses! File template CSV berhasil dibuat dengan {len(files)} baris data.")
print(f"📂 Lokasi file: {output_csv}")
print("Silakan bagikan file ini beserta gambarnya ke tim Data Scientist.")