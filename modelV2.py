import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Path to your dataset directory
train_data_dir = r"C:\Users\naray\Desktop\Homework\Computer Science\dataset.zip\Garbage classification\Garbage classification"
validation_data_dir = r"C:\Users\naray\Desktop\Homework\Computer Science\dataset.zip\one-indexed-files-notrash_val.txt"

# Image size for MobileNetV2 input
image_size = (224, 224)

# Number of classes in your dataset
num_classes = 6

# Batch size for training
batch_size = 32

# Number of training and validation samples
num_train_samples = 2362  # Sum of samples from all classes in your training set
num_validation_samples = 1977  # Sum of samples from all classes in your validation set

# Data augmentation for training (optional but recommended)
train_data_gen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Validation data generator (only rescaling for validation data)
validation_data_gen = ImageDataGenerator(rescale=1./255)

# Create training data generator
train_generator = train_data_gen.flow_from_directory(
    train_data_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical'
)

# Create validation data generator
validation_generator = validation_data_gen.flow_from_directory(
    validation_data_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical'
)

# Load MobileNetV2 without the classification head
base_model = hub.load("https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4")

# Add a new classification head
model = models.Sequential([
    base_model,
    layers.Dense(num_classes, activation='softmax')
])

# Freeze the base model (optional but recommended)
base_model.trainable = False

# Compile the model
model.compile(
    optimizer=optimizers.Adam(),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Print model summary (optional)
model.summary()

# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=num_train_samples // batch_size,
    epochs=10,  # You can increase the number of epochs for better training
    validation_data=validation_generator,
    validation_steps=num_validation_samples // batch_size
)

# Save the trained model (optional)
model.save('garbage_classification_model.h5')

# Evaluate the model on the validation set
val_loss, val_accuracy = model.evaluate(validation_generator, steps=num_validation_samples // batch_size)
print("Validation Accuracy: {:.2f}%".format(val_accuracy * 100))
