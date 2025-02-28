import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dropout, Dense, BatchNormalization
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

# Ruta al dataset
base_dir = "C:\\Users\\reyna\\Desktop\\Bot\\reciclaje"
data_dir = os.path.join(base_dir, "dataset-resized")

# Contar imágenes por categoría
def count_images(directory):
    categories = os.listdir(directory)
    counts = {}
    for category in categories:
        cat_path = os.path.join(directory, category)
        counts[category] = len(os.listdir(cat_path))
    return counts

print("Imágenes por categoría:", count_images(data_dir))

# Configuración de hiperparámetros
img_height, img_width = 128, 128  # Aumentar tamaño de imagen
batch_size = 16  # Reducir el tamaño del batch para que el modelo aprenda más gradualmente
n_epochs = 40
learn_rate = 1e-4
drop_prob = 0.5

# Generador de imágenes con mejor augmentación
datagen = ImageDataGenerator(
    rescale=1.0/255.0,
    rotation_range=50,
    width_shift_range=0.3,
    height_shift_range=0.3,
    zoom_range=[0.6, 1.4],
    shear_range=25,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    validation_split=0.3  # Ampliar el tamaño del conjunto de validación
)

train_generator = datagen.flow_from_directory(
    data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)

# Construcción del modelo optimizado
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(img_height, img_width, 3))
base_model.trainable = False  # Congelar capas preentrenadas

model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    BatchNormalization(),  # Añadir Batch Normalization para estabilizar las salidas intermedias
    Dropout(drop_prob),  # Regularización para evitar sobreajuste
    Dense(256, activation='relu'),  # Capa densa adicional para aprender patrones complejos
    Dropout(drop_prob),  # Otra capa de regularización
    Dense(train_generator.num_classes, activation='softmax')  # Salida categórica
])

# Compilación del modelo
model.compile(
    optimizer=Adam(learning_rate=learn_rate),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Callbacks para mejorar el entrenamiento
early_stop = EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True)

# Entrenamiento del modelo
history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=n_epochs,
    callbacks=[early_stop],
    verbose=1
)

# Guardar el modelo en el nuevo formato
model.save(os.path.join(base_dir, "modelo", "model_mobilenetv2.keras"))
print("Modelo guardado correctamente.")
