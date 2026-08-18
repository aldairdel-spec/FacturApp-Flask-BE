import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError(
        "La variable de entorno SECRET_KEY no está configurada. "
        "Crea un archivo .env en la raíz del proyecto con: SECRET_KEY=tu-clave-aqui"
    )
