# Ruta Amauta

**Buscador y comparador de becas, maestrías, doctorados y diplomados** en Perú,
Latinoamérica y el resto del mundo.

- Producción: <https://ruta.amauta.online>
- Espejo: <https://oprbguitar.github.io/becas/>

Sitio 100 % estático (HTML + CSS + JavaScript sin dependencias) publicado en
GitHub Pages. No hay servidor, base de datos ni build: los datos viven en
`data/*.json` y el navegador los filtra en memoria.

---

## Novedades · noviembre 2026

- **Convocatorias vigentes** (`#/convocatorias`): 11 convocatorias para
  peruanos (PRONABEC Bicentenario extraordinaria, Gates Cambridge, Eiffel,
  Erasmus Mundus, OEA, Fundación Carolina, Türkiye Bursları, Chevening,
  Fulbright) con fechas leídas el 02/11/2026 en la **fuente oficial**,
  cronograma, requisitos, documentos y estado recalculado con la fecha del
  día. Datos en `data/convocatorias.json`.
- **Contraste SUNEDU** (`#/sunedu`):
  1. verificador de universidades peruanas contra las listas oficiales de
     licenciadas (107) y denegadas (41), con número y PDF de la resolución;
  2. evaluador de la ruta de reconocimiento de un grado extranjero (tratado,
     criterio de calidad, título oficial/propio, modalidad), que nunca afirma
     un reconocimiento;
  3. fichas con evidencia y cinco verificaciones separadas (institución,
     programa, ruta SUNEDU, admisión, oferta y costo);
  4. consulta previa a SUNEDU: la plantilla de la guía se completa con los
     datos del programa y se copia o abre en el correo;
  5. la guía de verificación íntegra (`data/guia-sunedu.html`).
- **Cruce oficial en todo el catálogo**: `scraper/sunedu_listas.py` descarga
  las listas de SUNEDU y contrasta las 60 universidades peruanas del
  catálogo. Corrigió dos casos que la semilla tenía «en trámite» y que SUNEDU
  lista como licenciadas (San Juan Bautista y San Luis Gonzaga). La ficha de
  cada programa muestra la resolución; las extranjeras indican si el país
  tiene tratado.
- **Interfaz más sobria**: barra superior de cuatro enlaces (Convocatorias,
  Becas, Posgrados, SUNEDU), titulares grandes, listas antes que tarjetas,
  control segmentado para maestrías/doctorados/diplomados. Se mantienen la
  paleta y el logotipo. Ver `DESIGN.md`.
- **Honestidad del catálogo**: las maestrías, doctorados y diplomados
  generados por área se rotulan como *fichas exploratorias*.

> Apify: el MCP `https://mcp.apify.com` está configurado en `.mcp.json`, pero
> en esta actualización no expuso herramientas (falta autorizarlo o definir
> `APIFY_API_TOKEN`). Ningún dato de esta versión proviene de un Actor; todo se
> leyó directamente en las fuentes oficiales. Cuando se use un Actor, cada
> registro debe guardar su nombre en el campo `actor`.

## Qué hace

| Sección | Qué resuelve |
|---|---|
| **Inicio** | Búsqueda global y accesos por tipo de programa |
| **Becas** | 86 convocatorias con cobertura, requisitos y fecha de cierre |
| **Maestrías / Doctorados / Diplomados** | +4 200 programas filtrables |
| **Comparador** | Hasta 4 programas lado a lado, con recomendación automática |
| **Favoritos** | Guardado local en el navegador (`localStorage`) |
| **Instituciones** | 248 universidades de 65 países con su estado de licenciamiento |

### Filtros disponibles

Palabra clave · país · región · área de estudio · modalidad · institución ·
costo máximo en USD · **licenciamiento SUNEDU** (licenciada / en trámite /
extranjera con reconocimiento) · cobertura y nivel (en becas) · orden por
relevancia, costo, duración, cierre más próximo, nombre o país.

Los filtros son enlazables: `#/maestrias?pais=Perú&sunedu=licenciada`.

---

## De dónde salen los datos

Hay **tres piezas**, y conviene no confundirlas:

### 1. `data/becas.json` — rastreo real

86 convocatorias obtenidas por `scraper/scrape.py`, que visita las páginas
oficiales (PRONABEC, Chevening, DAAD, Fulbright, OEA, MEXT, la Caixa, Clarendon,
Knight-Hennessy…) y extrae requisitos y fechas. Corre solo, cada lunes, en
GitHub Actions. El semillero vive en `scraper/seed.py` y `scraper/becas_extra.py`.

### 2. `data/{maestrias,doctorados,diplomados,instituciones}.json` — catálogo curado

Generados por `scraper/generar_catalogo.py` a partir de las tablas semilla
`scraper/instituciones*.py`: **248 instituciones de 65 países** verificadas a
mano —60 peruanas, 56 del resto de Latinoamérica, 75 europeas, 24 asiáticas,
15 norteamericanas, 10 africanas y 8 de Oceanía— que se expanden con plantillas
de programas por área académica.

> **Importante.** Los costos son **rangos referenciales de mercado**, no precios
> oficiales, y las duraciones y modalidades son valores típicos del nivel. Cada
> programa enlaza a la **página oficial de posgrado de su institución**, que es
> la única fuente de verdad para precio, fecha y requisitos. La interfaz lo
> advierte en cada ficha. Verifica el licenciamiento en el
> [registro de SUNEDU](https://enlinea.sunedu.gob.pe/).

El generador es **determinista**: dos ejecuciones producen exactamente el mismo
JSON, así que el diff en git siempre es limpio y CI puede comprobar que el
catálogo publicado corresponde a la semilla.

### 3. `data/enlaces.json` — verificación de enlaces

Producido por `scraper/validar_enlaces.py`. Comprueba que **cada destino
publicado abra de verdad** y lo repara cuando no:

1. prueba la ruta de posgrado declarada en la semilla (con y sin `www`);
2. si falla, **abre la portada del dominio y lee el HTML**, puntúa los enlaces
   cuyo texto o URL hablen de posgrado, maestría, doctorado, *graduate* o
   *master*, y comprueba los mejores. Así descubrió, por ejemplo,
   `posgrado.pucp.edu.pe`, `admision.uc.cl/postgrado/` o `posgrado.upeu.edu.pe`;
3. si tampoco, se queda con la portada oficial;
4. `scraper/enlaces_manuales.py` permite fijar a mano cualquier enlace: tiene
   prioridad sobre todo lo anterior.

Muchas universidades responden 403 o 418 a clientes automatizados aunque la
página abra bien en un navegador. Esos casos se marcan como *activo, protegido*
y el enlace se conserva. **Nunca se publica un enlace de buscador como “sitio
oficial”**: la búsqueda restringida al dominio existe solo como botón secundario
*Buscar el programa*, disponible siempre.

Estado actual: 222 enlaces comprobados automáticamente, 18 fijados a mano, 8
protegidos, **0 sin resolver**, sobre 248 instituciones.

```bash
python scraper/validar_enlaces.py                    # todo
python scraper/validar_enlaces.py --solo-becas
python scraper/validar_enlaces.py --solo-instituciones
```

### Contraste SUNEDU

```bash
python scraper/sunedu_listas.py              # descarga las listas y cruza el catálogo
python scraper/sunedu_listas.py --local DIR  # usa lic.html y den.html ya descargados
```

Corre cada lunes en GitHub Actions. Si SUNEDU no responde, conserva el último
`data/sunedu.json` marcado como `desactualizado`.

### Actualizar convocatorias

`data/convocatorias.json` se edita a mano tras leer la fuente oficial. Reglas:
`estado` es `abierta` solo si la fuente muestra fechas vigentes; cada registro
lleva `url`, `consultado` y `fuente_tipo` (`oficial`, `oficial + prensa`…). La
interfaz pasa a «Cerrada» cualquier convocatoria cuyo cierre ya venció.

---

## Estructura

```
index.html                  cáscara de la SPA
assets/css/estilos.css      sistema de diseño v3 (tokens en :root, ver DESIGN.md)
assets/js/ruta.js           router, filtros, comparador, favoritos, fichas
data/becas.json                 86 convocatorias rastreadas
data/maestrias.json           2 077 programas
data/doctorados.json          1 313 programas
data/diplomados.json            907 programas
data/instituciones.json         248 instituciones
data/enlaces.json               informe de verificación de enlaces
data/sunedu.json                listas oficiales SUNEDU + cruce con el catálogo
data/convocatorias.json         convocatorias verificadas en fuente oficial
data/programas_verificados.json fichas con cinco verificaciones y fuentes
data/guia-sunedu.html           guía de verificación SUNEDU (texto íntegro)
scraper/sunedu_listas.py        descarga y cruce de las listas de SUNEDU
data/meta*.json                 facetas y fecha de actualización
scraper/instituciones*.py       tabla semilla curada de instituciones
scraper/seed.py                 semillero de becas
scraper/becas_extra.py          ampliación del semillero de becas
scraper/generar_catalogo.py     expansión determinista -> data/*.json
scraper/validar_enlaces.py      comprobación y reparación de enlaces
scraper/enlaces_manuales.py     correcciones de enlaces fijadas a mano
scraper/generar_favicon.py      favicon e iconos PWA desde imagenes/logo.png
scraper/generar_og.py           imagen 1200x630 para compartir
scraper/generar_paginas.py      páginas indexables + sitemap.xml + robots.txt
scraper/scrape.py               rastreo de convocatorias de becas
imagenes/                   marca original y mockups de referencia
```

---

## Descubrimiento y compartido

La aplicación es una SPA con rutas por hash (`#/maestrias`), y **los buscadores
no indexan nada detrás de un `#`**. Por eso `scraper/generar_paginas.py`
construye, con los mismos datos, **413 páginas HTML reales**:

| Ruta | Qué contiene |
|---|---|
| `/explorar/` | Mapa del sitio: países, áreas y todas las becas |
| `/u/<id>/` | 248 páginas, una por universidad, con su tabla de programas |
| `/pais/<slug>/` | 65 páginas, una por país |
| `/area/<slug>/` | 12 páginas, una por área de estudio |
| `/beca/<slug>/` | 86 páginas, una por convocatoria |

Cada una lleva su propio `<title>`, meta description, `canonical`, Open Graph,
Twitter Card y datos estructurados JSON-LD (`CollegeOrUniversity`,
`CollectionPage`, `EducationalOccupationalProgram`), migas de pan y enlaces de
vuelta al buscador con los filtros ya aplicados. Ninguna universidad queda a más
de tres clics de la portada.

Además:

- `sitemap.xml` con las 413 URLs y `robots.txt` que lo referencia.
- Imagen de vista previa 1200×630 (`assets/img/compartir.png`) para WhatsApp,
  LinkedIn y X, generada por `scraper/generar_og.py`.
- La SPA actualiza `<title>`, la meta description y el `canonical` en cada
  vista, así que compartir `#/doctorados` o una ficha concreta tiene sentido.
- Los filtros son enlazables y **un enlace con filtros parte de cero**: muestra
  exactamente lo que anuncia, sin arrastrar los filtros previos del visitante.
- `<noscript>` con enlace a `/explorar/` para quien navegue sin JavaScript.
- JSON-LD `WebSite` + `SearchAction` en la portada, para el cuadro de búsqueda
  de Google.

Las páginas generadas **no se versionan** (están en `.gitignore`): se
construyen en cada despliegue para que nunca queden desfasadas.

```bash
python scraper/generar_paginas.py
```

---

## Trabajar en local

```bash
python -m http.server 8000
```

Abre <http://127.0.0.1:8000>. No hay paso de compilación: edita y recarga.

Para regenerar el catálogo tras tocar la semilla:

```bash
python scraper/generar_catalogo.py
```

### Añadir una institución

Agrega una fila en la lista correspondiente de `scraper/instituciones.py`:

```python
("uni-id", "Nombre completo", "SIGLA", "País", "Ciudad",
 "dominio.edu.pe", "/ruta-posgrado", "licenciada", "Privada", 2, "GES ING DAT")
```

El penúltimo campo es el nivel de costo (1 pública económica … 4 premium
internacional) y el último son los códigos de área. Vuelve a correr el generador
y súbelo.

---

## Publicación

`.github/workflows/pages.yml` valida los JSON, comprueba que el catálogo esté al
día respecto de la semilla, **genera las páginas indexables y el sitemap**, y
publica en GitHub Pages en cada push a `main`.

`.github/workflows/actualizar-becas.yml` rastrea convocatorias, regenera el
catálogo y **revalida todos los enlaces** cada lunes, y solo hace commit si algo
cambió. Los runners de GitHub alcanzan sitios que bloquean otras redes, así que
la verificación semanal suele resolver enlaces que fallan en local.

---

## Aviso

Ruta Amauta es un directorio independiente. No gestiona admisiones, no cobra por
postular y no está afiliado a las instituciones listadas. Los logotipos se
resuelven desde el dominio oficial de cada institución y pertenecen a sus
titulares.

## Apify desde Python

El proyecto incluye el cliente oficial `apify-client` en las dependencias del scraper y una instalación local aislada en `.venv` (Python 3.11+). Claude Code y Codex tienen instrucciones específicas en `CLAUDE.md`, `AGENTS.md` y las skills del proyecto.

En PowerShell, configura el token solo para la sesión actual y ejecuta un Actor:

```powershell
$env:APIFY_API_TOKEN = "<tu-token-de-Apify>"
.\.venv\Scripts\python scraper\apify_run_actor.py apify/hello-world --output resultados.json
```

Para pasar parámetros, guarda un objeto JSON con la entrada que espera ese Actor y añade `--input entrada.json`. El ejecutor guarda el dataset predeterminado como JSON. Obtén el token desde [Integraciones de Apify](https://console.apify.com/settings/integrations); no lo guardes en el repositorio. Ejecutar un Actor puede consumir créditos.

Para reinstalar las dependencias en otro equipo:

```powershell
py -m venv .venv
.\.venv\Scripts\python -m pip install -r scraper\requirements.txt
```
