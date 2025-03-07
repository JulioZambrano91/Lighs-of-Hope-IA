# ============ CORE =============
import os
import sys
import shutil
import json
from collections import deque

# ========== TKINTER ============
import tkinter as tk
from tkinter import (
    ttk,
    font,
    filedialog,
    messagebox
)

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

# ========== FORMULARIOS =========
from formularios.form_inicio_design import FormularioInicioDesign
from formularios.form_sitio_construccion import FormularioSitioConstruccionDesign
from formularios.form_info_design import FormularioInfoDesign
from formularios.form_clasificadorIMG_design import FormularioClasificadorIMGDesign

# ========== INICIALIZACIONES ====
# Para PyInstaller y TensorFlow
try:
    from tensorflow.python.keras.api._v2 import keras
except ImportError:
    from tensorflow import keras
# Fijar semilla para reproducibilidad
np.random.seed(42)
tf.random.set_seed(42)