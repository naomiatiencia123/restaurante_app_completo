# restaurante_app

Aplicación de escritorio para la gestión básica de un restaurante, desarrollada en Python con programación orientada a objetos y Tkinter.

## Características

- Inicio de sesión con identificación y contraseña.
- Gestión CRUD de usuarios.
- Gestión CRUD de productos.
- Registro de ventas.
- Persistencia de información mediante archivos JSON.
- Arquitectura modular separando modelos, servicios e interfaz gráfica.
- Uso de diccionarios como índices para acelerar búsquedas por identificación y código.
- Manejo de eventos de Tkinter mediante botones, selección de tablas, Enter y cierre de ventana.

## Estructura

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md
```

## Requisitos

- Python 3.10 o superior.
- Tkinter, incluido normalmente con Python en Windows.

## Ejecución

Desde la carpeta raíz:

```bash
python main.py
```

## Usuarios de prueba

| Identificación | Contraseña | Rol |
|---|---|---|
| admin | 1234 | Administrador |
| empleado | 1234 | Empleado |
| cliente | 1234 | Cliente |

## GitHub

```bash
git init
git add .
git commit -m "Proyecto restaurante_app completo"
git branch -M main
git remote add origin TU_REPOSITORIO
git push -u origin main
```
