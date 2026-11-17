# Contract: Página raíz

## Endpoint

- **Method**: `GET`
- **Path**: `/`
- **Authentication**: Ninguna
- **Input**: Ninguno

## Successful response

- **Status**: `200 OK`
- **Content-Type**: `text/html` con codificación compatible con UTF-8
- **Body constraints**:
  - Documento HTML completo.
  - `<title>Hola mundo</title>`.
  - Contenido visible como `<h1>Hola mundo</h1>`.
  - Sin dependencia de JavaScript, estilos externos ni recursos remotos.

## Example

```http
GET / HTTP/1.1
Host: 127.0.0.1:8000
```

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<!DOCTYPE html>
<html lang="es">
  <head><title>Hola mundo</title></head>
  <body><h1>Hola mundo</h1></body>
</html>
```

## Scope exclusions

- No existe contrato `/api/v1` para esta feature.
- No se esperan parámetros, headers personalizados, credenciales, sesión ni cuerpo de solicitud.
- Casos de validación o recursos inexistentes no aplican a una página raíz estática sin entradas.

