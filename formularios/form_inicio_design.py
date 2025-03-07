from imports import tk, Image, ImageTk, font
import webbrowser

class FormularioInicioDesign():
    def __init__(self, panel_principal):
        self.fuente_titulo = ("Montserrat", 22, "bold")
        self.fuente_seccion = ("Open Sans", 18, "bold")
        self.fuente_texto = ("Open Sans", 16)
        self.fuente_negrita = font.Font(family="Open Sans", size=14, weight="bold")
        self.color_titulo = "#2C3E50"
        self.color_seccion = "#2980B9"
        self.color_texto = "#2C3E50"
        self.color_fondo = "#F8F9FA"
        self.color_borde = "#DEE2E6"
        self.agregar_contenido(panel_principal)

    def agregar_contenido(self, panel_principal):
        canvas = tk.Canvas(panel_principal, width=1000, height=800, bg=self.color_fondo)
        scrollbar = tk.Scrollbar(panel_principal, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.color_fondo)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, bg=self.color_fondo)

        # Secciones del contenido
        self.crear_titulo(scrollable_frame)
        self.crear_descripcion(scrollable_frame)
        self.crear_tabla_contenidos(scrollable_frame)
        self.crear_librerias(scrollable_frame)
        self.crear_data(scrollable_frame)
        self.crear_interfaz(scrollable_frame)
        self.crear_agradecimientos(scrollable_frame)
        self.crear_acerca_de(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configuración del scroll mediante el mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")
        
        def bind_children(parent):
            parent.bind("<MouseWheel>", _on_mousewheel)
            for child in parent.winfo_children():
                bind_children(child)
        
        bind_children(scrollable_frame)
        canvas.bind("<MouseWheel>", _on_mousewheel)

    def crear_marco_texto(self, frame, texto, fuente, margen=(10, 10)):
        """
        Crea un marco (Frame) con un Label interno.
        Se utiliza wraplength para ajustar el texto y el contenido se ancla a la izquierda.
        """
        marco = tk.Frame(frame, bg="white", bd=2, relief="solid", 
                         padx=20, pady=10, highlightbackground=self.color_borde)
        marco.pack(pady=margen, fill="x", padx=50, anchor="w")
        tk.Label(
            marco, 
            text=texto, 
            wraplength=800, 
            justify="left", 
            anchor="w", 
            font=fuente, 
            fg=self.color_texto, 
            bg="white"
        ).pack(fill="x")
        return marco

    def crear_titulo(self, frame):
        contenedor_titulo = tk.Frame(frame, bg=self.color_fondo)
        contenedor_titulo.pack(pady=20)
        
        # Texto del título centrado
        tk.Label(
            contenedor_titulo, 
            text="Clasificador de Imágenes de Reciclaje (CNN)", 
            font=self.fuente_titulo, 
            fg=self.color_titulo,
            bg=self.color_fondo,
            justify="center", 
            anchor="center"
        ).pack(pady=5, fill="x")

        # Se muestra la imagen del título (centrada)
        try:
            imagen = Image.open("imagenes/logo.png")
            imagen = imagen.resize((120, 120), Image.LANCZOS)
            photo = ImageTk.PhotoImage(imagen)
            tk.Label(contenedor_titulo, image=photo, bg=self.color_fondo).pack(pady=5)
            contenedor_titulo.image = photo  # Evita que la imagen se elimine de memoria
        except Exception as e:
            print(f"Error cargando logo: {e}")

    def crear_descripcion(self, frame):
        marco = tk.Frame(frame, bg=self.color_fondo)
        marco.pack(pady=20, fill="x")

        # Texto descriptivo (alineado a la izquierda)
        texto = (
            "Nuestro proyecto busca contribuir al reciclaje mediante una red neuronal "
            "convolucional capaz de clasificar imágenes en 5 categorías:"
        )
        self.crear_marco_texto(marco, texto, self.fuente_texto)

        # Lista de categorías (alineadas a la izquierda)
        categorias = [
            "⬤ Cartón (Cardboard)",
            "⬤ Vidrio (Glass)",
            "⬤ Metal",
            "⬤ Papel",
            "⬤ Plástico"
        ]

        marco_categorias = tk.Frame(frame, bg=self.color_fondo)
        marco_categorias.pack(pady=10, fill="x")
        for categoria in categorias:
            tk.Label(
                marco_categorias, 
                text=categoria, 
                font=self.fuente_negrita, 
                fg=self.color_texto, 
                bg=self.color_fondo,
                justify="left", 
                anchor="w"
            ).pack(anchor="w", padx=100, fill="x")

        # Texto final del apartado
        texto_final = (
            "El objetivo es que cualquier usuario pueda identificar cómo desechar correctamente "
            "diferentes materiales y obtener información sobre puntos de reciclaje."
        )
        self.crear_marco_texto(frame, texto_final, self.fuente_texto)

    def crear_tabla_contenidos(self, frame):
        marco = self.crear_marco_texto(frame, "Tabla de Contenidos", self.fuente_seccion)
        secciones = [
            "1. Librerías", 
            "2. Extracción de datos", 
            "3. Gráficas",
            "4. Interfaz Gráfica", 
            "5. PDF", 
            "6. Acerca de", 
            "7. Agradecimientos"
        ]
        for seccion in secciones:
            tk.Label(
                marco, 
                text=seccion, 
                font=self.fuente_texto, 
                fg=self.color_texto, 
                bg="white",
                justify="left", 
                anchor="w"
            ).pack(pady=3, anchor="w", fill="x")

    def crear_librerias(self, frame):
        contenido = (
            "Librerías Principales Utilizadas\n\n"
            "Para el modelo CNN:\n"
            "- TensorFlow/Keras\n- OpenCV\n- NumPy\n- Matplotlib\n\n"
            "Para la interfaz gráfica:\n"
            "- Tkinter\n- Pillow (PIL)\n- OS\n- Shutil"
        )
        self.crear_marco_texto(frame, contenido, self.fuente_texto)

    def crear_data(self, frame):
        contenido = (
            "Fuente de Datos\n\n"
            "Dataset de Waste Classification de Kaggle.\n"
            "Enlace al dataset: https://www.kaggle.com/datasets/techsash/waste-classification-data"
        )
        marco = self.crear_marco_texto(frame, contenido, self.fuente_texto)
        enlace = tk.Label(
            marco, 
            text="Abrir enlace", 
            fg="blue", 
            cursor="hand2", 
            font=self.fuente_texto, 
            bg="white",
            justify="left", 
            anchor="w"
        )
        enlace.pack(pady=5, anchor="w", fill="x")
        enlace.bind("<Button-1>", lambda e: webbrowser.open("https://www.kaggle.com/datasets/techsash/waste-classification-data"))

    def crear_interfaz(self, frame):
        contenido = (
            "Funcionalidades de la Interfaz Gráfica del Usuario (GUI)\n\n"
            "- Clasificación de imágenes mediante carga directa o uso de cámara web\n"
            "- Visualización de gráficas de entrenamiento y desempeño del modelo\n"
            "- Información detallada sobre tiempos de degradación de materiales\n"
            "- Guías de reciclaje interactivas\n"
            "- Generación y exportación de reportes en PDF"
        )
        self.crear_marco_texto(frame, contenido, self.fuente_texto)

    def crear_agradecimientos(self, frame):
        contenido = (
            "Agradecimientos Especiales\n\n"
            "Equipo desarrollador:\n"
            "- Julio Zambrano\n- Angel Villegas\n- Andrea Ruiz\n\n"
            "Tutores:\n"
            "- Jenny Remolina\n- Álvaro Arauz\n\n"
            "Agradecimiento especial a Samsung Innovation Campus"
        )
        marco = self.crear_marco_texto(frame, contenido, self.fuente_texto)
        try:
            imagen = Image.open("imagenes/integrantes.png")
            imagen = imagen.resize((800, 400), Image.LANCZOS)
            photo = ImageTk.PhotoImage(imagen)
            tk.Label(frame, image=photo, bg=self.color_fondo).pack(pady=20)
            frame.image = photo
        except Exception as e:
            print(f"Error cargando imagen integrantes: {e}")

    def crear_acerca_de(self, frame):
        # Crear un marco unificado para el logo y el texto
        marco = tk.Frame(frame, bg=self.color_fondo, bd=2, relief="solid", padx=10, pady=10)
        marco.pack(pady=20, fill="x", padx=50)
        
        # Cargar y mostrar el logotipo "light.png" en la columna izquierda del mismo marco
        try:
            imagen = Image.open("imagenes/light.png")
            imagen = imagen.resize((150, 150), Image.LANCZOS)
            photo = ImageTk.PhotoImage(imagen)
            tk.Label(marco, image=photo, bg=self.color_fondo).grid(row=0, column=0, rowspan=2, padx=10, pady=10)
            marco.image = photo  # Conserva la referencia a la imagen
        except Exception as e:
            print(f"Error cargando logo: {e}")
        
        # Definir el contenido de texto
        contenido = (
            "Acerca de Lights of Hope\n\n"
            "Proyectos realizados:\n"
            "- Análisis de desastres naturales\n"
            "- Sistema de clasificación de residuos con IA\n\n"
            "Repositorio GitHub: https://github.com/JulioZambrano91/Lights-of-Hope-IA"
        )
        
        # Mostrar el contenido de texto en la columna derecha
        tk.Label(marco, text=contenido, wraplength=600, justify="left", anchor="w",
                font=self.fuente_texto, fg=self.color_texto, bg="white").grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Agregar el enlace para GitHub debajo del texto
        enlace = tk.Label(marco, text="Visitar GitHub", fg="blue", cursor="hand2", 
                        font=self.fuente_texto, bg="white", justify="left", anchor="w")
        enlace.grid(row=1, column=1, padx=10, pady=(0,10), sticky="w")
        enlace.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/JulioZambrano91/Lights-of-Hope-IA"))

