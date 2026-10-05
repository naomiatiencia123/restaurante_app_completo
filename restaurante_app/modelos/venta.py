class Venta:
    def __init__(self, usuario_id, codigo_producto, cantidad):
        self.usuario_id = str(usuario_id)
        self.codigo_producto = str(codigo_producto)
        self.cantidad = int(cantidad)

    def to_dict(self):
        return {
            "usuario_id": self.usuario_id,
            "codigo_producto": self.codigo_producto,
            "cantidad": self.cantidad
        }
