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

    @staticmethod
    def cambiar_estado(
        id_ticket,
        nuevo_estado,
        usuario_sesion
    ):

        # Solo técnicos, EncargadoTI y Administrador
        if usuario_sesion["rol"] not in (
            "Tecnico",
            "EncargadoTI",
            "Administrador"
        ):
            return (
                False,
                "No tiene permisos para cambiar el estado."
            )

        estados_permitidos = (
            "Asignado",
            "En Proceso",
            "En Espera",
            "Solucionado"
        )

        if nuevo_estado not in estados_permitidos:
            return (
                False,
                "El estado seleccionado no es válido."
            )

        try:
            Ticket.cambiar_estado(
                id_ticket=id_ticket,
                nuevo_estado=nuevo_estado,
                id_usuario_accion=usuario_sesion["id_usuario"]
            )

            return (
                True,
                f"Estado actualizado a '{nuevo_estado}'."
            )

        except mysql.connector.Error as error:
            return (
                False,
                f"Error de base de datos: {error}"
            )

        except Exception as error:
            return (
                False,
                f"No fue posible cambiar el estado: {error}"
            )

    @staticmethod
    def agregar_comentario(
        id_ticket,
        comentario,
        publico,
        usuario_sesion
    ):
        comentario = comentario.strip()

        if not comentario:
            return (
                False,
                "Escriba un comentario."
            )

        if len(comentario) < 3:
            return (
                False,
                "El comentario es demasiado corto."
            )

        rol = usuario_sesion["rol"]

        # Un empleado no puede crear notas privadas
        if not publico and rol == "Empleado":
            return (
                False,
                "No tiene permisos para crear notas internas."
            )

        try:
            Ticket.agregar_comentario(
                id_ticket=id_ticket,
                id_usuario=usuario_sesion["id_usuario"],
                comentario=comentario,
                publico=publico
            )

            return (
                True,
                "Comentario guardado correctamente."
            )

        except mysql.connector.Error as error:
            return (
                False,
                f"Error de base de datos: {error}"
            )

        except Exception as error:
            return (
                False,
                f"No fue posible guardar el comentario: {error}"
            )

    @staticmethod
    def listar_comentarios(
        id_ticket,
        usuario_sesion
    ):
        try:
            incluir_privados = (
                usuario_sesion["rol"]
                in (
                    "Administrador",
                    "EncargadoTI",
                    "Tecnico"
                )
            )

            comentarios = Ticket.listar_comentarios(
                id_ticket=id_ticket,
                incluir_privados=incluir_privados
            )

            return (
                True,
                comentarios
            )

        except mysql.connector.Error as error:
            return (
                False,
                f"Error al consultar comentarios: {error}"
            )

        except Exception as error:
            return (
                False,
                f"No fue posible consultar comentarios: {error}"
            )

    @staticmethod
    def listar_historial(id_ticket):
        try:

            historial = Ticket.listar_historial(
                id_ticket=id_ticket
            )

            return (
                True,
                historial
            )

        except mysql.connector.Error as error:
            return (
                False,
                f"Error al consultar el historial: {error}"
            )

        except Exception as error:
            return (
                False,
                f"No fue posible consultar el historial: {error}"
            )   

    @staticmethod
    def confirmar_solucion(
            id_ticket,
            confirmado,
            usuario_sesion
        ):

            # Solo el empleado puede confirmar
            if usuario_sesion["rol"] != "Empleado":
                return (
                    False,
                    "Solo el empleado que reportó el problema "
                    "puede confirmar la solución."
                )

            try:
                Ticket.confirmar_solucion(
                    id_ticket=id_ticket,
                    id_usuario=usuario_sesion["id_usuario"],
                    confirmado=confirmado
                )

                if confirmado:
                    return (
                        True,
                        "La solución fue confirmada.\n\n"
                        "El ticket ha sido cerrado."
                    )

                return (
                    True,
                    "Se indicó que el problema continúa.\n\n"
                    "El ticket regresó a En Proceso."
                )

            except mysql.connector.Error as error:
                return (
                    False,
                    f"Error de base de datos: {error}"
                )

            except Exception as error:
                return (
                    False,
                    f"No fue posible confirmar la solución: {error}"
                )    
        