import json
from pathlib import Path


def cargar_datos(ruta):
    archivo = Path(ruta)
    if not archivo.exists():
        return []
    try:
        with archivo.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def guardar_datos(ruta, datos):
    archivo = Path(ruta)
    archivo.parent.mkdir(parents=True, exist_ok=True)
    with archivo.open("w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
