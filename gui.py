

from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,Label


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\popil\OneDrive\Desktop\Python Programs\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

from tkinter import filedialog
from PIL import Image, ImageTk


def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((1280*0.7, 720)) 
        photo = ImageTk.PhotoImage(image)
        return photo
    return None

def get_photo():
    photo = open_image()
    if photo:
        image_label.config(image=photo)
        image_label.photo = photo  
    else:
        image_label.config(image=None)

window = Tk()

window.geometry("1280x720")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    384.0,
    720.0,
    fill="#36A692",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=get_photo,
    relief="flat"
)
button_1.place(
    x=33.0,
    y=136.0,
    width=316.0-4,
    height=124.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=window.destroy,
    relief="flat"
)
button_2.place(
    x=92.0,
    y=547.0,
    width=203.0,
    height=81.28125
)
image_label = Label(window)
image_label.place(x=1280*0.3,y=0)
window.mainloop()
