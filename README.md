# Sistema de Gestión de Incidencias TI

Sistema de escritorio desarrollado en Python para registrar, administrar y dar seguimiento a incidencias internas dentro de una empresa.

El objetivo principal es centralizar los reportes de problemas técnicos, evitando el uso de medios informales como llamadas, mensajes o reportes verbales.

El sistema permite registrar tickets, asignarlos a técnicos, controlar su estado, agregar comentarios, consultar el historial y cerrar las incidencias cuando han sido solucionadas.

---

## Funciones principales

- Inicio de sesión por usuario y contraseña.
- Control de acceso mediante roles.
- Registro de tickets de incidencias.
- Generación automática de folios.
- Clasificación por categoría y prioridad.
- Asignación y reasignación de técnicos.
- Seguimiento mediante estados.
- Comentarios públicos.
- Notas internas para el personal de TI.
- Historial de movimientos del ticket.
- Confirmación de solución por parte del empleado.
- Rechazo de solución para continuar trabajando el ticket.
- Cierre administrativo por Administrador o EncargadoTI.
- Administración de usuarios.
- Administración de catálogos.
- Dashboard con métricas.
- Reportes con filtros por fechas.

---

## Roles del sistema

### Empleado

Puede:

- Crear tickets.
- Consultar sus propios tickets.
- Agregar comentarios públicos.
- Consultar el seguimiento de sus incidencias.
- Confirmar una solución.
- Rechazar una solución si el problema continúa.

### Técnico

Puede:

- Consultar los tickets que tiene asignados.
- Cambiar el estado de los tickets.
- Agregar comentarios públicos.
- Agregar notas internas.
- Consultar el historial del ticket.

### EncargadoTI

Puede:

- Consultar todos los tickets.
- Asignar y reasignar técnicos.
- Cambiar estados.
- Agregar comentarios públicos.
- Agregar notas internas.
- Consultar reportes.
- Consultar métricas generales.
- Realizar cierres administrativos de tickets solucionados.

### Administrador

Cuenta con los permisos administrativos principales del sistema.

Puede:

- Consultar todos los tickets.
- Asignar y reasignar técnicos.
- Cambiar estados.
- Realizar cierres administrativos.
- Administrar usuarios.
- Administrar categorías.
- Administrar prioridades.
- Administrar áreas.
- Consultar reportes.
- Consultar métricas generales.

---

## Flujo de un ticket

El flujo general de una incidencia es:

```text
Nuevo
  ↓
Asignado
  ↓
En Proceso
  ↓
En Espera
  ↓
En Proceso
  ↓
Solucionado
  ↓
Cerrado