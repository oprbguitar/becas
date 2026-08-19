<p align="center">
  <img src="assets/img/logo.svg" width="88" alt="BecaRadar">
</p>

<h1 align="center">BecaRadar</h1>

<p align="center">
  <strong>Buscador avanzado de becas de Perú, Latinoamérica, Europa, Asia, China y el mundo.</strong><br>
  Filtra, compara y guarda convocatorias en tu navegador. Sin cuentas, sin servidor, sin costo.
</p>

---

## ¿De qué se trata?

**BecaRadar** es un portal web que reúne convocatorias de becas de todo el mundo en un
solo lugar y te deja filtrarlas como quieras: por especialidad, nivel de estudios, país,
región, fechas de postulación, tu edad, la duración del programa, el costo de postular,
la distancia hasta el destino y lo que la beca cubre (matrícula, hospedaje, pasajes,
manutención, seguro, curso de idioma).

Cada beca enlaza **directo a la página oficial de postulación** y a sus **bases**, para que
nadie postule con información de segunda mano.

### Cómo está pensado

| Zona | Qué hace |
|---|---|
| **Panel izquierdo** | *Mis becas*: lo que guardes se queda en **tu navegador** (`localStorage`). Puedes exportarlo e importarlo como archivo `.json`. |
| **Centro** | Listado de todas las becas que pasan tus filtros, con estado de la convocatoria, cuenta regresiva y requisitos desplegables. |
| **Panel derecho** | Todos los filtros, agrupados y con contador de cuántos tienes activos. |

En móvil los dos paneles laterales se convierten en cajones deslizantes.

## Lo que puedes filtrar

- **Región del mundo** — Perú · Latinoamérica · Norteamérica · Europa · Asia · China · Oceanía · África · Global
- **País de destino** y **ciudad** (con coordenadas reales)
- **Especialidad / área** — ingeniería, salud, ciencias, tecnología, negocios, derecho, arte, educación, agricultura, medio ambiente…
- **Nivel** — técnico, pregrado, maestría, doctorado, posdoctorado, curso corto, intercambio
- **Cobertura económica** — completa, parcial, solo matrícula, solo estipendio
- **Qué incluye** — matrícula · manutención mensual · hospedaje · pasajes aéreos · seguro médico · curso de idioma · equipos
- **Fechas** — rango de cierre, y estado: abiertas ahora, cierran en 15 días, próximas a abrir, cerradas
- **Tu edad** — muestra solo las becas cuyo rango de edad te acepta
- **Tiempo** — duración máxima del programa en meses
- **Costo** — cuánto cuesta postular (casi todas son gratuitas)
- **Distancia** — a cuántos kilómetros estás del destino, usando tu ubicación real (GPS del navegador) o una ciudad de referencia
- **Idioma de estudio** y **modalidad** (presencial, virtual, mixta)

Además: buscador de texto libre, ordenamiento (cierra pronto, recién abiertas, A-Z,
mayor cobertura, más cerca de mí, mayor duración), chips de filtros activos y
**los filtros quedan en la URL**, así que puedes compartir una búsqueda tal cual la armaste.

## Actualización automática de los datos

El catálogo **no se mantiene a mano**. Un rastreador escrito en Python
(`scraper/scrape.py`) corre **cada lunes en GitHub Actions** — en los servidores de
GitHub, no en tu computadora — y para cada beca:

1. Visita la página oficial de bases.
2. Comprueba que el enlace siga vivo (para no mandarte a un 404).
3. Extrae los **requisitos** publicados en esa página.
4. Detecta **fechas de cierre** visibles y las adopta si la fecha que teníamos ya venció.
5. Vuelve a escribir `data/becas.json` y `data/meta.json`, y hace commit del cambio.

Es un script determinista y educado: pausa entre peticiones al mismo dominio, se
identifica con su propio *User-Agent* y **jamás borra datos**: si una página no responde
o cambió de forma, la ficha original del semillero se conserva intacta.

```bash
python scraper/scrape.py              # rastrea todo el catálogo
python scraper/scrape.py --limite 5   # prueba rápida con 5 becas
python scraper/scrape.py --sin-red    # solo regenera desde el semillero, sin internet
```

## Estructura del repositorio

```
├── index.html                 Portal completo (una sola página)
├── manifest.webmanifest       Metadatos para instalarlo como app
├── assets/
│   ├── css/styles.css         Temas claro/oscuro, animaciones, responsive
│   ├── img/                   Logo y favicon (SVG)
│   └── js/
│       ├── app.js             Orquestador: carga datos y conecta todo
│       ├── filtros.js         Motor de filtrado, orden y sincronía con la URL
│       ├── interfaz.js        Construcción del DOM (panel, tarjetas, guardadas)
│       ├── almacen.js         localStorage: becas guardadas, tema y filtros
│       └── utils.js           Fechas, distancias, animaciones, utilidades
├── data/
│   ├── becas.json             El catálogo
│   └── meta.json              Fecha de actualización y estadísticas
├── scraper/
│   ├── seed.py                Semillero: catálogo base curado a mano
│   ├── scrape.py              Rastreador que enriquece el semillero
│   └── requirements.txt
└── .github/workflows/
    ├── actualizar-becas.yml   Rastreo semanal automático
    └── pages.yml              Despliegue a GitHub Pages
```

## Cómo verlo

**En línea:** una vez activado GitHub Pages, el portal vive en
`https://oprbguitar.github.io/becas/`.

Para activarlo: **Settings → Pages → Source: GitHub Actions**. El workflow `pages.yml`
publica en cada push a `main`.

**En tu máquina:** el portal es HTML, CSS y JavaScript estándar — sin build, sin
dependencias, sin framework. Solo necesita servirse por HTTP para que `fetch` pueda
leer el JSON:

```bash
python -m http.server 8000
# abre http://localhost:8000
```

## Detalles técnicos

- **Cero dependencias en el navegador.** Módulos ES nativos, CSS con variables propias.
- **Accesible.** Navegación por teclado (`/` enfoca el buscador, `Esc` cierra paneles),
  roles ARIA, foco visible y respeto por `prefers-reduced-motion`.
- **Rápido.** El listado se pinta por lotes de 24 con carga progresiva, la búsqueda usa
  un índice normalizado precalculado y los eventos de scroll van sincronizados al frame.
- **Privado.** No hay analítica, cookies ni peticiones a terceros. Lo que guardas es tuyo
  y vive solo en tu dispositivo.
- **Temas.** Claro y oscuro, con botón manual que recuerda tu elección y respeta la
  preferencia del sistema la primera vez.

## Aviso importante

Las fechas del catálogo son **referenciales**: las convocatorias son anuales y sus
plazos cambian cada año. **Verifica siempre la convocatoria oficial** en el enlace de
cada beca antes de postular.

## Añadir o corregir una beca

Edita `scraper/seed.py` (la función `b(...)` documenta cada campo), ejecuta
`python scraper/scrape.py --sin-red` para regenerar el JSON y abre un pull request.

Para comprobar que el extractor sigue reconociendo requisitos y fechas:

```bash
python scraper/test_extraccion.py
```
