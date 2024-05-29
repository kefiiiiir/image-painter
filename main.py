import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import cv2
import numpy as np


def paint_effect(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


    gray_image = cv2.medianBlur(gray_image, 7)


    edges = cv2.adaptiveThreshold(gray_image, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 2)


    color = cv2.bilateralFilter(image, 9, 300, 300)


    stylized_image = cv2.stylization(color, sigma_s=60, sigma_r=0.6)


    painted_image = cv2.bitwise_and(stylized_image, stylized_image, mask=edges)

    return Image.fromarray(painted_image)



def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")])
    if file_path:
        display_image(file_path)
    print('Processing')



def display_image(image_path):
    original_image = Image.open(image_path)
    painted_image = paint_effect(image_path)


    original_image_resized = original_image.resize((400, 400))
    painted_image_resized = painted_image.resize((400, 400))


    original_image_ctk = ctk.CTkImage(light_image=original_image_resized, size=(400, 400))
    painted_image_ctk = ctk.CTkImage(light_image=painted_image_resized, size=(400, 400))


    original_label.configure(image=original_image_ctk)
    original_label.image = original_image_ctk
    painted_label.configure(image=painted_image_ctk)
    painted_label.image = painted_image_ctk



app = ctk.CTk()

app.title("Image Painter")
app.geometry("850x500")


open_button = ctk.CTkButton(app, text="Open Image", command=open_file)
open_button.pack(pady=20)


original_label = ctk.CTkLabel(app, text='Original Image')
original_label.pack(side=ctk.LEFT, padx=20)

painted_label = ctk.CTkLabel(app, text='Painted Image')
painted_label.pack(side=ctk.RIGHT, padx=20)

app.iconbitmap('icons/app.ico')


app.mainloop()
