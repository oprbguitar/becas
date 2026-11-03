---
name: apify-client
description: Usar el cliente oficial de Apify para Python en este proyecto Ruta Amauta.
---

# Apify en Ruta Amauta

Esta skill aplica a las búsquedas web de este proyecto: becas y convocatorias, programas de posgrado, e instituciones educativas. Usa el plugin/MCP de Apify en Claude Code para buscar Actors, inspeccionar sus esquemas, ejecutarlos y recuperar resultados. Para código Python usa también la dependencia `apify-client` en `scraper/requirements.txt` y el entorno `.venv` (Python 3.11+).

## Tipos de búsqueda del proyecto

1. **Becas y convocatorias:** localizar convocatorias abiertas o próximas, fechas, elegibilidad, cobertura, requisitos, idiomas, organización y enlaces oficiales. Prioriza PRONABEC y los sitios de los financiadores (por ejemplo DAAD, Chevening, Fulbright, OEA, MEXT).
2. **Posgrados:** buscar maestrías, doctorados y diplomados por país, institución y área; extraer nombre, modalidad, duración, costos publicados, idioma, admisión, financiación y URL oficial del programa.
3. **Instituciones:** descubrir y verificar universidades, escuelas de posgrado, dominio oficial, ubicación y página de posgrado. Para instituciones peruanas, trata el estado SUNEDU como un dato que debe comprobarse contra SUNEDU; no lo infieras de resultados de búsqueda.
4. **Verificación de enlaces:** comprobar páginas oficiales existentes y registrar si son accesibles, redirigen, están protegidas o ya no existen. No sustituyas un enlace oficial por una página de resultados de Google.

## Flujo de búsqueda

- Primero revisa `data/becas.json`, `data/maestrias.json`, `data/doctorados.json`, `data/diplomados.json` y `data/instituciones.json` para delimitar qué falta y evitar duplicados.
- Usa `search-actors` para encontrar candidatos de scraping y `fetch-actor-details` para revisar mantenimiento, permisos, costes, entrada y esquema de salida. Prefiere Actors activos, con salidas estructuradas y fuentes que puedan restringirse a dominios oficiales.
- Formula una búsqueda concreta por país, programa/convocatoria y rango de fechas. No hagas crawls amplios de sitios sin relación con la petición.
- Ejecuta el Actor solo cuando la tarea pida la búsqueda; informa si la ejecución puede generar cargos relevantes. No ejecutes ejecuciones de prueba que no aporten resultados a la tarea.
- Conserva por resultado: URL de origen, fecha de consulta, nombre/ID del Actor y los campos usados para decidir que coincide. Deduplica por URL oficial e institución/programa.
- Contrasta fechas, costes, elegibilidad, acreditación y estado de la convocatoria en la página oficial. Marca como no verificado lo que el scraping no permita confirmar; no completes campos faltantes por inferencia.
- Si se pide preparar una actualización, adapta los datos a las claves ya usadas en los JSON, presenta primero diferencias y fuentes, y modifica `data/*.json` solo cuando la tarea pida expresamente incorporarlas.

Campos de referencia: `data/becas.json` contiene, entre otros, `nombre`, `organizacion`, `pais`, `niveles`, `areas`, `cobertura`, `requisitos`, `fecha_apertura`, `fecha_cierre`, `url` y `url_requisitos`. Los catálogos de posgrado contienen `nombre`, `institucion`, `pais`, `area`, `modalidad`, `duracion_meses`, `costo_min_usd`, `costo_max_usd` y `url`.

## Credenciales

- Obtén el token solo de la variable de entorno `APIFY_API_TOKEN`.
- No incluyas tokens en el código, prompts que se guarden, archivos `.env` versionados, argumentos de shell, salidas de consola ni commits.
- Si falta el token, explica cómo definirlo localmente y detente antes de llamar a la API.

PowerShell:

```powershell
$env:APIFY_API_TOKEN = "<token-local>"
```

## Ejecutar un Actor desde Python

Hay un ejecutor local reutilizable para llamadas directas desde scripts:

```powershell
.\.venv\Scripts\python scraper\apify_run_actor.py <actor-id> --input <entrada.json> --output <resultados.json>
```

La entrada debe ser un objeto JSON compatible con el Actor. Se puede omitir `--input` cuando el Actor no requiere entrada y `--output` para imprimir el dataset en stdout. Revisa el esquema y los límites del Actor antes de preparar su entrada.

## SDK

Usa `ApifyClient` para código síncrono o `ApifyClientAsync` para código asíncrono. En la versión 3, la respuesta de `call()` expone atributos tipados como `run.default_dataset_id`, y `list_items()` devuelve una página cuyo contenido está en `.items`.

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_API_TOKEN"])
run = client.actor("apify/hello-world").call(run_input={"key": "value"})
if run is not None:
    items = client.dataset(run.default_dataset_id).list_items().items
```

Documentación oficial: https://docs.apify.com/api/client/python/docs
