from config.database import conectar


class Usuario:

    @staticmethod
    def login(nombre_usuario):
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
                    u.usuario,
                    u.password,
                    u.estado,
                    u.id_rol,
                    u.id_area,
                    r.nombre AS rol,
                    a.nombre AS area
                FROM usuarios AS u
                INNER JOIN roles AS r
                    ON u.id_rol = r.id_rol
                LEFT JOIN areas AS a
                    ON u.id_area = a.id_area
                WHERE u.usuario = %s
                LIMIT 1
            """

            cursor.execute(sql, (nombre_usuario,))
            return cursor.fetchone()

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None and conexion.is_connected():
                conexion.close()

    @staticmethod
    def listar():
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
                    u.usuario,
                    u.estado,
                    u.fecha_alta,
                    u.id_rol,
                    u.id_area,
                    r.nombre AS rol,
                    COALESCE(a.nombre, 'Sin área') AS area
                FROM usuarios AS u
                INNER JOIN roles AS r
                    ON u.id_rol = r.id_rol
                LEFT JOIN areas AS a
                    ON u.id_area = a.id_area
                ORDER BY u.id_usuario DESC
            """

            cursor.execute(sql)
            return cursor.fetchall()

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None and conexion.is_connected():
                conexion.close()

    @staticmethod
    def crear(
        nombre,
        apellido,
        nombre_usuario,
        password,
        id_rol,
        id_area
    ):
        conexion = None
        cursor = None

        try:
            conexion = conectar()
            cursor = conexion.cursor()

            sql = """
                INSERT INTO usuarios (
                    nombre,
                    apellido,
                    usuario,
                    password,
                    estado,
                    id_rol,
                    id_area
                )
                VALUES (%s, %s, %s, %s, 1, %s, %s)
            """

            cursor.execute(
                sql,
                (
                    nombre,
                    apellido,
                    nombre_usuario,
                    password,
                    id_rol,
                    id_area
                )
            )

            conexion.commit()
            return cursor.lastrowid

        except Exception:
            if conexion is not None:
                conexion.rollback()
            raise

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None and conexion.is_connected():
                conexion.close()

    @staticmethod
    def actualizar(
        id_usuario,
        nombre,
        apellido,
        nombre_usuario,
        id_rol,
        id_area
    ):
        conexion = None
        cursor = None

        try:
            conexion = conectar()
            cursor = conexion.cursor()

            sql = """
                UPDATE usuarios
                SET
                    nombre = %s,
                    apellido = %s,
                    usuario = %s,
                    id_rol = %s,
                    id_area = %s
                WHERE id_usuario = %s
            """

            cursor.execute(
                sql,
                (
                    nombre,
                    apellido,
                    nombre_usuario,
                    id_rol,
                    id_area,
                    id_usuario
                )
            )

            conexion.commit()
            return cursor.rowcount > 0

        except Exception:
            if conexion is not None:
                conexion.rollback()
            raise

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None and conexion.is_connected():
                conexion.close()

    @staticmethod
    def cambiar_estado(id_usuario, nuevo_estado):
        conexion = None
        cursor = None

        try:
            conexion = conectar()
            cursor = conexion.cursor()

            sql = """
                UPDATE usuarios
                SET estado = %s
                WHERE id_usuario = %s
            """

            cursor.execute(sql, (nuevo_estado, id_usuario))
            conexion.commit()

            return cursor.rowcount > 0

        except Exception:
            if conexion is not None:
                conexion.rollback()
            raise

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None and conexion.is_connected():
                conexion.close()

    @staticmethod
    def cambiar_password(id_usuario, nueva_password):
        conexion = None
        cursor = None

        try:
            conexion = conectar()
            cursor = conexion.cursor()

            sql = """
                UPDATE usuarios
                SET password = %s
                WHERE id_usuario = %s
            """

            cursor.execute(sql, (nueva_password, id_usuario))
            conexion.commit()

            return cursor.rowcount > 0

        except Exception:
            if conexion is not None:
                conexion.rollback()
            raise

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None and conexion.is_connected():
                conexion.close()

    @staticmethod
    def usuario_existe(nombre_usuario, id_usuario_excluir=None):
        conexion = None
        cursor = None

        try:
            conexion = conectar()
            cursor = conexion.cursor(dictionary=True)

            if id_usuario_excluir is None:
                sql = """
                    SELECT id_usuario
                    FROM usuarios
                    WHERE usuario = %s
                    LIMIT 1
                """

                cursor.execute(sql, (nombre_usuario,))

            else:
                sql = """
                    SELECT id_usuario
                    FROM usuarios
                    WHERE usuario = %s
                      AND id_usuario <> %s
                    LIMIT 1
                """

                cursor.execute(
                    sql,
                    (nombre_usuario, id_usuario_excluir)
                )

            return cursor.fetchone() is not None

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None and conexion.is_connected():
                conexion.close()