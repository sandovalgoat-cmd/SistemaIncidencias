import customtkinter as ctk
from tkinter import messagebox

from views.usuarios import VistaUsuarios
from views.nuevo_ticket import VistaNuevoTicket
from views.tickets import VistaTickets
from controllers.ticket_controller import TicketController

class Dashboard(ctk.CTkToplevel):

    def __init__(self, ventana_login, usuario):

        super().__init__()

        self.ventana_login = ventana_login
        self.usuario = usuario

        self.title("Sistema de Atención de Incidencias")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        # Al cerrar la ventana desde la X
        self.protocol("WM_DELETE_WINDOW", self.cerrar_sistema)

        self.crear_interfaz()
        self.mostrar_inicio()

        self.after(100, self.focus_force)

    # ==================================================
    # CREAR INTERFAZ GENERAL
    # ==================================================

    def crear_interfaz(self):

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==============================================
        # MENÚ LATERAL
        # ==============================================

        self.menu_lateral = ctk.CTkFrame(
            self,
            width=250,
            corner_radius=0,
            fg_color="#1565C0"
        )

        self.menu_lateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.menu_lateral.grid_propagate(False)

        titulo = ctk.CTkLabel(
            self.menu_lateral,
            text="Sistema de\nIncidencias",
            font=("Arial", 25, "bold"),
            text_color="white"
        )

        titulo.pack(pady=(30, 10))

        nombre_completo = (
            f"{self.usuario['nombre']} "
            f"{self.usuario['apellido']}"
        )

        etiqueta_usuario = ctk.CTkLabel(
            self.menu_lateral,
            text=nombre_completo,
            font=("Arial", 16, "bold"),
            text_color="white"
        )

        etiqueta_usuario.pack(pady=(15, 2))

        etiqueta_rol = ctk.CTkLabel(
            self.menu_lateral,
            text=self.usuario["rol"],
            font=("Arial", 13),
            text_color="#DCEBFA"
        )

        etiqueta_rol.pack(pady=(0, 25))

        # Botón disponible para todos
        self.crear_boton_menu(
            "Inicio",
            self.mostrar_inicio
        )

        # Crear opciones según el rol
        self.crear_menu_por_rol()

        # Botón cerrar sesión
        boton_salir = ctk.CTkButton(
            self.menu_lateral,
            text="Cerrar sesión",
            height=42,
            fg_color="#C62828",
            hover_color="#B71C1C",
            command=self.cerrar_sesion
        )

        boton_salir.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=25
        )

        # ==============================================
        # ÁREA DE CONTENIDO PRINCIPAL
        # ==============================================

        self.contenido = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="#F3F6F9"
        )

        self.contenido.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

    # ==================================================
    # CREAR BOTONES DEL MENÚ
    # ==================================================

    def crear_boton_menu(self, texto, comando):

        boton = ctk.CTkButton(
            self.menu_lateral,
            text=texto,
            height=42,
            anchor="w",
            fg_color="transparent",
            hover_color="#0D47A1",
            text_color="white",
            font=("Arial", 15),
            command=comando
        )

        boton.pack(
            fill="x",
            padx=15,
            pady=4
        )

    # ==================================================
    # MENÚ SEGÚN EL ROL
    # ==================================================

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

    # ==================================================
    # LIMPIAR EL ÁREA DE CONTENIDO
    # ==================================================

    def limpiar_contenido(self):

        for widget in self.contenido.winfo_children():
            widget.destroy()

    # ==================================================
    # CREAR TÍTULOS
    # ==================================================

    def crear_titulo(self, texto):

        titulo = ctk.CTkLabel(
            self.contenido,
            text=texto,
            font=("Arial", 30, "bold"),
            text_color="#1F2937"
        )

        titulo.pack(
            anchor="w",
            padx=40,
            pady=(35, 20)
        )

    # ==================================================
    # PANTALLA DE INICIO
    # ==================================================

    def mostrar_inicio(self):

        self.limpiar_contenido()
        self.crear_titulo("Panel principal")

        bienvenida = ctk.CTkLabel(
            self.contenido,
            text=(
                f"Bienvenido, {self.usuario['nombre']} "
                f"{self.usuario['apellido']}"
            ),
            font=("Arial", 22),
            text_color="#374151"
        )

        bienvenida.pack(
            anchor="w",
            padx=40,
            pady=10
        )

        descripcion = ctk.CTkLabel(
            self.contenido,
            text=(
                "Desde este panel puedes acceder a las funciones "
                "disponibles según tu rol."
            ),
            font=("Arial", 15),
            text_color="#6B7280"
        )

        descripcion.pack(
            anchor="w",
            padx=40,
            pady=5
        )

        self.crear_tarjetas_inicio()

    # ==================================================
    # TARJETAS DE RESUMEN
    # ==================================================

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

        # Consultar estadísticas reales
        exito, resultado = TicketController.obtener_estadisticas(
            self.usuario
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

            print(
                "Error cargando estadísticas:",
                resultado
            )

        tarjetas = [
            (
                "Tickets nuevos",
                nuevos
            ),
            (
                "En proceso",
                en_proceso
            ),
            (
                "Urgentes",
                urgentes
            ),
            (
                "Cerrados",
                cerrados
            )
        ]

        for indice, datos in enumerate(tarjetas):

            tarjeta = ctk.CTkFrame(
                contenedor,
                height=130,
                corner_radius=12,
                fg_color="white"
            )

            tarjeta.grid(
                row=0,
                column=indice,
                padx=8,
                sticky="nsew"
            )

            contenedor.grid_columnconfigure(
                indice,
                weight=1
            )

            etiqueta = ctk.CTkLabel(
                tarjeta,
                text=datos[0],
                font=("Arial", 15),
                text_color="#6B7280"
            )

            etiqueta.pack(
                pady=(25, 5)
            )

            cantidad = ctk.CTkLabel(
                tarjeta,
                text=str(datos[1]),
                font=("Arial", 32, "bold"),
                text_color="#1565C0"
            )

            cantidad.pack()

    # ==================================================
    # MÓDULO DE USUARIOS
    # ==================================================

    def mostrar_usuarios(self):

        self.limpiar_contenido()

        VistaUsuarios(
            master=self.contenido,
            usuario_sesion=self.usuario
        )

    # ==================================================
    # MÓDULO PARA REGISTRAR UN TICKET
    # ==================================================

    def mostrar_nuevo_ticket(self):

        self.limpiar_contenido()

        VistaNuevoTicket(
            master=self.contenido,
            usuario_sesion=self.usuario
        )

    # ==================================================
    # MÓDULO DE TICKETS
    # ==================================================

    def mostrar_tickets(self):

            self.limpiar_contenido()

            VistaTickets(
                master=self.contenido,
                usuario_sesion=self.usuario
            )

    # ==================================================
    # CATÁLOGOS
    # ==================================================

    def mostrar_catalogos(self):

        self.limpiar_contenido()
        self.crear_titulo("Catálogos del sistema")

        texto = ctk.CTkLabel(
            self.contenido,
            text=(
                "Aquí se administrarán las categorías, "
                "prioridades, estados, áreas y roles."
            ),
            font=("Arial", 17)
        )

        texto.pack(
            padx=40,
            pady=20,
            anchor="w"
        )

    # ==================================================
    # REPORTES
    # ==================================================

    def mostrar_reportes(self):

        self.limpiar_contenido()
        self.crear_titulo("Reportes y estadísticas")

        texto = ctk.CTkLabel(
            self.contenido,
            text=(
                "Aquí se mostrarán estadísticas y reportes "
                "del sistema."
            ),
            font=("Arial", 17)
        )

        texto.pack(
            padx=40,
            pady=20,
            anchor="w"
        )

    # ==================================================
    # ASIGNACIÓN DE TÉCNICOS
    # ==================================================

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

    # ==================================================
    # HISTORIAL
    # ==================================================

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

    # ==================================================
    # CERRAR SESIÓN
    # ==================================================

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

    # ==================================================
    # CERRAR COMPLETAMENTE EL SISTEMA
    # ==================================================

    def cerrar_sistema(self):

        respuesta = messagebox.askyesno(
            "Salir",
            "¿Desea cerrar completamente el sistema?"
        )

        if respuesta:
            self.ventana_login.destroy()
            