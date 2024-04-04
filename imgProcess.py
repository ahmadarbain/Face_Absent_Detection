import cv2 as cv
import os

# Fungsi untuk mengubah ukuran semua gambar dalam folder
def resize_images(folder_path, target_size):
    # Membuat direktori untuk menyimpan gambar yang sudah diubah ukurannya
    output_folder = "Images"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Mendapatkan daftar file dalam folder
    file_list = os.listdir(folder_path)
    
    # Iterasi melalui setiap file dalam folder
    for file_name in file_list:
        # Membaca gambar
        img_path = os.path.join(folder_path, file_name)
        img = cv.imread(img_path)
        
        # Mengubah ukuran gambar
        resized_img = cv.resize(img, target_size)
        
        # Menyimpan gambar yang sudah diubah ukurannya
        output_path = os.path.join(output_folder, file_name)
        cv.imwrite(output_path, resized_img)
        print(f"Image {file_name} resized and saved to {output_path}")

# Path folder yang berisi gambar-gambar yang ingin diubah ukurannya
folder_path = "RawImages"

# Ukuran target yang diinginkan (misalnya: 200x200 piksel)
target_size = (400, 400)

# Panggil fungsi untuk mengubah ukuran gambar dalam folder
resize_images(folder_path, target_size)
