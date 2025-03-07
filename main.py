from formularios.form_maestro_design import FormularioMaestroDesign, resource_path

app = FormularioMaestroDesign()
app.iconbitmap(resource_path("./imagenes/logo.ico")) 
app.mainloop()
print("Fin de la ejecución.")