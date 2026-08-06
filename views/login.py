import customtkinter as ctk
from tkinter import messagebox

from controllers.login_controller import LoginController
from views.dashboard import Dashboard


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class Login(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Sistema de Atención de Incidencias")
        self.geometry("1000x600")
        self.resizable(False, False)

        self.crear_componentes()

        # Coloca automáticamente el cursor en el campo Usuario
        self.after(100, self.usuario.focus)

    def crear_componentes(self):

        # ==================================================
        # PANEL IZQUIERDO
        # ==================================================

        panel_izquierdo = ctk.CTkFrame(
            self,
            width=450,
            fg_color="#1565C0",
            corner_radius=0
        )

        panel_izquierdo.pack(
            side="left",
            fill="both"
        )

        panel_izquierdo.pack_propagate(False)

        titulo = ctk.CTkLabel(
            panel_izquierdo,
            text="Sistema de\nAtención de\nIncidencias",
            font=("Arial", 34, "bold"),
            text_color="white"
        )

        titulo.place(
            relx=0.5,
            rely=0.30,
            anchor="center"
        )

        subtitulo = ctk.CTkLabel(
            panel_izquierdo,
            text="Departamento de Tecnologías de Información",
            font=("Arial", 16),
            text_color="white"
        )

        subtitulo.place(
            relx=0.5,
            rely=0.47,
            anchor="center"
        )

        descripcion = ctk.CTkLabel(
            panel_izquierdo,
            text=(
                "Registra, consulta y da seguimiento\n"
                "a los problemas tecnológicos de la empresa."
            ),
            font=("Arial", 14),
            text_color="#DCEBFA",
            justify="center"
        )

        descripcion.place(
            relx=0.5,
            rely=0.58,
            anchor="center"
        )

        # ==================================================
        # PANEL DERECHO
        # ==================================================

        panel_derecho = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=0
        )

        panel_derecho.pack(
            side="right",
            expand=True,
            fill="both"
        )

        etiqueta_login = ctk.CTkLabel(
            panel_derecho,
            text="Iniciar sesión",
            font=("Arial", 30, "bold"),
            text_color="#1565C0"
        )

        etiqueta_login.pack(
            pady=(90, 10)
        )

        instrucciones = ctk.CTkLabel(
            panel_derecho,
            text="Ingrese sus credenciales para acceder al sistema",
            font=("Arial", 14),
            text_color="#6B7280"
        )

        instrucciones.pack(
            pady=(0, 25)
        )

        # Campo Usuario
        self.usuario = ctk.CTkEntry(
            panel_derecho,
            width=320,
            height=45,
            placeholder_text="Usuario"
        )

        self.usuario.pack(
            pady=10
        )

        # Campo Contraseña
        self.password = ctk.CTkEntry(
            panel_derecho,
            width=320,
            height=45,
            placeholder_text="Contraseña",
            show="*"
        )

        self.password.pack(
            pady=10
        )

        # Enter en Usuario mueve el cursor a Contraseña
        self.usuario.bind(
            "<Return>",
            self.ir_password
        )

        # Enter en Contraseña inicia sesión
        self.password.bind(
            "<Return>",
            self.enter_presionado
        )

        # Botón de ingreso
        self.boton_ingresar = ctk.CTkButton(
            panel_derecho,
            text="Ingresar",
            width=320,
            height=45,
            command=self.iniciar_sesion
        )

        self.boton_ingresar.pack(
            pady=25
        )

    # ==================================================
    # ENTER EN EL CAMPO USUARIO
    # ==================================================

    def ir_password(self, event=None):
        self.password.focus()

    # ==================================================
    # ENTER EN EL CAMPO CONTRASEÑA
    # ==================================================

    def enter_presionado(self, event=None):
        self.iniciar_sesion()

    # ==================================================
    # INICIAR SESIÓN
    # ==================================================

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