import os
from collections import Counter

# Sesuaikan dengan path folder label Anda
label_dir = r'C:\Users\ilmal\OneDrive\Dokumen\KODING\kodebaru\train\labels'

print("=== MENCARI FILE DENGAN LABEL GANDA ===")

for label_file in os.listdir(label_dir):
    if not label_file.endswith('.txt'): continue
    
    with open(os.path.join(label_dir, label_file), 'r') as f:
        lines = f.readlines()
        
    # Ambil ID kelas (angka pertama di setiap baris)
    class_ids = [line.split()[0] for line in lines]
    counts = Counter(class_ids)
    
    # Cek apakah ada ID kelas yang muncul lebih dari 1 kali
    for cls_id, count in counts.items():
        if count > 1:
            # Ganti angka ID dengan nama kelas agar mudah dibaca
            class_names = ['calories', 'carbs', 'fat', 'sodium', 'sugar']
            if int(cls_id) < len(class_names):
                cls_name = class_names[int(cls_id)]
                print(f"[DOUBLE] File '{label_file}' memiliki label '{cls_name}' sebanyak {count} kotak.")

print("\nPencarian Selesai.")