import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import requests
from io import BytesIO

model_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4"
try:
    model = hub.load(model_url)
except Exception as e:
    print("Error loading the model from TensorFlow Hub:", e)
    exit()

def get_image_from_url(image_url):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    return image

def get_image_from_file(file_path):
    image = Image.open(file_path)
    return image

def classify_waste(input_image, image_type='url'):
    if image_type == 'url':
        image = get_image_from_url(input_image)
    elif image_type == 'file':
        image = get_image_from_file(input_image)
    else:
        raise ValueError("Invalid image_type. Use 'url' for image from URL or 'file' for image from local file.")

    image = image.resize((224, 224))
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array = image_array / 255.0
    image_array = tf.expand_dims(image_array, axis=0)

    predictions = model(image_array)
    predicted_class_idx = tf.argmax(predictions, axis=1)[0]

    waste_categories = {
        0: "Cardboard",
        1: "Glass",
        2: "Metal",
        3: "Paper",
        4: "Plastic",
        5: "Trash"
    }

    waste_category = waste_categories.get(predicted_class_idx, "Unknown")

    recycling_instructions = {
        "Cardboard": "Cardboard can be recycled by flattening and placing it in recycling bins.",
        "Glass": "Glass can be recycled by placing it in recycling bins. Make sure it's clean and dry.",
        "Metal": "Metal can be recycled by placing it in recycling bins. Remove any non-recyclable parts.",
        "Paper": "Paper can be recycled by placing it in recycling bins. Avoid soiled or wet paper.",
        "Plastic": "Plastic can be recycled by placing it in recycling bins. Check the recycling number for specific instructions.",
        "Trash": "This item is not recyclable. Please dispose of it properly."
    }

    recycling_instruction = recycling_instructions.get(waste_category, "Recycling information not available.")

    return waste_category, recycling_instruction

if __name__ == "__main__":
    try: 
        image_url = r"Path_to_image"
        waste_category, recycling_instruction = classify_waste(image_url, image_type='url')
        print("Detected waste category:", waste_category)
        print("Recycling instructions:", recycling_instruction)
    except Exception as e:
        print(e)
