class Usuario:
    def __init__(self, identificacion, nombre, rol="Cliente", contrasena=""):
        self.identificacion = str(identificacion)
        self.nombre = str(nombre)
        self.rol = str(rol)
        self.contrasena = str(contrasena)

    def to_dict(self):
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "rol": self.rol,
            "contrasena": self.contrasena
        }
