import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.catalogo_controller import CatalogoController
from config.estilos import (
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_HOVER,
    COLOR_FONDO,
    COLOR_PANEL,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE,
    COLOR_EXITO,
    COLOR_EXITO_HOVER,
    COLOR_ERROR,
    COLOR_ERROR_HOVER,
    COLOR_NEUTRO,
    COLOR_NEUTRO_HOVER,
    FUENTE_TITULO,
    ALTO_BOTON,
    RADIO_PANEL
)

class VistaCatalogos(ctk.CTkFrame):

    def __init__(
        self,
        master,
        usuario_sesion
    ):
        super().__init__(
            master,
            fg_color=COLOR_FONDO,
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
                font=FUENTE_TITULO,
                text_color=COLOR_TEXTO
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                encabezado,
                text="Gestiona los catálogos utilizados por el sistema",
                font=("Arial", 12),
                text_color=COLOR_TEXTO_SECUNDARIO
            ).pack(
                side="left",
                padx=20
            )

            # ==========================================
            # NAVEGACIÓN DE CATÁLOGOS
            # ==========================================

            navegacion = ctk.CTkFrame(
                self,
                fg_color=COLOR_PANEL,
                corner_radius=RADIO_PANEL,
                border_width=1,
                border_color=COLOR_BORDE
            )

            navegacion.pack(
                fill="x",
                padx=30,
                pady=(0, 15)
            )

            botones = [
                ("Categorías", "categorias"),
                ("Prioridades", "prioridades"),
                ("Áreas", "areas"),
                ("Estados", "estados")
            ]

            self.botones_catalogo = {}

            for texto, tabla in botones:

                boton = ctk.CTkButton(
                    navegacion,
                    text=texto,
                    width=140,
                    height=ALTO_BOTON,
                    fg_color=COLOR_NEUTRO,
                    hover_color=COLOR_NEUTRO_HOVER,
                    command=lambda t=tabla:
                        self.cargar_catalogo(t)
                )

                boton.pack(
                    side="left",
                    padx=8,
                    pady=15
                )

                self.botones_catalogo[tabla] = boton

            # ==========================================
            # FORMULARIO
            # ==========================================

            formulario = ctk.CTkFrame(
                self,
                fg_color=COLOR_PANEL,
                corner_radius=RADIO_PANEL,
                border_width=1,
                border_color=COLOR_BORDE
            )

            formulario.pack(
                fill="x",
                padx=30,
                pady=(0, 15)
            )

            formulario.grid_columnconfigure(
                0,
                weight=1
            )

            ctk.CTkLabel(
                formulario,
                text="Nombre del registro",
                font=("Arial", 13, "bold"),
                text_color=COLOR_TEXTO
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
                placeholder_text="Escriba el nombre..."
            )

            self.entrada_nombre.grid(
                row=1,
                column=0,
                sticky="ew",
                padx=(20, 10),
                pady=(0, 15)
            )

            self.boton_nuevo = ctk.CTkButton(
                formulario,
                text="Nuevo",
                width=110,
                height=ALTO_BOTON,
                fg_color=COLOR_NEUTRO,
                hover_color=COLOR_NEUTRO_HOVER,
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
                height=ALTO_BOTON,
                fg_color=COLOR_EXITO,
                hover_color=COLOR_EXITO_HOVER,
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
                height=ALTO_BOTON,
                fg_color=COLOR_ERROR,
                hover_color=COLOR_ERROR_HOVER,
                command=self.eliminar
            )

            self.boton_eliminar.grid(
                row=1,
                column=3,
                padx=(5, 20),
                pady=(0, 15)
            )

            # ==========================================
            # ESTILO DE TABLA
            # ==========================================

            estilo = ttk.Style()

            estilo.theme_use("default")

            estilo.configure(
                "Catalogos.Treeview",
                background=COLOR_PANEL,
                foreground=COLOR_TEXTO,
                fieldbackground=COLOR_PANEL,
                rowheight=38,
                borderwidth=0,
                font=("Arial", 11)
            )

            estilo.configure(
                "Catalogos.Treeview.Heading",
                background="#EAF2F8",
                foreground=COLOR_TEXTO,
                relief="flat",
                font=("Arial", 11, "bold")
            )

            estilo.map(
                "Catalogos.Treeview",
                background=[
                    ("selected", COLOR_PRIMARIO)
                ],
                foreground=[
                    ("selected", "white")
                ]
            )

            # ==========================================
            # TABLA
            # ==========================================

            tabla_frame = ctk.CTkFrame(
                self,
                fg_color=COLOR_PANEL,
                corner_radius=RADIO_PANEL,
                border_width=1,
                border_color=COLOR_BORDE
            )

            tabla_frame.pack(
                fill="both",
                expand=True,
                padx=30,
                pady=(0, 30)
            )

            tabla_frame.grid_rowconfigure(
                0,
                weight=1
            )

            tabla_frame.grid_columnconfigure(
                0,
                weight=1
            )

            self.tabla = ttk.Treeview(
                tabla_frame,
                columns=(
                    "id",
                    "nombre"
                ),
                show="headings",
                style="Catalogos.Treeview"
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
                minwidth=80,
                anchor="center"
            )

            self.tabla.column(
                "nombre",
                width=500,
                minwidth=250
            )

            scroll = ttk.Scrollbar(
                tabla_frame,
                orient="vertical",
                command=self.tabla.yview
            )

            self.tabla.configure(
                yscrollcommand=scroll.set
            )

            self.tabla.grid(
                row=0,
                column=0,
                sticky="nsew",
                padx=(15, 0),
                pady=15
            )

            scroll.grid(
                row=0,
                column=1,
                sticky="ns",
                padx=(0, 15),
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

        for nombre_tabla, boton in self.botones_catalogo.items():

            if nombre_tabla == tabla:

                boton.configure(
                    fg_color=COLOR_PRIMARIO,
                    hover_color=COLOR_PRIMARIO_HOVER
                )

            else:

                boton.configure(
                    fg_color=COLOR_NEUTRO,
                    hover_color=COLOR_NEUTRO_HOVER
                )

        self.nuevo()

        try:

            exito, resultado = (
                CatalogoController.listar(
                    tabla=tabla,
                    usuario_sesion=self.usuario_sesion
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                (
                    "No fue posible cargar el catálogo.\n\n"
                    f"Detalle: {error}"
                )
            )

            return

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

        # ==========================================
        # VALIDAR NOMBRE
        # ==========================================

        if not nombre:

            messagebox.showwarning(
                "Catálogo",
                "El nombre del registro no puede estar vacío."
            )

            self.entrada_nombre.focus()

            return

        try:

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

        except Exception as error:

            messagebox.showerror(
                "Error",
                (
                    "No fue posible guardar el registro.\n\n"
                    f"Detalle: {error}"
                )
            )

            return

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

        try:

            exito, mensaje = (
                CatalogoController.eliminar(
                    tabla=self.catalogo_actual,
                    id_registro=
                        self.registro_seleccionado["id"],
                    usuario_sesion=self.usuario_sesion
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                (
                    "No fue posible eliminar el registro.\n\n"
                    f"Detalle: {error}"
                )
            )

            return
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