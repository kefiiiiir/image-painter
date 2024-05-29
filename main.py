import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import cv2
import numpy as np


# Function to give the image a more realistic painted effect
def paint_effect(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Apply bilateral filter to reduce noise while keeping edges sharp
    color = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)

    # Convert to grayscale and apply median blur
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray = cv2.medianBlur(gray, 7)

    # Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(gray, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 2)

    # Apply an edge-preserving filter
    filtered = cv2.edgePreservingFilter(image, flags=1, sigma_s=60, sigma_r=0.4)

    # Combine the edges with the smoothed image
    cartoon = cv2.bitwise_and(filtered, filtered, mask=edges)

    # Use a custom kernel to create a more painterly effect
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    painterly_image = cv2.filter2D(cartoon, -1, kernel)

    return Image.fromarray(painterly_image)


# Function to open a file dialog and get the image path
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")])
    if file_path:
        display_image(file_path)


# Function to display the original and processed images
def display_image(image_path):
    original_image = Image.open(image_path)
    painted_image = paint_effect(image_path)

    # Resize images for display
    original_image_resized = original_image.resize((400, 400))
    painted_image_resized = painted_image.resize((400, 400))

    # Convert images to CTkImage with specified size
    original_image_ctk = ctk.CTkImage(light_image=original_image_resized, size=(400, 400))
    painted_image_ctk = ctk.CTkImage(light_image=painted_image_resized, size=(400, 400))

    # Display the images in the GUI
    original_label.configure(image=original_image_ctk)
    original_label.image = original_image_ctk
    painted_label.configure(image=painted_image_ctk)
    painted_label.image = painted_image_ctk

    # Create and place the Save button
    save_button = ctk.CTkButton(app, text="Save Image", command=lambda: save_image(painted_image, image_path))
    save_button.pack(pady=10)


# Function to save the processed image
def save_image(image, original_path):
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        image.save(save_path)


# Create the main window
app = ctk.CTk()
app.title("Image Painter")
app.geometry("1050x500")
app.iconbitmap('icons/app.ico')

# Create and place the Open File button
open_button = ctk.CTkButton(app, text="Open Image", command=open_file)
open_button.pack(pady=20)

# Create labels to display images
original_label = ctk.CTkLabel(app, text='Original image')
original_label.pack(side=ctk.LEFT, padx=20)

painted_label = ctk.CTkLabel(app, text='Painted Image')
painted_label.pack(side=ctk.RIGHT, padx=20)

# Run the application
app.mainloop()
