from tkinter import *
from tkinter import filedialog
import tkinter as tk
import os
from stegano import lsb

# Simple encryption/decryption functions
def encrypt(text, key):
    encrypted = ""
    for char in text:
        encrypted += chr(ord(char) + key)
    return encrypted

def decrypt(text, key):
    decrypted = ""
    for char in text:
        decrypted += chr(ord(char) - key)
    return decrypted

def select_image():
    global image_path
    image_path = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title='Select Image File',
        filetypes=(("Image files", ".png;.jpg;.jpeg"), ("All files", ".*"))
    )
    if image_path:
        print("Selected Image:", image_path)
        image_label.config(text="Image Selected")

def hide_message():
    global image_path
    text_to_hide = text_input.get("1.0", "end-1c")
    password = password_input.get()
    key = len(password)  # Determine the key based on password length
    encrypted_message = encrypt(text_to_hide, key)
    try:
        secret = lsb.hide(image_path, encrypted_message)
        output_path = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            title='Save Output File',
            filetypes=(("PNG files", ".png"), ("JPEG files", ".jpg"), ("All files", "."))
        )
        if output_path:
            # Ensure a default extension is added
            if not output_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                output_path += '.png'
            try:
                secret.save(output_path)
                print("Output Path:", output_path)
                hide_label.config(text="Message Hidden in Image")
                clear_inputs()
            except Exception as e:
                print("Error saving the image:", e)
    except Exception as e:
        print("Error hiding message:", e)

def reveal_message():
    global image_path
    password = password_reveal_input.get()
    key = len(password)
    try:
        encrypted_message = lsb.reveal(image_path)
        decrypted_message = decrypt(encrypted_message, key)
        revealed_output.config(state=NORMAL)
        revealed_output.delete("1.0", END)
        revealed_output.insert(END, decrypted_message)
        revealed_output.config(state=DISABLED)
        clear_inputs()
    except Exception as e:
        print("Error revealing message:", e)

def clear_inputs():
    text_input.delete("1.0", END)
    password_input.delete(0, END)
    password_reveal_input.delete(0, END)

root = Tk()
root.title("Steganography - Hide a Secret Text Message in an Image")
root.geometry("600x500+200+100")
root.resizable(False, False)
root.configure(bg="#37474f")

Label(root, text="Steganography Tool", bg="#37474f", fg="white", font=("Arial", 20)).pack(pady=10)

# Select Image Section
Button(root, text="Select Image", command=select_image, bg="#455a64", fg="white").pack(pady=10)
image_label = Label(root, text="", bg="#37474f", fg="white")
image_label.pack()

# Hide Message Section
Label(root, text="Enter Text to Hide:", bg="#37474f", fg="white").pack()
text_input = Text(root, height=4, width=50)
text_input.pack()

Label(root, text="Set Password:", bg="#37474f", fg="white").pack()
password_input = Entry(root, show="*")
password_input.pack()

Button(root, text="Hide Message", command=hide_message, bg="#455a64", fg="white").pack(pady=10)
hide_label = Label(root, text="", bg="#37474f", fg="white")
hide_label.pack()

# Reveal Message Section
Label(root, text="Reveal Hidden Message:", bg="#37474f", fg="white").pack()

revealed_output = Text(root, height=4, width=50, state=DISABLED)
revealed_output.pack()

Label(root, text="Enter Password:", bg="#37474f", fg="white").pack()
password_reveal_input = Entry(root, show="*")
password_reveal_input.pack()

Button(root, text="Reveal Message", command=reveal_message, bg="#455a64", fg="white").pack(pady=10)

root.mainloop()
