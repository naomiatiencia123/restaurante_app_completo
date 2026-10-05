import tkinter as tk
from tkinter import ttk, messagebox
from modelos.usuario import Usuario
from modelos.producto import Producto
from modelos.venta import Venta


class MainView:
    def __init__(self, root, servicio, usuario_actual, on_logout=None):
        self.root = root
        self.servicio = servicio
        self.usuario_actual = usuario_actual
        self.on_logout = on_logout

        self.root.title("Restaurante App - Gestión")
        self.root.geometry("900x620")
        self.root.protocol("WM_DELETE_WINDOW", self.salir)

        self.crear_interfaz()

    def crear_interfaz(self):
        cabecera = ttk.Frame(self.root, padding=10)
        cabecera.pack(fill="x")

        ttk.Label(
            cabecera,
            text=f"Restaurante App | {self.usuario_actual.nombre} "
                 f"({self.usuario_actual.rol})",
            font=("Arial", 16, "bold")
        ).pack(side="left")

        ttk.Button(cabecera, text="Cerrar sesión", command=self.salir).pack(side="right")

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_usuarios = ttk.Frame(notebook, padding=10)
        self.tab_productos = ttk.Frame(notebook, padding=10)
        self.tab_ventas = ttk.Frame(notebook, padding=10)

        notebook.add(self.tab_usuarios, text="Usuarios")
        notebook.add(self.tab_productos, text="Productos")
        notebook.add(self.tab_ventas, text="Ventas")

        self.crear_tab_usuarios()
        self.crear_tab_productos()
        self.crear_tab_ventas()

        if self.usuario_actual.rol != "Administrador":
            notebook.hide(self.tab_usuarios)

    # ---------- Usuarios ----------
    def crear_tab_usuarios(self):
        formulario = ttk.LabelFrame(self.tab_usuarios, text="Datos del usuario", padding=10)
        formulario.pack(fill="x")

        ttk.Label(formulario, text="Identificación:").grid(row=0, column=0, padx=5, pady=5)
        self.u_id = ttk.Entry(formulario, width=25)
        self.u_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Nombre:").grid(row=0, column=2, padx=5, pady=5)
        self.u_nombre = ttk.Entry(formulario, width=25)
        self.u_nombre.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Rol:").grid(row=1, column=0, padx=5, pady=5)
        self.u_rol = ttk.Combobox(
            formulario,
            values=["Administrador", "Empleado", "Cliente"],
            state="readonly",
            width=22
        )
        self.u_rol.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Contraseña:").grid(row=1, column=2, padx=5, pady=5)
        self.u_pass = ttk.Entry(formulario, width=25, show="*")
        self.u_pass.grid(row=1, column=3, padx=5, pady=5)

        botones = ttk.Frame(self.tab_usuarios)
        botones.pack(pady=10)
        ttk.Button(botones, text="Registrar", command=self.registrar_usuario).pack(side="left", padx=5)
        ttk.Button(botones, text="Actualizar", command=self.actualizar_usuario).pack(side="left", padx=5)
        ttk.Button(botones, text="Eliminar", command=self.eliminar_usuario).pack(side="left", padx=5)
        ttk.Button(botones, text="Limpiar", command=self.limpiar_usuario).pack(side="left", padx=5)

        self.tree_usuarios = ttk.Treeview(
            self.tab_usuarios,
            columns=("id", "nombre", "rol"),
            show="headings"
        )
        for col, title, width in [
            ("id", "Identificación", 160),
            ("nombre", "Nombre", 260),
            ("rol", "Rol", 180)
        ]:
            self.tree_usuarios.heading(col, text=title)
            self.tree_usuarios.column(col, width=width)
        self.tree_usuarios.pack(fill="both", expand=True)
        self.tree_usuarios.bind("<<TreeviewSelect>>", self.seleccionar_usuario)
        self.cargar_usuarios()

    def cargar_usuarios(self):
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        for u in self.servicio.listar_usuarios():
            self.tree_usuarios.insert("", "end", values=(u.identificacion, u.nombre, u.rol))

    def seleccionar_usuario(self, event=None):
        sel = self.tree_usuarios.selection()
        if not sel:
            return
        valores = self.tree_usuarios.item(sel[0], "values")
        u = self.servicio.consultar_usuario(valores[0])
        if u:
            self.u_id.delete(0, tk.END); self.u_id.insert(0, u.identificacion)
            self.u_nombre.delete(0, tk.END); self.u_nombre.insert(0, u.nombre)
            self.u_rol.set(u.rol)
            self.u_pass.delete(0, tk.END); self.u_pass.insert(0, u.contrasena)

    def registrar_usuario(self):
        try:
            u = Usuario(self.u_id.get().strip(), self.u_nombre.get().strip(),
                        self.u_rol.get().strip(), self.u_pass.get().strip())
            if not all([u.identificacion, u.nombre, u.rol, u.contrasena]):
                raise ValueError("Complete todos los campos.")
            self.servicio.registrar_usuario(u)
            self.cargar_usuarios()
            self.limpiar_usuario()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def actualizar_usuario(self):
        try:
            u = Usuario(self.u_id.get().strip(), self.u_nombre.get().strip(),
                        self.u_rol.get().strip(), self.u_pass.get().strip())
            self.servicio.actualizar_usuario(u)
            self.cargar_usuarios()
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def eliminar_usuario(self):
        ident = self.u_id.get().strip()
        if not ident:
            messagebox.showwarning("Aviso", "Seleccione un usuario.")
            return
        if ident == self.usuario_actual.identificacion:
            messagebox.showwarning("Aviso", "No puede eliminar al usuario conectado.")
            return
        if messagebox.askyesno("Confirmar", "¿Desea eliminar este usuario?"):
            try:
                self.servicio.eliminar_usuario(ident)
                self.cargar_usuarios()
                self.limpiar_usuario()
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def limpiar_usuario(self):
        for entry in [self.u_id, self.u_nombre, self.u_pass]:
            entry.delete(0, tk.END)
        self.u_rol.set("")

    # ---------- Productos ----------
    def crear_tab_productos(self):
        formulario = ttk.LabelFrame(self.tab_productos, text="Datos del producto", padding=10)
        formulario.pack(fill="x")

        ttk.Label(formulario, text="Código:").grid(row=0, column=0, padx=5, pady=5)
        self.p_codigo = ttk.Entry(formulario, width=20)
        self.p_codigo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Nombre:").grid(row=0, column=2, padx=5, pady=5)
        self.p_nombre = ttk.Entry(formulario, width=25)
        self.p_nombre.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Precio:").grid(row=1, column=0, padx=5, pady=5)
        self.p_precio = ttk.Entry(formulario, width=20)
        self.p_precio.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Stock:").grid(row=1, column=2, padx=5, pady=5)
        self.p_stock = ttk.Entry(formulario, width=25)
        self.p_stock.grid(row=1, column=3, padx=5, pady=5)

        botones = ttk.Frame(self.tab_productos)
        botones.pack(pady=10)
        ttk.Button(botones, text="Registrar", command=self.registrar_producto).pack(side="left", padx=5)
        ttk.Button(botones, text="Actualizar", command=self.actualizar_producto).pack(side="left", padx=5)
        ttk.Button(botones, text="Eliminar", command=self.eliminar_producto).pack(side="left", padx=5)
        ttk.Button(botones, text="Limpiar", command=self.limpiar_producto).pack(side="left", padx=5)

        self.tree_productos = ttk.Treeview(
            self.tab_productos,
            columns=("codigo", "nombre", "precio", "stock"),
            show="headings"
        )
        for col, title, width in [
            ("codigo", "Código", 130), ("nombre", "Nombre", 260),
            ("precio", "Precio", 130), ("stock", "Stock", 130)
        ]:
            self.tree_productos.heading(col, text=title)
            self.tree_productos.column(col, width=width)
        self.tree_productos.pack(fill="both", expand=True)
        self.tree_productos.bind("<<TreeviewSelect>>", self.seleccionar_producto)
        self.cargar_productos()

    def cargar_productos(self):
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        for p in self.servicio.listar_productos():
            self.tree_productos.insert("", "end", values=(p.codigo, p.nombre, f"{p.precio:.2f}", p.stock))

    def seleccionar_producto(self, event=None):
        sel = self.tree_productos.selection()
        if not sel:
            return
        valores = self.tree_productos.item(sel[0], "values")
        p = self.servicio.consultar_producto(valores[0])
        if p:
            self.p_codigo.delete(0, tk.END); self.p_codigo.insert(0, p.codigo)
            self.p_nombre.delete(0, tk.END); self.p_nombre.insert(0, p.nombre)
            self.p_precio.delete(0, tk.END); self.p_precio.insert(0, p.precio)
            self.p_stock.delete(0, tk.END); self.p_stock.insert(0, p.stock)

    def datos_producto(self):
        try:
            return Producto(
                self.p_codigo.get().strip(),
                self.p_nombre.get().strip(),
                float(self.p_precio.get()),
                int(self.p_stock.get())
            )
        except ValueError:
            raise ValueError("Precio y stock deben ser valores numéricos.")

    def registrar_producto(self):
        try:
            self.servicio.registrar_producto(self.datos_producto())
            self.cargar_productos()
            self.limpiar_producto()
            messagebox.showinfo("Éxito", "Producto registrado correctamente.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def actualizar_producto(self):
        try:
            self.servicio.actualizar_producto(self.datos_producto())
            self.cargar_productos()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def eliminar_producto(self):
        codigo = self.p_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Aviso", "Seleccione un producto.")
            return
        if messagebox.askyesno("Confirmar", "¿Desea eliminar este producto?"):
            try:
                self.servicio.eliminar_producto(codigo)
                self.cargar_productos()
                self.limpiar_producto()
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def limpiar_producto(self):
        for entry in [self.p_codigo, self.p_nombre, self.p_precio, self.p_stock]:
            entry.delete(0, tk.END)

    # ---------- Ventas ----------
    def crear_tab_ventas(self):
        formulario = ttk.LabelFrame(self.tab_ventas, text="Registrar venta", padding=10)
        formulario.pack(fill="x")

        ttk.Label(formulario, text="Producto:").grid(row=0, column=0, padx=5, pady=5)
        self.v_producto = ttk.Combobox(formulario, state="readonly", width=30)
        self.v_producto.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Cantidad:").grid(row=0, column=2, padx=5, pady=5)
        self.v_cantidad = ttk.Entry(formulario, width=15)
        self.v_cantidad.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(
            formulario, text="Registrar venta", command=self.registrar_venta
        ).grid(row=1, column=1, pady=10)

        self.tree_ventas = ttk.Treeview(
            self.tab_ventas,
            columns=("usuario", "producto", "cantidad"),
            show="headings"
        )
        for col, title in [("usuario", "Usuario"), ("producto", "Producto"), ("cantidad", "Cantidad")]:
            self.tree_ventas.heading(col, text=title)
            self.tree_ventas.column(col, width=220)
        self.tree_ventas.pack(fill="both", expand=True)

        self.actualizar_combo_productos()
        self.cargar_ventas()

    def actualizar_combo_productos(self):
        self.v_producto["values"] = [
            p.codigo for p in self.servicio.listar_productos()
        ]

    def cargar_ventas(self):
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)
        for v in self.servicio.ventas:
            self.tree_ventas.insert(
                "", "end",
                values=(v.usuario_id, v.codigo_producto, v.cantidad)
            )

    def registrar_venta(self):
        try:
            codigo = self.v_producto.get()
            cantidad = int(self.v_cantidad.get())
            if not codigo:
                raise ValueError("Seleccione un producto.")

            venta = Venta(
                self.usuario_actual.identificacion,
                codigo,
                cantidad
            )
            self.servicio.registrar_venta(venta)
            self.cargar_productos()
            self.actualizar_combo_productos()
            self.cargar_ventas()
            self.v_cantidad.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Venta registrada correctamente.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def salir(self):
        if self.on_logout:
            self.on_logout()
        else:
            self.root.destroy()
