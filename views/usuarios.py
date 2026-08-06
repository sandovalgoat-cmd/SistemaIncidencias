import customtkinter as ctk
from tkinter import ttk, messagebox

from config.database import conectar
from controllers.usuario_controller import UsuarioController


class VistaUsuarios(ctk.CTkFrame):

    def __init__(self, master, usuario_sesion):
        super().__init__(
            master,
            fg_color="#F3F6F9",
            corner_radius=0
        )

        self.usuario_sesion = usuario_sesion
        self.usuario_seleccionado = None

        self.roles = {}
        self.areas = {}

        self.pack(fill="both", expand=True)

        self.configurar_estilos()
        self.crear_interfaz()
        self.cargar_catalogos()
        self.cargar_usuarios()

    def configurar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "Usuarios.Treeview",
            rowheight=35,
            font=("Arial", 11),
            background="white",
            fieldbackground="white"
        )

        estilo.configure(
            "Usuarios.Treeview.Heading",
            font=("Arial", 11, "bold")
        )

    def crear_interfaz(self):
        encabezado = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        encabezado.pack(fill="x", padx=30, pady=(25, 10))

        ctk.CTkLabel(
            encabezado,
            text="Administración de usuarios",
            font=("Arial", 28, "bold"),
            text_color="#1F2937"
        ).pack(side="left")

        ctk.CTkButton(
            encabezado,
            text="Nuevo usuario",
            width=150,
            height=40,
            command=self.abrir_formulario_nuevo
        ).pack(side="right")

        buscador_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=10
        )
        buscador_frame.pack(fill="x", padx=30, pady=10)

        self.entrada_busqueda = ctk.CTkEntry(
            buscador_frame,
            placeholder_text="Buscar por nombre, usuario, rol o área",
            height=40
        )
        self.entrada_busqueda.pack(
            side="left",
            fill="x",
            expand=True,
            padx=15,
            pady=15
        )

        self.entrada_busqueda.bind(
            "<KeyRelease>",
            lambda evento: self.cargar_usuarios()
        )

        tabla_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=10
        )
        tabla_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(10, 15)
        )

        columnas = (
            "id",
            "nombre",
            "usuario",
            "rol",
            "area",
            "estado"
        )

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            style="Usuarios.Treeview"
        )

        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre completo")
        self.tabla.heading("usuario", text="Usuario")
        self.tabla.heading("rol", text="Rol")
        self.tabla.heading("area", text="Área")
        self.tabla.heading("estado", text="Estado")

        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("nombre", width=230)
        self.tabla.column("usuario", width=140)
        self.tabla.column("rol", width=140)
        self.tabla.column("area", width=160)
        self.tabla.column("estado", width=100, anchor="center")

        scroll = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(15, 0),
            pady=15
        )

        scroll.pack(
            side="right",
            fill="y",
            padx=(0, 15),
            pady=15
        )

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_usuario
        )

        acciones = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        acciones.pack(fill="x", padx=30, pady=(0, 25))

        ctk.CTkButton(
            acciones,
            text="Editar",
            width=130,
            command=self.abrir_formulario_editar
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            acciones,
            text="Cambiar contraseña",
            width=170,
            fg_color="#6D28D9",
            hover_color="#5B21B6",
            command=self.abrir_cambio_password
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            acciones,
            text="Activar / Desactivar",
            width=170,
            fg_color="#D97706",
            hover_color="#B45309",
            command=self.cambiar_estado
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            acciones,
            text="Actualizar lista",
            width=150,
            fg_color="#4B5563",
            hover_color="#374151",
            command=self.cargar_usuarios
        ).pack(side="right")

    def cargar_catalogos(self):
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT id_rol, nombre FROM roles ORDER BY nombre"
            )
            datos_roles = cursor.fetchall()

            self.roles = {
                fila["nombre"]: fila["id_rol"]
                for fila in datos_roles
            }

            if self.usuario_sesion["rol"] == "EncargadoTI":
                roles_permitidos = [
                "Empleado",
                "Tecnico"
                ]

            self.roles = {
                nombre: id_rol
                for nombre, id_rol in self.roles.items()
                if nombre in roles_permitidos
            }

            cursor.execute(
                "SELECT id_area, nombre FROM areas ORDER BY nombre"
            )
            datos_areas = cursor.fetchall()

            self.areas = {
                fila["nombre"]: fila["id_area"]
                for fila in datos_areas
            }

        finally:
            cursor.close()
            conexion.close()

    def cargar_usuarios(self):
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)

        texto = self.entrada_busqueda.get().strip().lower()
        usuarios = UsuarioController.listar()

        for usuario in usuarios:
            nombre_completo = (
                f"{usuario['nombre']} {usuario['apellido']}"
            )

            valores_busqueda = (
                nombre_completo,
                usuario["usuario"],
                usuario["rol"],
                usuario["area"]
            )

            coincide = any(
                texto in str(valor).lower()
                for valor in valores_busqueda
            )

            if texto and not coincide:
                continue

            estado_texto = (
                "Activo"
                if usuario["estado"]
                else "Inactivo"
            )

            self.tabla.insert(
                "",
                "end",
                values=(
                    usuario["id_usuario"],
                    nombre_completo,
                    usuario["usuario"],
                    usuario["rol"],
                    usuario["area"],
                    estado_texto
                ),
                tags=(str(usuario["id_usuario"]),)
            )

        self.usuario_seleccionado = None

    def seleccionar_usuario(self, evento=None):
        seleccion = self.tabla.selection()

        if not seleccion:
            self.usuario_seleccionado = None
            return

        valores = self.tabla.item(seleccion[0], "values")
        id_usuario = int(valores[0])

        usuarios = UsuarioController.listar()

        self.usuario_seleccionado = next(
            (
                usuario
                for usuario in usuarios
                if usuario["id_usuario"] == id_usuario
            ),
            None
        )

    def abrir_formulario_nuevo(self):
        self.mostrar_formulario()

    def abrir_formulario_editar(self):
        if self.usuario_seleccionado is None:
            messagebox.showwarning(
                "Seleccionar usuario",
                "Seleccione un usuario de la tabla."
            )
            return

        self.mostrar_formulario(self.usuario_seleccionado)

    def mostrar_formulario(self, usuario=None):
        ventana = ctk.CTkToplevel(self)
        ventana.title(
            "Editar usuario" if usuario else "Nuevo usuario"
        )
        ventana.geometry("500x610")
        ventana.resizable(False, False)
        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text="Editar usuario" if usuario else "Nuevo usuario",
            font=("Arial", 24, "bold")
        ).pack(pady=(25, 15))

        entrada_nombre = ctk.CTkEntry(
            ventana,
            width=380,
            height=40,
            placeholder_text="Nombre"
        )
        entrada_nombre.pack(pady=8)

        entrada_apellido = ctk.CTkEntry(
            ventana,
            width=380,
            height=40,
            placeholder_text="Apellido"
        )
        entrada_apellido.pack(pady=8)

        entrada_usuario = ctk.CTkEntry(
            ventana,
            width=380,
            height=40,
            placeholder_text="Nombre de usuario"
        )
        entrada_usuario.pack(pady=8)

        entrada_password = None

        if usuario is None:
            entrada_password = ctk.CTkEntry(
                ventana,
                width=380,
                height=40,
                placeholder_text="Contraseña",
                show="*"
            )
            entrada_password.pack(pady=8)

        ctk.CTkLabel(
            ventana,
            text="Rol",
            anchor="w",
            width=380
        ).pack(pady=(12, 2))

        combo_rol = ctk.CTkComboBox(
            ventana,
            width=380,
            height=40,
            values=list(self.roles.keys()),
            state="readonly"
        )
        combo_rol.pack(pady=5)

        ctk.CTkLabel(
            ventana,
            text="Área",
            anchor="w",
            width=380
        ).pack(pady=(12, 2))

        combo_area = ctk.CTkComboBox(
            ventana,
            width=380,
            height=40,
            values=list(self.areas.keys()),
            state="readonly"
        )
        combo_area.pack(pady=5)

        if usuario:
            entrada_nombre.insert(0, usuario["nombre"])
            entrada_apellido.insert(0, usuario["apellido"])
            entrada_usuario.insert(0, usuario["usuario"])
            combo_rol.set(usuario["rol"])

            if usuario["area"] in self.areas:
                combo_area.set(usuario["area"])

        elif self.roles and self.areas:
            combo_rol.set(next(iter(self.roles)))
            combo_area.set(next(iter(self.areas)))

        def guardar():
            rol_seleccionado = combo_rol.get()
            area_seleccionada = combo_area.get()

            if rol_seleccionado not in self.roles:
                messagebox.showwarning(
                    "Rol",
                    "Seleccione un rol válido.",
                    parent=ventana
                )
                return

            if area_seleccionada not in self.areas:
                messagebox.showwarning(
                    "Área",
                    "Seleccione un área válida.",
                    parent=ventana
                )
                return

            if usuario is None:
                exito, mensaje = UsuarioController.crear(
                    entrada_nombre.get(),
                    entrada_apellido.get(),
                    entrada_usuario.get(),
                    entrada_password.get(),
                    self.roles[rol_seleccionado],
                    self.areas[area_seleccionada]
                )

            else:
                exito, mensaje = UsuarioController.actualizar(
                    usuario["id_usuario"],
                    entrada_nombre.get(),
                    entrada_apellido.get(),
                    entrada_usuario.get(),
                    self.roles[rol_seleccionado],
                    self.areas[area_seleccionada]
                )

            if exito:
                messagebox.showinfo(
                    "Correcto",
                    mensaje,
                    parent=ventana
                )
                ventana.destroy()
                self.cargar_usuarios()

            else:
                messagebox.showerror(
                    "Error",
                    mensaje,
                    parent=ventana
                )

        ctk.CTkButton(
            ventana,
            text="Guardar",
            width=380,
            height=42,
            command=guardar
        ).pack(pady=25)

    def abrir_cambio_password(self):
        if self.usuario_seleccionado is None:
            messagebox.showwarning(
                "Seleccionar usuario",
                "Seleccione un usuario de la tabla."
            )
            return

        ventana = ctk.CTkToplevel(self)
        ventana.title("Cambiar contraseña")
        ventana.geometry("430x300")
        ventana.resizable(False, False)
        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text="Cambiar contraseña",
            font=("Arial", 22, "bold")
        ).pack(pady=(25, 15))

        nueva_password = ctk.CTkEntry(
            ventana,
            width=330,
            height=42,
            placeholder_text="Nueva contraseña",
            show="*"
        )
        nueva_password.pack(pady=10)

        confirmar_password = ctk.CTkEntry(
            ventana,
            width=330,
            height=42,
            placeholder_text="Confirmar contraseña",
            show="*"
        )
        confirmar_password.pack(pady=10)

        def guardar_password():
            if nueva_password.get() != confirmar_password.get():
                messagebox.showerror(
                    "Contraseñas",
                    "Las contraseñas no coinciden.",
                    parent=ventana
                )
                return

            exito, mensaje = UsuarioController.cambiar_password(
                self.usuario_seleccionado["id_usuario"],
                nueva_password.get()
            )

            if exito:
                messagebox.showinfo(
                    "Correcto",
                    mensaje,
                    parent=ventana
                )
                ventana.destroy()

            else:
                messagebox.showerror(
                    "Error",
                    mensaje,
                    parent=ventana
                )

        ctk.CTkButton(
            ventana,
            text="Guardar contraseña",
            width=330,
            height=42,
            command=guardar_password
        ).pack(pady=20)

    def cambiar_estado(self):
        if self.usuario_seleccionado is None:
            messagebox.showwarning(
                "Seleccionar usuario",
                "Seleccione un usuario de la tabla."
            )
            return

        if (
            self.usuario_seleccionado["id_usuario"]
            == self.usuario_sesion["id_usuario"]
        ):
            messagebox.showwarning(
                "Acción no permitida",
                "No puede desactivar su propia cuenta."
            )
            return

        estado_actual = self.usuario_seleccionado["estado"]

        accion = "desactivar" if estado_actual else "activar"

        confirmar = messagebox.askyesno(
            "Confirmar",
            f"¿Desea {accion} al usuario seleccionado?"
        )

        if not confirmar:
            return

        exito, mensaje = UsuarioController.cambiar_estado(
            self.usuario_seleccionado["id_usuario"],
            estado_actual
        )

        if exito:
            messagebox.showinfo("Correcto", mensaje)
            self.cargar_usuarios()

        else:
            messagebox.showerror("Error", mensaje)