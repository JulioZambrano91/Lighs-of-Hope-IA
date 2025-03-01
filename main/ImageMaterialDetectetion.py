import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
import os
import shutil

class RecyclingClassifierApp:
    def __init__(self, master):
        self.master = master
        master.title("Clasificador de Residuos")
        
        # Cargar el modelo
        self.model = None
        self.class_names = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
        self.load_model()
        
        # Configurar directorio para correcciones
        self.corrections_dir = "user_corrections"
        os.makedirs(self.corrections_dir, exist_ok=True)
        
        # Configurar la interfaz
        self.create_widgets()
        self.current_correction = None
        
    def load_model(self):
        try:
            model_path = os.path.abspath('C:\\Users\\reyna\\Desktop\\Bot\\reciclaje\\modelo_reciclaje.h5')
            self.model = tf.keras.models.load_model(model_path)
            print("Modelo cargado exitosamente!")
        except Exception as e:
            print(f"Error cargando el modelo: {str(e)}")
            self.master.destroy()
            raise
        
    def create_widgets(self):
        # Configuración del estilo
        bg_color = '#F0F0F0'
        btn_color = '#4CAF50'
        text_color = '#333333'
        
        self.master.configure(bg=bg_color)
        
        # Marco principal
        main_frame = tk.Frame(self.master, bg=bg_color)
        main_frame.pack(pady=20)
        
        # Botones principales
        self.upload_btn = tk.Button(
            main_frame,
            text="Cargar Imagen",
            command=self.load_image,
            bg=btn_color,
            fg='white',
            font=('Arial', 12, 'bold')
        )
        self.upload_btn.grid(row=0, column=0, padx=10, pady=10)
        
        self.classify_btn = tk.Button(
            main_frame,
            text="Clasificar",
            command=self.classify_image,
            state=tk.DISABLED,
            bg='#2196F3',
            fg='white',
            font=('Arial', 12, 'bold')
        )
        self.classify_btn.grid(row=0, column=1, padx=10, pady=10)
        
        # Etiqueta para la imagen
        self.image_label = tk.Label(main_frame, bg=bg_color)
        self.image_label.grid(row=1, column=0, columnspan=2, pady=15)
        
        # Widget de texto para resultados
        self.result_text = tk.Text(
            main_frame,
            bg=bg_color,
            fg=text_color,
            font=('Arial', 12),
            width=40,
            height=10,
            wrap=tk.WORD
        )
        self.result_text.grid(row=2, column=0, columnspan=2, pady=10)
        self.result_text.tag_configure('bold', font=('Arial', 12, 'bold'))
        
        # Marco de retroalimentación
        self.feedback_frame = tk.Frame(main_frame, bg=bg_color)
        self.feedback_label = tk.Label(
            self.feedback_frame,
            text="¿La clasificación es correcta?",
            bg=bg_color,
            fg=text_color,
            font=('Arial', 12)
        )
        self.feedback_label.pack(side=tk.LEFT, padx=5)
        
        self.yes_btn = tk.Button(
            self.feedback_frame,
            text="Sí",
            bg='#4CAF50',
            fg='white',
            command=lambda: self.handle_feedback(True)
        )
        self.yes_btn.pack(side=tk.LEFT, padx=5)
        
        self.no_btn = tk.Button(
            self.feedback_frame,
            text="No",
            bg='#f44336',
            fg='white',
            command=lambda: self.handle_feedback(False)
        )
        self.no_btn.pack(side=tk.LEFT, padx=5)
        
        # Dropdown para correcciones
        self.correction_var = tk.StringVar()
        self.correction_dropdown = ttk.Combobox(
            self.feedback_frame,
            textvariable=self.correction_var,
            values=self.class_names,
            state='readonly'
        )
        
        # Botón de confirmación de corrección
        self.confirm_btn = tk.Button(
            self.feedback_frame,
            text="Confirmar Corrección",
            bg='#FFC107',
            fg='black',
            command=self.save_correction
        )
        
        self.feedback_frame.grid(row=3, column=0, columnspan=2, pady=10)
        self.feedback_frame.grid_remove()
        
        # Etiqueta de estado
        self.status_label = tk.Label(
            main_frame,
            text="",
            bg=bg_color,
            fg=text_color,
            font=('Arial', 10)
        )
        self.status_label.grid(row=4, column=0, columnspan=2)
        
    def handle_feedback(self, is_correct):
        if is_correct:
            self.status_label.config(text="¡Gracias por tu retroalimentación!")
            self.feedback_frame.grid_remove()
        else:
            self.correction_dropdown.pack(side=tk.LEFT, padx=5)
            self.confirm_btn.pack(side=tk.LEFT, padx=5)
            self.status_label.config(text="Selecciona la categoría correcta:")
            
    def save_correction(self):
        correct_class = self.correction_var.get()
        if not correct_class:
            messagebox.showerror("Error", "Selecciona una categoría válida")
            return
        
        # Crear directorio para la clase si no existe
        class_dir = os.path.join(self.corrections_dir, correct_class)
        os.makedirs(class_dir, exist_ok=True)
        
        # Copiar imagen al directorio de correcciones
        filename = os.path.basename(self.image_path)
        dest_path = os.path.join(class_dir, filename)
        shutil.copyfile(self.image_path, dest_path)
        
        # Actualizar modelo
        self.update_model(dest_path, correct_class)
        
        self.status_label.config(text="Corrección guardada y modelo actualizado!")
        self.feedback_frame.grid_remove()
        self.correction_dropdown.pack_forget()
        self.confirm_btn.pack_forget()
        
    def update_model(self, image_path, correct_class):
        try:
            # Preprocesar imagen
            img_array = self.preprocess_image(image_path)
            
            # Convertir etiqueta a índice
            label_index = self.class_names.index(correct_class)
            labels = tf.convert_to_tensor([label_index])
            
            # Configurar aprendizaje de transferencia
            self.model.trainable = True
            fine_tune_epochs = 1
            learning_rate = 0.0001
            
            # Compilar modelo
            self.model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy']
            )
            
            # Entrenamiento con la nueva imagen
            self.model.fit(
                x=img_array,
                y=labels,
                epochs=fine_tune_epochs
            )
            
        except Exception as e:
            print(f"Error actualizando modelo: {str(e)}")
            
    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path = file_path
            self.display_image(file_path)
            self.classify_btn.config(state=tk.NORMAL)
            self.feedback_frame.grid_remove()
            self.result_text.delete(1.0, tk.END)
            self.status_label.config(text="")
            
    def display_image(self, path):
        img = Image.open(path)
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        self.image_label.config(image=img)
        self.image_label.image = img
        
    def preprocess_image(self, path):
        img = tf.keras.utils.load_img(path, target_size=(224, 224))
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        return img_array / 255.0
        
    def classify_image(self):
        try:
            img_array = self.preprocess_image(self.image_path)
            predictions = self.model.predict(img_array)
            scores = tf.nn.softmax(predictions[0])
            
            # Mostrar resultados
            class_confidences = list(zip(self.class_names, scores.numpy() * 100))
            sorted_confidences = sorted(class_confidences, key=lambda x: x[1], reverse=True)
            
            self.result_text.delete(1.0, tk.END)
            for i, (class_name, confidence) in enumerate(sorted_confidences):
                line = f"{class_name.upper()}: {confidence:.2f}%\n"
                self.result_text.insert(tk.END, line, 'bold' if i == 0 else '')
            
            self.feedback_frame.grid()
            
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RecyclingClassifierApp(root)
    root.geometry("650x800")
    root.mainloop()