# Minimal HTML demo

Demo local mínima: FastAPI sirve directamente una página HTML en `/`.

## Requisitos

- Python 3.11 o posterior
- Windows PowerShell o una terminal compatible con el comando de activación indicado

## Preparación

Desde `my-project`:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev]"
```

## Inicio

```powershell
.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Abrí [http://127.0.0.1:8000/](http://127.0.0.1:8000/) y se mostrará `Hola mundo`.

## Verificación

```powershell
.venv\Scripts\python -m pytest
.venv\Scripts\python -m ruff check .
.venv\Scripts\python -m ruff format --check .
```

La prueba automatizada comprueba HTTP 200, contenido `text/html`, el título `Hola mundo`, su presencia visible y que dos solicitudes produzcan HTML idéntico.

## Revisión de dependencias

Última revisión: 2026-11-17.

| Paquete | Instalada | Más reciente | Tipo | Acción recomendada |
|---|---:|---:|---|---|
| pip | 25.0.1 | 26.3 | Herramienta del entorno; no es dependencia directa ni transitiva del proyecto | Opcional: actualizar después de revisar las [notas oficiales de pip](https://pip.pypa.io/en/stable/news/). No se considera bloqueante ni justifica cambiar dependencias del proyecto. |

La revisión se ejecutó con `.venv\Scripts\python -m pip list --outdated --format=json`. Las dependencias declaradas en `pyproject.toml` estaban actualizadas según el índice consultado. No hay lockfile. No se actualizaron paquetes automáticamente.
