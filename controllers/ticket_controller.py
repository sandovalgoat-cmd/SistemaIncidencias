import mysql.connector

from models.ticket import Ticket


class TicketController:

    @staticmethod
    def crear_ticket(
        titulo,
        descripcion,
        id_usuario,
        id_categoria,
        id_prioridad
    ):
        titulo = titulo.strip()
        descripcion = descripcion.strip()

        if not titulo:
            return False, "El título es obligatorio."

        if len(titulo) < 5:
            return False, "El título debe tener al menos 5 caracteres."

        if not descripcion:
            return False, "La descripción es obligatoria."

        if len(descripcion) < 10:
            return False, (
                "La descripción debe tener al menos 10 caracteres."
            )

        if not id_categoria:
            return False, "Seleccione una categoría."

        if not id_prioridad:
            return False, "Seleccione una prioridad."

        try:
            resultado = Ticket.crear(
                titulo=titulo,
                descripcion=descripcion,
                id_usuario=id_usuario,
                id_categoria=id_categoria,
                id_prioridad=id_prioridad
            )

            return (
                True,
                "Ticket registrado correctamente.\n\n"
                f"Folio: {resultado['folio']}"
            )

        except mysql.connector.Error as error:
            return (
                False,
                f"Error de base de datos: {error}"
            )

        except Exception as error:
            return (
                False,
                f"No fue posible crear el ticket: {error}"
            )

    @staticmethod
    def listar_tickets(usuario_sesion):
        try:
            tickets = Ticket.listar_por_usuario(
                id_usuario=usuario_sesion["id_usuario"],
                rol=usuario_sesion["rol"]
            )

            return True, tickets

        except mysql.connector.Error as error:
            return (
                False,
                "No fue posible consultar los tickets.\n\n"
                f"Error de base de datos: {error}"
            )

        except Exception as error:
            return (
                False,
                "No fue posible consultar los tickets.\n\n"
                f"Detalle: {error}"
            )

    @staticmethod
    def obtener_estadisticas(usuario_sesion):

        try:
            estadisticas = Ticket.obtener_estadisticas(
                id_usuario=usuario_sesion["id_usuario"],
                rol=usuario_sesion["rol"]
            )

            return True, estadisticas

        except mysql.connector.Error as error:
            return (
                False,
                f"Error al consultar estadísticas: {error}"
            )

        except Exception as error:
            return (
                False,
                f"No fue posible consultar las estadísticas: {error}"
            )   

    @staticmethod
    def listar_tecnicos():
        try:
            tecnicos = Ticket.listar_tecnicos()

            return True, tecnicos

        except mysql.connector.Error as error:
            return (
                False,
                f"Error al consultar técnicos: {error}"
            )

        except Exception as error:
            return (
                False,
                f"No fue posible consultar técnicos: {error}"
            )
           
    @staticmethod
    def asignar_tecnico(
        id_ticket,
        id_tecnico,
        usuario_sesion
    ):
        rol = usuario_sesion["rol"]

        if rol not in (
            "Administrador",
            "EncargadoTI"
        ):
            return (
                False,
                "No tiene permisos para asignar técnicos."
            )

        if not id_tecnico:
            return (
                False,
                "Seleccione un técnico."
            )

        try:
            Ticket.asignar_tecnico(
                id_ticket=id_ticket,
                id_tecnico=id_tecnico,
                id_usuario_accion=usuario_sesion["id_usuario"]
            )

            return (
                True,
                "Técnico asignado correctamente."
            )

        except mysql.connector.Error as error:
            return (
                False,
                f"Error de base de datos: {error}"
            )

        except Exception as error:
            return (
                False,
                f"No fue posible asignar el técnico: {error}"
            )    

