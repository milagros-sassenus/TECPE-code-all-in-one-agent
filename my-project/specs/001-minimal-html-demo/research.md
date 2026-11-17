# Research: Demo mínima "Hola mundo"

## Rendering approach

**Decision**: Devolver un literal HTML con `fastapi.responses.HTMLResponse` desde la ruta raíz.

**Rationale**: Es la opción más simple para una página estática única y conserva una respuesta HTML correcta sin motor de plantillas ni archivos externos.

**Alternatives considered**:

- Motor de plantillas: rechazado porque agrega una dependencia y archivos sin valor para una sola cadena HTML.
- Archivo HTML estático separado: rechazado porque la página puede permanecer autocontenida y servida directamente por FastAPI.
- Respuesta JSON y renderizado del cliente: rechazada porque contradice el requisito de HTML en `/` y la prohibición de JavaScript.

## Application structure

**Decision**: Mantener la instancia FastAPI, la ruta `GET /` y la respuesta HTML en `app/main.py`.

**Rationale**: Una ruta sin lógica de negocio no necesita capas de servicios ni repositorios; separarlas aumentaría la superficie sin cubrir ningún requisito.

**Alternatives considered**:

- Arquitectura por capas: rechazada por ser innecesaria sin reglas de negocio, modelos ni persistencia.
- Frontend separado: rechazado por el límite explícito de alcance.
- CSS externo: rechazado porque el texto visible no requiere presentación adicional.

## Integration testing

**Decision**: Usar pytest con FastAPI TestClient para una petición real al enrutador ASGI.

**Rationale**: El test comprueba estado, encabezado HTML y contenido sin iniciar otro proceso.

**Alternatives considered**:

- Solo prueba manual: rechazada porque la constitución exige automatización.
- Llamar directamente a la función de ruta: rechazado porque no verificaría la respuesta HTTP.
- Lanzar Uvicorn durante el test: rechazado como coordinación innecesaria para este contrato.

## Dependency and tooling choices

**Decision**: Declarar FastAPI y Uvicorn como dependencias de ejecución, y pytest, httpx y Ruff como herramientas de desarrollo en `pyproject.toml`.

**Rationale**: Cubre ejecución, prueba y controles de calidad exigidos. Pydantic será utilizado por FastAPI, aunque no se declaran modelos específicos porque no hay entradas.

**Alternatives considered**:

- Ejecutar sin `pyproject.toml`: rechazado porque contradice la constitución.
- Instalar herramientas globales: rechazado porque la constitución exige un `.venv` local.

