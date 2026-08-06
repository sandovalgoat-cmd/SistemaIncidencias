from datetime import datetime
from config.database import conectar


class Ticket:

    @staticmethod
    def obtener_estado_por_nombre(nombre_estado):
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)
        

        try:
            sql = """
                SELECT id_estado
                FROM estados
                WHERE nombre = %s
                LIMIT 1
            """

            cursor.execute(sql, (nombre_estado,))
            return cursor.fetchone()

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def crear(
        titulo,
        descripcion,
        id_usuario,
        id_categoria,
        id_prioridad
    ):
        conexion = conectar()
        cursor = conexion.cursor()

        try:
            estado = Ticket.obtener_estado_por_nombre("Nuevo")

            if estado is None:
                raise ValueError(
                    "No existe el estado 'Nuevo' en la base de datos."
                )

            id_estado = estado["id_estado"]

            sql_ticket = """
                INSERT INTO tickets (
                    folio,
                    titulo,
                    descripcion,
                    fecha_creacion,
                    confirmado,
                    id_usuario,
                    id_tecnico,
                    id_categoria,
                    id_estado,
                    id_prioridad
                )
                VALUES (
                    '',
                    %s,
                    %s,
                    NOW(),
                    0,
                    %s,
                    NULL,
                    %s,
                    %s,
                    %s
                )
            """

            cursor.execute(
                sql_ticket,
                (
                    titulo,
                    descripcion,
                    id_usuario,
                    id_categoria,
                    id_estado,
                    id_prioridad
                )
            )

            id_ticket = cursor.lastrowid

            fecha = datetime.now().strftime("%Y%m%d")
            folio = f"TK-{fecha}-{id_ticket:04d}"

            sql_folio = """
                UPDATE tickets
                SET folio = %s
                WHERE id_ticket = %s
            """

            cursor.execute(
                sql_folio,
                (folio, id_ticket)
            )

            sql_historial = """
                INSERT INTO historial (
                    id_ticket,
                    id_usuario,
                    accion,
                    fecha
                )
                VALUES (%s, %s, %s, NOW())
            """

            cursor.execute(
                sql_historial,
                (
                    id_ticket,
                    id_usuario,
                    "Ticket creado"
                )
            )

            conexion.commit()

            return {
                "id_ticket": id_ticket,
                "folio": folio
            }

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()