from imports import (
    tk, ttk, filedialog, messagebox,
    Image, ImageTk, np, tf,
    os, shutil, deque, json
)

# Clase para el entrenamiento por refuerzo
class ReinforcementTrainer:
    def __init__(self, model):
        self.model = model
        self.state_size = model.input_shape[1]  # Tamaño de entrada del modelo
        self.action_size = 3  # Acciones: ajustar lr, epochs, o ambos
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # Factor de descuento
        self.epsilon = 1.0  # Exploración
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        
    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        q_values = self.model.predict(state, verbose=0)
        return np.argmax(q_values[0])
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def replay(self, batch_size=32):
        if len(self.memory) < batch_size:
            return
        minibatch = np.random.choice(len(self.memory), batch_size, replace=False)
        for idx in minibatch:
            state, action, reward, next_state, done = self.memory[idx]
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state, verbose=0)[0])
            target_f = self.model.predict(state, verbose=0)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def get_training_parameters(self, action):
        params = {
            'learning_rate': 0.0001,
            'epochs': 3
        }
        if action == 0:
            params['learning_rate'] *= 1.2
        elif action == 1:
            params['epochs'] += 1
        elif action == 2:
            params['learning_rate'] *= 0.8
            params['epochs'] -= 1
        return params

# Clase principal del formulario 
class FormularioClasificadorIMGDesign(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        
        # Inicializar atributos
        self.class_names = ['cardboard', 'glass', 'metal', 'paper', 'plastic']
        self.corrections_dir = "user_corrections"
        self.image_path = None
        self.current_correction = None
        self.zoom_button = None
        
        # Configurar scroll
        self._configurar_scroll()
        
        # Cargar modelo e información
        self.load_model()
        self.rl_trainer = ReinforcementTrainer(self.model)
        self.reciclaje_data = self._cargar_info_reciclaje()
        
        # Crear widgets
        self.create_widgets()
        os.makedirs(self.corrections_dir, exist_ok=True)
        
    def _cargar_info_reciclaje(self):
        try:
            with open('reciclaje_info.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la información de reciclaje: {str(e)}")
            return {}
        
    def load_model(self):
        try:
            model_path = os.path.abspath('best_model.keras')
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Modelo no encontrado en: {model_path}")
            self.model = tf.keras.models.load_model(model_path)
            print("Modelo cargado exitosamente!")
            if not hasattr(self.model, "input_shape"):
                raise ValueError("El modelo no tiene atributo input_shape")
        except Exception as e:
            messagebox.showerror("Error crítico", f"No se pudo cargar el modelo:\n{str(e)}")
            self.master.destroy()
            
    def create_widgets(self):
        # Configuración del estilo
        bg_color = '#F0F0F0'
        btn_color = '#4CAF50'
        text_color = '#333333'
        
        # Main frame dividido en dos columnas: izquierda (clasificador) y derecha (info reciclaje)
        main_frame = tk.Frame(self.scrollable_frame, bg=bg_color)
        main_frame.pack(pady=20, fill="both", expand=True, padx=20)
        
        # Left Frame: Contiene controles de la aplicación
        left_frame = tk.Frame(main_frame, bg=bg_color)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0,20))
        
        # Right Frame: Muestra la información completa del JSON (se oculta por defecto)
        self.right_frame = tk.Frame(main_frame, bg=bg_color, bd=2, relief='groove')
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=1)
        
        # Ocultar el panel derecho hasta tener una clasificación
        self.right_frame.grid_remove()
        
        # CONTROLES DEL LEFT FRAME
        self.upload_btn = tk.Button(
            left_frame,
            text="Cargar Imagen",
            command=self.load_image,
            bg=btn_color,
            fg='white',
            font=('Arial', 12, 'bold')
        )
        self.upload_btn.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.classify_btn = tk.Button(
            left_frame,
            text="Clasificar",
            command=self.classify_image,
            state=tk.DISABLED,
            bg='#2196F3',
            fg='white',
            font=('Arial', 12, 'bold')
        )
        self.classify_btn.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        self.save_model_btn = tk.Button(
            left_frame,
            text="Guardar Modelo",
            command=self.save_model,
            bg='#FFC107',
            fg='black',
            font=('Arial', 12, 'bold')
        )
        self.save_model_btn.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        
        self.image_label = tk.Label(left_frame, bg=bg_color)
        self.image_label.grid(row=1, column=0, columnspan=3, pady=15)
        
        self.result_text = tk.Text(
            left_frame,
            bg=bg_color,
            fg=text_color,
            font=('Arial', 12),
            width=40,
            height=10,
            wrap=tk.WORD
        )
        self.result_text.grid(row=2, column=0, columnspan=3, pady=10)
        self.result_text.tag_configure('bold', font=('Arial', 12, 'bold'))
        
        self.feedback_frame = tk.Frame(left_frame, bg=bg_color)
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
        
        self.correction_var = tk.StringVar()
        self.correction_dropdown = ttk.Combobox(
            self.feedback_frame,
            textvariable=self.correction_var,
            values=self.class_names,
            state='readonly'
        )
        self.confirm_btn = tk.Button(
            self.feedback_frame,
            text="Confirmar Corrección",
            bg='#FFC107',
            fg='black',
            command=self.save_correction
        )
        self.feedback_frame.grid(row=3, column=0, columnspan=3, pady=10)
        self.feedback_frame.grid_remove()
        
        self.status_label = tk.Label(
            left_frame,
            text="",
            bg=bg_color,
            fg=text_color,
            font=('Arial', 12)
        )
        self.status_label.grid(row=4, column=0, columnspan=3)
        
        # CONTROLES DEL RIGHT FRAME: Información de reciclaje
        
        self.info_imagen = tk.Label(self.right_frame, bg=bg_color)
        self.info_imagen.pack(padx=10, pady=10)
        
        self.info_table = ttk.Treeview(
            self.right_frame, 
            columns=("Propiedad", "Valor"), 
            show="headings", 
            height=7
        )
        self.info_table.heading("Propiedad", text="Propiedad")
        self.info_table.heading("Valor", text="Valor")
        self.info_table.column("Propiedad", anchor="w", width=120)
        # Se aumenta el ancho para que textos largos no se corten
        self.info_table.column("Valor", anchor="w", width=300)
        self.info_table.pack(padx=10, pady=10, fill="both", expand=True)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading",
                        font=("Helvetica", 10, "bold"),
                        background="#4CAF50",
                        foreground="white")
        style.configure("Treeview",
                        font=("Helvetica", 10),
                        rowheight=25)
        
        self.zoom_button = None
        
    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path = file_path
            self.display_image(file_path)
            self.classify_btn.config(state=tk.NORMAL)
            self.feedback_frame.grid_remove()
            self.result_text.delete(1.0, tk.END)
            self.status_label.config(text="")
            # Ocultamos el panel derecho hasta clasificar
            self.right_frame.grid_remove()
            
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
            class_confidences = list(zip(self.class_names, scores.numpy() * 100))
            sorted_confidences = sorted(class_confidences, key=lambda x: x[1], reverse=True)
            self.result_text.delete(1.0, tk.END)
            for i, (class_name, confidence) in enumerate(sorted_confidences):
                line = f"{class_name.upper()}: {confidence:.2f}%\n"
                self.result_text.insert(tk.END, line, 'bold' if i == 0 else '')
            # Mostrar el panel derecho solo si hay una clasificación válida
            top_class = sorted_confidences[0][0]
            self.display_recycling_info(top_class)
            self.feedback_frame.grid()
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error: {str(e)}")
            
    def update_model(self, image_path, correct_class):
        try:
            img_array = self.preprocess_image(image_path)
            label_index = self.class_names.index(correct_class)
            labels = tf.convert_to_tensor([label_index])
            state = np.expand_dims(img_array.numpy().flatten(), axis=0)
            action = self.rl_trainer.get_action(state)
            params = self.rl_trainer.get_training_parameters(action)
            self.model.trainable = True
            self.model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=params['learning_rate']),
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy']
            )
            history = self.model.fit(
                img_array,
                labels,
                epochs=params['epochs'],
                verbose=0
            )
            reward = history.history['accuracy'][-1] * 100
            next_state = np.expand_dims(img_array.numpy().flatten(), axis=0)
            self.rl_trainer.remember(state, action, reward, next_state, False)
            self.rl_trainer.replay()
            self.display_recycling_info(correct_class)
            print(f"Modelo actualizado con LR: {params['learning_rate']}, Epochs: {params['epochs']}, Recompensa: {reward:.2f}%")
            self.save_model()
        except Exception as e:
            self.status_label.config(text=f"Error actualizando modelo: {str(e)}")
            
    def save_model(self):
        try:
            self.model.save('best_model.keras')
            self.status_label.config(text="Modelo guardado exitosamente!")
        except Exception as e:
            self.status_label.config(text="Error al guardar el modelo.")
            print(f"Error guardando el modelo: {str(e)}")
            
    def display_recycling_info(self, clase):
        # Mostrar u ocultar el panel derecho según la información
        if clase in self.reciclaje_data:
            self.right_frame.grid()
        else:
            self.right_frame.grid_remove()
            return
        
        # Limpiar el contenido previo de la tabla
        for item in self.info_table.get_children():
            self.info_table.delete(item)

        info = self.reciclaje_data.get(clase, None)
        if not info:
            self.info_table.insert("", "end", values=("Información", "No disponible"))
            self.info_imagen.config(image='')
            return

        # Mostrar la imagen ilustrativa
        try:
            img = Image.open(info['imagen'])
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            self.info_img = ImageTk.PhotoImage(img)
            self.info_imagen.config(image=self.info_img)
        except Exception as e:
            print(f"Error cargando imagen: {str(e)}")
            self.info_imagen.config(image='')

        # Insertar la información en la tabla
        self.info_table.insert("", "end", values=("TIPO", info.get('tipo', 'N/A')))
        self.info_table.insert("", "end", values=("DURACIÓN", info.get('duracion', 'N/A')))
        self.info_table.insert("", "end", values=("INFORMACIÓN", info.get('informacion', 'N/A')))
        reciclaje = info.get('reciclaje', {})
        self.info_table.insert("", "end", values=("CONTENEDOR", reciclaje.get('contenedor', 'N/A')))
        self.info_table.insert("", "end", values=("SÍMBOLO", reciclaje.get('simbolo', 'N/A')))
        self.info_table.insert("", "end", values=("COLOR", reciclaje.get('color', 'N/A')))
        self.info_table.insert("", "end", values=("OTROS", info.get('otros', 'N/A')))

        # Crear o actualizar el botón para ver imagen completa
        if self.zoom_button:
            self.zoom_button.destroy()
        self.zoom_button = tk.Button(
            self.info_imagen.master,
            text="Ver imagen completa",
            command=lambda: self.show_full_image(info['imagen'])
        )
        self.zoom_button.pack(pady=5)
        
    def show_full_image(self, img_path):
        try:
            img = Image.open(img_path)
            top = tk.Toplevel(self.master)
            top.title("Imagen completa")
            full_img = ImageTk.PhotoImage(img)
            lbl = tk.Label(top, image=full_img)
            lbl.image = full_img  # Prevenir recolección de basura
            lbl.pack()
            top.geometry(f"{img.width}x{img.height}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar la imagen completa: {str(e)}")
            
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
        class_dir = os.path.join(self.corrections_dir, correct_class)
        os.makedirs(class_dir, exist_ok=True)
        filename = os.path.basename(self.image_path)
        dest_path = os.path.join(class_dir, filename)
        shutil.copyfile(self.image_path, dest_path)
        self.update_model(dest_path, correct_class)
        self.status_label.config(text="Corrección guardada y modelo actualizado!")
        self.feedback_frame.grid_remove()
        self.correction_dropdown.pack_forget()
        self.confirm_btn.pack_forget()

    def _configurar_scroll(self):
        self.canvas = tk.Canvas(self, bg='#F0F0F0', highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#F0F0F0')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        def _on_mousewheel(event):
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
            else:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        def bind_children(parent):
            parent.bind("<MouseWheel>", _on_mousewheel)
            parent.bind("<Button-4>", _on_mousewheel)
            parent.bind("<Button-5>", _on_mousewheel)
            for child in parent.winfo_children():
                bind_children(child)

        bind_children(self.scrollable_frame)
        self.canvas.bind("<MouseWheel>", _on_mousewheel)
        self.canvas.bind("<Button-4>", _on_mousewheel)
        self.canvas.bind("<Button-5>", _on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")