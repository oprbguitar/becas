# Ruta Amauta

**Buscador y comparador de becas, maestrías, doctorados y diplomados** en Perú,
Latinoamérica y el resto del mundo.

- Producción: <https://ruta.amauta.online>
- Espejo: <https://oprbguitar.github.io/becas/>

Sitio 100 % estático (HTML + CSS + JavaScript sin dependencias) publicado en
GitHub Pages. No hay servidor, base de datos ni build: los datos viven en
`data/*.json` y el navegador los filtra en memoria.

---

## Qué hace

| Sección | Qué resuelve |
|---|---|
| **Inicio** | Búsqueda global y accesos por tipo de programa |
| **Becas** | 59 convocatorias con cobertura, requisitos y fecha de cierre |
| **Maestrías / Doctorados / Diplomados** | +1 000 programas filtrables |
| **Comparador** | Hasta 4 programas lado a lado, con recomendación automática |
| **Favoritos** | Guardado local en el navegador (`localStorage`) |
| **Instituciones** | 96 universidades con su estado de licenciamiento |

### Filtros disponibles

Palabra clave · país · región · área de estudio · modalidad · institución ·
costo máximo en USD · **licenciamiento SUNEDU** (licenciada / en trámite /
extranjera con reconocimiento) · cobertura y nivel (en becas) · orden por
relevancia, costo, duración, cierre más próximo, nombre o país.

Los filtros son enlazables: `#/maestrias?pais=Perú&sunedu=licenciada`.

---

## De dónde salen los datos

Hay **dos fuentes distintas**, y conviene no confundirlas:

### 1. `data/becas.json` — rastreo real

Convocatorias de becas obtenidas por `scraper/scrape.py`, que visita las páginas
oficiales (PRONABEC, Chevening, DAAD, Fulbright, OEA, MEXT…) y extrae requisitos
y fechas. Corre solo, cada lunes, en GitHub Actions.

### 2. `data/{maestrias,doctorados,diplomados,instituciones}.json` — catálogo curado

Generados por `scraper/generar_catalogo.py` a partir de la tabla semilla
`scraper/instituciones.py`: 96 instituciones verificadas a mano (nombre, país,
dominio oficial, URL de su escuela de posgrado, estado de licenciamiento) que se
expanden con plantillas de programas por área académica.

> **Importante.** Los costos son **rangos referenciales de mercado**, no precios
> oficiales, y las duraciones y modalidades son valores típicos del nivel. Cada
> programa enlaza a la **página oficial de posgrado de su institución**, que es
> la única fuente de verdad para precio, fecha y requisitos. La interfaz lo
> advierte en cada ficha. Verifica el licenciamiento en el
> [registro de SUNEDU](https://enlinea.sunedu.gob.pe/).

El generador es **determinista**: dos ejecuciones producen exactamente el mismo
JSON, así que el diff en git siempre es limpio y CI puede comprobar que el
catálogo publicado corresponde a la semilla.

---

## Estructura

```
index.html                  cáscara de la SPA
assets/css/estilos.css      sistema de diseño (terracota / oliva / arena)
assets/js/ruta.js           router, filtros, comparador, favoritos, fichas
data/becas.json             convocatorias rastreadas
data/maestrias.json         473 programas
data/doctorados.json        288 programas
data/diplomados.json        271 programas
data/instituciones.json      96 instituciones
data/meta*.json             facetas y fecha de actualización
scraper/instituciones.py    tabla semilla curada
scraper/generar_catalogo.py expansión determinista -> data/*.json
scraper/scrape.py           rastreo de convocatorias de becas
imagenes/                   marca original y mockups de referencia
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
día respecto de la semilla y publica en GitHub Pages en cada push a `main`.

`.github/workflows/actualizar-becas.yml` rastrea convocatorias y regenera el
catálogo cada lunes, y solo hace commit si algo cambió.

---

## Aviso

Ruta Amauta es un directorio independiente. No gestiona admisiones, no cobra por
postular y no está afiliado a las instituciones listadas. Los logotipos se
resuelven desde el dominio oficial de cada institución y pertenecen a sus
titulares.
