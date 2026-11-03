# Instrucciones del proyecto

Ruta Amauta es un sitio estático. Sus fuentes de datos y herramientas de scraping están en `scraper/`; instala las dependencias Python desde `scraper/requirements.txt` dentro del entorno virtual `.venv`.

## Apify

- Claude Code carga el MCP remoto de Apify desde `.mcp.json`; Codex lo carga desde su configuración de MCP de escritorio. Sigue la skill del proyecto `apify-client` (`.agents/skills/apify-client/SKILL.md` o `.claude/skills/apify-client/SKILL.md`) para escoger Actors y realizar las búsquedas propias de Ruta Amauta.
- Lee `APIFY_API_TOKEN` desde una variable de entorno; nunca lo escribas en código, documentación, argumentos de comandos ni archivos versionados.
- Cuando la tarea solicite investigar becas, posgrados o instituciones, puedes buscar Actors y ejecutar los adecuados para esa búsqueda. Las ejecuciones pueden consumir créditos: limita el alcance a la petición concreta e informa antes de una ejecución potencialmente costosa.
- No uses Apify para sustituir el rastreador actual de becas sin que la tarea lo pida.
- Usa fuentes oficiales como evidencia principal y conserva URL, fecha de consulta y Actor usado; los resultados de scraping son candidatos que deben verificarse antes de incorporarse a `data/*.json`.

## Comandos

```powershell
py -m venv .venv
.\.venv\Scripts\python -m pip install -r scraper\requirements.txt
```

Los scripts de catálogo existentes siguen ejecutándose con `python scraper\...` desde la raíz; activa `.venv` o invoca `.venv\Scripts\python` para usar las dependencias instaladas aquí.
