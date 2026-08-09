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

        # ==============================================
        # CAMBIO DE ESTADO
        # ==============================================

        if self.usuario_sesion["rol"] in (
            "Tecnico",
            "Administrador",
            "EncargadoTI"
        ):
            self.crear_panel_estado(
                contenedor,
                fila=13
            )


        # ==============================================
        # COMENTARIOS
        # TODOS LOS ROLES PUEDEN VERLOS
        # ==============================================

        self.crear_panel_comentarios(
            contenedor,
            fila=14
        )

        if (
    self.usuario_sesion["rol"] == "Empleado"
    and self.ticket["estado"] == "Solucionado"
):
            self.crear_panel_confirmacion(
                contenedor,
                fila=15
            )

            fila_historial = 16

        else:
            fila_historial = 15


        self.crear_panel_historial(
            contenedor,
            fila=fila_historial
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

    def crear_panel_estado(
        self,
        master,
        fila
    ):

        panel = ctk.CTkFrame(
            master,
            fg_color="#ECFDF5",
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
            weight=0
        )

        ctk.CTkLabel(
            panel,
            text="Cambiar estado del ticket",
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

        estados = [
            "Asignado",
            "En Proceso",
            "En Espera",
            "Solucionado"
        ]

        self.combo_estado_ticket = ctk.CTkComboBox(
            panel,
            values=estados,
            state="readonly",
            height=42
        )

        self.combo_estado_ticket.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=(5, 20)
        )

        estado_actual = self.ticket["estado"]

        if estado_actual in estados:
            self.combo_estado_ticket.set(
                estado_actual
            )

        else:
            self.combo_estado_ticket.set(
                estados[0]
            )

        self.boton_estado = ctk.CTkButton(
            panel,
            text="Actualizar estado",
            width=180,
            height=42,
            fg_color="#059669",
            hover_color="#047857",
            command=self.actualizar_estado
        )

        self.boton_estado.grid(
            row=1,
            column=1,
            padx=(10, 20),
            pady=(5, 20)
        )

    def actualizar_estado(self):

        nuevo_estado = (
            self.combo_estado_ticket.get()
        )

        estado_actual = self.ticket["estado"]

        if nuevo_estado == estado_actual:
            messagebox.showinfo(
                "Estado",
                "El ticket ya tiene ese estado."
            )
            return

        confirmar = messagebox.askyesno(
            "Cambiar estado",
            f"¿Desea cambiar el estado de "
            f"'{estado_actual}' a '{nuevo_estado}'?"
        )

        if not confirmar:
            return

        self.boton_estado.configure(
            state="disabled",
            text="Actualizando..."
        )

        try:

            exito, mensaje = (
                TicketController.cambiar_estado(
                    id_ticket=self.ticket["id_ticket"],
                    nuevo_estado=nuevo_estado,
                    usuario_sesion=self.usuario_sesion
                )
            )

            if exito:

                messagebox.showinfo(
                    "Correcto",
                    mensaje
                )

                # Regresa a la lista para recargar
                self.regresar_callback()

            else:

                messagebox.showerror(
                    "Error",
                    mensaje
                )

        finally:

            self.boton_estado.configure(
                state="normal",
                text="Actualizar estado"
            )

    def crear_panel_comentarios(
        self,
        master,
        fila
    ):
        panel = ctk.CTkFrame(
            master,
            fg_color="#F8FAFC",
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

        ctk.CTkLabel(
            panel,
            text="Comentarios y seguimiento",
            font=("Arial", 18, "bold"),
            text_color="#1F2937"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 10)
        )

        # ==============================================
        # CONTENEDOR DE COMENTARIOS
        # ==============================================

        self.frame_comentarios = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )

        self.frame_comentarios.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=(5, 15)
        )

        self.frame_comentarios.grid_columnconfigure(
            0,
            weight=1
        )

        self.cargar_comentarios()

        # ==============================================
        # NUEVO COMENTARIO
        # ==============================================

        ctk.CTkLabel(
            panel,
            text="Agregar comentario",
            font=("Arial", 14, "bold"),
            text_color="#374151"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 5)
        )

        self.texto_comentario = ctk.CTkTextbox(
            panel,
            height=100,
            wrap="word"
        )

        self.texto_comentario.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 10)
        )

        # ==============================================
        # TIPO DE COMENTARIO
        # ==============================================

        acciones = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )

        acciones.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 20)
        )

        rol = self.usuario_sesion["rol"]

        if rol in (
            "Administrador",
            "EncargadoTI",
            "Tecnico"
        ):
            self.tipo_comentario = ctk.StringVar(
                value="Público"
            )

            self.combo_tipo_comentario = ctk.CTkComboBox(
                acciones,
                width=180,
                height=40,
                values=[
                    "Público",
                    "Nota interna"
                ],
                state="readonly",
                variable=self.tipo_comentario
            )

            self.combo_tipo_comentario.pack(
                side="left"
            )

        else:
            self.tipo_comentario = ctk.StringVar(
                value="Público"
            )

        self.boton_comentario = ctk.CTkButton(
            acciones,
            text="Agregar comentario",
            width=180,
            height=40,
            command=self.guardar_comentario
        )

        self.boton_comentario.pack(
            side="right"
        )

    def cargar_comentarios(self):

        for widget in self.frame_comentarios.winfo_children():
            widget.destroy()

        exito, resultado = TicketController.listar_comentarios(
            id_ticket=self.ticket["id_ticket"],
            usuario_sesion=self.usuario_sesion
        )

        if not exito:
            ctk.CTkLabel(
                self.frame_comentarios,
                text=resultado,
                text_color="#C62828"
            ).grid(
                row=0,
                column=0,
                sticky="w",
                pady=10
            )

            return

        if not resultado:
            ctk.CTkLabel(
                self.frame_comentarios,
                text="Todavía no hay comentarios.",
                text_color="#6B7280"
            ).grid(
                row=0,
                column=0,
                sticky="w",
                pady=10
            )

            return

        for indice, comentario in enumerate(resultado):

            privado = not bool(
                comentario["publico"]
            )

            texto_tipo = (
                "NOTA INTERNA"
                if privado
                else "PÚBLICO"
            )

            fecha = comentario["fecha"]

            fecha_texto = (
                fecha.strftime("%d/%m/%Y %H:%M")
                if fecha
                else ""
            )

            tarjeta = ctk.CTkFrame(
                self.frame_comentarios,
                fg_color=(
                    "#FFF7ED"
                    if privado
                    else "#EFF6FF"
                ),
                corner_radius=8
            )

            tarjeta.grid(
                row=indice,
                column=0,
                sticky="ew",
                pady=5
            )

            tarjeta.grid_columnconfigure(
                0,
                weight=1
            )

            encabezado = (
                f"{comentario['usuario']} "
                f"({comentario['rol']})"
            )

            ctk.CTkLabel(
                tarjeta,
                text=encabezado,
                font=("Arial", 13, "bold"),
                anchor="w"
            ).grid(
                row=0,
                column=0,
                sticky="ew",
                padx=15,
                pady=(12, 2)
            )

            ctk.CTkLabel(
                tarjeta,
                text=f"{texto_tipo} • {fecha_texto}",
                font=("Arial", 11),
                text_color="#6B7280",
                anchor="w"
            ).grid(
                row=1,
                column=0,
                sticky="ew",
                padx=15
            )

            ctk.CTkLabel(
                tarjeta,
                text=comentario["comentario"],
                font=("Arial", 13),
                anchor="w",
                justify="left",
                wraplength=850
            ).grid(
                row=2,
                column=0,
                sticky="ew",
                padx=15,
                pady=(8, 12)
            )  

    def guardar_comentario(self):

        comentario = self.texto_comentario.get(
            "1.0",
            "end"
        ).strip()

        tipo = self.tipo_comentario.get()

        publico = tipo == "Público"

        self.boton_comentario.configure(
            state="disabled",
            text="Guardando..."
        )

        try:
            exito, mensaje = TicketController.agregar_comentario(
                id_ticket=self.ticket["id_ticket"],
                comentario=comentario,
                publico=publico,
                usuario_sesion=self.usuario_sesion
            )

            if exito:
                self.texto_comentario.delete(
                    "1.0",
                    "end"
                )

                self.cargar_comentarios()

                messagebox.showinfo(
                    "Correcto",
                    mensaje
                )

            else:
                messagebox.showwarning(
                    "Comentario",
                    mensaje
                )

        finally:
            self.boton_comentario.configure(
                state="normal",
                text="Agregar comentario"
            )

    def crear_panel_historial(
            self,
            master,
            fila
        ):

        panel = ctk.CTkFrame(
            master,
            fg_color="#F9FAFB",
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

        # ==============================================
        # TÍTULO
        # ==============================================

        ctk.CTkLabel(
            panel,
            text="Historial del ticket",
            font=("Arial", 18, "bold"),
            text_color="#1F2937"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            panel,
            text=(
                "Registro cronológico de las actividades "
                "realizadas sobre la incidencia."
            ),
            font=("Arial", 12),
            text_color="#6B7280"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 15)
        )

        # ==============================================
        # CONTENEDOR DEL HISTORIAL
        # ==============================================

        self.frame_historial = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )

        self.frame_historial.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 20)
        )

        self.frame_historial.grid_columnconfigure(
            0,
            weight=1
        )

        self.cargar_historial()

    def cargar_historial(self):

        # Eliminar elementos anteriores
        for widget in self.frame_historial.winfo_children():
            widget.destroy()

        exito, resultado = (
            TicketController.listar_historial(
                id_ticket=self.ticket["id_ticket"]
            )
        )

        if not exito:

            ctk.CTkLabel(
                self.frame_historial,
                text=resultado,
                text_color="#C62828"
            ).grid(
                row=0,
                column=0,
                sticky="w",
                pady=10
            )

            return

        # ==============================================
        # SIN HISTORIAL
        # ==============================================

        if not resultado:

            ctk.CTkLabel(
                self.frame_historial,
                text="No existen movimientos registrados.",
                text_color="#6B7280"
            ).grid(
                row=0,
                column=0,
                sticky="w",
                pady=10
            )

            return

        # ==============================================
        # MOSTRAR MOVIMIENTOS
        # ==============================================

        for indice, movimiento in enumerate(resultado):

            fecha = movimiento["fecha"]

            fecha_texto = (
                fecha.strftime("%d/%m/%Y %H:%M")
                if fecha
                else "Sin fecha"
            )

            tarjeta = ctk.CTkFrame(
                self.frame_historial,
                fg_color="white",
                corner_radius=8,
                border_width=1,
                border_color="#E5E7EB"
            )

            tarjeta.grid(
                row=indice,
                column=0,
                sticky="ew",
                pady=5
            )

            tarjeta.grid_columnconfigure(
                1,
                weight=1
            )

            # ==========================================
            # INDICADOR
            # ==========================================

            indicador = ctk.CTkLabel(
                tarjeta,
                text="●",
                width=30,
                font=("Arial", 18),
                text_color="#1565C0"
            )

            indicador.grid(
                row=0,
                column=0,
                rowspan=3,
                padx=(12, 5),
                pady=10
            )

            # ==========================================
            # ACCIÓN
            # ==========================================

            ctk.CTkLabel(
                tarjeta,
                text=movimiento["accion"],
                font=("Arial", 13, "bold"),
                text_color="#1F2937",
                anchor="w"
            ).grid(
                row=0,
                column=1,
                sticky="ew",
                padx=(5, 15),
                pady=(10, 2)
            )

            # ==========================================
            # USUARIO
            # ==========================================

            usuario_texto = (
                f"{movimiento['usuario']} "
                f"({movimiento['rol']})"
            )

            ctk.CTkLabel(
                tarjeta,
                text=usuario_texto,
                font=("Arial", 12),
                text_color="#4B5563",
                anchor="w"
            ).grid(
                row=1,
                column=1,
                sticky="ew",
                padx=(5, 15)
            )

            # ==========================================
            # FECHA
            # ==========================================

            ctk.CTkLabel(
                tarjeta,
                text=fecha_texto,
                font=("Arial", 11),
                text_color="#9CA3AF",
                anchor="w"
            ).grid(
                row=2,
                column=1,
                sticky="ew",
                padx=(5, 15),
                pady=(2, 10)
            )

    def crear_panel_confirmacion(
        self,
        master,
        fila
    ):
        panel = ctk.CTkFrame(
            master,
            fg_color="#FEFCE8",
            corner_radius=10,
            border_width=1,
            border_color="#FACC15"
        )

        panel.grid(
            row=fila,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=25,
            pady=(10, 30)
        )

        panel.grid_columnconfigure(0, weight=1)

        # ==========================================
        # TÍTULO
        # ==========================================

        ctk.CTkLabel(
            panel,
            text="Confirmación de solución",
            font=("Arial", 18, "bold"),
            text_color="#854D0E"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            panel,
            text=(
                "El técnico indicó que el problema "
                "ya fue solucionado."
            ),
            font=("Arial", 14),
            text_color="#713F12"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 2)
        )

        ctk.CTkLabel(
            panel,
            text="¿El problema quedó resuelto correctamente?",
            font=("Arial", 14, "bold"),
            text_color="#713F12"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 15)
        )

        # ==========================================
        # CONTENEDOR DE BOTONES
        # ==========================================

        botones = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )

        botones.grid(
            row=3,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 20)
        )

        # ==========================================
        # BOTÓN CONFIRMAR
        # ==========================================

        self.boton_confirmar = ctk.CTkButton(
            botones,
            text="Sí, quedó solucionado",
            width=220,
            height=42,
            fg_color="#16A34A",
            hover_color="#15803D",
            command=self.confirmar_solucion
        )

        self.boton_confirmar.grid(
            row=0,
            column=0,
            padx=(0, 10)
        )

        # ==========================================
        # BOTÓN RECHAZAR
        # ==========================================

        self.boton_rechazar = ctk.CTkButton(
            botones,
            text="No, el problema continúa",
            width=220,
            height=42,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.rechazar_solucion
        )

        self.boton_rechazar.grid(
            row=0,
            column=1,
            padx=(10, 0)
        )

    def confirmar_solucion(self):

        confirmar = messagebox.askyesno(
            "Confirmar solución",
            (
                "¿Confirma que el problema quedó "
                "solucionado correctamente?\n\n"
                "Al continuar, el ticket será cerrado."
            )
        )

        if not confirmar:
            return

        self.boton_confirmar.configure(
            state="disabled",
            text="Confirmando..."
        )

        self.boton_rechazar.configure(
            state="disabled"
        )

        try:

            exito, mensaje = (
                TicketController.confirmar_solucion(
                    id_ticket=self.ticket["id_ticket"],
                    confirmado=True,
                    usuario_sesion=self.usuario_sesion
                )
            )

            if exito:

                messagebox.showinfo(
                    "Ticket cerrado",
                    mensaje
                )

                self.regresar_callback()
                return

            else:

                messagebox.showerror(
                    "Error",
                    mensaje
                )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Ocurrió un error al confirmar la solución.\n\n{error}"
            )

        finally:

            try:
                if self.boton_confirmar.winfo_exists():

                    self.boton_confirmar.configure(
                        state="normal",
                        text="Sí, quedó solucionado"
                    )

                if self.boton_rechazar.winfo_exists():

                    self.boton_rechazar.configure(
                        state="normal"
                    )

            except Exception:
                pass

    def rechazar_solucion(self):    

        confirmar = messagebox.askyesno(
            "Problema no solucionado",
            (
                "¿Confirma que el problema continúa?\n\n"
                "El ticket regresará al estado "
                "'En Proceso' para que el técnico "
                "continúe trabajando."
            )
        )

        if not confirmar:
            return

        self.boton_confirmar.configure(
            state="disabled"
        )

        self.boton_rechazar.configure(
            state="disabled",
            text="Procesando..."
        )

        try:

            exito, mensaje = (
                TicketController.confirmar_solucion(
                    id_ticket=self.ticket["id_ticket"],
                    confirmado=False,
                    usuario_sesion=self.usuario_sesion
                )
            )

            if exito:

                messagebox.showinfo(
                    "Ticket reabierto",
                    mensaje
                )

                self.regresar_callback()
                return

            else:

                messagebox.showerror(
                    "Error",
                    mensaje
                )

        except Exception as error:

            messagebox.showerror(
                "Error",
                (
                    "Ocurrió un error al rechazar "
                    f"la solución.\n\n{error}"
                )
            )

        finally:

            try:

                if self.boton_confirmar.winfo_exists():

                    self.boton_confirmar.configure(
                        state="normal"
                    )

                if self.boton_rechazar.winfo_exists():

                    self.boton_rechazar.configure(
                        state="normal",
                        text="No, el problema continúa"
                    )

            except Exception:
                pass            