import bcrypt

from models.usuario import Usuario


class LoginController:

    @staticmethod
    def iniciar_sesion(usuario, password):
        datos = Usuario.login(usuario)

        if datos is None:
            return None

        password_guardada = str(datos["password"])
        password_ingresada = password.encode("utf-8")

        # Contraseña cifrada con bcrypt
        if password_guardada.startswith("$2"):
            password_correcta = bcrypt.checkpw(
                password_ingresada,
                password_guardada.encode("utf-8")
            )

        # Compatibilidad temporal con el administrador en texto plano
        else:
            password_correcta = password_guardada == password

        if not password_correcta:
            return None

        if not datos["estado"]:
            return "INACTIVO"

        return datos