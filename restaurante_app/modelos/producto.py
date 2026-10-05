class Producto:
    def __init__(self, codigo, nombre, precio, stock):
        self.codigo = str(codigo)
        self.nombre = str(nombre)
        self.precio = float(precio)
        self.stock = int(stock)

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock
        }
