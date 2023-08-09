import PySimpleGUI as sg
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tensorflow as tf
import tensorflow_hub as hub
import io
import numpy as np
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

layout_main_menu = [
    [sg.Text("Main Menu", font=("Helvetica", 30))],
    [sg.Button("Open Image Classification", font=("Helvetica", 20)), sg.Button("Exit", font=("Helvetica", 20))],
    [sg.Image(data='', key='-IMAGE-', size=(640, 360))],
]

layout_classification = [
    [sg.Text("Image Classification", font=("Helvetica", 30))],
    [sg.Image(data='', key='-CLASSIFIED-', size=(640, 360))],
    [sg.Text("", font=("Helvetica", 20), key='-RESULT-')],
    [sg.Button("Open Image", font=("Helvetica", 20)), sg.Button("Close", font=("Helvetica", 20))]
]

window_main_menu = sg.Window("Main Menu", layout_main_menu, finalize=True, size=(800, 600))
window_classification = None

while True:
    try:
        event, values = window_main_menu.read()

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break

        if event == 'Open Image Classification':
            window_main_menu.hide()
            layout = layout_classification
            window_classification = sg.Window("Image Classification", layout, finalize=True, size=(800, 600))

            while True:
                try:
                    event, values = window_classification.read()

                    if event == sg.WINDOW_CLOSED or event == 'Close':
                        window_classification.close()
                        window_main_menu.un_hide()
                        break

                    if event == 'Open Image':
                        image_path = sg.popup_get_file("Select an image", file_types=(("Image files", "*.png;*.jpg;*.jpeg;*.gif"),))
                        if image_path:
                            waste_category, recycling_instruction = classify_waste_image(image_path)
                            image = Image.open(image_path)
                            image.thumbnail((640, 360))

                            # Convert PIL image to bytes and display using PySimpleGUI
                            img_byte_array = io.BytesIO()
                            image.save(img_byte_array, format="PNG")
                            img_data = img_byte_array.getvalue()
                            window_classification['-CLASSIFIED-'].update(data=img_data)
                            window_classification['-RESULT-'].update(f"Detected waste category: {waste_category}\nRecycling instructions: {recycling_instruction}")
                        else:
                            sg.popup_error("No image selected")
                except Exception as classification_error:
                    print(classification_error)
                    sg.popup_error(f"An error occurred during image classification: {classification_error}")
    except Exception as main_menu_error:
        sg.popup_error(f"An error occurred in the main menu: {main_menu_error}")
        print(main_menu_error)
