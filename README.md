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
| **Becas** | 86 convocatorias con cobertura, requisitos y fecha de cierre |
| **Maestrías / Doctorados / Diplomados** | +2 900 programas filtrables |
| **Comparador** | Hasta 4 programas lado a lado, con recomendación automática |
| **Favoritos** | Guardado local en el navegador (`localStorage`) |
| **Instituciones** | 152 universidades con su estado de licenciamiento |

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
`scraper/instituciones.py` y `scraper/instituciones_extra.py`: 152 instituciones
verificadas a mano —60 peruanas, 22 españolas y el resto de Latinoamérica,
Europa, Norteamérica, Asia y Oceanía— que se expanden con plantillas de
programas por área académica.

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

Estado actual: 136 enlaces comprobados automáticamente, 15 fijados a mano, 1
protegido, 0 sin resolver, sobre 152 instituciones.

```bash
python scraper/validar_enlaces.py                    # todo
python scraper/validar_enlaces.py --solo-becas
python scraper/validar_enlaces.py --solo-instituciones
```

---

## Estructura

```
index.html                  cáscara de la SPA
assets/css/estilos.css      sistema de diseño (terracota / oliva / arena)
assets/js/ruta.js           router, filtros, comparador, favoritos, fichas
data/becas.json                 86 convocatorias rastreadas
data/maestrias.json           1 322 programas
data/doctorados.json            832 programas
data/diplomados.json            753 programas
data/instituciones.json         152 instituciones
data/enlaces.json               informe de verificación de enlaces
data/meta*.json                 facetas y fecha de actualización
scraper/instituciones*.py       tabla semilla curada de instituciones
scraper/seed.py                 semillero de becas
scraper/becas_extra.py          ampliación del semillero de becas
scraper/generar_catalogo.py     expansión determinista -> data/*.json
scraper/validar_enlaces.py      comprobación y reparación de enlaces
scraper/enlaces_manuales.py     correcciones de enlaces fijadas a mano
scraper/generar_favicon.py      favicon e iconos PWA desde imagenes/logo.png
scraper/scrape.py               rastreo de convocatorias de becas
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
