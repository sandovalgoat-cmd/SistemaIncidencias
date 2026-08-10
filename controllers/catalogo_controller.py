import mysql.connector

from models.catalogo import Catalogo


class CatalogoController:

    ESTADOS_PROTEGIDOS = {
        "Nuevo",
        "Asignado",
        "En Proceso",
        "En Espera",
        "Solucionado",
        "Cerrado"
    }

    @staticmethod
    def validar_permiso(usuario_sesion):
        return usuario_sesion["rol"] == "Administrador"

    @staticmethod
    def listar(
        tabla,
        usuario_sesion
    ):
        if not CatalogoController.validar_permiso(
            usuario_sesion
        ):
            return (
                False,
                "No tiene permisos para administrar catálogos."
            )

        try:
            registros = Catalogo.listar(tabla)

            return True, registros

        except mysql.connector.Error as error:
            return (
                False,
                f"Error de base de datos: {error}"
            )

        except Exception as error:
            return (
                False,
                f"No fue posible consultar el catálogo: {error}"
            )

    @staticmethod
    def crear(
        tabla,
        nombre,
        usuario_sesion
    ):
        if not CatalogoController.validar_permiso(
            usuario_sesion
        ):
            return (
                False,
                "No tiene permisos para crear registros."
            )

        if tabla == "estados":
            return (
                False,
                "Los estados del sistema son fijos "
                "y no pueden agregarse manualmente."
            )

        nombre = nombre.strip()

        if not nombre:
            return (
                False,
                "El nombre es obligatorio."
            )

        if len(nombre) < 2:
            return (
                False,
                "El nombre es demasiado corto."
            )

        try:
            Catalogo.crear(
                tabla,
                nombre
            )

            return (
                True,
                "Registro creado correctamente."
            )

        except mysql.connector.IntegrityError:
            return (
                False,
                "Ya existe un registro con ese nombre "
                "o está siendo utilizado."
            )

        except mysql.connector.Error as error:
            return (
                False,
                f"Error de base de datos: {error}"
            )

        except Exception as error:
            return (
                False,
                f"No fue posible crear el registro: {error}"
            )

    @staticmethod
    def editar(
        tabla,
        id_registro,
        nombre,
        usuario_sesion
    ):

        # ==========================================
        # VALIDAR PERMISOS
        # ==========================================

        if not CatalogoController.validar_permiso(
            usuario_sesion
        ):
            return (
                False,
                "No tiene permisos para editar registros."
            )

        # ==========================================
        # LIMPIAR NOMBRE
        # ==========================================

        nombre = nombre.strip()

        if not nombre:
            return (
                False,
                "El nombre es obligatorio."
            )

        # ==========================================
        # PROTEGER ESTADOS DEL SISTEMA
        # ==========================================

        if tabla == "estados":

            exito, registros = CatalogoController.listar(
                tabla="estados",
                usuario_sesion=usuario_sesion
            )

            if not exito:
                return (
                    False,
                    registros
                )

            estado_actual = next(
                (
                    registro
                    for registro in registros
                    if registro["id"] == id_registro
                ),
                None
            )

            if estado_actual is None:
                return (
                    False,
                    "No se encontró el estado seleccionado."
                )

            if (
                estado_actual["nombre"]
                in CatalogoController.ESTADOS_PROTEGIDOS
                and nombre != estado_actual["nombre"]
            ):
                return (
                    False,
                    "Este estado forma parte del flujo interno "
                    "del sistema y no puede renombrarse."
                )

        # ==========================================
        # ACTUALIZAR REGISTRO
        # ==========================================

        try:

            actualizado = Catalogo.editar(
                tabla,
                id_registro,
                nombre
            )

            if not actualizado:
                return (
                    False,
                    "No se encontró el registro."
                )

            return (
                True,
                "Registro actualizado correctamente."
            )

        except mysql.connector.IntegrityError:
            return (
                False,
                "Ya existe un registro con ese nombre."
            )

        except mysql.connector.Error as error:
            return (
                False,
                f"Error de base de datos: {error}"
            )

        except Exception as error:
            return (
                False,
                f"No fue posible editar el registro: {error}"
            )

    @staticmethod
    def eliminar(
        tabla,
        id_registro,
        usuario_sesion
    ):
        if not CatalogoController.validar_permiso(
            usuario_sesion
        ):
            return (
                False,
                "No tiene permisos para eliminar registros."
            )

        if tabla == "estados":
            return (
                False,
                "Los estados del sistema no pueden eliminarse."
            )

        try:
            eliminado = Catalogo.eliminar(
                tabla,
                id_registro
            )

            if not eliminado:
                return (
                    False,
                    "No se encontró el registro."
                )

            return (
                True,
                "Registro eliminado correctamente."
            )

        except mysql.connector.IntegrityError:
            return (
                False,
                (
                    "No puede eliminarse porque está siendo "
                    "utilizado por otros registros."
                )
            )

        except mysql.connector.Error as error:
            return (
                False,
                f"Error de base de datos: {error}"
            )

        except Exception as error:
            return (
                False,
                f"No fue posible eliminar el registro: {error}"
            )