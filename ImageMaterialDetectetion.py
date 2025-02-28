import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from tkinter import Tk, Label, Button, filedialog
from PIL import Image, ImageTk

# Deshabilitar eager execution de TensorFlow 2.x
tf.compat.v1.disable_eager_execution()

# Ruta del modelo y dataset
model_path = "C:\\Users\\reyna\\Desktop\\Bot\\reciclaje\\modelo\\model.ckpt"
data_dir = "C:\\Users\\reyna\\Desktop\\Bot\\reciclaje\\dataset-resized"

# Configuración de categorías según tu dataset
categories = os.listdir(data_dir)
num_classes = len(categories)

# Definir el modelo (debe coincidir con el modelo entrenado)
X_ph = tf.compat.v1.placeholder(tf.float32, [None, 64, 64, 3])
drop_prob_ph = tf.compat.v1.placeholder(tf.float32)

W1 = tf.Variable(tf.random.normal([5, 5, 3, 32], mean=0, stddev=0.1))
b1 = tf.Variable(tf.fill([32], 0.1))
conv1 = tf.nn.relu(tf.nn.conv2d(X_ph, W1, strides=[1, 1, 1, 1], padding='SAME') + b1)
pool1 = tf.nn.max_pool2d(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

W2 = tf.Variable(tf.random.normal([5, 5, 32, 64], mean=0, stddev=0.1))
b2 = tf.Variable(tf.fill([64], 0.1))
conv2 = tf.nn.relu(tf.nn.conv2d(pool1, W2, strides=[1, 1, 1, 1], padding='SAME') + b2)
pool2 = tf.nn.max_pool2d(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

W3 = tf.Variable(tf.random.normal([16 * 16 * 64, 1024], mean=0, stddev=0.1))
b3 = tf.Variable(tf.fill([1024], 0.1))
flattened = tf.reshape(pool2, [-1, 16 * 16 * 64])
fc = tf.nn.relu(tf.matmul(flattened, W3) + b3)
dropout = tf.nn.dropout(fc, rate=drop_prob_ph)

W4 = tf.Variable(tf.random.normal([1024, num_classes], mean=0, stddev=0.1))
b4 = tf.Variable(tf.fill([num_classes], 0.1))
y_model = tf.matmul(dropout, W4) + b4

# Crear la clase de la interfaz gráfica
class ImageClassifierApp:
    def __init__(self, master):
        self.master = master
        master.title("Clasificador de Imágenes de Reciclaje")

        # Etiqueta de instrucciones
        self.label = Label(master, text="Sube una imagen para clasificar:")
        self.label.pack()

        # Botón para cargar imagen
        self.upload_button = Button(master, text="Cargar Imagen", command=self.upload_image)
        self.upload_button.pack()

        # Botón para clasificar
        self.classify_button = Button(master, text="Clasificar Imagen", command=self.classify_image, state="disabled")
        self.classify_button.pack()

        # Etiqueta para mostrar resultados
        self.result_label = Label(master, text="")
        self.result_label.pack()

        # Área para mostrar la imagen cargada
        self.image_label = Label(master)
        self.image_label.pack()

        # Iniciar sesión de TensorFlow y cargar el modelo
        self.sess = tf.compat.v1.Session()
        saver = tf.compat.v1.train.Saver()
        saver.restore(self.sess, model_path)
        print("Modelo cargado correctamente.")

    def upload_image(self):
        # Abrir cuadro de diálogo para elegir archivo
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path = file_path
            img = Image.open(file_path)
            img = img.resize((200, 200), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)

            # Mostrar imagen en la interfaz
            self.image_label.configure(image=img)
            self.image_label.image = img

            # Habilitar el botón de clasificación
            self.classify_button.config(state="normal")

    def classify_image(self):
        # Procesar la imagen para el modelo
        img = image.load_img(self.image_path, target_size=(64, 64))  # Tamaño 64x64 según tu modelo
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Añadir dimensión para el batch
        img_array = img_array / 255.0  # Normalización

        # Realizar la predicción
        prediction = self.sess.run(tf.argmax(y_model, axis=1), feed_dict={X_ph: img_array, drop_prob_ph: 0.0})
        result = categories[prediction[0]]

        # Mostrar el resultado
        self.result_label.configure(text="Clasificación: " + result)

# Crear la ventana principal de Tkinter
if __name__ == "__main__":
    root = Tk()
    app = ImageClassifierApp(root)
    root.mainloop()
