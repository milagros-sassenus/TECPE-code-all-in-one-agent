# Feature Specification: Demo mínima "Hola mundo"

**Feature Branch**: `001-minimal-html-demo`

**Created**: 2026-11-17

**Status**: Draft

**Input**: User description: "Una página web mínima de demo: al abrir http://127.0.0.1:8000/ en el navegador debe mostrarse una página HTML con el título visible "Hola mundo". Sin frontend separado, JavaScript, autenticación ni base de datos. La página debe ser servida por Python/FastAPI. El endpoint raíz devuelve HTML; no es un endpoint JSON de /api/v1."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ver la página de demo (Priority: P1)

Como visitante local, quiero abrir la dirección raíz de la aplicación y ver inmediatamente una página que diga "Hola mundo", sin pasos previos ni interacción adicional.

**Why this priority**: Es el único objetivo de valor de la demo y permite verificar de forma directa que la aplicación web está disponible.

**Independent Test**: Iniciar la aplicación localmente, abrir `http://127.0.0.1:8000/` en un navegador nuevo y confirmar que aparece una página HTML con "Hola mundo" visible.

**Acceptance Scenarios**:

1. **Given** que la aplicación está ejecutándose localmente, **When** el visitante abre `http://127.0.0.1:8000/`, **Then** el navegador muestra una página HTML cuyo contenido visible incluye exactamente "Hola mundo".
2. **Given** que la aplicación está ejecutándose localmente, **When** el visitante solicita la ruta raíz repetidamente, **Then** cada solicitud muestra la misma página de demo sin requerir JavaScript, autenticación ni datos almacenados.

### Edge Cases

- Si el navegador incluye parámetros de consulta al abrir la ruta raíz, la página de demo debe seguir mostrándose normalmente.
- Si JavaScript está deshabilitado en el navegador, el texto "Hola mundo" debe continuar visible.
- La solicitud no debe depender de credenciales, sesiones, una base de datos ni un servicio externo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La ruta raíz MUST responder con un documento HTML navegable.
- **FR-002**: El documento HTML MUST mostrar visualmente el texto "Hola mundo" al abrirse.
- **FR-003**: La demo MUST estar disponible en `http://127.0.0.1:8000/` durante su ejecución local.
- **FR-004**: La ruta raíz MUST devolver HTML y MUST NOT ser un endpoint JSON bajo `/api/v1`.
- **FR-005**: La página MUST funcionar sin JavaScript del lado del cliente.
- **FR-006**: La solución MUST NOT requerir un frontend separado.
- **FR-007**: La página MUST NOT requerir autenticación ni permitir que una sesión afecte su acceso.
- **FR-008**: La solución MUST NOT requerir ni utilizar una base de datos.
- **FR-009**: La entrega MUST respetar la restricción solicitada de ser servida mediante Python/FastAPI.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: En el 100 % de las aperturas nuevas de `http://127.0.0.1:8000/`, "Hola mundo" es visible sin interacción adicional.
- **SC-002**: El 100 % de las solicitudes directas a la ruta raíz recibe una página HTML, no una respuesta JSON.
- **SC-003**: Una persona puede completar la verificación principal en menos de 10 segundos después de abrir la dirección local.
- **SC-004**: La página conserva el resultado visible con JavaScript deshabilitado y sin autenticación, datos persistidos ni servicios externos.

## Assumptions

- La aplicación se ejecutará localmente y la prueba principal se realizará contra la dirección loopback indicada.
- "Título visible" significa contenido presentado de forma visible al usuario, no exclusivamente el título interno de la pestaña del navegador.
- El alcance termina en la página única de demo; no se requieren otras rutas, estilos avanzados, formularios, acciones ni capacidades de administración.
- La restricción de Python/FastAPI es una decisión explícita del solicitante y prevalece como límite técnico de esta feature. La constitución actual reserva `/api/v1` para respuestas JSON; esta especificación solicita deliberadamente una respuesta HTML en `/`, sin introducir un endpoint `/api/v1`.

