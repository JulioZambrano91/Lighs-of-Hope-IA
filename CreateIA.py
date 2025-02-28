import os
import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# Deshabilitar eager execution de TensorFlow 2.x para usar TensorFlow 1.x
tf.compat.v1.disable_eager_execution()

# 1. Cargar y preprocesar los datos
base_dir = "C:\\Users\\reyna\\Desktop\\Bot\\reciclaje"  # Ruta específica
data_dir = os.path.join(base_dir, "dataset-resized")  # Ruta al dataset

# Función para contar imágenes por categoría
def count_images(directory):
    categories = os.listdir(directory)
    counts = {}
    for category in categories:
        cat_path = os.path.join(directory, category)
        counts[category] = len(os.listdir(cat_path))
    return counts

print("Data recolectada:", count_images(data_dir))

# 2. Preparar los datos
categories = os.listdir(data_dir)
num_classes = len(categories)

# Hiperparámetros
batch_size = 32
img_height, img_width = 64, 64  # Redimensionar imágenes a 64x64
n_epochs = 40
learn_rate = 0.0001
drop_prob = 0.5

# Generador de imágenes para cargar y preprocesar los datos
#datagen = ImageDataGenerator(rescale=1.0/255.0, validation_split=0.2)
rango_rotacion = 30
mov_ancho = 0.25
mov_alto = 0.25
#rango_inclinacion=15 #No uso este de momento pero si quieres puedes probar usandolo!
rango_acercamiento=[0.5,1.5]

datagen = ImageDataGenerator(
    rotation_range = rango_rotacion,
    width_shift_range = mov_ancho,
    height_shift_range = mov_alto,
    zoom_range=rango_acercamiento,
    #shear_range=rango_inclinacion #No uso este de momento pero si quieres puedes probar usandolo!
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

# 3. Definir el modelo
X_ph = tf.compat.v1.placeholder(tf.float32, [None, img_height, img_width, 3])
y_ph = tf.compat.v1.placeholder(tf.float32, [None, num_classes])
drop_prob_ph = tf.compat.v1.placeholder(tf.float32)

# Capas convolucionales
W1 = tf.Variable(tf.random.normal([5, 5, 3, 32], mean=0, stddev=0.1))
b1 = tf.Variable(tf.fill([32], 0.1))
y1 = tf.nn.conv2d(X_ph, W1, strides=[1, 1, 1, 1], padding='SAME') + b1
conv1 = tf.nn.relu(y1)
pool1 = tf.nn.max_pool2d(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

W2 = tf.Variable(tf.random.normal([5, 5, 32, 64], mean=0, stddev=0.1))
b2 = tf.Variable(tf.fill([64], 0.1))
y2 = tf.nn.conv2d(pool1, W2, strides=[1, 1, 1, 1], padding='SAME') + b2
conv2 = tf.nn.relu(y2)
pool2 = tf.nn.max_pool2d(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

# Capa fully connected
W3 = tf.Variable(tf.random.normal([16 * 16 * 64, 1024], mean=0, stddev=0.1))
b3 = tf.Variable(tf.fill([1024], 0.1))
pool2_flattened = tf.reshape(pool2, [-1, 16 * 16 * 64])
y3 = tf.matmul(pool2_flattened, W3) + b3
full_layer = tf.nn.relu(y3)

# Dropout
dropout_layer = tf.nn.dropout(full_layer, rate=drop_prob_ph)

# Capa de salida
W4 = tf.Variable(tf.random.normal([1024, num_classes], mean=0, stddev=0.1))
b4 = tf.Variable(tf.fill([num_classes], 0.1))
y_model = tf.matmul(dropout_layer, W4) + b4

# 4. Definir la función de pérdida y el optimizador
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_ph, logits=y_model))
optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learn_rate)
train = optimizer.minimize(loss)

# Métricas de precisión
correct_predictions = tf.equal(tf.argmax(y_ph, axis=1), tf.argmax(y_model, axis=1))
accuracy = tf.reduce_mean(tf.cast(correct_predictions, tf.float32))

# 5. Entrenamiento
init = tf.compat.v1.global_variables_initializer()
saver = tf.compat.v1.train.Saver()

with tf.compat.v1.Session() as sess:
    sess.run(init)
    for epoch in range(n_epochs):
        print(f"Epoch {epoch + 1}/{n_epochs}")
        for i in range(train_generator.samples // batch_size):
            batch_X, batch_y = train_generator.__next__()  # Usar __next__() en lugar de next()
            my_feed = {X_ph: batch_X, y_ph: batch_y, drop_prob_ph: drop_prob}
            sess.run(train, feed_dict=my_feed)
        
        # Validación
        val_acc = []
        for i in range(validation_generator.samples // batch_size):
            batch_X, batch_y = validation_generator.__next__()  # Usar __next__() en lugar de next()
            my_feed = {X_ph: batch_X, y_ph: batch_y, drop_prob_ph: 0.0}
            acc = sess.run(accuracy, feed_dict=my_feed)
            val_acc.append(acc)
        print(f"Validation Accuracy: {np.mean(val_acc):.4f}")

    # Guardar el modelo
    save_path = saver.save(sess, "C:\\Users\\reyna\\Desktop\\Bot\\reciclaje\\modelo\\model.ckpt")
    print(f"Model saved in path: {save_path}")

print("Entrenamiento finalizado")