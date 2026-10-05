import tkinter as tk
from tkinter import ttk, messagebox


class LoginView:
    def __init__(self, root, servicio, on_login):
        self.root = root
        self.servicio = servicio
        self.on_login = on_login

        self.root.title("Restaurante App - Inicio de Sesión")
        self.root.geometry("430x300")
        self.root.resizable(False, False)

        self.crear_interfaz()

    def crear_interfaz(self):
        ttk.Label(
            self.root,
            text="Restaurante App",
            font=("Arial", 22, "bold")
        ).pack(pady=(30, 5))

        ttk.Label(
            self.root,
            text="Inicio de sesión"
        ).pack(pady=5)

        formulario = ttk.LabelFrame(self.root, text="Acceso")
        formulario.pack(fill="x", padx=45, pady=20)

        ttk.Label(formulario, text="Identificación:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_identificacion = ttk.Entry(formulario, width=25)
        self.entry_identificacion.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(formulario, text="Contraseña:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_contrasena = ttk.Entry(formulario, width=25, show="*")
        self.entry_contrasena.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(
            self.root,
            text="Ingresar",
            command=self.iniciar_sesion
        ).pack(pady=5)

        self.entry_identificacion.focus()
        self.root.bind("<Return>", lambda event: self.iniciar_sesion())

    def iniciar_sesion(self):
        identificacion = self.entry_identificacion.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not identificacion or not contrasena:
            messagebox.showwarning("Datos incompletos", "Ingrese identificación y contraseña.")
            return

        usuario = self.servicio.autenticar_usuario(identificacion, contrasena)

        if usuario is None:
            messagebox.showerror("Error", "Identificación o contraseña incorrecta.")
            return

        self.on_login(usuario)
