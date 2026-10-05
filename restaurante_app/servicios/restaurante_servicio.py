from pathlib import Path
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import cargar_datos, guardar_datos


class RestauranteServicio:
    def __init__(self):
        self.ruta_base = Path(__file__).resolve().parent.parent / "datos"
        self.productos = []
        self.usuarios = []
        self.ventas = []

        # Índices para búsquedas rápidas con diccionarios.
        self.indice_productos = {}
        self.indice_usuarios = {}
        self.indice_ventas_usuario = {}

        self.cargar_datos()
        self.reconstruir_indices()

    def cargar_datos(self):
        productos = cargar_datos(self.ruta_base / "productos.json")
        usuarios = cargar_datos(self.ruta_base / "usuarios.json")
        ventas = cargar_datos(self.ruta_base / "ventas.json")

        self.productos = [
            Producto(p["codigo"], p["nombre"], p["precio"], p["stock"])
            for p in productos
        ]

        self.usuarios = [
            Usuario(
                u["identificacion"],
                u["nombre"],
                u.get("rol", "Cliente"),
                u.get("contrasena", "")
            )
            for u in usuarios
        ]

        self.ventas = [
            Venta(v["usuario_id"], v["codigo_producto"], v["cantidad"])
            for v in ventas
        ]

    def guardar_datos(self):
        guardar_datos(
            self.ruta_base / "productos.json",
            [p.to_dict() for p in self.productos]
        )
        guardar_datos(
            self.ruta_base / "usuarios.json",
            [u.to_dict() for u in self.usuarios]
        )
        guardar_datos(
            self.ruta_base / "ventas.json",
            [v.to_dict() for v in self.ventas]
        )

    def reconstruir_indices(self):
        self.indice_productos = {p.codigo: p for p in self.productos}
        self.indice_usuarios = {u.identificacion: u for u in self.usuarios}
        self.indice_ventas_usuario = {}

        for venta in self.ventas:
            self.indice_ventas_usuario.setdefault(venta.usuario_id, []).append(venta)

    # ---------- Usuarios ----------
    def listar_usuarios(self):
        return list(self.usuarios)

    def consultar_usuario(self, identificacion):
        return self.indice_usuarios.get(str(identificacion))

    def registrar_usuario(self, usuario):
        if self.consultar_usuario(usuario.identificacion):
            raise ValueError("Ya existe un usuario con esa identificación.")
        self.usuarios.append(usuario)
        self.indice_usuarios[usuario.identificacion] = usuario
        self.guardar_datos()

    def actualizar_usuario(self, usuario):
        existente = self.consultar_usuario(usuario.identificacion)
        if existente is None:
            raise ValueError("El usuario no existe.")

        existente.nombre = usuario.nombre
        existente.rol = usuario.rol
        existente.contrasena = usuario.contrasena
        self.guardar_datos()

    def eliminar_usuario(self, identificacion):
        identificacion = str(identificacion)
        usuario = self.consultar_usuario(identificacion)
        if usuario is None:
            raise ValueError("El usuario no existe.")

        self.usuarios.remove(usuario)
        self.indice_usuarios.pop(identificacion, None)
        self.guardar_datos()

    def autenticar_usuario(self, identificacion, contrasena):
        usuario = self.consultar_usuario(identificacion)
        if usuario and usuario.contrasena == contrasena:
            return usuario
        return None

    # ---------- Productos ----------
    def listar_productos(self):
        return list(self.productos)

    def consultar_producto(self, codigo):
        return self.indice_productos.get(str(codigo))

    def registrar_producto(self, producto):
        if self.consultar_producto(producto.codigo):
            raise ValueError("Ya existe un producto con ese código.")
        self.productos.append(producto)
        self.indice_productos[producto.codigo] = producto
        self.guardar_datos()

    def actualizar_producto(self, producto):
        existente = self.consultar_producto(producto.codigo)
        if existente is None:
            raise ValueError("El producto no existe.")
        existente.nombre = producto.nombre
        existente.precio = producto.precio
        existente.stock = producto.stock
        self.guardar_datos()

    def eliminar_producto(self, codigo):
        producto = self.consultar_producto(codigo)
        if producto is None:
            raise ValueError("El producto no existe.")
        self.productos.remove(producto)
        self.indice_productos.pop(str(codigo), None)
        self.guardar_datos()

    # ---------- Ventas ----------
    def listar_ventas_usuario(self, identificacion):
        return self.indice_ventas_usuario.get(str(identificacion), [])

    def registrar_venta(self, venta):
        producto = self.consultar_producto(venta.codigo_producto)
        if producto is None:
            raise ValueError("El producto no existe.")
        if venta.cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        if producto.stock < venta.cantidad:
            raise ValueError("No hay suficiente stock.")

        producto.stock -= venta.cantidad
        self.ventas.append(venta)
        self.indice_ventas_usuario.setdefault(venta.usuario_id, []).append(venta)
        self.guardar_datos()
