from tkinter import Tk, Canvas, Button, Label, PhotoImage
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw,ImageFont
import tensorflow as tf
import tensorflow_hub as hub

# Function to classify waste image
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

def open_classification_window():
    window.withdraw()  # Hide the main menu window
    classification_window = Tk()
    classification_window.geometry("1280x720")
    classification_window.title("Image Classification")

    # Create canvas and rectangle
    classification_canvas = Canvas(
        classification_window,
        bg="white",
        height=720,
        width=1280,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    classification_canvas.place(x=0, y=0)
    classification_canvas.create_rectangle(
        0.0,
        0.0,
        384.0,
        720.0,
        fill="#36A692",
        outline="")

    # Create image label and result text
    classification_image_label = Label(classification_window)
    classification_result_text = Label(
        classification_window,
        text="",
        font=("Helvetica", 12),
        bg="#FFFFFF"
    )
    classification_result_text.place(x=1280 * 0.3, y=450)

    open_image_button = Button(
        classification_window,
        text="Open Image",
        bg="#FF7F50",
        activebackground="#FF6347",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: display_image(classification_image_label, classification_result_text),
        relief="flat"
    )
    open_image_button.place(
        x=33.0,
        y=136.0,
        width=316.0 - 4,
        height=124.0
    )

    close_button = Button(
        classification_window,
        text="Close",
        bg="#FF7F50",
        activebackground="#FF6347",
        borderwidth=0,
        highlightthickness=0,
        command=classification_window.destroy,  # Close the classification window
        relief="flat"
    )
    close_button.place(
        x=92.0,
        y=547.0,
        width=203.0,
        height=81.28125
    )

    classification_window.mainloop()

# Function to open the image and display it in the classification window
def display_image(classification_image_label, classification_result_text):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((1280 * 0.7, 720))

        image = image.resize((640, 360))  # Change the dimensions as needed
        # Add text to the image
        draw = ImageDraw.Draw(image)
        text = "Shri Sabrang Project By Yash Narayan and Pranay Narang"
        font = ImageFont.truetype("arial.ttf", 20)  # Specify the font and size
        
        # Calculate the text width and position it at the bottom center
        text_width, text_height = draw.textsize(text, font)
        x = (image.width - text_width) // 2
        y = image.height - text_height - 10  # Leave some space from the bottom
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)  # Fill color is white
        

        photo = ImageTk.PhotoImage(image)
        classification_image_label.config(image=photo)
        classification_image_label.photo = photo
        waste_category, recycling_instruction = classify_waste_image(file_path)
        classification_result_text.config(
            text=f"Detected waste category: {waste_category}\nRecycling instructions: {recycling_instruction}"
        )
# Function to close the application
def close_window():
    window.destroy()
try: 
    window = Tk()
    window.geometry("1280x720")
    window.title("Main Menu")

    # Create canvas and rectangle
    canvas = Canvas(
        window,
        bg="white",
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

    # Create buttons for main menu
    classification_button = Button(
        text="Open Image Classification",
        bg="#FF7F50",
        activebackground="#FF6347",
        borderwidth=0,
        highlightthickness=0,
        command=open_classification_window,
        relief="flat"
    )
    classification_button.place(
        x=33.0,
        y=136.0,
        width=316.0 - 4,
        height=124.0
    )

    exit_button = Button(
        text="Exit",
        bg="#FF7F50",
        activebackground="#FF6347",
        borderwidth=0,
        highlightthickness=0,
        command=close_window,
        relief="flat"
    )
    exit_button.place(
        x=92.0,
        y=547.0,
        width=203.0,
        height=81.28125
    )
    main_menu_image = PhotoImage(file="G20.png")  # Replace with file path
    main_menu_image_label = Label(canvas, image=main_menu_image)
    main_menu_image_label.place(x=600, y=50) 

    window.mainloop()
except Exception as e:
    print(e)
