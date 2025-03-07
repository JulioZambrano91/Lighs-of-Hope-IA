# Proyecto: Clasificador de Imagenes de reciclaje (CNN)

Nuestro proyecto esta basado en la idea del reciclaje, ¿Como podemos aportar a este mundo?, ¿Como podemos crear algo de conciencia sobre este tema? Son preguntas que son dificiles de responder, por que a lo largo de la historia han habido miles de personas luchando contra esta conciencia, nosotros no venimos a cambiar esta realidad, pero podemos aportar un grano de arena. En este proyecto entrenamos una red neuronal convolucional capaz de detectar imagenes, estas imagenesson clasificadas en 5 categorias principales, estas son: cardboard (cartón), glass (vidrio), metal (metales), paper (papel) y Plastic (plastico). Con esta red convolucional lo que queremos lograr es que un usuario comun y corriente pueda subir una foto de cualquier tipo de basura, el modelo se lo dectecte y este le de informacion sencilla y basica de comprender acerca de como se puede desechar ese modelo o reciclarlo en las papeleras mas cercanas. Nuestra idea no es revolucionar el mercado, es simplemente que un usuario comun y corriente pase un buen rato y que aprenda algo util.

## Tabla de contenido:
1. [Librerias](#Librerias)
2. [Extraccion de la data](#Data)
3. [Graficas](#Graficas)
4. [Interfaz Grafica](#Interfaz_Grafica)
5. [PDF](#PDF)
6. [Acerca de](#Acerca_de)
7. [Agradecimientos](#Agradecimientos)

## Librerias:
> [!IMPORTANT]
> Es importante verificar si las librerias estan instaladas en su equipo. Todas las librerias usadas se encuentran en imports.py

Estas son las librerias que usamos para la creacion de nuestro proyecto.

**Modelo CNN**:

* Google.colab (Solo para entrenar el modelo)
* OS
* numpy
* matplotlib
* tensorflow
* sklearn.metrics
* cv2
* glob

**Interfaz Grafica**:

* tkinter
* PIL (Pillow)
* numpy
* OS
* tensorflow
* shutil


## Data:

Nuestra data fue extraida desde [aqui.](https://www.kaggle.com/datasets/techsash/waste-classification-data)

Detalles del manejo de la data y entrenamiento del modelo: [Jupyter]

Mas detalle del manejo de nuestra data se encuentra en este PDF: [PDF]


## Interfaz Grafica:

En nuestra interfaz grafica podras conocer mas detalle acerca del reciclaje, informacion sencilla de digerir y intuitiva, tambien encontrara detalles mas tecnicos como graficas de perdida de valor y un clasificador de reporte final. Pero la funcion principal que hace nuestra interfaz grafica es poder interactuar con nuestro modelo entrenado, podras subir imagenes y este te la clasificara en una categoria, te dara informacion util de sobre el tiempo de vida de ese tipo de elementos y como reciclarlo, a la ves podras prender tu camara y nuestro modelo sera capaz de detectar el material que estas sosteniendo y darte esa misma informacion sin la tediosa tarea de subir una imagen manualmente.

> [!IMPORTANT]
>Para ejecutar la interfaz grafica es solo necesario abrir y ejecutar el archivo: main.py

## Agradecimientos

Este proyecto fue creado por: Julio Zambrano, Angel Villegas y Andrea Ruiz. Junto a la constante ayuda de nuestro tutores: Jenny Remolina y Alvaro Arauz.

Desde Lights of Hope le agradecemos de todo corazon su constante ayuda y enseñanza a lo largo de estos 6 meses del curso, junto al equipo de Samsung Innovation Campus por hacer esto posible. 

## Acerca de: Lights Of Hope 

![Light_of_Hope_logo](https://github.com/user-attachments/assets/b01e8d97-32d6-4e93-b57a-370c48492a4a)

Somos un equipo de actualmente tres personas, conformados por: Julio Zambrano, Angel Villegas y Andrea Ruiz. Creamos este nombre para conformar nuestro equipo y hacer nuestros proyectos en Samsung Innovation Campus (SIC).

> [!NOTE]
> Mencion honorifica: A nuestros compañeros Jose Villalobos y Rodolfo Rodriguez por aportar a la creacion de este nombre y primer proyecto hecho.

### Proyectos realizados:

[Analisis de desastres naturales: Tendencias, Patrones y Correlacion](https://github.com/JulioZambrano91/Lights-of-Hope)

# Fin.
