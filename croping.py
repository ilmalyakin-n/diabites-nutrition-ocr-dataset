import cv2
import os

# Konfigurasi Path
base_dir = r'C:\Users\ilmal\OneDrive\Dokumen\KODING\kodebaru'
output_dir = os.path.join(base_dir, 'hasil_crop_ocr')
splits = ['train', 'valid']
classes = ['calories', 'carbs', 'fat', 'sodium', 'sugar']

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

counters = {cls: 1 for cls in classes}
total_berhasil = 0

print("=== MEMULAI AUTO-CROP (SUPPORT KOTAK & POLYGON) ===")

for split in splits:
    image_dir = os.path.join(base_dir, split, 'images')
    label_dir = os.path.join(base_dir, split, 'labels')

    if not os.path.exists(label_dir) or not os.path.exists(image_dir):
        continue

    print(f">>> Mengekstrak {split.upper()}...")

    for label_file in os.listdir(label_dir):
        if not label_file.endswith('.txt'): continue

        base_name = os.path.splitext(label_file)[0]
        img_path = None
        
        for ext in ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']:
            path_cek = os.path.join(image_dir, base_name + ext)
            if os.path.exists(path_cek):
                img_path = path_cek
                break

        if img_path is None: continue

        img = cv2.imread(img_path)
        if img is None: continue
        h, w, _ = img.shape

        with open(os.path.join(label_dir, label_file), 'r') as f:
            lines = f.readlines()

        for line in lines:
            data = line.strip().split()
            
            # Jika isinya kurang dari 5, berarti data rusak/tidak valid
            if len(data) < 5: continue

            class_id = int(data[0])
            if class_id >= len(classes): continue
            class_name = classes[class_id]
            
            # === LOGIKA BARU: DETEKSI JENIS KOTAK ===
            
            if len(data) == 5:
                # 1. Format Kotak Lurus Biasa (Bounding Box)
                x_center, y_center, width, height = map(float, data[1:])
                x1 = int((x_center - width / 2) * w)
                y1 = int((y_center - height / 2) * h)
                x2 = int((x_center + width / 2) * w)
                y2 = int((y_center + height / 2) * h)
                
            else:
                # 2. Format Polygon / Smart Polygon (> 5 nilai)
                # Mengubah titik-titik acak menjadi satu kotak utuh (Bounding Box terluar)
                coords = list(map(float, data[1:]))
                x_coords = coords[0::2] # Ambil semua titik X
                y_coords = coords[1::2] # Ambil semua titik Y
                
                # Cari nilai paling ujung untuk X dan Y
                x1 = int(min(x_coords) * w)
                x2 = int(max(x_coords) * w)
                y1 = int(min(y_coords) * h)
                y2 = int(max(y_coords) * h)

            # Pastikan koordinat tidak keluar dari batas gambar
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)

            crop_img = img[y1:y2, x1:x2]
            if crop_img.size == 0: continue

            # Simpan file
            file_name = f"{class_name}_{counters[class_name]:03d}.png"
            cv2.imwrite(os.path.join(output_dir, file_name), crop_img)
            
            counters[class_name] += 1
            total_berhasil += 1

print("\n=============================================")
print("             LAPORAN AKHIR                   ")
print("=============================================")
print(f"Total Kotak yang Ditemukan & Di-Crop: {total_berhasil} potongan")
print("=============================================\n")
if total_berhasil >= 400:
    print("[SUKSES] Semua data berhasil diekstrak dengan sempurna!")