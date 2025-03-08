from imports import (
    tk, Image, ImageTk, font,
    resource_path, webbrowser
)

class FormularioProyectoDesign(tk.Frame):
    def __init__(self, panel_principal):
        super().__init__(panel_principal, bg="#F8F9FA")
        self.pack(fill="both", expand=True)
        
        # Configuración inicial
        self.fuente_titulo = ("Montserrat", 18, "bold")
        self.fuente_seccion = ("Open Sans", 14, "bold")
        self.fuente_texto = ("Open Sans", 12)
        self.color_titulo = "#2C3E50"
        self.color_seccion = "#2980B9"
        self.color_texto = "#2C3E50"
        self.color_fondo = "#F8F9FA"
        self.color_borde = "#DEE2E6"
        
        # Configurar sistema de scroll
        self.configurar_scroll()
        
        # Cargar contenido
        self.agregar_contenido()

    def configurar_scroll(self):
        # Contenedor principal
        self.main_frame = tk.Frame(self, bg=self.color_fondo)
        self.main_frame.pack(fill="both", expand=True)
        
        # Canvas y scrollbar
        self.canvas = tk.Canvas(
            self.main_frame,
            bg=self.color_fondo,
            highlightthickness=0
        )
        self.scrollbar = tk.Scrollbar(
            self.main_frame,
            orient="vertical",
            command=self.canvas.yview
        )
        
        # Frame scrollable
        self.scrollable_frame = tk.Frame(
            self.canvas,
            bg=self.color_fondo
        )
        
        # Configurar canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Empaquetar elementos
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Evento de scroll con rueda del mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def agregar_contenido(self):
        self.crear_titulo()
        self.crear_exploracion_datos()
        self.crear_preparacion_datos()
        self.crear_modelo()
        self.crear_entrenamiento()
        self.crear_evaluacion()
        self.crear_exportacion()
        
    def agregar_imagen(self, frame, ruta_imagen, tamaño, titulo=None):
        try:
            imagen = Image.open(resource_path(ruta_imagen))
            imagen = imagen.resize(tamaño, Image.LANCZOS)
            photo = ImageTk.PhotoImage(imagen)
            label = tk.Label(frame, image=photo, bg="white")
            label.image = photo
            if titulo:
                tk.Label(frame, text=titulo, bg="white", font=("Open Sans", 10)).pack()
            return label
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            return self.crear_placeholder(frame, tamaño, titulo)

    def crear_placeholder(self, frame, tamaño, titulo=None):
        try:
            imagen = Image.open(resource_path("imagenes/data.png"))
            imagen = imagen.resize(tamaño, Image.LANCZOS)
            photo = ImageTk.PhotoImage(imagen)
            label = tk.Label(frame, image=photo, bg="white")
            label.image = photo
            if titulo:
                tk.Label(frame, text=titulo, bg="white", font=("Open Sans", 10)).pack()
            return label
        except Exception as e:
            print(f"Error cargando placeholder: {e}")
            placeholder = tk.Canvas(frame, width=tamaño[0], height=tamaño[1], bg="#e1e1e1")
            placeholder.create_text(
                tamaño[0]//2, tamaño[1]//2,
                text="Imagen no disponible\n(Placeholder)",
                fill="#666",
                font=("Arial", 10),
                justify="center"
            )
            if titulo:
                tk.Label(frame, text=titulo, bg="white", font=("Open Sans", 10)).pack()
            return placeholder

    def crear_marco_seccion(self, texto, fuente):
        marco = tk.Frame(
            self.scrollable_frame,
            bg="white",
            bd=2,
            relief="solid",
            padx=20,
            pady=10,
            highlightbackground=self.color_borde
        )
        marco.pack(pady=10, fill="x", padx=20)
        
        tk.Label(
            marco,
            text=texto,
            wraplength=900,
            justify="left",
            anchor="w",
            font=fuente,
            fg=self.color_texto,
            bg="white"
        ).pack(fill="x")
        
        return marco

    def crear_titulo(self):
        contenedor = tk.Frame(
            self.scrollable_frame,
            bg=self.color_fondo
        )
        contenedor.pack(pady=20, fill="x")
        
        tk.Label(
            contenedor,
            text="Proceso de Desarrollo del Modelo CNN",
            font=self.fuente_titulo,
            fg=self.color_titulo,
            bg=self.color_fondo
        ).pack()

    def crear_exploracion_datos(self):
        contenido = (
            "1. Exploración de Datos\n\n"
            "• Verificación estructural:\n"
            "  o 5 carpetas (cardboard, glass, metal, paper, plastic)\n"
            "  o 1,000 imágenes por clase en RGB\n\n"
            "• Distribución balanceada:\n"
            "  o 20% por clase (evitando sesgos)\n\n"
            "• Visualización de muestras:\n"
            "  o 3 imágenes representativas por clase"
        )
        marco = self.crear_marco_seccion(contenido, self.fuente_texto)
        
        # Contenedor para imágenes
        img_frame = tk.Frame(marco, bg="white")
        img_frame.pack(pady=10, fill="x")
        
        # Imagen 1
        frame_img1 = tk.Frame(img_frame, bg="white")
        frame_img1.pack(side="left", padx=10)
        self.agregar_imagen(
            frame_img1,
            "imagenes/data.png",
            (400, 200),
            "Estructura de Carpetas"
        ).pack()
        

    def crear_preparacion_datos(self):
        contenido = (
            "2. Preparación de Datos\n\n"
            "• Aumento de datos:\n"
            "  o Rotación ±25°\n"
            "  o Zoom 15%\n"
            "  o Ajuste de brillo\n\n"
            "• Normalización:\n"
            "  o Valores 0-255 → 0-1"
        )
        marco = self.crear_marco_seccion(contenido, self.fuente_texto)
        self.agregar_imagen(
            marco,
            "imagenes/clases.png",
            (400, 60),
            "Distribucion de la data"
        ).pack(pady=10)

    def crear_modelo(self):
        contenido = (
            "3. Construcción del Modelo\n\n"
            "• MobileNetV2 con capas congeladas\n"
            "• Arquitectura personalizada:\n"
            "  o GlobalAveragePooling2D\n"
            "  o Dropout(0.6)\n"
            "  o Dense(256)"
        )
        marco = self.crear_marco_seccion(contenido, self.fuente_texto)
        self.agregar_imagen(
            marco,
            "imagenes/modelo.png",
            (900, 400),
            "Diagrama de Arquitectura"
        ).pack(pady=10)

    def crear_entrenamiento(self):
        contenido = (
            "4. Entrenamiento\n\n"
            "• Curvas de aprendizaje\n"
            "• Métricas de rendimiento\n"
            "• Early Stopping"
        )
        marco = self.crear_marco_seccion(contenido, self.fuente_texto)
        self.agregar_imagen(
            marco,
            "imagenes/entrenamiento.png",
            (1000, 100),
            "Gráficas de Entrenamiento"
        ).pack(pady=10)

    def crear_evaluacion(self):
        contenido = (
            "5. Evaluación\n\n"
            "• Matriz de confusión\n"
            "• Métricas por clase\n"
            "• Resultados finales"
        )
        marco = self.crear_marco_seccion(contenido, self.fuente_texto)
        self.agregar_imagen(
            marco,
            "imagenes/graficas.png",
            (1000, 400),
            "Resultados Finales"
        ).pack(pady=10)

    def crear_exportacion(self):
        contenido = (
            "6. Exportación del Modelo\n\n"
            "• Arquitectura guardada\n"
            "• Peso del modelo\n"
            "• Ejemplos de implementación"
        )
        marco = self.crear_marco_seccion(contenido, self.fuente_texto)
        
        # Enlace a GitHub
        enlace_frame = tk.Frame(marco, bg="white")
        enlace_frame.pack(pady=10)
        enlace = tk.Label(
            enlace_frame,
            text="Repositorio GitHub",
            fg="blue",
            cursor="hand2",
            font=("Open Sans", 12)
        )
        enlace.pack()
        enlace.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/JulioZambrano91/Lighs-of-Hope-IA"))