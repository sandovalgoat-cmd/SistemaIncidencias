import customtkinter as ctk
from tkinter import messagebox

from views.catalogos import VistaCatalogos
from views.usuarios import VistaUsuarios
from views.nuevo_ticket import VistaNuevoTicket
from views.tickets import VistaTickets
from views.reportes import VistaReportes

from controllers.ticket_controller import TicketController

from config.estilos import (
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_OSCURO,
    COLOR_PRIMARIO_HOVER,
    COLOR_SIDEBAR,
    COLOR_SIDEBAR_HOVER,
    COLOR_TOPBAR,
    COLOR_TOPBAR_HOVER,
    COLOR_FONDO,
    COLOR_PANEL,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_ERROR,
    COLOR_ERROR_HOVER,
    COLOR_NEUTRO,
    FUENTE_TITULO,
    FUENTE_SUBTITULO,
    FUENTE_MENU,
    FUENTE_MENU_TITULO,
    FUENTE_NUMERO_TARJETA,
    ANCHO_SIDEBAR,
    ALTO_BOTON,
    RADIO_TARJETA
)

class Dashboard(ctk.CTkToplevel):

    def __init__(self, ventana_login, usuario):

        super().__init__()

        self.ventana_login = ventana_login
        self.usuario = usuario

        self.title("Sistema de Atención de Incidencias")
        self.geometry("1350x780")
        self.minsize(1100, 650)

        # Al cerrar la ventana desde la X
        self.protocol("WM_DELETE_WINDOW", self.cerrar_sistema)

        self.crear_interfaz()
        self.mostrar_inicio()

        self.after(100, self.focus_force)

    def crear_interfaz(self):

        # ==============================================
        # CONFIGURACIÓN GENERAL
        # ==============================================

        self.configure(
            fg_color=COLOR_FONDO
        )

        self.grid_columnconfigure(
            0,
            weight=0
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=0
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        # ==============================================
        # MENÚ LATERAL
        # ==============================================

        self.menu_lateral = ctk.CTkFrame(
            self,
            width=ANCHO_SIDEBAR,
            corner_radius=0,
            fg_color=COLOR_SIDEBAR
        )

        self.menu_lateral.grid(
            row=0,
            column=0,
            rowspan=2,
            sticky="nsew"
        )

        self.menu_lateral.grid_propagate(
            False
        )

        # ==============================================
        # LOGO / NOMBRE DEL SISTEMA
        # ==============================================

        ctk.CTkLabel(
            self.menu_lateral,
            text="Sistema de\nIncidencias",
            font=FUENTE_MENU_TITULO,
            text_color="white",
            justify="left"
        ).pack(
            anchor="w",
            padx=22,
            pady=(28, 10)
        )

        # ==============================================
        # USUARIO
        # ==============================================

        nombre_completo = (
            f"{self.usuario['nombre']} "
            f"{self.usuario['apellido']}"
        )

        ctk.CTkLabel(
            self.menu_lateral,
            text=nombre_completo,
            font=("Arial", 15, "bold"),
            text_color="white"
        ).pack(
            anchor="w",
            padx=22,
            pady=(18, 2)
        )

        ctk.CTkLabel(
            self.menu_lateral,
            text=self.usuario["rol"],
            font=("Arial", 12),
            text_color="#CBD5E1"
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 25)
        )

        # Línea separadora
        ctk.CTkFrame(
            self.menu_lateral,
            height=1,
            fg_color="#475569"
        ).pack(
            fill="x",
            padx=18,
            pady=(0, 15)
        )

        # ==============================================
        # OPCIONES DEL MENÚ
        # ==============================================

        self.crear_boton_menu(
            "Inicio",
            self.mostrar_inicio
        )

        self.crear_menu_por_rol()

        # ==============================================
        # CERRAR SESIÓN
        # ==============================================

        boton_salir = ctk.CTkButton(
            self.menu_lateral,
            text="Cerrar sesión",
            height=ALTO_BOTON,
            fg_color=COLOR_ERROR,
            hover_color=COLOR_ERROR_HOVER,
            text_color="white",
            font=FUENTE_MENU,
            command=self.cerrar_sesion
        )

        boton_salir.pack(
            side="bottom",
            fill="x",
            padx=18,
            pady=22
        )

        # ==============================================
        # BARRA SUPERIOR
        # ==============================================

        self.barra_superior = ctk.CTkFrame(
            self,
            height=60,
            corner_radius=0,
            fg_color=COLOR_TOPBAR
        )

        self.barra_superior.grid(
            row=0,
            column=1,
            sticky="ew"
        )

        self.barra_superior.grid_propagate(
            False
        )

        # Nombre de sección / aplicación
        ctk.CTkLabel(
            self.barra_superior,
            text="Sistema de Atención de Incidencias",
            font=("Arial", 18, "bold"),
            text_color="white"
        ).pack(
            side="left",
            padx=25
        )

        # Usuario en esquina derecha
        ctk.CTkLabel(
            self.barra_superior,
            text=nombre_completo,
            font=("Arial", 13),
            text_color="white"
        ).pack(
            side="right",
            padx=25
        )

        # ==============================================
        # ÁREA PRINCIPAL
        # ==============================================

        self.contenido = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=COLOR_FONDO
        )

        self.contenido.grid(
            row=1,
            column=1,
            sticky="nsew"
        )

    def crear_boton_menu(
        self,
        texto,
        comando
    ):

        boton = ctk.CTkButton(
            self.menu_lateral,
            text=texto,
            height=ALTO_BOTON,
            anchor="w",
            fg_color="transparent",
            hover_color=COLOR_SIDEBAR_HOVER,
            text_color="white",
            font=FUENTE_MENU,
            corner_radius=6,
            command=comando
        )

        boton.pack(
            fill="x",
            padx=12,
            pady=3
        )

    def crear_menu_por_rol(self):

        rol = self.usuario["rol"]

        # ----------------------------------------------
        # ADMINISTRADOR
        # ----------------------------------------------

        if rol == "Administrador":

            self.crear_boton_menu(
                "Usuarios",
                self.mostrar_usuarios
            )

            self.crear_boton_menu(
                "Nuevo ticket",
                self.mostrar_nuevo_ticket
            )

            self.crear_boton_menu(
                "Todos los tickets",
                self.mostrar_tickets
            )

            self.crear_boton_menu(
                "Catálogos",
                self.mostrar_catalogos
            )

            self.crear_boton_menu(
                "Reportes",
                self.mostrar_reportes
            )

        # ----------------------------------------------
        # ENCARGADO DE TI
        # ----------------------------------------------

        elif rol == "EncargadoTI":

            self.crear_boton_menu(
             "Usuarios",
             self.mostrar_usuarios
            )    

            self.crear_boton_menu(
                "Nuevo ticket",
                self.mostrar_nuevo_ticket
            )

            self.crear_boton_menu(
                "Todos los tickets",
                self.mostrar_tickets
            )

            self.crear_boton_menu(
                "Asignar técnicos",
                self.mostrar_asignaciones
            )

            self.crear_boton_menu(
                "Estadísticas",
                self.mostrar_reportes
            )

        # ----------------------------------------------
        # TÉCNICO
        # ----------------------------------------------

        elif rol == "Tecnico":

            self.crear_boton_menu(
                "Mis tickets asignados",
                self.mostrar_tickets
            )

            self.crear_boton_menu(
                "Historial",
                self.mostrar_historial
            )

        # ----------------------------------------------
        # EMPLEADO
        # ----------------------------------------------

        elif rol == "Empleado":

            self.crear_boton_menu(
                "Nuevo ticket",
                self.mostrar_nuevo_ticket
            )

            self.crear_boton_menu(
                "Mis tickets",
                self.mostrar_tickets
            )

    def limpiar_contenido(self):

        for widget in self.contenido.winfo_children():
            widget.destroy()

    def crear_titulo(
        self,
        texto
    ):

        titulo = ctk.CTkLabel(
            self.contenido,
            text=texto,
            font=FUENTE_TITULO,
            text_color=COLOR_TEXTO
        )

        titulo.pack(
            anchor="w",
            padx=35,
            pady=(30, 15)
        )

    def mostrar_inicio(self):

        self.limpiar_contenido()

        self.crear_titulo(
            "Panel principal"
        )

        bienvenida = ctk.CTkLabel(
            self.contenido,
            text=(
                f"Bienvenido, "
                f"{self.usuario['nombre']} "
                f"{self.usuario['apellido']}"
            ),
            font=FUENTE_SUBTITULO,
            text_color=COLOR_TEXTO
        )

        bienvenida.pack(
            anchor="w",
            padx=35,
            pady=(0, 4)
        )

        descripcion = ctk.CTkLabel(
            self.contenido,
            text=(
                "Resumen general de la actividad "
                "del sistema."
            ),
            font=("Arial", 14),
            text_color=COLOR_TEXTO_SECUNDARIO
        )

        descripcion.pack(
            anchor="w",
            padx=35,
            pady=(0, 10)
        )

        self.crear_tarjetas_inicio()

        if self.usuario["rol"] in (
            "Administrador",
            "EncargadoTI"
        ):
            self.crear_resumen_operativo()

    def crear_tarjetas_inicio(self):

        contenedor = ctk.CTkFrame(
            self.contenido,
            fg_color="transparent"
        )

        contenedor.pack(
            fill="x",
            padx=40,
            pady=35
        )

        # ==============================================
        # IDENTIFICAR ROL
        # ==============================================

        rol = self.usuario["rol"]

        # ==============================================
        # ADMINISTRADOR / ENCARGADO TI
        # ==============================================

        if rol in (
            "Administrador",
            "EncargadoTI"
        ):

            exito, resultado = (
                TicketController.obtener_estadisticas(
                    self.usuario
                )
            )

            if exito:
                nuevos = resultado["nuevos"]
                en_proceso = resultado["en_proceso"]
                urgentes = resultado["urgentes"]
                cerrados = resultado["cerrados"]

            else:
                nuevos = 0
                en_proceso = 0
                urgentes = 0
                cerrados = 0

            exito_metricas, metricas = (
                TicketController.obtener_metricas_dashboard(
                    self.usuario
                )
            )

            if exito_metricas:
                total = metricas["total"]
                sin_asignar = metricas["sin_asignar"]
                pendientes = metricas[
                    "pendientes_confirmacion"
                ]

            else:
                total = 0
                sin_asignar = 0
                pendientes = 0

            tarjetas = [
                ("Total de tickets", total),
                ("Tickets nuevos", nuevos),
                ("En proceso", en_proceso),
                ("Urgentes", urgentes),
                ("Cerrados", cerrados),
                ("Sin asignar", sin_asignar),
                ("Por confirmar", pendientes)
            ]

        # ==============================================
        # TÉCNICO
        # ==============================================

        elif rol == "Tecnico":

            exito, metricas = (
                TicketController.obtener_metricas_por_usuario(
                    self.usuario
                )
            )

            if exito:
                tarjetas = [
                    ("Mis tickets", metricas["total"]),
                    ("Asignados", metricas["asignados"]),
                    ("En proceso", metricas["en_proceso"]),
                    ("En espera", metricas["en_espera"]),
                    ("Solucionados", metricas["solucionados"])
                ]

            else:
                tarjetas = [
                    ("Mis tickets", 0),
                    ("Asignados", 0),
                    ("En proceso", 0),
                    ("En espera", 0),
                    ("Solucionados", 0)
                ]

        # ==============================================
        # EMPLEADO
        # ==============================================

        elif rol == "Empleado":

            exito, metricas = (
                TicketController.obtener_metricas_por_usuario(
                    self.usuario
                )
            )

            if exito:
                tarjetas = [
                    ("Mis tickets", metricas["total"]),
                    ("Nuevos", metricas["nuevos"]),
                    ("En proceso", metricas["en_proceso"]),
                    ("Solucionados", metricas["solucionados"]),
                    ("Cerrados", metricas["cerrados"])
                ]

            else:
                tarjetas = [
                    ("Mis tickets", 0),
                    ("Nuevos", 0),
                    ("En proceso", 0),
                    ("Solucionados", 0),
                    ("Cerrados", 0)
                ]

        else:
            tarjetas = []

        # ==============================================
        # CONFIGURAR COLUMNAS
        # ==============================================

        for columna in range(4):

            contenedor.grid_columnconfigure(
                columna,
                weight=1
            )

        # ==============================================
        # DIBUJAR TARJETAS
        # ==============================================

        for indice, datos in enumerate(tarjetas):

            fila = indice // 4
            columna = indice % 4

            tarjeta = ctk.CTkFrame(
                contenedor,
                height=120,
                corner_radius=RADIO_TARJETA,
                fg_color=COLOR_PANEL,
                border_width=1,
                border_color="#E5E7EB"
            )

            tarjeta.grid(
                row=fila,
                column=columna,
                padx=8,
                pady=8,
                sticky="nsew"
            )

            etiqueta = ctk.CTkLabel(
                tarjeta,
                text=str(datos[0]),
                font=("Arial", 13),
                text_color=COLOR_TEXTO_SECUNDARIO
            )

            etiqueta.pack(
                pady=(22, 5)
            )

            cantidad = ctk.CTkLabel(
                tarjeta,
                text=str(datos[1]),
                font=FUENTE_NUMERO_TARJETA,
                text_color=COLOR_PRIMARIO_OSCURO
            )

            cantidad.pack(
                pady=(0, 18)
            )

    def mostrar_usuarios(self):

        self.limpiar_contenido()

        VistaUsuarios(
            master=self.contenido,
            usuario_sesion=self.usuario
        )

    def mostrar_nuevo_ticket(self):

        self.limpiar_contenido()

        VistaNuevoTicket(
            master=self.contenido,
            usuario_sesion=self.usuario
        )

    def mostrar_tickets(self):

            self.limpiar_contenido()

            VistaTickets(
                master=self.contenido,
                usuario_sesion=self.usuario
            )

    def mostrar_catalogos(self):

        self.limpiar_contenido()

        VistaCatalogos(
            master=self.contenido,
            usuario_sesion=self.usuario
        )

    def mostrar_reportes(self):

        self.limpiar_contenido()

        VistaReportes(
            master=self.contenido,
            usuario_sesion=self.usuario
        )

    def mostrar_asignaciones(self):

        self.limpiar_contenido()
        self.crear_titulo("Asignación de técnicos")

        texto = ctk.CTkLabel(
            self.contenido,
            text=(
                "Aquí el EncargadoTI podrá asignar tickets "
                "a los técnicos."
            ),
            font=("Arial", 17)
        )

        texto.pack(
            padx=40,
            pady=20,
            anchor="w"
        )

    def mostrar_historial(self):

        self.limpiar_contenido()
        self.crear_titulo("Historial de tickets")

        texto = ctk.CTkLabel(
            self.contenido,
            text=(
                "Aquí se mostrará el historial de actividades "
                "del técnico."
            ),
            font=("Arial", 17)
        )

        texto.pack(
            padx=40,
            pady=20,
            anchor="w"
        )

    def cerrar_sesion(self):

        respuesta = messagebox.askyesno(
            "Cerrar sesión",
            "¿Desea cerrar la sesión actual?"
        )

        if not respuesta:
            return

        self.destroy()

        self.ventana_login.deiconify()

        self.ventana_login.usuario.delete(0, "end")
        self.ventana_login.password.delete(0, "end")
        self.ventana_login.usuario.focus()

    def cerrar_sistema(self):

        respuesta = messagebox.askyesno(
            "Salir",
            "¿Desea cerrar completamente el sistema?"
        )

        if respuesta:
            self.ventana_login.destroy()

    def crear_resumen_operativo(self):

        exito, resultado = (
            TicketController.obtener_resumen_dashboard(
                self.usuario
            )
        )

        if not exito:
            print(
                "Error cargando resumen operativo:",
                resultado
            )
            return

        contenedor = ctk.CTkFrame(
            self.contenido,
            fg_color="transparent"
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(0, 35)
        )

        contenedor.grid_columnconfigure(
            0,
            weight=1
        )

        contenedor.grid_columnconfigure(
            1,
            weight=2
        )

        # ==============================================
        # CARGA POR TÉCNICO
        # ==============================================

        panel_tecnicos = ctk.CTkFrame(
            contenedor,
            fg_color="white",
            corner_radius=12
        )

        panel_tecnicos.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        ctk.CTkLabel(
            panel_tecnicos,
            text="Carga de trabajo por técnico",
            font=("Arial", 18, "bold"),
            text_color="#1F2937"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        carga = resultado["carga_tecnicos"]

        if not carga:

            ctk.CTkLabel(
                panel_tecnicos,
                text="No hay técnicos disponibles.",
                text_color="#6B7280"
            ).pack(
                anchor="w",
                padx=20,
                pady=(0, 20)
            )

        else:

            for tecnico in carga:

                fila = ctk.CTkFrame(
                    panel_tecnicos,
                    fg_color="transparent"
                )

                fila.pack(
                    fill="x",
                    padx=20,
                    pady=6
                )

                ctk.CTkLabel(
                    fila,
                    text=tecnico["tecnico"],
                    font=("Arial", 13),
                    text_color="#374151"
                ).pack(
                    side="left"
                )

                ctk.CTkLabel(
                    fila,
                    text=str(tecnico["cantidad"]),
                    font=("Arial", 13, "bold"),
                    text_color="#1565C0"
                ).pack(
                    side="right"
                )

        # ==============================================
        # TICKETS RECIENTES
        # ==============================================

        panel_tickets = ctk.CTkFrame(
            contenedor,
            fg_color="white",
            corner_radius=12
        )

        panel_tickets.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        ctk.CTkLabel(
            panel_tickets,
            text="Tickets recientes",
            font=("Arial", 18, "bold"),
            text_color="#1F2937"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        tickets = resultado["tickets_recientes"]

        if not tickets:

            ctk.CTkLabel(
                panel_tickets,
                text="No hay tickets registrados.",
                text_color="#6B7280"
            ).pack(
                anchor="w",
                padx=20,
                pady=(0, 20)
            )

            return

        for ticket in tickets:

            fecha = ticket["fecha_creacion"]

            fecha_texto = (
                fecha.strftime("%d/%m/%Y %H:%M")
                if fecha
                else ""
            )

            tarjeta = ctk.CTkFrame(
                panel_tickets,
                fg_color="#F9FAFB",
                corner_radius=8
            )

            tarjeta.pack(
                fill="x",
                padx=20,
                pady=5
            )

            ctk.CTkLabel(
                tarjeta,
                text=(
                    f"{ticket['folio']} - "
                    f"{ticket['titulo']}"
                ),
                font=("Arial", 13, "bold"),
                text_color="#1F2937",
                anchor="w"
            ).pack(
                fill="x",
                padx=12,
                pady=(10, 2)
            )

            ctk.CTkLabel(
                tarjeta,
                text=(
                    f"{ticket['estado']} | "
                    f"{ticket['prioridad']} | "
                    f"{ticket['tecnico']} | "
                    f"{fecha_texto}"
                ),
                font=("Arial", 11),
                text_color="#6B7280",
                anchor="w"
            ).pack(
                fill="x",
                padx=12,
                pady=(0, 10)
            )        