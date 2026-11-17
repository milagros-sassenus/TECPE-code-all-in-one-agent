# Tasks: Demo mínima "Hola mundo"

**Input**: Design documents from `/specs/001-minimal-html-demo/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/ and quickstart.md

**Tests**: Se requiere un test de integración porque así lo solicita el plan y la constitución.

**Organization**: La única historia de usuario se implementa como MVP completo.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Puede ejecutarse en paralelo
- **[Story]**: Identifica la historia de usuario
- Todas las descripciones incluyen rutas de archivo concretas

## Phase 1: Setup

**Purpose**: Declarar el mínimo de dependencias y herramientas requerido.

- [X] T001 Configure Python 3.11+, FastAPI, Uvicorn, Pydantic, pytest, httpx y Ruff en `pyproject.toml`, incluyendo Ruff como herramienta de desarrollo

---

## Phase 2: Foundational

**Purpose**: No se requieren tareas fundacionales adicionales; no hay base de datos, autenticación, modelos ni infraestructura compartida.

**Checkpoint**: La estructura mínima puede implementarse directamente después de T001.

---

## Phase 3: User Story 1 - Ver la página de demo (Priority: P1) 🎯 MVP

**Goal**: Abrir la raíz local y ver un documento HTML con "Hola mundo".

**Independent Test**: Iniciar FastAPI, solicitar `GET /` y comprobar HTTP 200, `Content-Type: text/html`, `<title>Hola mundo</title>` y contenido visible "Hola mundo".

### Tests for User Story 1

- [X] T002 [US1] Create the integration test with FastAPI TestClient in `tests/test_app.py`, covering HTTP 200, HTML content type, the "Hola mundo" title and visible "Hola mundo" text, and make two requests to verify each succeeds with identical HTML
- [X] T003 [US1] Run `python -m pytest` for `tests/test_app.py` and confirm the test fails before the route is implemented

### Implementation for User Story 1

- [X] T004 [US1] Create the FastAPI application and `GET /` route returning inline HTML through `HTMLResponse` in `app/main.py`, with public function type annotations, `<title>Hola mundo</title>`, visible `<h1>Hola mundo</h1>`, and no JavaScript or external assets
- [X] T005 [US1] Run `python -m pytest` for `tests/test_app.py` and confirm the acceptance test passes

**Checkpoint**: La página de demo es funcional y verificable de manera independiente.

---

## Phase 4: Documentation & Verification

**Purpose**: Documentar el uso local y completar las puertas de calidad de la constitución.

- [X] T006 Update `README.md` with project-local `.venv` setup, dependency installation, the loopback Uvicorn command for `127.0.0.1:8000`, and verification at `http://127.0.0.1:8000/`
- [X] T007 Run `python -m pytest`, `python -m ruff check .` and `python -m ruff format --check .` from the project root and resolve all failures
- [X] T008 Confirm `python` resolves to the project `.venv`, run `python -m pip list --outdated --format=json`, and document in `README.md` the dependency review results against `pyproject.toml`, including installed and latest versions, dependency type, and recommended action

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: No tasks; no bloquea trabajo adicional.
- **User Story 1 (Phase 3)**: Depende de T001; T002 precede T003, T004 y T005.
- **Documentation & Verification (Phase 4)**: T006 puede prepararse tras T004; T007 depende de T004–T006. T008 depende de T001.

### User Story Dependencies

- **User Story 1 (P1)**: No depende de otras historias y constituye el MVP completo.

### Parallel Opportunities

- No hay trabajo paralelo que simplifique esta feature: la ruta y su test son inseparables como contrato, y la lista prioriza un flujo mínimo.
- T006 puede realizarse en paralelo con la preparación de T007 solo cuando la ruta ya exista; no debe omitirse la validación final secuencial.

## Implementation Strategy

### MVP First

1. Completar T001.
2. Escribir y ejecutar el test fallido con T002–T003.
3. Implementar la ruta mínima con T004.
4. Confirmar el test con T005.
5. Documentar el inicio local y ejecutar todas las verificaciones con T006–T008.

### Scope Guardrails

- No crear frontend, plantillas, JavaScript ni CSS separado.
- No agregar servicios, repositorios, base de datos o autenticación.
- No crear rutas `/api/v1`.
- No agregar archivos o capas que no estén requeridos por una tarea anterior.
