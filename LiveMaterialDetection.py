import os
import cv2
import tensorflow as tf
import numpy as np
from tkinter import Tk, Label, Button
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

# Clase para la detección en vivo
class LiveMaterialDetectionApp:
    def __init__(self, master):
        self.master = master
        master.title("Clasificador de Materiales en Vivo")

        # Etiqueta de instrucciones
        self.label = Label(master, text="Presiona 'Iniciar Cámara' para comenzar la detección:")
        self.label.pack()

        # Botón para iniciar la cámara
        self.start_button = Button(master, text="Iniciar Cámara", command=self.start_camera)
        self.start_button.pack()

        # Botón para detener la cámara
        self.stop_button = Button(master, text="Detener Cámara", command=self.stop_camera, state="disabled")
        self.stop_button.pack()

        # Etiqueta para mostrar resultados
        self.result_label = Label(master, text="Clasificación: ")
        self.result_label.pack()

        # Área para mostrar el video
        self.video_label = Label(master)
        self.video_label.pack()

        # Iniciar sesión de TensorFlow y cargar el modelo
        self.sess = tf.compat.v1.Session()
        saver = tf.compat.v1.train.Saver()
        saver.restore(self.sess, model_path)
        print("Modelo cargado correctamente.")

        # Cámara y bandera de estado
        self.cap = None
        self.running = False

    def start_camera(self):
        # Iniciar la cámara
        self.cap = cv2.VideoCapture(0)  # 0 para cámara predeterminada
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Configurar ancho
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Configurar alto
        self.running = True
        self.update_frame()
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def stop_camera(self):
        # Detener la cámara
        self.running = False
        self.cap.release()
        self.video_label.config(image='')
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def update_frame(self):
        if self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Procesar el cuadro en vivo
                frame_resized = cv2.resize(frame, (64, 64))  # Redimensionar para el modelo
                img_array = np.expand_dims(frame_resized, axis=0)  # Añadir dimensión para el batch
                img_array = img_array / 255.0  # Normalización

                # Realizar predicción con el modelo
                prediction = self.sess.run(tf.argmax(y_model, axis=1), feed_dict={X_ph: img_array, drop_prob_ph: 0.0})
                result = categories[prediction[0]]

                # Mostrar el resultado
                self.result_label.config(text="Clasificación: " + result)

                # Convertir el cuadro para mostrar en Tkinter
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = img.resize((400, 300), Image.Resampling.NEAREST)  # Redimensionar para ventana
                img_tk = ImageTk.PhotoImage(img)

                # Mostrar el cuadro en vivo
                self.video_label.img_tk = img_tk
                self.video_label.config(image=img_tk)

            # Llamar de nuevo a update_frame después de 10 ms
            self.master.after(10, self.update_frame)

# Crear la ventana principal de Tkinter
if __name__ == "__main__":
    root = Tk()
    app = LiveMaterialDetectionApp(root)
    root.mainloop()
