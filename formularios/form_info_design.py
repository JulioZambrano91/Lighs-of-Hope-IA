from imports import tk, util_ventana


class FormularioInfoDesign(tk.Toplevel):

    def __init__(self) -> None:
        super().__init__()
        self.config_window()
        self.contruirWidget()

    def config_window(self):
        # Configuración inicial de la ventana
        self.title('About us: Lights of Hope')
        self.iconbitmap("./imagenes/logo.ico")
        w, h = 700, 300        
        util_ventana.centrar_ventana(self, w, h)     
    
    def contruirWidget(self):         
        self.labelVersion = tk.Label(self, text="Version GUI: 1.2")
        self.labelVersion.config(fg="#000000", font=("Roboto", 15), pady=30, width=30)
        self.labelVersion.pack()

        self.labelVersionClasificador = tk.Label(self, text="Version Clasificador: 3.0")
        self.labelVersionClasificador.config(fg="#000000", font=(
            "Roboto", 15), pady=30, width=30)
        self.labelVersionClasificador.pack()

        self.labelAutor = tk.Label(self, text="Autores:\nJulio Zambrano, Andrea Ruiz, Angel Villegas")
        self.labelAutor.config(fg="#000000", font=(
            "Roboto", 15), pady=70, width=50)
        self.labelAutor.pack()