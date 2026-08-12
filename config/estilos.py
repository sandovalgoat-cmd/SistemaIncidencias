# ==================================================
# COLORES GENERALES
# ==================================================

COLOR_PRIMARIO = "#1E88E5"
COLOR_PRIMARIO_OSCURO = "#1565C0"
COLOR_PRIMARIO_HOVER = "#0D47A1"

COLOR_SIDEBAR = "#263746"
COLOR_SIDEBAR_HOVER = "#34495E"

COLOR_FONDO = "#F4F6F8"
COLOR_PANEL = "#FFFFFF"

COLOR_TEXTO = "#1F2937"
COLOR_TEXTO_SECUNDARIO = "#6B7280"

COLOR_BORDE = "#D1D5DB"

# ==================================================
# COLORES DE ACCIÓN
# ==================================================

COLOR_EXITO = "#16A34A"
COLOR_EXITO_HOVER = "#15803D"

COLOR_ADVERTENCIA = "#F59E0B"
COLOR_ADVERTENCIA_HOVER = "#D97706"

COLOR_ERROR = "#DC2626"
COLOR_ERROR_HOVER = "#B91C1C"

COLOR_NEUTRO = "#6B7280"
COLOR_NEUTRO_HOVER = "#4B5563"

# ==================================================
# PRIORIDADES
# ==================================================

COLOR_PRIORIDAD_BAJA = "#22C55E"
COLOR_PRIORIDAD_MEDIA = "#3B82F6"
COLOR_PRIORIDAD_ALTA = "#F59E0B"
COLOR_PRIORIDAD_URGENTE = "#EF4444"

# ==================================================
# ESTADOS
# ==================================================

COLOR_ESTADO_NUEVO = "#64748B"
COLOR_ESTADO_ASIGNADO = "#2563EB"
COLOR_ESTADO_PROCESO = "#F59E0B"
COLOR_ESTADO_ESPERA = "#EA580C"
COLOR_ESTADO_SOLUCIONADO = "#16A34A"
COLOR_ESTADO_CERRADO = "#374151"

# ==================================================
# TIPOGRAFÍAS
# ==================================================

FUENTE_TITULO = ("Arial", 28, "bold")
FUENTE_SUBTITULO = ("Arial", 20, "bold")
FUENTE_SECCION = ("Arial", 17, "bold")

FUENTE_NORMAL = ("Arial", 14)
FUENTE_PEQUENA = ("Arial", 12)

FUENTE_MENU = ("Arial", 14)
FUENTE_MENU_TITULO = ("Arial", 24, "bold")

FUENTE_NUMERO_TARJETA = ("Arial", 30, "bold")

# ==================================================
# MEDIDAS GENERALES
# ==================================================

ANCHO_SIDEBAR = 220

ALTO_BOTON = 42
ALTO_CAMPO = 40

RADIO_PANEL = 10
RADIO_BOTON = 8
RADIO_TARJETA = 10

PADDING_GENERAL = 30
PADDING_PANEL = 20

# ==================================================
# FUNCIONES AUXILIARES
# ==================================================

def obtener_color_prioridad(prioridad):
    colores = {
        "Baja": COLOR_PRIORIDAD_BAJA,
        "Media": COLOR_PRIORIDAD_MEDIA,
        "Alta": COLOR_PRIORIDAD_ALTA,
        "Urgente": COLOR_PRIORIDAD_URGENTE
    }

    return colores.get(
        prioridad,
        COLOR_NEUTRO
    )


def obtener_color_estado(estado):
    colores = {
        "Nuevo": COLOR_ESTADO_NUEVO,
        "Asignado": COLOR_ESTADO_ASIGNADO,
        "En Proceso": COLOR_ESTADO_PROCESO,
        "En Espera": COLOR_ESTADO_ESPERA,
        "Solucionado": COLOR_ESTADO_SOLUCIONADO,
        "Cerrado": COLOR_ESTADO_CERRADO
    }

    return colores.get(
        estado,
        COLOR_NEUTRO
    )

    # ==================================================
    # BARRA SUPERIOR
    # ==================================================

COLOR_TOPBAR = "#343A40"
COLOR_TOPBAR_HOVER = "#495057"