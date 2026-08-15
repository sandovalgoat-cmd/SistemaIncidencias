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

            ticket = Ticket.obtener_ticket_por_id(
                id_ticket
            )

            if ticket is None:
                return (
                    False,
                    "El ticket no existe."
                )

            if ticket["estado"] == "Cerrado":
                return (
                    False,
                    "No se puede reasignar un ticket cerrado."
                )

            Ticket.asignar_tecnico(
                id_ticket=id_ticket,
                id_tecnico=id_tecnico,
                id_usuario_accion=
                    usuario_sesion["id_usuario"]
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

        rol = usuario_sesion["rol"]

        # ==========================================
        # VALIDAR ROL
        # ==========================================

        if rol not in (
            "Tecnico",
            "EncargadoTI",
            "Administrador"
        ):
            return (
                False,
                "No tiene permisos para cambiar el estado."
            )

        # ==========================================
        # ESTADOS VÁLIDOS
        # ==========================================

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

            # ==========================================
            # CONSULTAR TICKET ACTUAL
            # ==========================================

            ticket = Ticket.obtener_ticket_por_id(
                id_ticket
            )

            if ticket is None:
                return (
                    False,
                    "El ticket no existe."
                )

            estado_actual = ticket["estado"]

            # ==========================================
            # TÉCNICO: SOLO SUS TICKETS
            # ==========================================

            if rol == "Tecnico":

                if (
                    ticket["id_tecnico"]
                    != usuario_sesion["id_usuario"]
                ):
                    return (
                        False,
                        "Este ticket no está asignado a usted."
                    )

            # ==========================================
            # NO MODIFICAR TICKETS CERRADOS
            # ==========================================

            if estado_actual == "Cerrado":
                return (
                    False,
                    "Un ticket cerrado no puede modificarse."
                )

            # ==========================================
            # TRANSICIONES PERMITIDAS
            # ==========================================

            transiciones = {

                "Nuevo": (
                    "Asignado",
                ),

                "Asignado": (
                    "En Proceso",
                ),

                "En Proceso": (
                    "En Espera",
                    "Solucionado"
                ),

                "En Espera": (
                    "En Proceso",
                    "Solucionado"
                ),

                "Solucionado": ()
            }

            permitidos_desde_actual = (
                transiciones.get(
                    estado_actual,
                    ()
                )
            )

            if nuevo_estado not in permitidos_desde_actual:

                return (
                    False,
                    (
                        f"No se puede cambiar de "
                        f"'{estado_actual}' a "
                        f"'{nuevo_estado}'."
                    )
                )

            # ==========================================
            # ACTUALIZAR
            # ==========================================

            Ticket.cambiar_estado(
                id_ticket=id_ticket,
                nuevo_estado=nuevo_estado,
                id_usuario_accion=
                    usuario_sesion["id_usuario"]
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

        # ==========================================
        # VALIDAR COMENTARIO
        # ==========================================

        comentario = comentario.strip()

        if not comentario:
            return (
                False,
                "El comentario no puede estar vacío."
            )

        # ==========================================
        # PROTEGER NOTAS INTERNAS
        # ==========================================

        if (
            not publico
            and usuario_sesion["rol"]
            not in (
                "Administrador",
                "EncargadoTI",
                "Tecnico"
            )
        ):
            return (
                False,
                "No tiene permisos para agregar notas internas."
            )

        try:

            # ==========================================
            # OBTENER TICKET
            # ==========================================

            ticket = Ticket.obtener_ticket_por_id(
                id_ticket
            )

            if ticket is None:
                return (
                    False,
                    "El ticket no existe."
                )

            # ==========================================
            # TICKET CERRADO
            # ==========================================

            if ticket["estado"] == "Cerrado":
                return (
                    False,
                    "No se pueden agregar comentarios "
                    "a un ticket cerrado."
                )

            # ==========================================
            # VALIDACIÓN PARA TÉCNICO
            # ==========================================

            if (
                usuario_sesion["rol"] == "Tecnico"
                and ticket["id_tecnico"]
                != usuario_sesion["id_usuario"]
            ):
                return (
                    False,
                    "Este ticket no está asignado a usted."
                )

            # ==========================================
            # VALIDACIÓN PARA EMPLEADO
            # ==========================================

            if (
                usuario_sesion["rol"] == "Empleado"
                and ticket["id_usuario"]
                != usuario_sesion["id_usuario"]
            ):
                return (
                    False,
                    "No puede comentar un ticket "
                    "que no le pertenece."
                )

            # ==========================================
            # GUARDAR COMENTARIO
            # ==========================================

            Ticket.agregar_comentario(
                id_ticket=id_ticket,
                id_usuario=usuario_sesion["id_usuario"],
                comentario=comentario,
                publico=publico
            )

            return (
                True,
                "Comentario agregado correctamente."
            )

        except mysql.connector.Error as error:

            return (
                False,
                f"Error de base de datos: {error}"
            )

        except Exception as error:

            return (
                False,
                f"No fue posible agregar el comentario: {error}"
            )

    @staticmethod
    def listar_comentarios(
        id_ticket,
        usuario_sesion
    ):

        try:

            # ==========================================
            # OBTENER TICKET
            # ==========================================

            ticket = Ticket.obtener_ticket_por_id(
                id_ticket
            )

            if ticket is None:
                return (
                    False,
                    "El ticket no existe."
                )

            rol = usuario_sesion["rol"]

            # ==========================================
            # VALIDAR ACCESO DEL EMPLEADO
            # ==========================================

            if (
                rol == "Empleado"
                and ticket["id_usuario"]
                != usuario_sesion["id_usuario"]
            ):
                return (
                    False,
                    "No tiene permisos para consultar "
                    "los comentarios de este ticket."
                )

            # ==========================================
            # VALIDAR ACCESO DEL TÉCNICO
            # ==========================================

            if (
                rol == "Tecnico"
                and ticket["id_tecnico"]
                != usuario_sesion["id_usuario"]
            ):
                return (
                    False,
                    "Este ticket no está asignado a usted."
                )

            # ==========================================
            # NOTAS INTERNAS
            # ==========================================

            incluir_privados = (
                rol in (
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
    def listar_historial(
        id_ticket,
        usuario_sesion
    ):

        try:

            ticket = Ticket.obtener_ticket_por_id(
                id_ticket
            )

            if ticket is None:
                return (
                    False,
                    "El ticket no existe."
                )

            rol = usuario_sesion["rol"]

            # ==========================================
            # EMPLEADO: SOLO SUS TICKETS
            # ==========================================

            if (
                rol == "Empleado"
                and ticket["id_usuario"]
                != usuario_sesion["id_usuario"]
            ):
                return (
                    False,
                    "No tiene permisos para consultar "
                    "el historial de este ticket."
                )

            # ==========================================
            # TÉCNICO: SOLO SUS TICKETS ASIGNADOS
            # ==========================================

            if (
                rol == "Tecnico"
                and ticket["id_tecnico"]
                != usuario_sesion["id_usuario"]
            ):
                return (
                    False,
                    "Este ticket no está asignado a usted."
                )

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

    @staticmethod
    def obtener_reportes(
        usuario_sesion,
        fecha_inicio=None,
        fecha_fin=None
    ):

        # ==========================================
        # VALIDAR PERMISOS
        # ==========================================

        if usuario_sesion["rol"] not in (
            "Administrador",
            "EncargadoTI"
        ):
            return (
                False,
                "No tiene permisos para consultar reportes."
            )

        try:

            # ==========================================
            # OBTENER INFORMACIÓN DEL MODELO
            # ==========================================

            resultado = {

                "general":
                    Ticket.obtener_reporte_general(),

                "estados":
                    Ticket.reporte_por_estado(
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin
                    ),

                "prioridades":
                    Ticket.reporte_por_prioridad(
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin
                    ),

                "categorias":
                    Ticket.reporte_por_categoria(
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin
                    ),

                "tecnicos":
                    Ticket.reporte_por_tecnico(
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin
                    )
            }

            return True, resultado

        except mysql.connector.Error as error:

            return (
                False,
                f"Error de base de datos: {error}"
            )

        except Exception as error:

            return (
                False,
                f"No fue posible generar los reportes: {error}"
            )   

    @staticmethod
    def obtener_metricas_tiempo(
        usuario_sesion,
        fecha_inicio=None,
        fecha_fin=None
    ):

        if usuario_sesion["rol"] not in (
            "Administrador",
            "EncargadoTI"
        ):
            return (
                False,
                "No tiene permisos para consultar métricas."
            )

        try:
            resultado = Ticket.obtener_metricas_tiempo(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )

            return True, resultado

        except mysql.connector.Error as error:
            return (
                False,
                f"Error de base de datos: {error}"
            )

        except Exception as error:
            return (
                False,
                f"No fue posible consultar las métricas: {error}"
            )

    @staticmethod
    def obtener_metricas_dashboard(
        usuario_sesion
    ):

        if usuario_sesion["rol"] not in (
            "Administrador",
            "EncargadoTI"
        ):
            return (
                False,
                "No tiene permisos para consultar "
                "las métricas del Dashboard."
            )

        try:

            metricas = (
                Ticket.obtener_metricas_dashboard()
            )

            return (
                True,
                metricas
            )

        except mysql.connector.Error as error:

            return (
                False,
                f"Error de base de datos: {error}"
            )

        except Exception as error:

            return (
                False,
                f"No fue posible obtener las métricas: {error}"
            )

    @staticmethod
    def obtener_metricas_por_usuario(
        usuario_sesion
    ):

        rol = usuario_sesion["rol"]

        if rol not in (
            "Tecnico",
            "Empleado"
        ):
            return (
                False,
                "Este tipo de usuario no utiliza "
                "métricas individuales."
            )

        try:

            metricas = (
                Ticket.obtener_metricas_por_usuario(
                    id_usuario=usuario_sesion["id_usuario"],
                    rol=rol
                )
            )

            return (
                True,
                metricas
            )

        except mysql.connector.Error as error:

            return (
                False,
                f"Error de base de datos: {error}"
            )

        except Exception as error:

            return (
                False,
                f"No fue posible obtener las métricas: {error}"
            ) 

    @staticmethod
    def obtener_resumen_dashboard(
        usuario_sesion
    ):

        if usuario_sesion["rol"] not in (
            "Administrador",
            "EncargadoTI"
        ):
            return (
                False,
                "No tiene permisos para consultar "
                "el resumen del Dashboard."
            )

        try:

            resultado = {
                "carga_tecnicos":
                    Ticket.obtener_carga_tecnicos(),

                "tickets_recientes":
                    Ticket.obtener_tickets_recientes(
                        limite=5
                    )
            }

            return (
                True,
                resultado
            )

        except mysql.connector.Error as error:

            return (
                False,
                f"Error de base de datos: {error}"
            )

        except Exception as error:

            return (
                False,
                f"No fue posible cargar el resumen: {error}"
            )    

    @staticmethod
    def cerrar_administrativamente(
        id_ticket,
        usuario_sesion
    ):
        rol = usuario_sesion["rol"]

        # ==========================================
        # VALIDAR ROL
        # ==========================================

        if rol not in (
            "Administrador",
            "EncargadoTI"
        ):
            return (
                False,
                "No tiene permisos para cerrar "
                "administrativamente un ticket."
            )

        try:

            ticket = Ticket.obtener_ticket_por_id(
                id_ticket
            )

            if ticket is None:
                return (
                    False,
                    "El ticket no existe."
                )

            if ticket["estado"] != "Solucionado":
                return (
                    False,
                    "Solo se pueden cerrar administrativamente "
                    "tickets que estén en estado Solucionado."
                )

            Ticket.cerrar_administrativamente(
                id_ticket=id_ticket,
                id_usuario_accion=
                    usuario_sesion["id_usuario"],
                rol_accion=rol
            )

            return (
                True,
                "El ticket fue cerrado administrativamente."
            )

        except mysql.connector.Error as error:
            return (
                False,
                f"Error de base de datos: {error}"
            )

        except Exception as error:
            return (
                False,
                f"No fue posible cerrar el ticket: {error}"
            )               