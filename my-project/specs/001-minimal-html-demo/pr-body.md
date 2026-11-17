# Minimal FastAPI HTML demo

## Summary

- Add a single FastAPI route at `GET /`.
- Return inline HTML with a visible `Hola mundo` heading and matching title.
- Add an integration test covering HTTP 200, HTML content, and repeated identical responses.
- Declare Python 3.11+, pytest, Ruff, FastAPI, Pydantic, Uvicorn, and httpx.
- Document local setup, startup, verification, and dependency review.

## Acceptance scenarios

- Opening `http://127.0.0.1:8000/` returns HTTP 200 with `text/html`.
- The document includes `<title>Hola mundo</title>` and visible `<h1>Hola mundo</h1>`.
- Two requests produce identical HTML without JavaScript, authentication, a database, or external assets.
- No `/api/v1` endpoint, separate frontend, templates, services, or repositories were added.

## Verification

- `python -m pytest`: 1 passed
- `python -m ruff check .`: passed
- `python -m ruff format --check .`: passed
- `python -m pip check`: passed
- Live request to `http://127.0.0.1:8000/`: HTTP 200 with `text/html; charset=utf-8`

## Dependency review

- `pip 25.0.1` is outdated; latest reported version is `26.3`.
- Type: environment/tooling dependency, not a direct application dependency.
- Recommended action: optional upgrade after consulting the official pip release notes.
- No automatic upgrade was performed; this result is advisory and not a publication blocker.
- No lockfile is present.

## Limitations

This is a local-only, single-page demo and is not intended as a production deployment.
