import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk

def add_watermark():
    global img, tk_image, final_image  # Keep references to avoid garbage collection

    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if not file_path:
        return

    img = Image.open(file_path).convert("RGBA")

    watermark = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(watermark)

    try:
        font = ImageFont.truetype("arial.ttf", 50)  # Adjust font size for visibility
    except IOError:
        font = ImageFont.truetype("DejaVuSans.ttf", 50)  # Alternative font if Arial is not available

    text = "Created by Aziz Hazim"

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (img.width - text_width) // 2
    y = (img.height - text_height) // 2

    draw.text((x, y), text, font=font, fill=(250, 250, 250, 200))
    watermarked_img = Image.alpha_composite(img, watermark)

    tk_image = ImageTk.PhotoImage(watermarked_img)
    img_label.config(image=tk_image)
    img_label.image = tk_image  # Keep reference to avoid garbage collection

    save_button.config(state=tk.NORMAL)

    final_image = watermarked_img.convert("RGB")

def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"),
                                                        ("JPEG files", "*.jpg"),
                                                        ("All Files", "*.*")])
    if file_path:
        final_image.save(file_path)

root = tk.Tk()
root.title("Created by Aziz Hazim")

frame = tk.Frame(root)
frame.pack(pady=10)

btn = tk.Button(frame, text="Open Image", command=add_watermark)
btn.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(frame, text="Save Image", command=save_image, state=tk.DISABLED)
save_button.pack(side=tk.LEFT, padx=5)

img_label = tk.Label(root)
img_label.pack()

root.mainloop()
