import tkinter as tk
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


def iniciar_aplicacion():
    servicio = RestauranteServicio()
    root = tk.Tk()

    def abrir_main_view(usuario):
        root.withdraw()
        ventana = tk.Toplevel(root)
        MainView(ventana, servicio, usuario, on_logout=lambda: cerrar_sesion(root, ventana))

    LoginView(root, servicio, abrir_main_view)
    root.mainloop()


def cerrar_sesion(root, ventana):
    ventana.destroy()
    root.deiconify()


if __name__ == "__main__":
    iniciar_aplicacion()
