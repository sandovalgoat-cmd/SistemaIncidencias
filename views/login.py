import customtkinter as ctk
from tkinter import messagebox

from controllers.login_controller import LoginController
from views.dashboard import Dashboard
from PIL import Image
from config.estilos import (
    COLOR_FONDO,
    COLOR_PANEL,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_HOVER,
    COLOR_TOPBAR,
    RADIO_PANEL
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class Login(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Sistema de Atención de Incidencias")
        self.geometry("1100x650")
        self.resizable(False, False)

        self.crear_componentes()

        # Coloca automáticamente el cursor en el campo Usuario
        self.after(100, self.usuario.focus)

    def crear_componentes(self):

        # ==================================================
        # CONFIGURACIÓN GENERAL
        # ==================================================

        self.configure(
            fg_color=COLOR_FONDO
        )

        # ==================================================
        # CONTENEDOR PRINCIPAL
        # ==================================================

        contenedor = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=30
        )

        contenedor.grid_columnconfigure(
            0,
            weight=3
        )

        contenedor.grid_columnconfigure(
            1,
            weight=2
        )

        contenedor.grid_rowconfigure(
            0,
            weight=1
        )

        # ==================================================
        # PANEL IZQUIERDO - IDENTIDAD DEL SISTEMA
        # ==================================================

        panel_izquierdo = ctk.CTkFrame(
            contenedor,
            fg_color=COLOR_PANEL,
            corner_radius=16,
            border_width=1,
            border_color="#E5E7EB"
        )

        panel_izquierdo.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 15)
        )

        # --------------------------------------------------
        # LOGO
        # --------------------------------------------------

        imagen_logo = Image.open(
            "assets/logo_sistema.png"
        )

        self.logo_sistema = ctk.CTkImage(
            light_image=imagen_logo,
            dark_image=imagen_logo,
            size=(400, 300)
        )

        ctk.CTkLabel(
            panel_izquierdo,
            text="",
            image=self.logo_sistema
        ).pack(
            expand=True,
            padx=25,
            pady=(70, 10)
        )

        # --------------------------------------------------
        # TEXTO INSTITUCIONAL
        # --------------------------------------------------

        ctk.CTkLabel(
            panel_izquierdo,
            text="Departamento de Tecnologías de Información",
            font=("Arial", 15),
            text_color=COLOR_TEXTO_SECUNDARIO
        ).pack(
            pady=(0, 8)
        )

        ctk.CTkLabel(
            panel_izquierdo,
            text=(
                "Registra, consulta y da seguimiento "
                "a las incidencias tecnológicas."
            ),
            font=("Arial", 13),
            text_color=COLOR_TEXTO_SECUNDARIO,
            wraplength=400,
            justify="center"
        ).pack(
            padx=30,
            pady=(0, 30)
        )

        # ==================================================
        # PANEL DERECHO - LOGIN
        # ==================================================

        panel_derecho = ctk.CTkFrame(
            contenedor,
            fg_color=COLOR_PANEL,
            corner_radius=16,
            border_width=1,
            border_color="#E5E7EB"
        )

        panel_derecho.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(15, 0)
        )

        # ==================================================
        # FORMULARIO
        # ==================================================

        formulario = ctk.CTkFrame(
            panel_derecho,
            fg_color="transparent"
        )

        formulario.place(
            relx=0.5,
            rely=0.48,
            anchor="center"
        )

        # --------------------------------------------------
        # TÍTULO
        # --------------------------------------------------

        ctk.CTkLabel(
            formulario,
            text="Iniciar sesión",
            font=("Arial", 30, "bold"),
            text_color=COLOR_TEXTO
        ).pack(
            pady=(0, 8)
        )

        ctk.CTkLabel(
            formulario,
            text="Ingrese sus credenciales para acceder al sistema",
            font=("Arial", 13),
            text_color=COLOR_TEXTO_SECUNDARIO
        ).pack(
            pady=(0, 30)
        )

        # ==================================================
        # USUARIO
        # ==================================================

        ctk.CTkLabel(
            formulario,
            text="Usuario",
            font=("Arial", 13, "bold"),
            text_color=COLOR_TEXTO
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        self.usuario = ctk.CTkEntry(
            formulario,
            width=320,
            height=45,
            placeholder_text="Ingrese su usuario"
        )

        self.usuario.pack(
            pady=(0, 18)
        )

        # ==================================================
        # CONTRASEÑA
        # ==================================================

        ctk.CTkLabel(
            formulario,
            text="Contraseña",
            font=("Arial", 13, "bold"),
            text_color=COLOR_TEXTO
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        self.password = ctk.CTkEntry(
            formulario,
            width=320,
            height=45,
            placeholder_text="Ingrese su contraseña",
            show="*"
        )

        self.password.pack(
            pady=(0, 25)
        )

        # ==================================================
        # EVENTOS ENTER
        # ==================================================

        self.usuario.bind(
            "<Return>",
            self.ir_password
        )

        self.password.bind(
            "<Return>",
            self.enter_presionado
        )

        # ==================================================
        # BOTÓN INGRESAR
        # ==================================================

        self.boton_ingresar = ctk.CTkButton(
            formulario,
            text="Ingresar",
            width=320,
            height=45,
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_HOVER,
            command=self.iniciar_sesion
        )

        self.boton_ingresar.pack()

    def ir_password(self, event=None):
        self.password.focus()

    def enter_presionado(self, event=None):
        self.iniciar_sesion()

    def iniciar_sesion(self):

        usuario = self.usuario.get().strip()
        password = self.password.get()

        if usuario == "" or password == "":
            messagebox.showwarning(
                "Campos vacíos",
                "Debe ingresar el usuario y la contraseña."
            )

            if usuario == "":
                self.usuario.focus()
            else:
                self.password.focus()

            return

        self.boton_ingresar.configure(
            state="disabled",
            text="Validando..."
        )

        try:
            resultado = LoginController.iniciar_sesion(
                usuario,
                password
            )

            if resultado is None:
                messagebox.showerror(
                    "Acceso denegado",
                    "Usuario o contraseña incorrectos."
                )

                # Conserva el usuario y limpia solo la contraseña
                self.password.delete(0, "end")
                self.password.focus()

                return

            if resultado == "INACTIVO":
                messagebox.showwarning(
                    "Usuario inactivo",
                    "Su cuenta ha sido deshabilitada. "
                    "Comuníquese con el administrador."
                )

                self.password.delete(0, "end")
                self.password.focus()

                return

            # Oculta la ventana de login
            self.withdraw()

            # Abre el Dashboard
            dashboard = Dashboard(
                ventana_login=self,
                usuario=resultado
            )

            dashboard.focus_force()

        except Exception as error:
            messagebox.showerror(
                "Error del sistema",
                "No fue posible iniciar sesión.\n\n"
                f"Detalle: {error}"
            )

        finally:
            self.boton_ingresar.configure(
                state="normal",
                text="Ingresar"
            )