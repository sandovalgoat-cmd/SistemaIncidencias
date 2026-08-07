import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.ticket_controller import TicketController
from views.detalle_ticket import VistaDetalleTicket



class VistaTickets(ctk.CTkFrame):

    def __init__(self, master, usuario_sesion):
        super().__init__(
            master,
            fg_color="#F3F6F9",
            corner_radius=0
        )

        self.usuario_sesion = usuario_sesion
        self.tickets = []
        self.ticket_seleccionado = None

        self.pack(fill="both", expand=True)

        self.configurar_estilos()
        self.crear_interfaz()
        self.cargar_tickets()

    def configurar_estilos(self):
        estilo = ttk.Style()

        try:
            estilo.theme_use("clam")
        except Exception:
            pass

        estilo.configure(
            "Tickets.Treeview",
            rowheight=36,
            font=("Arial", 10),
            background="white",
            fieldbackground="white",
            foreground="#1F2937"
        )

        estilo.configure(
            "Tickets.Treeview.Heading",
            font=("Arial", 10, "bold"),
            background="#E5E7EB",
            foreground="#1F2937"
        )

        estilo.map(
            "Tickets.Treeview",
            background=[("selected", "#1565C0")],
            foreground=[("selected", "white")]
        )

    def crear_interfaz(self):
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
            text=self.obtener_titulo(),
            font=("Arial", 28, "bold"),
            text_color="#1F2937"
        ).pack(side="left")

        ctk.CTkButton(
            encabezado,
            text="Actualizar",
            width=130,
            height=40,
            fg_color="#4B5563",
            hover_color="#374151",
            command=self.cargar_tickets
        ).pack(side="right")

        filtros = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=10
        )
        filtros.pack(
            fill="x",
            padx=30,
            pady=10
        )

        self.entrada_busqueda = ctk.CTkEntry(
            filtros,
            height=40,
            placeholder_text=(
                "Buscar por folio, título, usuario, técnico, "
                "categoría, estado o prioridad"
            )
        )
        self.entrada_busqueda.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(15, 10),
            pady=15
        )

        self.entrada_busqueda.bind(
            "<KeyRelease>",
            lambda evento: self.mostrar_tickets_filtrados()
        )

        self.combo_estado = ctk.CTkComboBox(
            filtros,
            width=170,
            height=40,
            state="readonly",
            values=["Todos"],
            command=lambda opcion: self.mostrar_tickets_filtrados()
        )
        self.combo_estado.pack(
            side="left",
            padx=10,
            pady=15
        )
        self.combo_estado.set("Todos")

        self.combo_prioridad = ctk.CTkComboBox(
            filtros,
            width=150,
            height=40,
            state="readonly",
            values=["Todas"],
            command=lambda opcion: self.mostrar_tickets_filtrados()
        )
        self.combo_prioridad.pack(
            side="left",
            padx=(10, 15),
            pady=15
        )
        self.combo_prioridad.set("Todas")

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
            "folio",
            "titulo",
            "reportado_por",
            "categoria",
            "prioridad",
            "estado",
            "tecnico",
            "fecha"
        )

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            style="Tickets.Treeview"
        )

        self.tabla.heading("folio", text="Folio")
        self.tabla.heading("titulo", text="Título")
        self.tabla.heading("reportado_por", text="Reportado por")
        self.tabla.heading("categoria", text="Categoría")
        self.tabla.heading("prioridad", text="Prioridad")
        self.tabla.heading("estado", text="Estado")
        self.tabla.heading("tecnico", text="Técnico")
        self.tabla.heading("fecha", text="Fecha")

        self.tabla.column(
            "folio",
            width=145,
            minwidth=130,
            anchor="center"
        )
        self.tabla.column(
            "titulo",
            width=250,
            minwidth=180
        )
        self.tabla.column(
            "reportado_por",
            width=180,
            minwidth=150
        )
        self.tabla.column(
            "categoria",
            width=130,
            minwidth=110
        )
        self.tabla.column(
            "prioridad",
            width=100,
            minwidth=90,
            anchor="center"
        )
        self.tabla.column(
            "estado",
            width=120,
            minwidth=110,
            anchor="center"
        )
        self.tabla.column(
            "tecnico",
            width=170,
            minwidth=140
        )
        self.tabla.column(
            "fecha",
            width=145,
            minwidth=130,
            anchor="center"
        )

        scroll_vertical = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla.yview
        )

        scroll_horizontal = ttk.Scrollbar(
            tabla_frame,
            orient="horizontal",
            command=self.tabla.xview
        )

        self.tabla.configure(
            yscrollcommand=scroll_vertical.set,
            xscrollcommand=scroll_horizontal.set
        )

        self.tabla.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(15, 0),
            pady=(15, 0)
        )

        scroll_vertical.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=(0, 15),
            pady=(15, 0)
        )

        scroll_horizontal.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(15, 0),
            pady=(0, 15)
        )

        tabla_frame.grid_rowconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(0, weight=1)

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_ticket
        )

        self.tabla.bind(
            "<Double-1>",
            lambda evento: self.ver_detalle()
        )

        acciones = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        acciones.pack(
            fill="x",
            padx=30,
            pady=(0, 25)
        )

        self.etiqueta_total = ctk.CTkLabel(
            acciones,
            text="0 tickets",
            font=("Arial", 14),
            text_color="#6B7280"
        )
        self.etiqueta_total.pack(side="left")

        ctk.CTkButton(
            acciones,
            text="Ver detalle",
            width=150,
            height=40,
            command=self.ver_detalle
        ).pack(side="right")

    def obtener_titulo(self):
        rol = self.usuario_sesion["rol"]

        if rol == "Empleado":
            return "Mis tickets"

        if rol == "Tecnico":
            return "Mis tickets asignados"

        return "Todos los tickets"

    def cargar_tickets(self):
        exito, resultado = TicketController.listar_tickets(
            self.usuario_sesion
        )

        if not exito:
            messagebox.showerror(
                "Error",
                resultado
            )
            return

        self.tickets = resultado
        self.ticket_seleccionado = None

        self.cargar_opciones_filtros()
        self.mostrar_tickets_filtrados()

    def cargar_opciones_filtros(self):
        estados = sorted({
            ticket["estado"]
            for ticket in self.tickets
        })

        prioridades = sorted({
            ticket["prioridad"]
            for ticket in self.tickets
        })

        opciones_estados = ["Todos"] + estados
        opciones_prioridades = ["Todas"] + prioridades

        self.combo_estado.configure(
            values=opciones_estados
        )

        self.combo_prioridad.configure(
            values=opciones_prioridades
        )

        if self.combo_estado.get() not in opciones_estados:
            self.combo_estado.set("Todos")

        if self.combo_prioridad.get() not in opciones_prioridades:
            self.combo_prioridad.set("Todas")

    def mostrar_tickets_filtrados(self):
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)

        texto = self.entrada_busqueda.get().strip().lower()
        estado_filtro = self.combo_estado.get()
        prioridad_filtro = self.combo_prioridad.get()

        cantidad = 0

        for ticket in self.tickets:
            valores_busqueda = (
                ticket["folio"],
                ticket["titulo"],
                ticket["reportado_por"],
                ticket["categoria"],
                ticket["prioridad"],
                ticket["estado"],
                ticket["tecnico"]
            )

            coincide_texto = any(
                texto in str(valor).lower()
                for valor in valores_busqueda
            )

            if texto and not coincide_texto:
                continue

            if (
                estado_filtro != "Todos"
                and ticket["estado"] != estado_filtro
            ):
                continue

            if (
                prioridad_filtro != "Todas"
                and ticket["prioridad"] != prioridad_filtro
            ):
                continue

            fecha = ticket["fecha_creacion"]

            fecha_texto = (
                fecha.strftime("%d/%m/%Y %H:%M")
                if fecha
                else ""
            )

            self.tabla.insert(
                "",
                "end",
                iid=str(ticket["id_ticket"]),
                values=(
                    ticket["folio"],
                    ticket["titulo"],
                    ticket["reportado_por"],
                    ticket["categoria"],
                    ticket["prioridad"],
                    ticket["estado"],
                    ticket["tecnico"],
                    fecha_texto
                )
            )

            cantidad += 1

        self.etiqueta_total.configure(
            text=(
                "1 ticket"
                if cantidad == 1
                else f"{cantidad} tickets"
            )
        )

        self.ticket_seleccionado = None

    def seleccionar_ticket(self, evento=None):
        seleccion = self.tabla.selection()

        if not seleccion:
            self.ticket_seleccionado = None
            return

        id_ticket = int(seleccion[0])

        self.ticket_seleccionado = next(
            (
                ticket
                for ticket in self.tickets
                if ticket["id_ticket"] == id_ticket
            ),
            None
        )

    def ver_detalle(self):

        if self.ticket_seleccionado is None:
            messagebox.showwarning(
                "Seleccionar ticket",
                "Seleccione un ticket de la tabla."
            )
            return

        # Limpia el área principal del Dashboard
        for widget in self.master.winfo_children():
            widget.destroy()

        # Muestra la vista completa del detalle del ticket
        VistaDetalleTicket(
            master=self.master,
            ticket=self.ticket_seleccionado,
            usuario_sesion=self.usuario_sesion,
            regresar_callback=self.regresar_a_lista
        )

    def regresar_a_lista(self):

        # Limpia el área principal
        for widget in self.master.winfo_children():
            widget.destroy()

        # Vuelve a mostrar la lista de tickets
        VistaTickets(
            master=self.master,
            usuario_sesion=self.usuario_sesion
        )    