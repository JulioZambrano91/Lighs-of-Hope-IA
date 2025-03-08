from imports import tk, Image, ImageTk, font
import webbrowser

class FormularioInicioDesign():
    def __init__(self, panel_principal):
        self.fuente_titulo = ("Montserrat", 22, "bold")
        self.fuente_seccion = ("Open Sans", 18, "bold")
        self.fuente_texto = ("Open Sans", 16)
        self.fuente_negrita = font.Font(family="Open Sans", size=14, weight="bold")
        self.color_titulo = "#3498DB"  # Azul claro para los títulos
        self.color_seccion = "#2C3E50"  # Negro para los subtítulos
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
        self.crear_por_que_reciclar(scrollable_frame) 
        self.crear_que_podemos_reciclar(scrollable_frame)
        self.crear_donde_reciclar(scrollable_frame)# Añadir nueva sección
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
        
        tk.Label(
            contenedor_titulo, 
            text="Clasificador de Imágenes de Reciclaje (CNN)", 
            font=self.fuente_titulo, 
            fg=self.color_titulo,
            bg=self.color_fondo,
            justify="center", 
            anchor="center"
        ).pack(pady=5, fill="x")

        try:
            imagen = Image.open("imagenes/logo.png")
            imagen = imagen.resize((120, 120), Image.LANCZOS)
            photo = ImageTk.PhotoImage(imagen)
            tk.Label(contenedor_titulo, image=photo, bg=self.color_fondo).pack(pady=5)
            contenedor_titulo.image = photo
        except Exception as e:
            print(f"Error cargando logo: {e}")

    def crear_descripcion(self, frame):
        marco = tk.Frame(frame, bg=self.color_fondo)
        marco.pack(pady=20, fill="x")

        texto = (
            "Nuestro proyecto busca contribuir al reciclaje mediante una red neuronal "
            "convolucional capaz de clasificar imágenes en 5 categorías:"
        )
        self.crear_marco_texto(marco, texto, self.fuente_texto)

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

        texto_final = (
            "El objetivo es que cualquier usuario pueda identificar cómo desechar correctamente "
            "diferentes materiales y obtener información sobre puntos de reciclaje."
        )
        self.crear_marco_texto(frame, texto_final, self.fuente_texto)

    def crear_por_que_reciclar(self, frame):
        contenedor_por_que = tk.Frame(frame, bg=self.color_fondo)
        contenedor_por_que.pack(pady=20, fill="x")

        # Título en azul claro, centrado
        tk.Label(
            contenedor_por_que, 
            text="¿Por qué Reciclar?", 
            font=self.fuente_titulo, 
            fg=self.color_titulo,
            bg=self.color_fondo,
            justify="center", 
            anchor="center"
        ).pack(pady=5, fill="x")

        contenido = (
            "Reciclar es esencial para reducir la cantidad de residuos que terminan en los vertederos, lo cual ayuda a disminuir "
            "la emisión de gases de efecto invernadero como el metano. Además, al reciclar conservamos recursos naturales limitados, "
            "como árboles, agua, y energía. Por ejemplo, reciclar aluminio ahorra hasta un 95% de la energía comparado con la producción "
            "de aluminio nuevo. Cada vez que reciclamos, contribuimos a proteger el medio ambiente y a conservar los recursos para futuras generaciones."
        )
        self.crear_marco_texto(contenedor_por_que, contenido, self.fuente_texto)

    def crear_que_podemos_reciclar(self, frame):
        contenedor_que = tk.Frame(frame, bg=self.color_fondo)
        contenedor_que.pack(pady=20, fill="x")

        # Título en azul claro, centrado
        tk.Label(
            contenedor_que, 
            text="¿Qué Podemos Reciclar?", 
            font=self.fuente_titulo, 
            fg=self.color_titulo,
            bg=self.color_fondo,
            justify="center", 
            anchor="center"
        ).pack(pady=5, fill="x")

        # Función para crear párrafos con subtítulos, contenido e imágenes
        def crear_parrafo_con_imagen(frame, subtitulo, contenido, imagen_path, tamaño_imagen=(600, 300)):
            marco = tk.Frame(frame, bg="white", bd=2, relief="solid", 
                             padx=20, pady=10, highlightbackground=self.color_borde)
            marco.pack(pady=(10, 10), fill="x", padx=50, anchor="w")
            tk.Label(
                marco, 
                text=subtitulo, 
                font=self.fuente_negrita, 
                fg=self.color_texto, 
                bg="white", 
                anchor="w"
            ).pack(fill="x")
            tk.Label(
                marco, 
                text=contenido, 
                font=self.fuente_texto, 
                fg=self.color_texto, 
                bg="white", 
                wraplength=800, 
                justify="left", 
                anchor="w"
            ).pack(fill="x")
            try:
                imagen = Image.open(imagen_path)
                imagen = imagen.resize(tamaño_imagen, Image.LANCZOS)
                photo = ImageTk.PhotoImage(imagen)
                tk.Label(marco, image=photo, bg="white").pack(pady=10)
                marco.image = photo  # Mantener una referencia de la imagen para evitar que sea recolectada por el garbage collector
            except Exception as e:
                print(f"Error cargando imagen: {e}")
            return marco

        subtitulo_papel = "Papel y Cartón"
        contenido_papel = (
            "El papel y cartón representan una gran parte de los residuos domésticos. Reciclando papel usado como periódicos, revistas, cuadernos y cajas de cartón, "
            "se puede reducir considerablemente la deforestación y el consumo de agua. Además, el papel reciclado puede convertirse en nuevos productos como papel higiénico, "
            "papel de impresión y embalajes."
        )
        crear_parrafo_con_imagen(contenedor_que, subtitulo_papel, contenido_papel, "imagenes/Papel_Caton.jpg")

        subtitulo_plastico = "Plásticos"
        contenido_plastico = (
            "Los plásticos son una de las mayores amenazas para el medio ambiente debido a su lenta descomposición. Botellas, envases, bolsas y otros plásticos pueden reciclarse "
            "para fabricar nuevos productos como fibras textiles, materiales de construcción y nuevos envases. Es importante limpiar los plásticos antes de reciclarlos para asegurar "
            "su correcta reutilización."
        )
        crear_parrafo_con_imagen(contenedor_que, subtitulo_plastico, contenido_plastico, "imagenes/plastico.jpg")

        subtitulo_vidrio = "Vidrio"
        contenido_vidrio = (
            "El vidrio es 100% reciclable y puede reciclarse una y otra vez sin perder su calidad. Botellas, frascos y recipientes de vidrio se pueden convertir en nuevos productos de vidrio, "
            "reduciendo la necesidad de extraer materias primas como la arena. Además, el reciclaje de vidrio consume menos energía que la producción de vidrio nuevo."
        )
        crear_parrafo_con_imagen(contenedor_que, subtitulo_vidrio, contenido_vidrio, "imagenes/vidrio.jpeg")

        subtitulo_metales = "Metales"
        contenido_metales = (
            "Los metales como el aluminio y el acero son altamente reciclables. Latas de aluminio, latas de comida y otros objetos metálicos pueden fundirse y reutilizarse para fabricar nuevos productos. "
            "El reciclaje de metales no solo ahorra recursos naturales sino que también requiere menos energía que la extracción y procesamiento de minerales vírgenes."
        )
        crear_parrafo_con_imagen(contenedor_que, subtitulo_metales, contenido_metales, "imagenes/Metales.jpeg")

    def crear_donde_reciclar(self, frame):
        # Título en azul claro, centrado
        tk.Label(
            frame, 
            text="¿Dónde Reciclar?", 
            font=self.fuente_titulo, 
            fg=self.color_titulo,
            bg=self.color_fondo,
            justify="center", 
            anchor="center"
        ).pack(pady=5, fill="x")

        # Contenido con imagen en un solo marco
        marco = tk.Frame(frame, bg="white", bd=2, relief="solid", 
                         padx=20, pady=10, highlightbackground=self.color_borde)
        marco.pack(pady=(10, 10), fill="x", padx=50, anchor="w")

        # Agregar imagen al marco
        try:
            imagen = Image.open("imagenes/reciclaje.jpg")
            imagen = imagen.resize((600, 400), Image.LANCZOS)
            photo = ImageTk.PhotoImage(imagen)
            tk.Label(marco, image=photo, bg="white").pack(pady=10)
            marco.image = photo  # Mantener una referencia de la imagen para evitar que sea recolectada por el garbage collector
        except Exception as e:
            print(f"Error cargando imagen: {e}")


    def crear_librerias(self, frame):
        # Título en azul claro, centrado
        tk.Label(
            frame, 
            text="Herramientas del proyecto", 
            font=self.fuente_titulo, 
            fg=self.color_titulo,
            bg=self.color_fondo,
            justify="center", 
            anchor="center"
        ).pack(pady=5, fill="x")

        # Contenido con subtítulos en un solo marco
        marco = tk.Frame(frame, bg="white", bd=2, relief="solid", 
                         padx=20, pady=10, highlightbackground=self.color_borde)
        marco.pack(pady=(10, 10), fill="x", padx=50, anchor="w")
        
        def agregar_parrafo(marco, subtitulo, contenido):
            tk.Label(
                marco, 
                text=subtitulo, 
                font=self.fuente_negrita, 
                fg=self.color_texto, 
                bg="white", 
                anchor="w"
            ).pack(fill="x", pady=(0, 5))
            tk.Label(
                marco, 
                text=contenido, 
                font=self.fuente_texto, 
                fg=self.color_texto, 
                bg="white", 
                wraplength=800, 
                justify="left", 
                anchor="w"
            ).pack(fill="x", pady=(0, 10))

        subtitulo_modelo_cnn = "Para el modelo CNN:"
        contenido_modelo_cnn = "- TensorFlow/Keras\n- OpenCV\n- NumPy\n- Matplotlib"
        agregar_parrafo(marco, subtitulo_modelo_cnn, contenido_modelo_cnn)

        subtitulo_interfaz_grafica = "Para la interfaz gráfica:"
        contenido_interfaz_grafica = "- Tkinter\n- Pillow (PIL)\n- OS\n- Shutil"
        agregar_parrafo(marco, subtitulo_interfaz_grafica, contenido_interfaz_grafica)

        # Agregar imagen al marco
        try:
            imagen = Image.open("imagenes/herramientas.png")
            imagen = imagen.resize((600, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(imagen)
            tk.Label(marco, image=photo, bg="white").pack(pady=10)
            marco.image = photo  # Mantener una referencia de la imagen para evitar que sea recolectada por el garbage collector
        except Exception as e:
            print(f"Error cargando imagen: {e}")     

    def crear_data(self, frame):
        # Título en azul claro, centrado
        tk.Label(
            frame, 
            text="Fuente de Datos", 
            font=self.fuente_titulo, 
            fg=self.color_titulo,
            bg=self.color_fondo,
            justify="center", 
            anchor="center"
        ).pack(pady=5, fill="x")

        # Contenido con subtítulos en un solo marco
        marco = tk.Frame(frame, bg="white", bd=2, relief="solid", 
                         padx=20, pady=10, highlightbackground=self.color_borde)
        marco.pack(pady=(10, 10), fill="x", padx=50, anchor="w")
        
        contenido_data = (
            "Dataset de Waste Classification de Kaggle.\n"
            "Enlace al dataset: https://www.kaggle.com/datasets/techsash/waste-classification-data"
        )
        tk.Label(
            marco, 
            text=contenido_data, 
            font=self.fuente_texto, 
            fg=self.color_texto, 
            bg="white", 
            wraplength=800, 
            justify="left", 
            anchor="w"
        ).pack(fill="x", pady=(0, 10))
        
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
        # Título en azul claro, centrado
        tk.Label(
            frame, 
            text="Funcionalidades de la Interfaz Gráfica del Usuario (GUI)", 
            font=self.fuente_titulo, 
            fg=self.color_titulo,
            bg=self.color_fondo,
            justify="center", 
            anchor="center"
        ).pack(pady=5, fill="x")

        # Contenido con subtítulos en un solo marco
        marco = tk.Frame(frame, bg="white", bd=2, relief="solid", 
                         padx=20, pady=10, highlightbackground=self.color_borde)
        marco.pack(pady=(10, 10), fill="x", padx=50, anchor="w")
        
        contenido_interfaz = (
            "- Clasificación de imágenes mediante carga directa o uso de cámara web\n"
            "- Visualización de gráficas de entrenamiento y desempeño del modelo\n"
            "- Información detallada sobre tiempos de degradación de materiales\n"
            "- Guías de reciclaje interactivas\n"
            "- Generación y exportación de reportes en PDF"
        )
        tk.Label(
            marco, 
            text=contenido_interfaz, 
            font=self.fuente_texto, 
            fg=self.color_texto, 
            bg="white", 
            wraplength=800, 
            justify="left", 
            anchor="w"
        ).pack(fill="x", pady=(0, 10))
        

    def crear_agradecimientos(self, frame):
        # Título en azul claro, centrado
        tk.Label(
            frame, 
            text="Agradecimientos Especiales", 
            font=self.fuente_titulo, 
            fg=self.color_titulo,
            bg=self.color_fondo,
            justify="center", 
            anchor="center"
        ).pack(pady=5, fill="x")

        # Contenido con subtítulos en un solo marco
        marco = tk.Frame(frame, bg="white", bd=2, relief="solid", 
                         padx=20, pady=10, highlightbackground=self.color_borde)
        marco.pack(pady=(10, 10), fill="x", padx=50, anchor="w")

        subtitulo_tutores = "Tutores:"
        contenido_tutores = "- Jenny Remolina\n- Álvaro Arauz"
        subtitulo_agradecimiento = "Agradecimiento especial a Samsung Innovation Campus"

        tk.Label(
            marco, 
            text=subtitulo_tutores, 
            font=self.fuente_negrita, 
            fg=self.color_texto, 
            bg="white", 
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        tk.Label(
            marco, 
            text=contenido_tutores, 
            font=self.fuente_texto, 
            fg=self.color_texto, 
            bg="white", 
            wraplength=800, 
            justify="left", 
            anchor="w"
        ).pack(fill="x", pady=(0, 10))
        tk.Label(
            marco, 
            text=subtitulo_agradecimiento, 
            font=self.fuente_texto, 
            fg=self.color_texto, 
            bg="white", 
            wraplength=800, 
            justify="left", 
            anchor="w"
        ).pack(fill="x", pady=(0, 10))
        
    def crear_acerca_de(self, frame):
    # Título en azul claro, centrado
        tk.Label(
            frame, 
            text="Lights of Hope", 
            font=self.fuente_titulo, 
            fg=self.color_titulo,
            bg=self.color_fondo,
            justify="center", 
            anchor="center"
        ).pack(pady=5, fill="x")

        # Contenido con subtítulos y la imagen en un solo marco
        marco = tk.Frame(frame, bg="white", bd=2, relief="solid", 
                     padx=20, pady=10, highlightbackground=self.color_borde)
        marco.pack(pady=(10, 10), fill="x", padx=50, anchor="w")

        contenedor_texto_imagen = tk.Frame(marco, bg="white")
        contenedor_texto_imagen.pack(fill="x")

        contenedor_texto = tk.Frame(contenedor_texto_imagen, bg="white")
        contenedor_texto.pack(side="left", fill="both", expand=True)

        subtitulo_acerca_de = "Acerca de Lights of Hope"
        contenido_acerca_de = (
            "Proyectos realizados:\n"
            "- Análisis de desastres naturales\n"
            "- Sistema de clasificación de residuos con IA"
        )
        enlace_github = "Repositorio GitHub: https://github.com/JulioZambrano91/Lights-of-Hope-IA"

        tk.Label(
            contenedor_texto, 
            text=subtitulo_acerca_de, 
            font=self.fuente_negrita, 
            fg=self.color_texto, 
            bg="white", 
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        tk.Label(
            contenedor_texto, 
            text=contenido_acerca_de, 
            font=self.fuente_texto, 
            fg=self.color_texto, 
            bg="white", 
            wraplength=400, 
            justify="left", 
            anchor="w"
        ).pack(fill="x", pady=(0, 10))
        tk.Label(
            contenedor_texto, 
            text=enlace_github, 
            font=self.fuente_texto, 
            fg=self.color_texto, 
            bg="white", 
            wraplength=400, 
            justify="left", 
            anchor="w"
        ).pack(fill="x", pady=(0, 10))

        # Agregar imagen al marco
        contenedor_imagen = tk.Frame(contenedor_texto_imagen, bg="white")
        contenedor_imagen.pack(side="right", padx=10, pady=10)

        try:
            imagen = Image.open("imagenes/light.png")
            imagen = imagen.resize((150, 150), Image.LANCZOS)
            photo = ImageTk.PhotoImage(imagen)
            tk.Label(contenedor_imagen, image=photo, bg="white").pack(pady=10)
            marco.image = photo  # Mantener una referencia de la imagen para evitar que sea recolectada por el garbage collector
        except Exception as e:
            print(f"Error cargando imagen: {e}")

        # Enlace clickable
        enlace = tk.Label(contenedor_texto, text="Visitar GitHub", fg="blue", cursor="hand2", 
                    font=self.fuente_texto, bg="white", justify="left", anchor="w")
        enlace.pack(pady=5, anchor="w", fill="x")
        enlace.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/JulioZambrano91/Lights-of-Hope-IA"))

