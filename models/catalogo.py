from config.database import conectar


class Catalogo:

    TABLAS_PERMITIDAS = {
        "categorias": "id_categoria",
        "prioridades": "id_prioridad",
        "areas": "id_area",
        "estados": "id_estado"
    }

    @staticmethod
    def listar(tabla):
        if tabla not in Catalogo.TABLAS_PERMITIDAS:
            raise ValueError("Catálogo no válido.")

        id_campo = Catalogo.TABLAS_PERMITIDAS[tabla]

        conexion = None
        cursor = None

        try:
            conexion = conectar()
            cursor = conexion.cursor(dictionary=True)

            sql = f"""
                SELECT
                    {id_campo} AS id,
                    nombre
                FROM {tabla}
                ORDER BY nombre
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
    def crear(tabla, nombre):
        if tabla not in Catalogo.TABLAS_PERMITIDAS:
            raise ValueError("Catálogo no válido.")

        conexion = None
        cursor = None

        try:
            conexion = conectar()
            cursor = conexion.cursor()

            sql = f"""
                INSERT INTO {tabla} (
                    nombre
                )
                VALUES (%s)
            """

            cursor.execute(
                sql,
                (nombre,)
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

            if (
                conexion is not None
                and conexion.is_connected()
            ):
                conexion.close()

    @staticmethod
    def editar(tabla, id_registro, nombre):
        if tabla not in Catalogo.TABLAS_PERMITIDAS:
            raise ValueError("Catálogo no válido.")

        id_campo = Catalogo.TABLAS_PERMITIDAS[tabla]

        conexion = None
        cursor = None

        try:
            conexion = conectar()
            cursor = conexion.cursor()

            sql = f"""
                UPDATE {tabla}
                SET nombre = %s
                WHERE {id_campo} = %s
            """

            cursor.execute(
                sql,
                (
                    nombre,
                    id_registro
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

            if (
                conexion is not None
                and conexion.is_connected()
            ):
                conexion.close()

    @staticmethod
    def eliminar(tabla, id_registro):
        if tabla not in Catalogo.TABLAS_PERMITIDAS:
            raise ValueError("Catálogo no válido.")

        id_campo = Catalogo.TABLAS_PERMITIDAS[tabla]

        conexion = None
        cursor = None

        try:
            conexion = conectar()
            cursor = conexion.cursor()

            sql = f"""
                DELETE FROM {tabla}
                WHERE {id_campo} = %s
            """

            cursor.execute(
                sql,
                (id_registro,)
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

            if (
                conexion is not None
                and conexion.is_connected()
            ):
                conexion.close()