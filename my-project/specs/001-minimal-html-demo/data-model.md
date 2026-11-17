# Data Model: Demo mínima "Hola mundo"

No se requieren entidades ni persistencia para esta feature.

- La aplicación no recibe datos estructurados.
- No existen modelos de dominio ni esquemas de validación específicos.
- La ruta raíz produce una respuesta HTML estática.
- No hay relaciones, transiciones de estado ni reglas de retención.
- No se utilizará una base de datos ni almacenamiento temporal.

Pydantic permanece como componente del stack FastAPI, pero no se planifican modelos Pydantic hasta que exista información real que validar.

