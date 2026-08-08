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

    @staticmethod
    def listar_por_usuario(id_usuario, rol):
        conexion = None
        cursor = None

        try:
            conexion = conectar()
            cursor = conexion.cursor(dictionary=True)

            consulta = """
                SELECT
                    t.id_ticket,
                    t.folio,
                    t.titulo,
                    t.descripcion,
                    t.fecha_creacion,
                    t.fecha_asignacion,
                    t.fecha_solucion,
                    t.fecha_cierre,
                    t.confirmado,

                    t.id_usuario,
                    t.id_tecnico,
                    t.id_categoria,
                    t.id_estado,
                    t.id_prioridad,

                    CONCAT(
                        reportante.nombre,
                        ' ',
                        reportante.apellido
                    ) AS reportado_por,

                    COALESCE(
                        CONCAT(
                            tecnico.nombre,
                            ' ',
                            tecnico.apellido
                        ),
                        'Sin asignar'
                    ) AS tecnico,

                    categoria.nombre AS categoria,
                    estado.nombre AS estado,
                    prioridad.nombre AS prioridad

                FROM tickets AS t

                INNER JOIN usuarios AS reportante
                    ON t.id_usuario = reportante.id_usuario

                LEFT JOIN usuarios AS tecnico
                    ON t.id_tecnico = tecnico.id_usuario

                INNER JOIN categorias AS categoria
                    ON t.id_categoria = categoria.id_categoria

                INNER JOIN estados AS estado
                    ON t.id_estado = estado.id_estado

                INNER JOIN prioridades AS prioridad
                    ON t.id_prioridad = prioridad.id_prioridad
            """

            parametros = ()

            if rol == "Empleado":
                consulta += """
                    WHERE t.id_usuario = %s
                """
                parametros = (id_usuario,)

            elif rol == "Tecnico":
                consulta += """
                    WHERE t.id_tecnico = %s
                """
                parametros = (id_usuario,)

            elif rol in ("Administrador", "EncargadoTI"):
                pass

            else:
                return []

            consulta += """
                ORDER BY
                    t.fecha_creacion DESC,
                    t.id_ticket DESC
            """

            cursor.execute(
                consulta,
                parametros
            )

            return cursor.fetchall()

        finally:
            if cursor is not None:
                cursor.close()

            if (
                conexion is not None
                and conexion.is_connected()
            ):
                conexion.close()

    @staticmethod
    def obtener_estadisticas(id_usuario, rol):
        conexion = None
        cursor = None

        try:
            conexion = conectar()
            cursor = conexion.cursor(dictionary=True)

            condiciones = []
            parametros = []

            # Empleado: solo sus propios tickets
            if rol == "Empleado":
                condiciones.append("t.id_usuario = %s")
                parametros.append(id_usuario)

            # Técnico: solo tickets que tiene asignados
            elif rol == "Tecnico":
                condiciones.append("t.id_tecnico = %s")
                parametros.append(id_usuario)

            # Administrador y EncargadoTI: todos
            elif rol in ("Administrador", "EncargadoTI"):
                pass

            else:
                return {
                    "nuevos": 0,
                    "en_proceso": 0,
                    "urgentes": 0,
                    "cerrados": 0
                }

            where_sql = ""

            if condiciones:
                where_sql = "WHERE " + " AND ".join(condiciones)

            sql = f"""
                SELECT

                    SUM(
                        CASE
                            WHEN e.nombre = 'Nuevo'
                            THEN 1
                            ELSE 0
                        END
                    ) AS nuevos,

                    SUM(
                        CASE
                            WHEN e.nombre = 'En Proceso'
                            THEN 1
                            ELSE 0
                        END
                    ) AS en_proceso,

                    SUM(
                        CASE
                            WHEN p.nombre = 'Urgente'
                            AND e.nombre <> 'Cerrado'
                            THEN 1
                            ELSE 0
                        END
                    ) AS urgentes,

                    SUM(
                        CASE
                            WHEN e.nombre = 'Cerrado'
                            THEN 1
                            ELSE 0
                        END
                    ) AS cerrados

                FROM tickets AS t

                INNER JOIN estados AS e
                    ON t.id_estado = e.id_estado

                INNER JOIN prioridades AS p
                    ON t.id_prioridad = p.id_prioridad

                {where_sql}
            """

            cursor.execute(
                sql,
                tuple(parametros)
            )

            resultado = cursor.fetchone()

            return {
                "nuevos": resultado["nuevos"] or 0,
                "en_proceso": resultado["en_proceso"] or 0,
                "urgentes": resultado["urgentes"] or 0,
                "cerrados": resultado["cerrados"] or 0
            }

        finally:
            if cursor is not None:
                cursor.close()

            if (
                conexion is not None
                and conexion.is_connected()
            ):
                conexion.close()

    @staticmethod
    def listar_tecnicos():
        conexion = None
        cursor = None

        try:
            conexion = conectar()
            cursor = conexion.cursor(dictionary=True)

            sql = """
                SELECT
                    u.id_usuario,
                    u.nombre,
                    u.apellido,
                    CONCAT(
                        u.nombre,
                        ' ',
                        u.apellido
                    ) AS nombre_completo
                FROM usuarios AS u
                INNER JOIN roles AS r
                    ON u.id_rol = r.id_rol
                WHERE r.nombre = 'Tecnico'
                  AND u.estado = 1
                ORDER BY
                    u.nombre,
                    u.apellido
            """

            cursor.execute(sql)

            return cursor.fetchall()

        finally:
            if cursor is not None:
                cursor.close()

            if (
                conexion is not None
                and conexion.is_connected()
            ):
                conexion.close()

    @staticmethod
    def asignar_tecnico(
        id_ticket,
        id_tecnico,
        id_usuario_accion
    ):
        conexion = None
        cursor = None

        try:
            conexion = conectar()
            cursor = conexion.cursor(dictionary=True)

            # ==========================================
            # OBTENER ESTADO "ASIGNADO"
            # ==========================================

            sql_estado = """
                SELECT id_estado
                FROM estados
                WHERE nombre = 'Asignado'
                LIMIT 1
            """

            cursor.execute(sql_estado)

            estado = cursor.fetchone()

            if estado is None:
                raise ValueError(
                    "No existe el estado 'Asignado' "
                    "en la base de datos."
                )

            id_estado_asignado = estado["id_estado"]

            # ==========================================
            # OBTENER DATOS DEL TÉCNICO
            # ==========================================

            sql_tecnico = """
                SELECT
                    nombre,
                    apellido
                FROM usuarios
                WHERE id_usuario = %s
                LIMIT 1
            """

            cursor.execute(
                sql_tecnico,
                (id_tecnico,)
            )

            tecnico = cursor.fetchone()

            if tecnico is None:
                raise ValueError(
                    "El técnico seleccionado no existe."
                )

            nombre_tecnico = (
                f"{tecnico['nombre']} "
                f"{tecnico['apellido']}"
            )

            # ==========================================
            # ACTUALIZAR TICKET
            # ==========================================

            sql_actualizar = """
                UPDATE tickets
                SET
                    id_tecnico = %s,
                    id_estado = %s,
                    fecha_asignacion = NOW()
                WHERE id_ticket = %s
            """

            cursor.execute(
                sql_actualizar,
                (
                    id_tecnico,
                    id_estado_asignado,
                    id_ticket
                )
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    "No fue posible encontrar el ticket."
                )

            # ==========================================
            # REGISTRAR HISTORIAL
            # ==========================================

            accion = (
                f"Ticket asignado al técnico "
                f"{nombre_tecnico}"
            )

            sql_historial = """
                INSERT INTO historial (
                    id_ticket,
                    id_usuario,
                    accion,
                    fecha
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    NOW()
                )
            """

            cursor.execute(
                sql_historial,
                (
                    id_ticket,
                    id_usuario_accion,
                    accion
                )
            )

            conexion.commit()

            return True

        except Exception:
            if conexion is not None:
                conexion.rollback()

            raise

        finally:
            if cursor is not None:
                cursor.close()

            if (
                conexion is not None
                and conexion.is_connected()
            ):
                conexion.close()