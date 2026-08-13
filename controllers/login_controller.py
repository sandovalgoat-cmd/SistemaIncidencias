import bcrypt
import mysql.connector

from models.usuario import Usuario


class LoginController:

    @staticmethod
    def iniciar_sesion(
        usuario,
        password
    ):

        usuario = usuario.strip()

        if not usuario or not password:
            return None

        try:

            datos = Usuario.login(
                usuario
            )

            if datos is None:
                return None

            password_guardada = str(
                datos["password"]
            )

            password_ingresada = (
                password.encode("utf-8")
            )

            # ==========================================
            # CONTRASEÑA CIFRADA CON BCRYPT
            # ==========================================

            if password_guardada.startswith("$2"):

                try:

                    password_correcta = (
                        bcrypt.checkpw(
                            password_ingresada,
                            password_guardada.encode(
                                "utf-8"
                            )
                        )
                    )

                except ValueError:

                    return None

            # ==========================================
            # COMPATIBILIDAD TEMPORAL
            # ==========================================

            else:

                password_correcta = (
                    password_guardada
                    == password
                )

            if not password_correcta:
                return None

            # ==========================================
            # USUARIO INACTIVO
            # ==========================================

            if not datos["estado"]:
                return "INACTIVO"

            return datos

        except mysql.connector.Error as error:

            raise RuntimeError(
                "No fue posible conectar con "
                f"la base de datos: {error}"
            )

        except Exception as error:

            raise RuntimeError(
                "No fue posible validar "
                f"las credenciales: {error}"
            )