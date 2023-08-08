from tkinter import Tk, Canvas, Button, Label, PhotoImage
from tkinter import filedialog
from PIL import Image, ImageTk
import tensorflow as tf
import tensorflow_hub as hub
global result_text
model = tf.keras.models.load_model('garbage_classification_model.h5', custom_objects={'KerasLayer': hub.KerasLayer})

def classify_waste_image(image_path):
    image_size = (224, 224)

    # Load the image using PIL
    image = Image.open(image_path)
    image = image.resize(image_size)
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array = image_array / 255.0
    image_array = tf.expand_dims(image_array, axis=0)

    # Make the prediction
    predictions = model.predict(image_array)
    predicted_class_idx = tf.argmax(predictions, axis=1)[0]

    waste_categories = {
        0: "Cardboard",
        1: "Glass",
        2: "Metal",
        3: "Paper",
        4: "Plastic",
        5: "Trash",
        6: "Misc"
    }

    waste_category = waste_categories.get(int(predicted_class_idx), "Unknown")

    recycling_instructions = {
        "Cardboard": "Cardboard can be recycled by flattening and placing it in recycling bins.",
        "Glass": "Glass can be recycled by placing it in recycling bins. Make sure it's clean and dry.",
        "Metal": "Metal can be recycled by placing it in recycling bins. Remove any non-recyclable parts.",
        "Paper": "Paper can be recycled by placing it in recycling bins. Avoid soiled or wet paper.",
        "Plastic": "Plastic can be recycled by placing it in recycling bins. Check the recycling number for specific instructions.",
        "Trash": "This item is not recyclable. Please dispose of it properly.",
        "Misc": "This only appears when an error occurs. Please try again"
    }

    recycling_instruction = recycling_instructions.get(waste_category, "Recycling information not available.")

    return waste_category, recycling_instruction

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((1280 * 0.7, 720))
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.photo = photo
        waste_category, recycling_instruction = classify_waste_image(file_path)
        result_text = Label(window, text="", font=("Helvetica", 14), bg="#FFFFFF")
        result_text.place(x=1280 * 0.3, y=300)
        result_text.config(text=f"Detected waste category: {waste_category}\nRecycling instructions: {recycling_instruction}")

    return None

def display_image():
    photo = open_image()
    if photo:
        image_label.config(image=photo)
        image_label.photo = photo
    else:
        image_label.config(image=None)
        result_text.config(text="")

def close_window():
    window.destroy()

window = Tk()
window.geometry("1280x720")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=720,
    width=1280,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)
canvas.create_rectangle(
    0.0,
    0.0,
    384.0,
    720.0,
    fill="#36A692",
    outline="")

button_1 = Button(
    text="Open Image",
    bg="#FF7F50",  # Button background color
    activebackground="#FF6347",  # Background color when clicked
    borderwidth=0,
    highlightthickness=0,
    command=display_image,
    relief="flat"
)
button_1.place(
    x=33.0,
    y=136.0,
    width=316.0 - 4,
    height=124.0
)

button_2 = Button(
    text="Close",
    bg="#FF7F50",  # Button background color
    activebackground="#FF6347",  # Background color when clicked
    borderwidth=0,
    highlightthickness=0,
    command=close_window,
    relief="flat"
)
button_2.place(
    x=92.0,
    y=547.0,
    width=203.0,
    height=81.28125
)

image_label = Label(window)
image_label.place(x=1280 * 0.3, y=0)
window.mainloop()
