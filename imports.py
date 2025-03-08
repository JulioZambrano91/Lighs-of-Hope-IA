# Elimina la función resource_path de aquí
# ============ CORE =============
import os
import sys
import shutil
import json
from collections import deque

# ========== TKINTER ============
import tkinter as tk
from tkinter import (
    ttk, font, filedialog, messagebox,
    Scrollbar, Canvas
)
import webbrowser

# ========== DATA SCIENCE ========
import numpy as np
import tensorflow as tf
from PIL import Image, ImageTk

# ========== CUSTOM MODULES ======
from config import (
    COLOR_BARRA_SUPERIOR,
    COLOR_MENU_LATERAL,
    COLOR_CUERPO_PRINCIPAL,
    COLOR_MENU_CURSOR_ENCIMA
)
import util.util_ventana as util_ventana
import util.util_imagenes as util_img
from util.utils import resource_path  

# ========== FORMULARIOS =========
# Mantén estas importaciones al final
from formularios.form_inicio_design import FormularioInicioDesign
from formularios.form_sitio_construccion import FormularioSitioConstruccionDesign
from formularios.form_info_design import FormularioInfoDesign
from formularios.form_clasificadorIMG_design import FormularioClasificadorIMGDesign
from formularios.form_proyecto_design import FormularioProyectoDesign