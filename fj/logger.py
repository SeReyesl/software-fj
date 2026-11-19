# logger.py
# Guarda eventos y fallos en archivo, sin meter base de datos.

import logging
import os

# Crea la carpeta logs si aun no esta ahi; asi no revienta al escribir.
os.makedirs("logs", exist_ok=True)

# Deja listo el archivo, el nivel desde donde anota, la hora y la codificacion.
logging.basicConfig(
    filename="logs/sistema.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)

# Instancia que importo en los demas archivos del grupo.
logger = logging.getLogger("SoftwareFJ")