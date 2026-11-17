# Quickstart: Demo mínima "Hola mundo"

Esta guía describe la validación prevista. Los archivos de aplicación y las dependencias se crearán durante `speckit-implement`, no como parte de esta fase de planificación.

## Prerequisites

- Python 3.11+
- Git
- Acceso local a `127.0.0.1:8000`

## Setup

Desde la raíz de `my-project`:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev]"
```

Confirmar que `python` corresponde al `.venv`:

```powershell
.venv\Scripts\python -c "import sys; print(sys.executable)"
```

## Run the application

```powershell
.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Abrir `http://127.0.0.1:8000/`. El resultado esperado es una página HTML con "Hola mundo" visible.

## Run acceptance validation

```powershell
.venv\Scripts\python -m pytest
.venv\Scripts\python -m ruff check .
.venv\Scripts\python -m ruff format --check .
```

La prueba de integración debe confirmar:

1. `GET /` retorna HTTP 200.
2. El encabezado identifica contenido `text/html`.
3. El documento contiene `<title>Hola mundo</title>`.
4. El documento muestra "Hola mundo" en contenido visible.

## Dependency review

Antes de declarar completa la feature:

```powershell
.venv\Scripts\python -m pip list --outdated --format=json
```

Comparar el resultado con `pyproject.toml` y reportar para cada paquete desactualizado su versión instalada, versión más reciente, tipo de dependencia y acción recomendada. No actualizar automáticamente.
