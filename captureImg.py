import cv2
import os
from tkinter import *
from PIL import Image, ImageTk

class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window_title = window_title
        self.cap = cv2.VideoCapture(0)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.image_count = self.get_latest_image_count()
        self.capture_button = None

        if self.window is not None:
            self.window.title(self.window_title)
            self.canvas = Canvas(window, width=self.width, height=self.height)
            self.canvas.pack()
            self.capture_button = Button(window, text="Capture Image", command=self.capture_image)
            self.capture_button.pack(fill=BOTH, expand=True)
            self.update()

    def update(self):
        ret, frame = self.cap.read()

        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(rgb_frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)

        if self.window is not None and self.capture_button is not None:
            if self.capture_button["state"] == "disabled":
                return  # Jika tombol capture sudah dinonaktifkan, berhenti perbarui tampilan
            self.window.after(20, self.update)

    def capture_image(self):
        folder_path = "RawImages"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        filename = os.path.join(folder_path, "FEA{:04d}.jpg".format(self.image_count))
        if not os.path.isfile(filename):  # Periksa apakah file sudah ada sebelum menyimpan gambar baru
            ret, frame = self.cap.read()

            if ret:
                cv2.imwrite(filename, frame)
                print("Gambar berhasil ditangkap dan disimpan sebagai", filename)
                self.image_count += 1
                # Nonaktifkan tombol capture setelah mengambil gambar
                if self.capture_button is not None:
                    self.capture_button.config(state="disabled")
            else:
                print("Tidak dapat membaca frame dari kamera")
        else:
            print("File sudah ada:", filename)

    def get_latest_image_count(self):
        folder_path = "RawImages"
        if not os.path.exists(folder_path):
            return 1
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            return 1
        return max(int(f[3:-4]) for f in files) + 1

if __name__ == '__main__':
    root = Tk()
    app = WebcamApp(root, "Webcam App")
    root.mainloop()
