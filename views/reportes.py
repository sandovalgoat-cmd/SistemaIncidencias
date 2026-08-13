from datetime import datetime
from tkcalendar import Calendar

import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.ticket_controller import TicketController
from config.estilos import (
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_HOVER,
    COLOR_FONDO,
    COLOR_PANEL,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE,
    COLOR_NEUTRO,
    COLOR_NEUTRO_HOVER,
    FUENTE_TITULO,
    FUENTE_NUMERO_TARJETA,
    ALTO_BOTON,
    RADIO_PANEL,
    RADIO_TARJETA
)


class VistaReportes(ctk.CTkFrame):

    def __init__(self, master, usuario_sesion):
        super().__init__(
            master,
            fg_color=COLOR_FONDO,
            corner_radius=0
        )

        self.usuario_sesion = usuario_sesion

        self.pack(fill="both", expand=True)

        self.crear_interfaz()
        self.cargar_reportes()

    def crear_interfaz(self):

    # ==============================================
    # ENCABEZADO
    # ==============================================

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
            text="Reportes y métricas",
            font=FUENTE_TITULO,
            text_color=COLOR_TEXTO
        ).pack(
            side="left"
        )

        ctk.CTkButton(
            encabezado,
            text="Actualizar",
            width=140,
            height=ALTO_BOTON,
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_HOVER,
            command=self.cargar_reportes
        ).pack(
            side="right"
        )

        # ==============================================
        # FILTROS
        # ==============================================

        filtros = ctk.CTkFrame(
            self,
            fg_color=COLOR_PANEL,
            corner_radius=RADIO_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )

        filtros.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        ctk.CTkLabel(
            filtros,
            text="Fecha inicial",
            font=("Arial", 13, "bold"),
            text_color=COLOR_TEXTO
        ).grid(
            row=0,
            column=0,
            padx=(20, 5),
            pady=(15, 5),
            sticky="w"
        )

        ctk.CTkLabel(
            filtros,
            text="Fecha final",
            font=("Arial", 13, "bold"),
            text_color=COLOR_TEXTO
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )

        self.entrada_fecha_inicio = ctk.CTkEntry(
            filtros,
            width=160,
            height=40,
            placeholder_text="AAAA-MM-DD"
        )

        self.entrada_fecha_inicio.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=(0, 15)
        )

        self.entrada_fecha_inicio.bind(
            "<Button-1>",
            lambda event:
                self.abrir_calendario(
                    self.entrada_fecha_inicio
                )
        )

        self.entrada_fecha_fin = ctk.CTkEntry(
            filtros,
            width=160,
            height=40,
            placeholder_text="AAAA-MM-DD"
        )

        self.entrada_fecha_fin.grid(
            row=1,
            column=1,
            padx=10,
            pady=(0, 15)
        )

        self.entrada_fecha_fin.bind(
            "<Button-1>",
            lambda event:
                self.abrir_calendario(
                    self.entrada_fecha_fin
                )
        )

        ctk.CTkButton(
            filtros,
            text="Aplicar filtros",
            width=140,
            height=ALTO_BOTON,
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_HOVER,
            command=self.aplicar_filtros
        ).grid(
            row=1,
            column=2,
            padx=10,
            pady=(0, 15)
        )

        ctk.CTkButton(
            filtros,
            text="Limpiar",
            width=110,
            height=ALTO_BOTON,
            fg_color=COLOR_NEUTRO,
            hover_color=COLOR_NEUTRO_HOVER,
            command=self.limpiar_filtros
        ).grid(
            row=1,
            column=3,
            padx=(10, 20),
            pady=(0, 15)
        )

        # ==============================================
        # ESTILO DE TABLAS
        # ==============================================

        estilo = ttk.Style()

        estilo.theme_use("default")

        estilo.configure(
            "Reportes.Treeview",
            background=COLOR_PANEL,
            foreground=COLOR_TEXTO,
            fieldbackground=COLOR_PANEL,
            rowheight=36,
            borderwidth=0,
            font=("Arial", 11)
        )

        estilo.configure(
            "Reportes.Treeview.Heading",
            background="#EAF2F8",
            foreground=COLOR_TEXTO,
            relief="flat",
            font=("Arial", 11, "bold")
        )

        estilo.map(
            "Reportes.Treeview",
            background=[
                ("selected", COLOR_PRIMARIO)
            ],
            foreground=[
                ("selected", "white")
            ]
        )

        # ==============================================
        # CONTENEDOR SCROLL
        # ==============================================

        self.contenedor = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.contenedor.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )
        
    def limpiar(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def cargar_reportes(
        self,
        fecha_inicio=None,
        fecha_fin=None
    ):

        # Limpiar información anterior
        self.limpiar()

        # ==========================================
        # OBTENER REPORTES GENERALES
        # ==========================================

        exito, resultado = (
            TicketController.obtener_reportes(
                self.usuario_sesion
            )
        )

        if not exito:
            messagebox.showerror(
                "Error",
                resultado
            )
            return

        # ==========================================
        # MOSTRAR RESUMEN GENERAL
        # ==========================================

        self.crear_resumen(
            resultado["general"]
        )

        # ==========================================
        # OBTENER MÉTRICAS POR FECHA
        # ==========================================

        exito_metricas, metricas = (
            TicketController.obtener_metricas_tiempo(
                usuario_sesion=self.usuario_sesion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
        )

        # ==========================================
        # MOSTRAR MÉTRICAS DE TIEMPO
        # ==========================================

        if exito_metricas:

            self.crear_metricas_tiempo(
                metricas
            )

        else:

            messagebox.showwarning(
                "Métricas",
                metricas
            )

        # ==========================================
        # MOSTRAR TABLAS
        # ==========================================

        self.crear_tabla(
            "Tickets por estado",
            resultado["estados"]
        )

        self.crear_tabla(
            "Tickets por prioridad",
            resultado["prioridades"]
        )

        self.crear_tabla(
            "Tickets por categoría",
            resultado["categorias"]
        )

        self.crear_tabla(
            "Tickets por técnico",
            resultado["tecnicos"]
        )

    def crear_resumen(self, datos):

        ctk.CTkLabel(
            self.contenedor,
            text="Resumen general",
            font=("Arial", 20, "bold"),
            text_color=COLOR_TEXTO
        ).pack(
            anchor="w",
            pady=(10, 15)
        )

        frame = ctk.CTkFrame(
            self.contenedor,
            fg_color="transparent"
        )

        frame.pack(
            fill="x",
            pady=(0, 25)
        )

        tarjetas = [
            ("Total", datos["total"]),
            ("Nuevos", datos["nuevos"]),
            ("En proceso", datos["en_proceso"]),
            ("Solucionados", datos["solucionados"]),
            ("Cerrados", datos["cerrados"]),
            ("Urgentes", datos["urgentes"]),
            ("Sin asignar", datos["sin_asignar"])
        ]

        # 4 tarjetas por fila
        for columna in range(4):
            frame.grid_columnconfigure(
                columna,
                weight=1
            )

        for indice, tarjeta in enumerate(tarjetas):

            fila = indice // 4
            columna = indice % 4

            card = ctk.CTkFrame(
                frame,
                height=110,
                fg_color=COLOR_PANEL,
                corner_radius=RADIO_TARJETA,
                border_width=1,
                border_color=COLOR_BORDE
            )

            card.grid(
                row=fila,
                column=columna,
                sticky="nsew",
                padx=5,
                pady=5
            )

            ctk.CTkLabel(
                card,
                text=tarjeta[0],
                font=("Arial", 13),
                text_color=COLOR_TEXTO_SECUNDARIO
            ).pack(
                pady=(18, 4)
            )

            ctk.CTkLabel(
                card,
                text=str(tarjeta[1]),
                font=FUENTE_NUMERO_TARJETA,
                text_color=COLOR_PRIMARIO
            ).pack(
                pady=(0, 18)
            )

    def crear_tabla(
        self,
        titulo,
        datos
    ):

        ctk.CTkLabel(
            self.contenedor,
            text=titulo,
            font=("Arial", 19, "bold"),
            text_color=COLOR_TEXTO
        ).pack(
            anchor="w",
            pady=(15, 10)
        )

        frame = ctk.CTkFrame(
            self.contenedor,
            fg_color=COLOR_PANEL,
            corner_radius=RADIO_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )

        frame.pack(
            fill="x",
            pady=(0, 20)
        )

        tabla = ttk.Treeview(
            frame,
            columns=(
                "nombre",
                "cantidad"
            ),
            show="headings",
            style="Reportes.Treeview",
            height=min(
                max(len(datos), 3),
                8
            )
        )

        tabla.heading(
            "nombre",
            text="Descripción"
        )

        tabla.heading(
            "cantidad",
            text="Cantidad"
        )

        tabla.column(
            "nombre",
            width=400
        )

        tabla.column(
            "cantidad",
            width=120,
            anchor="center"
        )

        for fila in datos:

            tabla.insert(
                "",
                "end",
                values=(
                    fila["nombre"],
                    fila["cantidad"]
                )
            )

        tabla.pack(
            fill="x",
            padx=15,
            pady=15
        )

    def aplicar_filtros(self):

        fecha_inicio = (
            self.entrada_fecha_inicio
            .get()
            .strip()
        )

        fecha_fin = (
            self.entrada_fecha_fin
            .get()
            .strip()
        )

        # ==========================================
        # VALIDAR CAMPOS VACÍOS
        # ==========================================

        if not fecha_inicio or not fecha_fin:

            messagebox.showwarning(
                "Fechas",
                "Seleccione la fecha inicial "
                "y la fecha final."
            )

            return

        # ==========================================
        # VALIDAR FORMATO
        # ==========================================

        try:

            inicio = datetime.strptime(
                fecha_inicio,
                "%Y-%m-%d"
            )

            fin = datetime.strptime(
                fecha_fin,
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showwarning(
                "Fechas",
                "Las fechas deben tener el formato "
                "AAAA-MM-DD."
            )

            return

        # ==========================================
        # VALIDAR ORDEN
        # ==========================================

        if inicio > fin:

            messagebox.showwarning(
                "Fechas",
                "La fecha inicial no puede ser "
                "mayor que la fecha final."
            )

            return

        # ==========================================
        # CARGAR REPORTE
        # ==========================================

        self.cargar_reportes(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

    def limpiar_filtros(self):

        self.entrada_fecha_inicio.delete(
            0,
            "end"
        )

        self.entrada_fecha_fin.delete(
            0,
            "end"
        )

        self.cargar_reportes()

    def formatear_minutos(
        self,
        minutos
    ):

        if not minutos:
            return "0 min"

        minutos = int(
            round(minutos)
        )

        if minutos < 60:
            return f"{minutos} min"

        horas = minutos // 60
        minutos_restantes = minutos % 60

        if horas < 24:

            if minutos_restantes:
                return (
                    f"{horas} h "
                    f"{minutos_restantes} min"
                )

            return f"{horas} h"

        dias = horas // 24
        horas_restantes = horas % 24

        if horas_restantes:
            return (
                f"{dias} d "
                f"{horas_restantes} h"
            )

        return f"{dias} d"

    def crear_metricas_tiempo(
        self,
        datos
    ):

        ctk.CTkLabel(
            self.contenedor,
            text="Métricas de tiempo",
            font=("Arial", 20, "bold"),
            text_color=COLOR_TEXTO
        ).pack(
            anchor="w",
            pady=(10, 15)
        )

        frame = ctk.CTkFrame(
            self.contenedor,
            fg_color="transparent"
        )

        frame.pack(
            fill="x",
            pady=(0, 25)
        )

        metricas = [
            (
                "Tickets del periodo",
                datos["total_periodo"]
            ),
            (
                "Promedio hasta solución",
                self.formatear_minutos(
                    datos["promedio_minutos_solucion"]
                )
            ),
            (
                "Promedio hasta cierre",
                self.formatear_minutos(
                    datos["promedio_minutos_cierre"]
                )
            ),
            (
                "Confirmación del empleado",
                self.formatear_minutos(
                    datos["promedio_confirmacion"]
                )
            )
        ]

        for indice in range(4):

            frame.grid_columnconfigure(
                indice,
                weight=1
            )

        for indice, metrica in enumerate(metricas):

            tarjeta = ctk.CTkFrame(
                frame,
                fg_color=COLOR_PANEL,
                corner_radius=RADIO_TARJETA,
                border_width=1,
                border_color=COLOR_BORDE
            )

            tarjeta.grid(
                row=0,
                column=indice,
                sticky="nsew",
                padx=5
            )

            ctk.CTkLabel(
                tarjeta,
                text=metrica[0],
                font=("Arial", 13),
                text_color=COLOR_TEXTO_SECUNDARIO
            ).pack(
                pady=(18, 4)
            )

            ctk.CTkLabel(
                tarjeta,
                text=str(metrica[1]),
                font=("Arial", 22, "bold"),
                text_color=COLOR_PRIMARIO
            ).pack(
                pady=(0, 18)
            )

    def abrir_calendario(
        self,
        entrada
    ):

        ventana = ctk.CTkToplevel(self)

        ventana.title("Seleccionar fecha")

        ventana.resizable(
            False,
            False
        )

        ventana.transient(
            self.winfo_toplevel()
        )

        calendario = Calendar(
            ventana,
            selectmode="day",
            date_pattern="yyyy-mm-dd"
        )

        calendario.pack(
            padx=10,
            pady=(10, 5)
        )

        def seleccionar():

            fecha = calendario.get_date()

            entrada.delete(
                0,
                "end"
            )

            entrada.insert(
                0,
                fecha
            )

            ventana.destroy()

        boton = ctk.CTkButton(
            ventana,
            text="Seleccionar",
            command=seleccionar
        )

        boton.pack(
            padx=10,
            pady=(5, 10)
        )

        # ==========================================
        # POSICIONAR ARRIBA DEL CAMPO
        # ==========================================

        ventana.update_idletasks()

        x = entrada.winfo_rootx()

        y = (
            entrada.winfo_rooty()
            - ventana.winfo_reqheight()
            - 10
        )

        # Evitar que quede fuera de pantalla
        if y < 0:
            y = (
                entrada.winfo_rooty()
                + entrada.winfo_height()
                + 10
            )

        ventana.geometry(
            f"+{x}+{y}"
        )

        ventana.grab_set()