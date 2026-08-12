import customtkinter as ctk
from tkinter import messagebox
from config.estilos import (
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_OSCURO,
    COLOR_PRIMARIO_HOVER,
    COLOR_FONDO,
    COLOR_PANEL,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE,
    COLOR_EXITO,
    COLOR_EXITO_HOVER,
    COLOR_ADVERTENCIA,
    COLOR_ERROR,
    COLOR_ERROR_HOVER,
    COLOR_NEUTRO,
    COLOR_NEUTRO_HOVER,
    FUENTE_TITULO,
    FUENTE_SUBTITULO,
    FUENTE_SECCION,
    FUENTE_NORMAL,
    FUENTE_PEQUENA,
    ALTO_BOTON,
    RADIO_PANEL
)


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
            padx=30,
            pady=(25, 15)
        )

        ctk.CTkButton(
            encabezado,
            text="← Regresar",
            width=120,
            height=ALTO_BOTON,
            fg_color=COLOR_NEUTRO,
            hover_color=COLOR_NEUTRO_HOVER,
            command=self.regresar_callback
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            encabezado,
            text="Detalle del ticket",
            font=FUENTE_TITULO,
            text_color=COLOR_TEXTO
        ).pack(
            side="left",
            padx=20
        )

        # ----------------------------------------------
        # CONTENEDOR PRINCIPAL
        # ----------------------------------------------

        contenedor = ctk.CTkScrollableFrame(
            self,
            fg_color=COLOR_PANEL,
            corner_radius=RADIO_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
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

        estado = self.ticket["estado"]

        colores_estado = {
            "Nuevo": (
                "#EFF6FF",
                "#1E40AF"
            ),
            "Asignado": (
                "#EEF2FF",
                "#3730A3"
            ),
            "En Proceso": (
                "#FEF3C7",
                "#92400E"
            ),
            "En Espera": (
                "#FFEDD5",
                "#9A3412"
            ),
            "Solucionado": (
                "#DCFCE7",
                "#166534"
            ),
            "Cerrado": (
                "#F3F4F6",
                "#6B7280"
            )
        }

        color_fondo_estado, color_texto_estado = (
            colores_estado.get(
                estado,
                (
                    "#F8FAFC",
                    COLOR_TEXTO
                )
            )
        )

        self.crear_campo_color(
            contenedor,
            estado,
            color_fondo_estado,
            color_texto_estado,
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

        prioridad = self.ticket["prioridad"]

        colores_prioridad = {
                "Baja": (
                    "#DCFCE7",
                    "#166534"
                ),
                "Media": (
                    "#DBEAFE",
                    "#1D4ED8"
                ),
                "Alta": (
                    "#FEF3C7",
                    "#92400E"
                ),
                "Urgente": (
                    "#FEE2E2",
                    "#991B1B"
                )
            }

        color_fondo_prioridad, color_texto_prioridad = (
                colores_prioridad.get(
                    prioridad,
                    (
                        "#F8FAFC",
                        COLOR_TEXTO
                    )
                )
            )

        self.crear_campo_color(
                contenedor,
                prioridad,
                color_fondo_prioridad,
                color_texto_prioridad,
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

        if (
            self.usuario_sesion["rol"] in (
                "Administrador",
                "EncargadoTI"
            )
            and self.ticket["estado"] != "Cerrado"
        ):
            self.crear_panel_asignacion(
                contenedor,
                fila=12
            )

        # ==============================================
        # CAMBIO DE ESTADO
        # ==============================================

        if (
            self.usuario_sesion["rol"] in (
                "Tecnico",
                "Administrador",
                "EncargadoTI"
            )
            and self.ticket["estado"] != "Cerrado"
        ):
            self.crear_panel_estado(
                contenedor,
                fila=13
            )


        # ==============================================
        # COMENTARIOS
        # ==============================================

        self.crear_panel_comentarios(
            contenedor,
            fila=14
        )


       # CONFIRMACIÓN
       
        if (
            self.usuario_sesion["rol"] == "Empleado"
            and self.ticket["estado"] == "Solucionado"
            and self.ticket["id_usuario"]
                == self.usuario_sesion["id_usuario"]
        ):
            self.crear_panel_confirmacion(
                contenedor,
                fila=15
            )

            fila_historial = 16
        else:
            fila_historial = 15

        # HISTORIAL
        self.crear_panel_historial(
            contenedor,
            fila=fila_historial
        )

    def crear_campo_color(
        self,
        master,
        texto,
        color_fondo,
        color_texto,
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
            fg_color=color_fondo,
            text_color=color_texto,
            anchor="center",
            font=("Arial", 13, "bold")
        )

        campo.grid(
            row=fila,
            column=columna,
            columnspan=columnas,
            sticky="ew",
            padx=padx,
            pady=(0, 5)
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
            font=("Arial", 12, "bold"),
            text_color=COLOR_TEXTO_SECUNDARIO,
            anchor="w"
        )

        etiqueta.grid(
            row=fila,
            column=columna,
            columnspan=columnas,
            sticky="ew",
            padx=padx,
            pady=(18, 4)
        )

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
            fg_color="#F8FAFC",
            text_color=COLOR_TEXTO,
            anchor="w",
            padx=12
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
            fg_color=COLOR_PANEL,
            corner_radius=RADIO_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )

        panel.grid(
            row=fila,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=25,
            pady=(10, 25)
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
            text="Asignación de técnico",
            font=FUENTE_SECCION,
            text_color=COLOR_TEXTO
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=20,
            pady=(18, 12)
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
            border_color=COLOR_BORDE,
            button_color=COLOR_PRIMARIO,
            button_hover_color=COLOR_PRIMARIO_HOVER
        )

        self.combo_tecnico.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=(0, 20)
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
            width=170,
            height=ALTO_BOTON,
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_HOVER,
            command=self.asignar_tecnico
        )

        self.boton_asignar.grid(
            row=1,
            column=1,
            padx=(10, 20),
            pady=(0, 20)
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
            fg_color=COLOR_PANEL,
            corner_radius=RADIO_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )

        panel.grid(
            row=fila,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=25,
            pady=(10, 25)
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
            font=FUENTE_SECCION,
            text_color=COLOR_TEXTO
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=20,
            pady=(18, 12)
        )

        estado_actual = self.ticket["estado"]

        transiciones = {
            "Asignado": [
                "En Proceso"
            ],

            "En Proceso": [
                "En Espera",
                "Solucionado"
            ],

            "En Espera": [
                "En Proceso"
            ],

            "Solucionado": []
        }

        estados = transiciones.get(
            estado_actual,
            []
        )

        if not estados:

            ctk.CTkLabel(
                panel,
                text=(
                    "No existen cambios de estado "
                    "disponibles para este ticket."
                ),
                font=("Arial", 13),
                text_color=COLOR_TEXTO_SECUNDARIO
            ).grid(
                row=1,
                column=0,
                columnspan=2,
                sticky="w",
                padx=20,
                pady=(0, 20)
            )

            return

        self.combo_estado_ticket = ctk.CTkComboBox(
            panel,
            values=estados,
            state="readonly",
            height=40,
            border_color=COLOR_BORDE,
            button_color=COLOR_PRIMARIO,
            button_hover_color=COLOR_PRIMARIO_HOVER
        )

        self.combo_estado_ticket.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=(0, 20)
        )

        self.combo_estado_ticket.set(
            estados[0]
        )

        self.boton_estado = ctk.CTkButton(
            panel,
            text="Actualizar estado",
            width=170,
            height=ALTO_BOTON,
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_HOVER,
            command=self.actualizar_estado
        )

        self.boton_estado.grid(
            row=1,
            column=1,
            padx=(10, 20),
            pady=(0, 20)
        )

    def actualizar_estado(self):
        nuevo_estado = (
            self.combo_estado_ticket.get()
        )

        if not nuevo_estado:
            messagebox.showwarning(
                "Estado",
                "Seleccione un estado."
            )
            return

        confirmar = messagebox.askyesno(
            "Actualizar estado",
            (
                "¿Desea cambiar el estado del ticket "
                f"a '{nuevo_estado}'?"
            )
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

                self.regresar_callback()

            else:

                messagebox.showerror(
                    "Error",
                    mensaje
                )

        finally:

            if self.boton_estado.winfo_exists():

                self.boton_estado.configure(
                    state="normal",
                    text="Actualizar estado"
                )

    def crear_panel_comentarios(
                self,
                master,
                fila
            ):
    
                # ==============================================
                # DATOS DE CONTROL
                # ==============================================
    
                rol = self.usuario_sesion["rol"]
    
                ticket_cerrado = (
                    self.ticket["estado"] == "Cerrado"
                )
    
                # ==============================================
                # PANEL PRINCIPAL
                # ==============================================
    
                panel = ctk.CTkFrame(
                    master,
                    fg_color=COLOR_PANEL,
                    corner_radius=RADIO_PANEL,
                    border_width=1,
                    border_color=COLOR_BORDE
                )
    
                panel.grid(
                    row=fila,
                    column=0,
                    columnspan=2,
                    sticky="ew",
                    padx=25,
                    pady=(10, 25)
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
                    text="Comentarios y seguimiento",
                    font=FUENTE_SECCION,
                    text_color=COLOR_TEXTO
                ).grid(
                    row=0,
                    column=0,
                    sticky="w",
                    padx=20,
                    pady=(18, 10)
                )
    
                # ==============================================
                # CONTENEDOR DE COMENTARIOS EXISTENTES
                # ==============================================
    
                self.frame_comentarios = ctk.CTkFrame(
                    panel,
                    fg_color="#F8FAFC",
                    corner_radius=8,
                    border_width=1,
                    border_color=COLOR_BORDE
                )
    
                self.frame_comentarios.grid(
                    row=1,
                    column=0,
                    sticky="ew",
                    padx=20,
                    pady=(0, 18)
                )
    
                self.frame_comentarios.grid_columnconfigure(
                    0,
                    weight=1
                )
    
                # Cargar comentarios existentes
                self.cargar_comentarios()
    
                # ==============================================
                # NUEVO COMENTARIO
                # ==============================================
    
                ctk.CTkLabel(
                    panel,
                    text="Agregar comentario",
                    font=("Arial", 13, "bold"),
                    text_color=COLOR_TEXTO
                ).grid(
                    row=2,
                    column=0,
                    sticky="w",
                    padx=20,
                    pady=(5, 6)
                )
    
                self.texto_comentario = ctk.CTkTextbox(
                    panel,
                    height=110,
                    wrap="word",
                    font=("Arial", 13),
                    fg_color="#F8FAFC",
                    border_width=1,
                    border_color=COLOR_BORDE
                )
    
                self.texto_comentario.grid(
                    row=3,
                    column=0,
                    sticky="ew",
                    padx=20,
                    pady=(0, 12)
                )
    
                # Si el ticket está cerrado no se puede escribir
                if ticket_cerrado:
                    self.texto_comentario.configure(
                        state="disabled"
                    )
    
                # ==============================================
                # ACCIONES
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
    
                # ==============================================
                # TIPO DE COMENTARIO
                # ==============================================
    
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
                        variable=self.tipo_comentario,
                        border_color=COLOR_BORDE,
                        button_color=COLOR_PRIMARIO,
                        button_hover_color=COLOR_PRIMARIO_HOVER
                    )
    
                    self.combo_tipo_comentario.pack(
                        side="left"
                    )
    
                    # Si está cerrado tampoco cambiar el tipo
                    if ticket_cerrado:
                        self.combo_tipo_comentario.configure(
                            state="disabled"
                        )
    
                else:
    
                    self.tipo_comentario = ctk.StringVar(
                        value="Público"
                    )
    
                # ==============================================
                # BOTÓN AGREGAR COMENTARIO
                # ==============================================
    
                self.boton_comentario = ctk.CTkButton(
                    acciones,
                    text="Agregar comentario",
                    width=180,
                    height=ALTO_BOTON,
                    fg_color=COLOR_PRIMARIO,
                    hover_color=COLOR_PRIMARIO_HOVER,
                    command=self.guardar_comentario
                )
    
                self.boton_comentario.pack(
                    side="right"
                )
    
                # ==============================================
                # TICKET CERRADO
                # ==============================================
    
                if ticket_cerrado:
    
                    self.boton_comentario.configure(
                        state="disabled",
                        text="Ticket cerrado"
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

        # ==============================================
        # PANEL PRINCIPAL
        # ==============================================

        panel = ctk.CTkFrame(
            master,
            fg_color=COLOR_PANEL,
            corner_radius=RADIO_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
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
            font=FUENTE_SECCION,
            text_color=COLOR_TEXTO
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 4)
        )

        ctk.CTkLabel(
            panel,
            text=(
                "Registro cronológico de las actividades "
                "realizadas sobre la incidencia."
            ),
            font=FUENTE_PEQUENA,
            text_color=COLOR_TEXTO_SECUNDARIO
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
            fg_color="#F8FAFC",
            corner_radius=8,
            border_width=1,
            border_color=COLOR_BORDE
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
                fg_color=COLOR_PANEL,
                corner_radius=8,
                border_width=1,
                border_color=COLOR_BORDE
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

            ctk.CTkLabel(
                tarjeta,
                text=movimiento["accion"],
                font=("Arial", 13, "bold"),
                text_color=COLOR_TEXTO,
                anchor="w"
            ).grid(
                row=0,
                column=1,
                sticky="ew",
                padx=(5, 15),
                pady=(10, 2)
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
                text_color=COLOR_TEXTO_SECUNDARIO,
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

            # ==============================================
            # PANEL PRINCIPAL
            # ==============================================

            panel = ctk.CTkFrame(
                master,
                fg_color=COLOR_PANEL,
                corner_radius=RADIO_PANEL,
                border_width=1,
                border_color=COLOR_ADVERTENCIA
            )

            panel.grid(
                row=fila,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=25,
                pady=(10, 25)
            )

            panel.grid_columnconfigure(
                0,
                weight=1
            )

            # ==============================================
            # ENCABEZADO
            # ==============================================

            encabezado = ctk.CTkFrame(
                panel,
                fg_color="transparent"
            )

            encabezado.grid(
                row=0,
                column=0,
                sticky="ew",
                padx=20,
                pady=(18, 8)
            )

            ctk.CTkLabel(
                encabezado,
                text="Confirmación de solución",
                font=FUENTE_SECCION,
                text_color=COLOR_TEXTO
            ).pack(
                side="left"
            )

            # Indicador visual
            ctk.CTkLabel(
                encabezado,
                text="Pendiente de confirmación",
                font=("Arial", 11, "bold"),
                fg_color="#FEF3C7",
                text_color="#92400E",
                corner_radius=8,
                padx=10,
                pady=4
            ).pack(
                side="right"
            )

            # ==============================================
            # MENSAJE INFORMATIVO
            # ==============================================

            mensaje = ctk.CTkFrame(
                panel,
                fg_color="#FFFBEB",
                corner_radius=8
            )

            mensaje.grid(
                row=1,
                column=0,
                sticky="ew",
                padx=20,
                pady=(0, 15)
            )

            ctk.CTkLabel(
                mensaje,
                text=(
                    "El técnico indicó que el problema "
                    "ya fue solucionado."
                ),
                font=FUENTE_NORMAL,
                text_color=COLOR_TEXTO,
                anchor="w"
            ).pack(
                fill="x",
                padx=15,
                pady=(12, 4)
            )

            ctk.CTkLabel(
                mensaje,
                text=(
                    "Confirma si la incidencia quedó "
                    "resuelta correctamente."
                ),
                font=("Arial", 13),
                text_color=COLOR_TEXTO_SECUNDARIO,
                anchor="w"
            ).pack(
                fill="x",
                padx=15,
                pady=(0, 12)
            )

            # ==============================================
            # PREGUNTA
            # ==============================================

            ctk.CTkLabel(
                panel,
                text="¿El problema quedó resuelto correctamente?",
                font=("Arial", 14, "bold"),
                text_color=COLOR_TEXTO
            ).grid(
                row=2,
                column=0,
                sticky="w",
                padx=20,
                pady=(0, 15)
            )

            # ==============================================
            # BOTONES
            # ==============================================

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

            self.boton_confirmar = ctk.CTkButton(
                botones,
                text="Sí, quedó solucionado",
                width=220,
                height=ALTO_BOTON,
                fg_color=COLOR_EXITO,
                hover_color=COLOR_EXITO_HOVER,
                command=self.confirmar_solucion
            )

            self.boton_confirmar.grid(
                row=0,
                column=0,
                padx=(0, 10)
            )

            self.boton_rechazar = ctk.CTkButton(
                botones,
                text="No, el problema continúa",
                width=220,
                height=ALTO_BOTON,
                fg_color=COLOR_ERROR,
                hover_color=COLOR_ERROR_HOVER,
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