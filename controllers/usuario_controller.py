from dbm import error

import bcrypt
import mysql.connector

from models.usuario import Usuario


class UsuarioController:

    @staticmethod
    def listar():
        return Usuario.listar()

    @staticmethod
    def crear(
        nombre,
        apellido,
        nombre_usuario,
        password,
        id_rol,
        id_area
    ):
        nombre = nombre.strip()
        apellido = apellido.strip()
        nombre_usuario = nombre_usuario.strip()
        password = password.strip()

        if not nombre or not apellido or not nombre_usuario or not password:
            return False, "Todos los campos obligatorios deben completarse."

        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres."

        if Usuario.usuario_existe(nombre_usuario):
            return False, "El nombre de usuario ya está registrado."

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        try:
            Usuario.crear(
                nombre,
                apellido,
                nombre_usuario,
                password_hash,
                id_rol,
                id_area
            )

            return True, "Usuario registrado correctamente."

        except mysql.connector.Error as error:
            return False, f"Error de base de datos: {error}"

        except Exception as error:
            return False, f"No fue posible crear el usuario: {error}"

    @staticmethod
    def actualizar(
        id_usuario,
        nombre,
        apellido,
        nombre_usuario,
        id_rol,
        id_area
    ):
        nombre = nombre.strip()
        apellido = apellido.strip()
        nombre_usuario = nombre_usuario.strip()

        if not nombre or not apellido or not nombre_usuario:
            return False, "Complete todos los campos obligatorios."

        if Usuario.usuario_existe(nombre_usuario, id_usuario):
            return False, "Ese nombre de usuario ya pertenece a otra cuenta."

        try:
            actualizado = Usuario.actualizar(
                id_usuario,
                nombre,
                apellido,
                nombre_usuario,
                id_rol,
                id_area
            )

            if actualizado:
                return True, "Usuario actualizado correctamente."

            return False, "No se realizaron cambios."

        except mysql.connector.Error as error:
            return False, f"Error de base de datos: {error}"

        except Exception as error:
            return False, f"No fue posible actualizar el usuario: {error}"
        
    @staticmethod
    def cambiar_estado(id_usuario, estado_actual):
        nuevo_estado = 0 if estado_actual else 1

        try:
            actualizado = Usuario.cambiar_estado(
                id_usuario,
                nuevo_estado
            )

            if actualizado:
                estado_texto = "activado" if nuevo_estado else "desactivado"
                return True, f"Usuario {estado_texto} correctamente."

            return False, "No fue posible modificar el usuario."

        except mysql.connector.Error as error:
            return False, f"Error de base de datos: {error}"

        except Exception as error:
            return False, f"No fue posible modificar el usuario: {error}"

    @staticmethod
    def cambiar_password(id_usuario, nueva_password):

        nueva_password = nueva_password.strip()

        if not nueva_password:
            return False, "La contraseña no puede estar vacía."

        if len(nueva_password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres."

        password_hash = bcrypt.hashpw(
            nueva_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        try:

            actualizado = Usuario.cambiar_password(
                id_usuario,
                password_hash
            )

            if actualizado:
                return True, "Contraseña actualizada correctamente."

            return False, "No fue posible actualizar la contraseña."

        except mysql.connector.Error as error:
            return False, f"Error de base de datos: {error}"

        except Exception as error:
            return False, f"No fue posible actualizar la contraseña: {error}"