from doctest import master

import customtkinter as ctk
import customtkinter as ctk
from tkinter import messagebox

from controllers.ticket_controller import TicketController


class VistaDetalleTicket(ctk.CTkFrame):

    def __init__(
        self,
        master,
        ticket,
        usuario_sesion,
        regresar_callback
    ):
        
        super().__init__(
            master,
            fg_color="#F3F6F9",
            corner_radius=0
        )
        

        self.ticket = ticket
        self.usuario_sesion = usuario_sesion
        self.regresar_callback = regresar_callback

        self.pack(fill="both", expand=True)

        self.crear_interfaz()

    # ==================================================
    # CREAR INTERFAZ
    # ==================================================

    def crear_interfaz(self):

        # ----------------------------------------------
        # ENCABEZADO
        # ----------------------------------------------

        encabezado = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        encabezado.pack(
            fill="x",
            padx=35,
            pady=(25, 15)
        )

        ctk.CTkButton(
            encabezado,
            text="← Regresar",
            width=120,
            height=38,
            fg_color="#4B5563",
            hover_color="#374151",
            command=self.regresar_callback
        ).pack(side="left")

        ctk.CTkLabel(
            encabezado,
            text="Detalle del ticket",
            font=("Arial", 28, "bold"),
            text_color="#1F2937"
        ).pack(
            side="left",
            padx=20
        )

        # ----------------------------------------------
        # CONTENEDOR PRINCIPAL
        # ----------------------------------------------

        contenedor = ctk.CTkScrollableFrame(
            self,
            fg_color="white",
            corner_radius=12
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(5, 30)
        )

        contenedor.grid_columnconfigure(
            0,
            weight=1
        )

        contenedor.grid_columnconfigure(
            1,
            weight=1
        )

        # ----------------------------------------------
        # FECHA
        # ----------------------------------------------

        fecha = self.ticket["fecha_creacion"]

        if fecha:
            fecha_texto = fecha.strftime(
                "%d/%m/%Y %H:%M"
            )
        else:
            fecha_texto = "Sin fecha"

        # ----------------------------------------------
        # FOLIO
        # ----------------------------------------------

        self.crear_etiqueta(
            contenedor,
            "Folio",
            fila=0,
            columna=0,
            padx=(25, 12)
        )

        # ----------------------------------------------
        # ESTADO
        # ----------------------------------------------

        self.crear_etiqueta(
            contenedor,
            "Estado",
            fila=0,
            columna=1,
            padx=(12, 25)
        )

        self.crear_campo(
            contenedor,
            self.ticket["folio"],
            fila=1,
            columna=0,
            padx=(25, 12)
        )

        self.crear_campo(
            contenedor,
            self.ticket["estado"],
            fila=1,
            columna=1,
            padx=(12, 25)
        )

        # ----------------------------------------------
        # TÍTULO
        # ----------------------------------------------

        self.crear_etiqueta(
            contenedor,
            "Título",
            fila=2,
            columna=0,
            columnas=2,
            padx=25
        )

        self.crear_campo(
            contenedor,
            self.ticket["titulo"],
            fila=3,
            columna=0,
            columnas=2,
            padx=25
        )

        # ----------------------------------------------
        # REPORTADO POR
        # ----------------------------------------------

        self.crear_etiqueta(
            contenedor,
            "Reportado por",
            fila=4,
            columna=0,
            padx=(25, 12)
        )

        # ----------------------------------------------
        # TÉCNICO
        # ----------------------------------------------

        self.crear_etiqueta(
            contenedor,
            "Técnico asignado",
            fila=4,
            columna=1,
            padx=(12, 25)
        )

        self.crear_campo(
            contenedor,
            self.ticket["reportado_por"],
            fila=5,
            columna=0,
            padx=(25, 12)
        )

        self.crear_campo(
            contenedor,
            self.ticket["tecnico"],
            fila=5,
            columna=1,
            padx=(12, 25)
        )

        # ----------------------------------------------
        # CATEGORÍA
        # ----------------------------------------------

        self.crear_etiqueta(
            contenedor,
            "Categoría",
            fila=6,
            columna=0,
            padx=(25, 12)
        )

        # ----------------------------------------------
        # PRIORIDAD
        # ----------------------------------------------

        self.crear_etiqueta(
            contenedor,
            "Prioridad",
            fila=6,
            columna=1,
            padx=(12, 25)
        )

        self.crear_campo(
            contenedor,
            self.ticket["categoria"],
            fila=7,
            columna=0,
            padx=(25, 12)
        )

        self.crear_campo(
            contenedor,
            self.ticket["prioridad"],
            fila=7,
            columna=1,
            padx=(12, 25)
        )

        # ----------------------------------------------
        # FECHA DE CREACIÓN
        # ----------------------------------------------

        self.crear_etiqueta(
            contenedor,
            "Fecha de creación",
            fila=8,
            columna=0,
            columnas=2,
            padx=25
        )

        self.crear_campo(
            contenedor,
            fecha_texto,
            fila=9,
            columna=0,
            columnas=2,
            padx=25
        )

        # ----------------------------------------------
        # DESCRIPCIÓN
        # ----------------------------------------------

        self.crear_etiqueta(
            contenedor,
            "Descripción del problema",
            fila=10,
            columna=0,
            columnas=2,
            padx=25
        )

        descripcion = ctk.CTkTextbox(
            contenedor,
            height=180,
            wrap="word",
            font=("Arial", 14)
        )

        descripcion.grid(
            row=11,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=25,
            pady=(4, 30)
        )

        descripcion.insert(
            "1.0",
            self.ticket["descripcion"]
        )

        descripcion.configure(
            state="disabled"
        )

        # ==============================================
        # ASIGNACIÓN DE TÉCNICO
        # ==============================================

        if self.usuario_sesion["rol"] in (
            "Administrador",
            "EncargadoTI"
        ):
            self.crear_panel_asignacion(
                contenedor,
                fila=12
            )


    def crear_etiqueta(
        self,
        master,
        texto,
        fila,
        columna,
        columnas=1,
        padx=0
    ):

        etiqueta = ctk.CTkLabel(
            master,
            text=texto,
            font=("Arial", 13, "bold"),
            text_color="#6B7280",
            anchor="w"
        )

        etiqueta.grid(
            row=fila,
            column=columna,
            columnspan=columnas,
            sticky="ew",
            padx=padx,
            pady=(20, 4)
        )

    # ==================================================
    # CREAR CAMPO DE INFORMACIÓN
    # ==================================================

    def crear_campo(
        self,
        master,
        texto,
        fila,
        columna,
        columnas=1,
        padx=0
    ):

        campo = ctk.CTkLabel(
            master,
            text=str(texto),
            height=42,
            corner_radius=8,
            fg_color="#F3F4F6",
            text_color="#1F2937",
            anchor="w"
        )

        campo.grid(
            row=fila,
            column=columna,
            columnspan=columnas,
            sticky="ew",
            padx=padx,
            pady=(0, 5)
        )

    def crear_panel_asignacion(
        self,
        master,
        fila
    ):

        panel = ctk.CTkFrame(
            master,
            fg_color="#EEF2FF",
            corner_radius=10
        )
        panel.grid(
            row=fila,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=25,
            pady=(10, 30)
        )

        panel.grid_columnconfigure(
            0,
            weight=1
        )

        panel.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            panel,
            text="Asignación de técnico",
            font=("Arial", 17, "bold"),
            text_color="#1F2937"
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=20,
            pady=(20, 10)
        )

        self.tecnicos = {}

        exito, resultado = (
            TicketController.listar_tecnicos()
        )

        if not exito:
            ctk.CTkLabel(
                panel,
                text=resultado,
                text_color="#C62828"
            ).grid(
                row=1,
                column=0,
                columnspan=2,
                padx=20,
                pady=10
            )

            return

        self.tecnicos = {
            tecnico["nombre_completo"]:
            tecnico["id_usuario"]
            for tecnico in resultado
        }

        lista_tecnicos = list(
            self.tecnicos.keys()
        )

        if not lista_tecnicos:
            lista_tecnicos = [
                "No hay técnicos disponibles"
            ]

        self.combo_tecnico = ctk.CTkComboBox(
            panel,
            values=lista_tecnicos,
            state="readonly",
            height=40,
            width=300
        )

        self.combo_tecnico.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=(5, 20)
        )

        # Seleccionar técnico actual si existe
        tecnico_actual = self.ticket["tecnico"]

        if (
            tecnico_actual
            and tecnico_actual != "Sin asignar"
            and tecnico_actual in self.tecnicos
        ):
            self.combo_tecnico.set(
                tecnico_actual
            )

        elif self.tecnicos:
            self.combo_tecnico.set(
                lista_tecnicos[0]
            )

        self.boton_asignar = ctk.CTkButton(
            panel,
            text="Asignar técnico",
            height=40,
            width=170,
            command=self.asignar_tecnico
        )

        self.boton_asignar.grid(
            row=1,
            column=1,
            padx=(10, 20),
            pady=(5, 20)
        )

    def asignar_tecnico(self):

        tecnico_seleccionado = (
            self.combo_tecnico.get()
        )

        if (
            tecnico_seleccionado
            not in self.tecnicos
        ):
            messagebox.showwarning(
                "Técnico",
                "Seleccione un técnico válido."
            )
            return

        id_tecnico = self.tecnicos[
            tecnico_seleccionado
        ]

        confirmar = messagebox.askyesno(
            "Asignar técnico",
            f"¿Desea asignar este ticket a "
            f"{tecnico_seleccionado}?"
        )

        if not confirmar:
            return

        self.boton_asignar.configure(
            state="disabled",
            text="Asignando..."
        )

        try:
            exito, mensaje = (
                TicketController.asignar_tecnico(
                    id_ticket=self.ticket["id_ticket"],
                    id_tecnico=id_tecnico,
                    usuario_sesion=self.usuario_sesion
                )
            )

            if exito:
                messagebox.showinfo(
                    "Correcto",
                    mensaje
                )

                # Regresar a la lista para refrescar datos
                self.regresar_callback()

            else:
                messagebox.showerror(
                    "Error",
                    mensaje
                )

        finally:
            self.boton_asignar.configure(
                state="normal",
                text="Asignar técnico"
            )