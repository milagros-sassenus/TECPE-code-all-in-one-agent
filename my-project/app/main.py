from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def read_root() -> HTMLResponse:
    return HTMLResponse(
        """<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <title>Hola mundo</title>
  </head>
  <body>
    <h1>Hola mundo</h1>
  </body>
</html>
"""
    )
