# Implementation Plan: Demo mínima "Hola mundo"

**Branch**: `001-minimal-html-demo` | **Date**: 2026-11-17 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-minimal-html-demo/spec.md`

## Summary

Implementar una demo local única con Python 3.11+ y FastAPI. Una ruta `GET /` devolverá directamente un documento HTML mínimo mediante `HTMLResponse`, con una etiqueta de título y contenido visible "Hola mundo". No habrá frontend separado, motor de plantillas, CSS externo, JavaScript, autenticación, base de datos, servicios ni repositorios. La verificación automatizada usará FastAPI TestClient para comprobar estado 200, tipo de contenido HTML y presencia del texto "Hola mundo".

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: FastAPI, Uvicorn y Pydantic

**Storage**: No aplica; no se persistirán datos

**Testing**: pytest y FastAPI TestClient, con httpx como dependencia compatible del cliente de pruebas

**Quality Tooling**: Ruff para lint y verificación de formato

**Target Platform**: Ejecución local en loopback mediante `http://127.0.0.1:8000/`

**Project Type**: Aplicación web Python única

**Performance Goals**: La página debe poder abrirse y verificarse en menos de 10 segundos; no se fijan objetivos de carga o concurrencia

**Constraints**: HTML inline servido desde la ruta raíz; sin frontend separado, plantillas, CSS externo, JavaScript, autenticación, base de datos, servicios ni repositorios; variables y funciones Python en inglés

**Scale/Scope**: Una ruta, un documento HTML estático, una aplicación y un test de aceptación

**Dependency Declaration**: `pyproject.toml` declarará las dependencias mínimas de ejecución y desarrollo; `.venv` será project-local

## Constitution Check

*GATE: Revisión inicial superada; se reevalúa después del diseño.*

- **I. Specify Before Implementing**: PASS. Existe especificación con alcance, escenarios, casos límite y criterios medibles.
- **II. Python API First**: PASS con alcance acotado. Se usa Python 3.11+, FastAPI y Pydantic provisto por el framework. No hay datos de entrada o modelos JSON que validar. La respuesta HTML se limita explícitamente a `/`, por solicitud de la feature, sin crear un endpoint `/api/v1`.
- **III. Small, Understandable Solutions**: PASS. Se selecciona una sola aplicación con una ruta delgada y se excluyen capas e infraestructura innecesarias.
- **IV. Observable, Testable Behavior**: PASS. El test con FastAPI TestClient cubre el escenario exitoso observable. Los escenarios de entrada inválida o recurso ausente no son aplicables a una única ruta estática sin entradas.
- **V. Explicit Errors and Safe Demo Data**: PASS. La página no procesa datos ni usa secretos; se conserva el manejo estándar de errores del servidor.
- **Technical constraints**: PASS. Ejecución local, loopback, `.venv`, `pyproject.toml`, pytest, Ruff, tipado público y guía reproducible quedan planificados.
- **Workflow gates**: PASS. Esta fase produce solo planificación; tareas, análisis e implementación ocurrirán en comandos posteriores.

## Project Structure

### Documentation (this feature)

```text
specs/001-minimal-html-demo/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── root-page.md
├── checklists/
│   └── requirements.md
└── tasks.md             # Lista ejecutable generada por speckit-tasks
```

### Source Code (repository root)

```text
pyproject.toml
app/
└── main.py
tests/
└── test_app.py
```

**Structure Decision**: Se adopta una aplicación Python única. `app/main.py` contendrá la instancia FastAPI y la única ruta; `tests/test_app.py` contendrá el test de integración solicitado. No se crean carpetas de servicios, repositorios, modelos, assets, plantillas ni frontend. Las herramientas y dependencias se declaran en `pyproject.toml`.

## Verification Strategy

- Un test de integración solicitará `GET /` mediante `TestClient`.
- Verificará HTTP 200, un encabezado `Content-Type` compatible con `text/html`, `<title>Hola mundo</title>` y contenido visible `<h1>Hola mundo</h1>`.
- Durante implementación se ejecutarán `python -m pytest`, `python -m ruff check .` y `python -m ruff format --check .`.
- Antes de completar la feature se ejecutará `python -m pip list --outdated --format=json`, confirmando previamente que `python` resuelve al `.venv` del proyecto.

## Complexity Tracking

No hay violaciones constitucionales que justificar. La respuesta HTML en `/` está solicitada explícitamente y no compite con endpoints JSON porque no se crea ningún endpoint `/api/v1`.

## Post-Design Constitution Check

- **I–V**: PASS. El diseño cubre el escenario con un test, no introduce complejidad y no utiliza datos sensibles.
- **Tooling and workflow**: PASS. El plan declara `.venv`, `pyproject.toml`, pytest, Ruff y revisión de dependencias.
- **Local delivery**: PASS. `quickstart.md` define arranque en loopback, prueba automatizada y verificación por navegador.

