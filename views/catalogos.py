import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.catalogo_controller import CatalogoController


class VistaCatalogos(ctk.CTkFrame):

    def __init__(
        self,
        master,
        usuario_sesion
    ):
        super().__init__(
            master,
            fg_color="#F3F6F9",
            corner_radius=0
        )

        self.usuario_sesion = usuario_sesion

        self.catalogo_actual = "categorias"

        self.registros = []
        self.registro_seleccionado = None

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_interfaz()

        self.cargar_catalogo(
            "categorias"
        )

    def crear_interfaz(self):

        # ==========================================
        # ENCABEZADO
        # ==========================================

        encabezado = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        encabezado.pack(
            fill="x",
            padx=30,
            pady=(25, 10)
        )

        ctk.CTkLabel(
            encabezado,
            text="Administración de catálogos",
            font=("Arial", 28, "bold"),
            text_color="#1F2937"
        ).pack(
            side="left"
        )

        # ==========================================
        # BOTONES DE CATÁLOGOS
        # ==========================================

        navegacion = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=10
        )

        navegacion.pack(
            fill="x",
            padx=30,
            pady=10
        )

        botones = [
            (
                "Categorías",
                "categorias"
            ),
            (
                "Prioridades",
                "prioridades"
            ),
            (
                "Áreas",
                "areas"
            ),
            (
                "Estados",
                "estados"
            )
        ]

        for texto, tabla in botones:

            ctk.CTkButton(
                navegacion,
                text=texto,
                width=140,
                height=40,
                command=lambda t=tabla:
                    self.cargar_catalogo(t)
            ).pack(
                side="left",
                padx=8,
                pady=15
            )

        # ==========================================
        # FORMULARIO
        # ==========================================

        formulario = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=10
        )

        formulario.pack(
            fill="x",
            padx=30,
            pady=10
        )

        ctk.CTkLabel(
            formulario,
            text="Nombre",
            font=("Arial", 13, "bold")
        ).grid(
            row=0,
            column=0,
            padx=(20, 10),
            pady=(15, 5),
            sticky="w"
        )

        self.entrada_nombre = ctk.CTkEntry(
            formulario,
            height=40,
            width=350,
            placeholder_text="Nombre del registro"
        )

        self.entrada_nombre.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=(0, 15)
        )

        self.boton_nuevo = ctk.CTkButton(
        formulario,
        text="Nuevo",
        width=110,
        command=self.nuevo
    )

        self.boton_nuevo.grid(
            row=1,
            column=1,
            padx=5,
            pady=(0, 15)
        )

        self.boton_guardar = ctk.CTkButton(
        formulario,
        text="Guardar",
        width=110,
        fg_color="#16A34A",
        hover_color="#15803D",
        command=self.guardar
    )

        self.boton_guardar.grid(
        row=1,
        column=2,
        padx=5,
        pady=(0, 15)
    )
        self.boton_eliminar = ctk.CTkButton(
            formulario,
            text="Eliminar",
            width=110,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.eliminar
        )

        self.boton_eliminar.grid(
            row=1,
            column=3,
            padx=(5, 20),
            pady=(0, 15)
        )

        # ==========================================
        # TABLA
        # ==========================================

        tabla_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=10
        )

        tabla_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(10, 30)
        )

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=(
                "id",
                "nombre"
            ),
            show="headings"
        )

        self.tabla.heading(
            "id",
            text="ID"
        )

        self.tabla.heading(
            "nombre",
            text="Nombre"
        )

        self.tabla.column(
            "id",
            width=100,
            anchor="center"
        )

        self.tabla.column(
            "nombre",
            width=400
        )

        self.tabla.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_registro
        )

    def cargar_catalogo(
        self,
        tabla
    ):

        self.catalogo_actual = tabla

        self.nuevo()

        exito, resultado = (
            CatalogoController.listar(
                tabla=tabla,
                usuario_sesion=self.usuario_sesion
            )
        )

        if not exito:
            messagebox.showerror(
                "Error",
                resultado
            )
            return

        self.registros = resultado

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for registro in resultado:

            self.tabla.insert(
                "",
                "end",
                iid=str(registro["id"]),
                values=(
                    registro["id"],
                    registro["nombre"]
                )
            )

        # Estados no se eliminan
        if tabla == "estados":

            self.boton_eliminar.configure(
                state="disabled"
            )

            self.boton_guardar.configure(
                state="disabled"
            )

            self.boton_nuevo.configure(
                state="disabled"
            )

            self.entrada_nombre.configure(
                state="disabled"
            )

        else:

            self.boton_eliminar.configure(
                state="normal"
            )

            self.boton_guardar.configure(
                state="normal"
            )

            self.boton_nuevo.configure(
                state="normal"
            )

            self.entrada_nombre.configure(
                state="normal"
            )

    def seleccionar_registro(
        self,
        evento=None
    ):

        seleccion = self.tabla.selection()

        if not seleccion:
            return

        id_registro = int(
            seleccion[0]
        )

        registro = next(
            (
                r
                for r in self.registros
                if r["id"] == id_registro
            ),
            None
        )

        if registro is None:
            return

        self.registro_seleccionado = registro

        self.entrada_nombre.delete(
            0,
            "end"
        )

        self.entrada_nombre.insert(
            0,
            registro["nombre"]
        )

    def nuevo(self):

        self.registro_seleccionado = None

        if hasattr(
            self,
            "entrada_nombre"
        ):
            self.entrada_nombre.delete(
                0,
                "end"
            )

    def guardar(self):

        nombre = (
            self.entrada_nombre
            .get()
            .strip()
        )

        if self.registro_seleccionado:

            exito, mensaje = (
                CatalogoController.editar(
                    tabla=self.catalogo_actual,
                    id_registro=
                        self.registro_seleccionado["id"],
                    nombre=nombre,
                    usuario_sesion=self.usuario_sesion
                )
            )

        else:

            exito, mensaje = (
                CatalogoController.crear(
                    tabla=self.catalogo_actual,
                    nombre=nombre,
                    usuario_sesion=self.usuario_sesion
                )
            )

        if exito:

            messagebox.showinfo(
                "Correcto",
                mensaje
            )

            self.cargar_catalogo(
                self.catalogo_actual
            )

        else:

            messagebox.showwarning(
                "Catálogo",
                mensaje
            )

    def eliminar(self):

        if self.registro_seleccionado is None:

            messagebox.showwarning(
                "Seleccionar",
                "Seleccione un registro."
            )

            return

        confirmar = messagebox.askyesno(
            "Eliminar registro",
            (
                "¿Desea eliminar el registro "
                f"'{self.registro_seleccionado['nombre']}'?"
            )
        )

        if not confirmar:
            return

        exito, mensaje = (
            CatalogoController.eliminar(
                tabla=self.catalogo_actual,
                id_registro=
                    self.registro_seleccionado["id"],
                usuario_sesion=self.usuario_sesion
            )
        )

        if exito:

            messagebox.showinfo(
                "Correcto",
                mensaje
            )

            self.cargar_catalogo(
                self.catalogo_actual
            )

        else:

            messagebox.showwarning(
                "Catálogo",
                mensaje
            )