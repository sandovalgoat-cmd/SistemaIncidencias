import customtkinter as ctk
from tkinter import messagebox

from config.database import conectar
from controllers.ticket_controller import TicketController


class VistaNuevoTicket(ctk.CTkFrame):

    def __init__(self, master, usuario_sesion):
        super().__init__(
            master,
            fg_color="#F3F6F9",
            corner_radius=0
        )

        self.usuario_sesion = usuario_sesion
        self.categorias = {}
        self.prioridades = {}

        self.pack(fill="both", expand=True)

        self.crear_interfaz()
        self.cargar_catalogos()

    def crear_interfaz(self):

        encabezado = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        encabezado.pack(
            fill="x",
            padx=40,
            pady=(30, 15)
        )

        ctk.CTkLabel(
            encabezado,
            text="Registrar nueva incidencia",
            font=("Arial", 28, "bold"),
            text_color="#1F2937"
        ).pack(anchor="w")

        ctk.CTkLabel(
            encabezado,
            text=(
                "Describe el problema con claridad para facilitar "
                "su atención."
            ),
            font=("Arial", 15),
            text_color="#6B7280"
        ).pack(anchor="w", pady=(5, 0))

        formulario = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12
        )
        formulario.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(10, 35)
        )

        formulario.grid_columnconfigure(0, weight=1)
        formulario.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            formulario,
            text="Título del problema",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=30,
            pady=(30, 5)
        )

        self.entrada_titulo = ctk.CTkEntry(
            formulario,
            height=42,
            placeholder_text=(
                "Ejemplo: La impresora de contabilidad no imprime"
            )
        )
        self.entrada_titulo.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=30,
            pady=(0, 15)
        )

        ctk.CTkLabel(
            formulario,
            text="Categoría",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).grid(
            row=2,
            column=0,
            sticky="ew",
            padx=(30, 15),
            pady=(10, 5)
        )

        ctk.CTkLabel(
            formulario,
            text="Prioridad",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).grid(
            row=2,
            column=1,
            sticky="ew",
            padx=(15, 30),
            pady=(10, 5)
        )

        self.combo_categoria = ctk.CTkComboBox(
            formulario,
            height=42,
            values=[],
            state="readonly"
        )
        self.combo_categoria.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=(30, 15),
            pady=(0, 15)
        )

        self.combo_prioridad = ctk.CTkComboBox(
            formulario,
            height=42,
            values=[],
            state="readonly"
        )
        self.combo_prioridad.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=(15, 30),
            pady=(0, 15)
        )

        ctk.CTkLabel(
            formulario,
            text="Descripción detallada",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=30,
            pady=(10, 5)
        )

        self.entrada_descripcion = ctk.CTkTextbox(
            formulario,
            height=220
        )
        self.entrada_descripcion.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=30,
            pady=(0, 20)
        )

        formulario.grid_rowconfigure(5, weight=1)

        self.boton_guardar = ctk.CTkButton(
            formulario,
            text="Registrar ticket",
            height=45,
            width=220,
            command=self.registrar_ticket
        )
        self.boton_guardar.grid(
            row=6,
            column=0,
            columnspan=2,
            pady=(5, 30)
        )

    def cargar_catalogos(self):
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT id_categoria, nombre
                FROM categorias
                ORDER BY nombre
                """
            )

            categorias = cursor.fetchall()

            self.categorias = {
                fila["nombre"]: fila["id_categoria"]
                for fila in categorias
            }

            cursor.execute(
                """
                SELECT id_prioridad, nombre
                FROM prioridades
                ORDER BY id_prioridad
                """
            )

            prioridades = cursor.fetchall()

            self.prioridades = {
                fila["nombre"]: fila["id_prioridad"]
                for fila in prioridades
            }

            lista_categorias = list(self.categorias.keys())
            lista_prioridades = list(self.prioridades.keys())

            self.combo_categoria.configure(
                values=lista_categorias
            )

            self.combo_prioridad.configure(
                values=lista_prioridades
            )

            if lista_categorias:
                self.combo_categoria.set(lista_categorias[0])

            if "Media" in self.prioridades:
                self.combo_prioridad.set("Media")

            elif lista_prioridades:
                self.combo_prioridad.set(lista_prioridades[0])

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible cargar los catálogos.\n\n{error}"
            )

        finally:
            cursor.close()
            conexion.close()

    def registrar_ticket(self):
        categoria_seleccionada = self.combo_categoria.get()
        prioridad_seleccionada = self.combo_prioridad.get()

        id_categoria = self.categorias.get(
            categoria_seleccionada
        )

        id_prioridad = self.prioridades.get(
            prioridad_seleccionada
        )

        self.boton_guardar.configure(state="disabled")

        try:
            exito, mensaje = TicketController.crear_ticket(
                titulo=self.entrada_titulo.get(),
                descripcion=(
                    self.entrada_descripcion.get("1.0", "end")
                ),
                id_usuario=self.usuario_sesion["id_usuario"],
                id_categoria=id_categoria,
                id_prioridad=id_prioridad
            )

            if exito:
                messagebox.showinfo(
                    "Ticket registrado",
                    mensaje
                )

                self.limpiar_formulario()

            else:
                messagebox.showwarning(
                    "No fue posible registrar",
                    mensaje
                )

        finally:
            self.boton_guardar.configure(state="normal")

    def limpiar_formulario(self):
        self.entrada_titulo.delete(0, "end")
        self.entrada_descripcion.delete("1.0", "end")

        if "Media" in self.prioridades:
            self.combo_prioridad.set("Media")

        self.entrada_titulo.focus()