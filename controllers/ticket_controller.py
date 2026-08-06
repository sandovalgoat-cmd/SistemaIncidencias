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
            return False, "Debe seleccionar una categoría."

        if not id_prioridad:
            return False, "Debe seleccionar una prioridad."

        try:
            resultado = Ticket.crear(
                titulo,
                descripcion,
                id_usuario,
                id_categoria,
                id_prioridad
            )

            return (
                True,
                f"Ticket registrado correctamente.\n\n"
                f"Folio: {resultado['folio']}"
            )

        except mysql.connector.Error as error:
            return False, f"Error de base de datos: {error}"

        except Exception as error:
            return False, f"No fue posible crear el ticket: {error}"