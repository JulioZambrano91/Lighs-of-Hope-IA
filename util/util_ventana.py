def centrar_ventana(ventana, aplicacion_ancho, aplicacion_largo):
    try:
        print("Centrando ventana...")
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_largo = ventana.winfo_screenheight()
        print(f"Dimensiones de la pantalla: ancho={pantalla_ancho}, largo={pantalla_largo}")
        x = int((pantalla_ancho / 2) - (aplicacion_ancho / 2))
        y = int((pantalla_largo / 2) - (aplicacion_largo / 2))
        ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")
        print("Ventana centrada correctamente.")
    except Exception as e:
        print(f"Error al centrar ventana: {e}")

