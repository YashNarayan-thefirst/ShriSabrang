import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image

# Load the trained model
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

if __name__ == "__main__":
    try:
        # Replace 'your_image.jpg' with the path to your local image file
        image_file_path = r"C:\Users\naray\Desktop\Shri_sabrang 2\Garbage classification\Garbage classification\trash\trash33.jpg"
        waste_category, recycling_instruction = classify_waste_image(image_file_path)
        print("Detected waste category:", waste_category)
        print("Recycling instructions:", recycling_instruction)
    except Exception as e:
        print(e)
