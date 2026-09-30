"""Estimaciones históricas (ficticias) que se inyectan en el prompt como few-shot examples.

Esta es la "base de conocimiento" de la arquitectura CAG: viaja completa en cada llamada al LLM.
"""

ESTIMATION_EXAMPLES = [
    {
        "meeting_summary": (
            "El cliente, una distribuidora de repuestos con 3 bodegas, necesita una plataforma web "
            "de gestión de inventario. Quiere registrar entradas y salidas de productos, ver el stock "
            "por bodega en tiempo real, recibir alertas cuando un producto baje del stock mínimo y "
            "tener un dashboard con métricas de rotación. Habrá usuarios administradores y operarios "
            "de bodega con permisos distintos. No tienen diseño previo."
        ),
        "estimation": """## Estimación: Plataforma de Gestión de Inventario

### Supuestos
- Aplicación web responsive; no se incluye app móvil nativa.
- No existe diseño previo: se incluye diseño UI/UX desde cero.
- Carga inicial de datos vía importación CSV provista por el cliente.

### Desglose de tareas:
1. Diseño UI/UX (wireframes + prototipo): 40 horas
2. Backend API (CRUD productos, bodegas, movimientos): 60 horas
3. Autenticación y roles (admin / operario): 20 horas
4. Alertas de stock mínimo (email + notificación en app): 16 horas
5. Dashboard con métricas de rotación: 30 horas
6. Importación inicial CSV: 8 horas
7. Testing y QA: 25 horas
8. Despliegue e infraestructura (CI/CD, entorno productivo): 12 horas

**Total estimado: 211 horas**
**Equipo recomendado: 2 desarrolladores full-stack + 1 diseñador UX (part-time)**
**Duración estimada: 6-8 semanas**

### Riesgos
- Calidad de los datos de la importación inicial.
- "Tiempo real" puede requerir websockets si el cliente espera actualización sin recargar.
""",
    },
    {
        "meeting_summary": (
            "Una clínica dental con 2 sucursales quiere un sistema de reserva de horas online. Los "
            "pacientes deben poder agendar, reprogramar y cancelar citas desde la web, recibir "
            "recordatorios por WhatsApp 24 horas antes y pagar un abono con tarjeta al reservar. "
            "La recepción necesita una agenda por dentista. Ya tienen la identidad de marca y un "
            "sitio web en WordPress donde se debe incrustar el widget de reservas."
        ),
        "estimation": """## Estimación: Sistema de Reservas Online para Clínica Dental

### Supuestos
- Existe identidad de marca; el diseño se limita a adaptar componentes.
- El widget se embebe en el WordPress existente (iframe o script).
- El cliente contrata la cuenta de WhatsApp Business API y la pasarela de pago.

### Desglose de tareas:
1. Diseño UI del widget y panel de recepción: 20 horas
2. Backend API (pacientes, dentistas, sucursales, citas): 50 horas
3. Lógica de disponibilidad y agenda por dentista: 30 horas
4. Integración pasarela de pago (abono al reservar + reembolsos): 24 horas
5. Recordatorios automáticos por WhatsApp (24 h antes): 16 horas
6. Widget embebible en WordPress: 14 horas
7. Panel de recepción (agenda diaria/semanal): 28 horas
8. Testing y QA: 22 horas
9. Despliegue e infraestructura: 10 horas

**Total estimado: 234 horas**
**Equipo recomendado: 2 desarrolladores full-stack + 1 diseñador UI (part-time)**
**Duración estimada: 7-9 semanas**

### Riesgos
- Aprobación de plantillas de WhatsApp Business por parte de Meta (puede tardar días).
- Políticas de cancelación/reembolso no definidas aún por el cliente.
""",
    },
]
