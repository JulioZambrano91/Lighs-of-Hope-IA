from imports import (
    tk, font, webbrowser,
    COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL,
    COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA,
    util_ventana, util_img, resource_path,
    FormularioInicioDesign, FormularioSitioConstruccionDesign,
    FormularioInfoDesign, FormularioClasificadorIMGDesign,
    FormularioProyectoDesign, Image, ImageTk
)

class FormularioMaestroDesign(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config_window()
        self.cargar_imagenes()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.controles_cuerpo()  

    def cargar_imagenes(self):
        try:
            self.logo = util_img.leer_imagen(resource_path("./imagenes/Perfil.png"), (500, 136))
            self.perfil = util_img.leer_imagen(resource_path("./imagenes/logo.ico"), (100, 100))  # Asegurar que existe
            self.img_sitio_construccion = util_img.leer_imagen(resource_path("./imagenes/sitio_construccion.jpg"), (200, 200))
        except Exception as e:
            print(f"Error crítico al cargar imágenes: {e}")
            sys.exit(1)  # Detener ejecución si fallan imágenes esenciales

    def config_window(self):
        self.title('Clasificador de Residuos')
        self.iconbitmap(resource_path("./imagenes/logo.ico"))
        w, h = 1280, 720
        util_ventana.centrar_ventana(self, w, h)

    def paneles(self):
        self.barra_superior = tk.Frame(self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')
        
        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)
        
        self.cuerpo_principal = tk.Frame(self, bg=COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def controles_barra_superior(self):
        font_awesome = font.Font(family='FontAwesome', size=12)
        self.labelTitulo = tk.Label(self.barra_superior, text="Lights of Hope")
        self.labelTitulo.config(fg="#fff", font=("Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        self.buttonMenuLateral = tk.Button(self.barra_superior, text="\uf0c9", font=font_awesome,
                                         command=self.toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT)

        self.labelInfo = tk.Label(self.barra_superior, text="SAMSUNG INNOVATION CAMPUS (SIC)")
        self.labelInfo.config(fg="#fff", font=("Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=25, width=25)
        self.labelInfo.pack(side=tk.RIGHT)

    def controles_cuerpo(self):
        """Configura los elementos del cuerpo principal"""
        try:
            label = tk.Label(
                self.cuerpo_principal, 
                image=self.logo, 
                bg=COLOR_CUERPO_PRINCIPAL
            )
            label.place(x=0, y=0, relwidth=1, relheight=1)
        except AttributeError as e:
            print(f"Error al cargar imagen en cuerpo principal: {e}")

    def controles_menu_lateral(self):
        ancho_menu = 20
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)

        self.labelPerfil = tk.Label(self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side=tk.TOP, pady=10)

        self.buttonDashBoard = tk.Button(self.menu_lateral)
        self.buttonProfile = tk.Button(self.menu_lateral)
        self.buttonPicture = tk.Button(self.menu_lateral)
        self.buttonInfo = tk.Button(self.menu_lateral)
        self.buttonSettings = tk.Button(self.menu_lateral)

        buttons_info = [
            ("Inicio", "\uf015", self.buttonDashBoard, self.abrir_panel_graficas),
            ("Datos del proyecto", "\uf007", self.buttonProfile, self.abrir_panel_proyecto),
            ("Clasificador de Imagenes", "\uf302", self.buttonPicture, self.abrir_panel_clasificadorIMG),
            ("Clasificador en vivo", "\uf030", self.buttonInfo, self.abrir_panel_info),
            ("About us", "\uf013", self.buttonSettings, self.abrir_about_us)
        ]

        for text, icon, button, comando in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu, comando)

    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu, comando):
        button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome, bd=0, 
                     bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu, command=comando)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button):
        button.config(bg=COLOR_MENU_LATERAL, fg='white')

    def toggle_panel(self):
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')

    def abrir_panel_graficas(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioInicioDesign(self.cuerpo_principal)

    def abrir_about_us(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioInfoDesign()

    def abrir_panel_proyecto(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioProyectoDesign(self.cuerpo_principal)

    def abrir_panel_info(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioSitioConstruccionDesign(self.cuerpo_principal, self.img_sitio_construccion)
        
    def abrir_panel_clasificadorIMG(self):
        self.limpiar_panel(self.cuerpo_principal)
        container = tk.Frame(self.cuerpo_principal)
        container.pack(fill="both", expand=True)
        FormularioClasificadorIMGDesign(container)

    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = FormularioMaestroDesign()
    app.mainloop()