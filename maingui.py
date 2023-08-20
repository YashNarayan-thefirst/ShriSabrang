from pathlib import Path
from g20query import search_database
from gui import classify_waste_image
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Scrollbar, Label
from tkinter import filedialog
from PIL import Image, ImageTk,ImagePath
import tensorflow as tf
import tensorflow_hub as hub
from g20query import search_database
import mysql.connector


Font_tuple = ("Inter", 15, "bold")
from os import getcwd 
path = getcwd()
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(rf"{path}\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path) 
searchquery=''

def submit():
    searchquery = entry_1.get()
    result = search_database(searchquery)  # Call the search_database function
    if result:
        entry_2.delete(1.0, "end")  # Clear existing text
        entry_2.insert("insert", result[1]) 
window = Tk()
window.geometry("1280x720")


def open_classification_window():
    def classify_and_display_image():
        image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if image_path:
            waste_category, recycling_instruction = classify_waste_image(image_path)
            classification_result.config(text=f"Detected waste category: {waste_category}\nRecycling instructions: {recycling_instruction}")

            image = Image.open(image_path)
            image.thumbnail((640, 360))
            img = ImageTk.PhotoImage(image)

            # Store the PhotoImage as an attribute of classified_image_label
            classified_image_label.img = img
            
            classified_image_label.config(image=img)


    classification_window = Tk()
    classification_window.title("Image Classification")

    classification_label = Label(classification_window, text="Image Classification", font=("Helvetica", 16, "bold"))
    classification_label.pack(pady=10)

    classify_button = Button(classification_window, text="Classify Image", command=classify_and_display_image, font=("Helvetica", 12))
    classify_button.pack(pady=5)

    classified_image_label = Label(classification_window)
    classified_image_label.pack(pady=10)

    classification_result = Label(classification_window, text="", font=("Helvetica", 12))
    classification_result.pack(pady=10)

    classification_window.mainloop()


image_list= []
canvas = Canvas(
    window,
    bg = "#1B8CC1",
    height = 607,
    width = 1080,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    777.0,
    136.49999999999997,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    font = Font_tuple
)
entry_1.place(
    x=572.0+30,
    y=97.99999999999997+6,
    width=400.0-50,
    height=75-10.0-6
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=submit,
    relief="flat"
)
button_1.place(
    x=984.0,
    y=102.99999999999997,
    width=93.0,
    height=63.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    270.0,
    375.0,
    image=image_image_1
)

canvas.create_text(
    26.0,
    51.99999999999997,
    anchor="nw",
    text="SHRI SABRANG PROJECT",
    fill="#FFFFFF",
    font=("Inter SemiBold", 41 * -1)
)

canvas.create_text(
    43.0,
    121.99999999999997,
    anchor="nw",
    text="BY YASH NARAYAN & PRANAV NARANG",
    fill="#FFFFFF",
    font=("Inter SemiBold", 22 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=open_classification_window,  
    relief="flat"
)
button_2.place(
    x=577.0,
    y=423.0,
    width=400.0,
    height=110.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    777.0,
    306.0,
    image=entry_image_2
)
entry_2 = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=572.0,
    y=193.99999999999997,
    width=410.0,
    height=222.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=window.destroy,
    relief="flat"
)
button_3.place(
    x=700.0,
    y=538.0,
    width=149.0,
    height=63.0
)

canvas.create_text(
    710.0,
    35.99999999999997,
    anchor="nw",
    text="Search",
    fill="#FFFFFF",
    font=("Inter Bold", 44 * -1)
)
window.resizable(False, False)
sb = Scrollbar(
    window, 
    orient= "vertical"
    )
sb.place(
    x=1000,
    y=193,
    height = 222
)
sb.config(command=entry_2.yview)
window.mainloop()
