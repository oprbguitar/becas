#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera las paginas estaticas indexables y el sitemap.

La aplicacion es una SPA con rutas por hash (#/maestrias), y los buscadores no
indexan nada que viva detras de un #. Este script crea, a partir de los mismos
datos, paginas HTML reales con contenido propio que si se pueden rastrear,
compartir y posicionar:

    /explorar/           mapa del sitio para personas y rastreadores
    /u/<id>/             una por institucion  (posgrados de esa universidad)
    /pais/<slug>/        una por pais         (universidades y programas)
    /area/<slug>/        una por area         (programas por area de estudio)
    /beca/<slug>/        una por convocatoria (requisitos, cobertura, fechas)
    /sitemap.xml         indice completo
    /robots.txt          permiso de rastreo + referencia al sitemap

Cada pagina lleva su propio <title>, meta description, canonical, Open Graph,
Twitter Card y datos estructurados JSON-LD, y enlaza de vuelta al buscador con
los filtros ya aplicados.

Uso:
    python scraper/generar_paginas.py
"""

from __future__ import annotations

import html
import json
import os
import re
import shutil
import unicodedata
from datetime import datetime, timezone

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, "data")
SITIO = "https://ruta.amauta.online"

TIPOS = {"maestria": "Maestría", "doctorado": "Doctorado", "diplomado": "Diplomado"}
PLURAL = {"maestria": "maestrías", "doctorado": "doctorados", "diplomado": "diplomados"}

SELLO = {
    "licenciada": ("Licenciada por SUNEDU", "ok"),
    "proceso": ("Licenciamiento en trámite", "proceso"),
    "extranjera": ("Extranjera · reconocimiento SUNEDU", "ext"),
}

SIMBOLO = {"PEN": "S/", "USD": "US$", "EUR": "€", "GBP": "£", "CLP": "CLP$",
           "COP": "COP$", "MXN": "MX$", "BRL": "R$", "CAD": "CA$", "AUD": "AU$",
           "CHF": "CHF", "SGD": "SG$", "SEK": "SEK", "NOK": "NOK", "DKK": "DKK",
           "PLN": "PLN", "CZK": "CZK", "INR": "₹", "MYR": "RM", "THB": "฿",
           "PHP": "₱", "HKD": "HK$", "TWD": "NT$", "ILS": "₪", "AED": "AED",
           "QAR": "QAR", "NZD": "NZ$", "ZAR": "R", "MAD": "MAD"}


# ------------------------------------------------------------- utilidades

def baba(texto: str) -> str:
    """Slug estable y legible."""
    t = unicodedata.normalize("NFD", str(texto or "").lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-") or "sin-nombre"


def e(texto) -> str:
    return html.escape(str(texto if texto is not None else ""), quote=True)


def miles(n) -> str:
    try:
        return f"{int(n):,}".replace(",", " ")
    except (TypeError, ValueError):
        return "—"


def dinero(p) -> str:
    if not p.get("costo_min"):
        return "Consultar"
    s = SIMBOLO.get(p.get("moneda"), (p.get("moneda") or "") + " ")
    return f"{s} {miles(p['costo_min'])} – {miles(p['costo_max'])}"


def duracion(p) -> str:
    if p.get("horas"):
        return f"{p['horas']} horas"
    m = p.get("duracion_meses")
    if not m:
        return "—"
    if m >= 12 and m % 12 == 0:
        return f"{m // 12} {'año' if m == 12 else 'años'}"
    return f"{m} meses"


def fecha_es(iso):
    if not iso:
        return "—"
    meses = ["ene", "feb", "mar", "abr", "may", "jun",
             "jul", "ago", "set", "oct", "nov", "dic"]
    try:
        a, m, d = iso.split("-")
        return f"{int(d):02d} {meses[int(m) - 1]}. {a}"
    except (ValueError, IndexError):
        return iso


def cargar(nombre, respaldo):
    ruta = os.path.join(DATOS, nombre)
    if not os.path.exists(ruta):
        return respaldo
    with open(ruta, encoding="utf-8") as fh:
        return json.load(fh)


# ------------------------------------------------------------- plantilla

CABECERA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<link rel="canonical" href="{canonica}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#C4552E">
<meta property="og:site_name" content="Ruta Amauta">
<meta property="og:locale" content="es_PE">
<meta property="og:type" content="{og_tipo}">
<meta property="og:title" content="{og_titulo}">
<meta property="og:description" content="{descripcion}">
<meta property="og:url" content="{canonica}">
<meta property="og:image" content="{sitio}/assets/img/compartir.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Ruta Amauta — tu ruta al conocimiento">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_titulo}">
<meta name="twitter:description" content="{descripcion}">
<meta name="twitter:image" content="{sitio}/assets/img/compartir.png">
<link rel="icon" href="{raiz}assets/img/favicon.ico" sizes="16x16 32x32 48x48">
<link rel="icon" href="{raiz}assets/img/icono-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="{raiz}assets/img/icono-180.png">
<link rel="manifest" href="{raiz}manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{raiz}assets/css/estilos.css">
<script type="application/ld+json">{jsonld}</script>
</head>
<body>
<header class="cabecera">
  <div class="contenedor cabecera-fila">
    <a class="marca" href="{raiz}" aria-label="Ruta Amauta — inicio">
      <img src="{raiz}assets/img/marca.png" alt="Ruta Amauta" width="220" height="46">
    </a>
    <nav class="nav">
      <a href="{raiz}#/becas">Becas</a>
      <a href="{raiz}#/maestrias">Maestrías</a>
      <a href="{raiz}#/doctorados">Doctorados</a>
      <a href="{raiz}#/diplomados">Diplomados</a>
      <a href="{raiz}#/comparador">Comparador</a>
      <a href="{raiz}explorar/">Explorar</a>
    </nav>
  </div>
</header>
<main>
<div class="contenedor" style="padding-top:26px">
  <nav class="miga" aria-label="Ruta de navegación">{miga}</nav>
</div>
"""

PIE = """</main>
<footer class="pie">
  <div class="contenedor">
    <div class="pie-rejilla">
      <div>
        <div class="pie-marca"><img src="{raiz}assets/img/marca.png" alt="Ruta Amauta" width="200" height="42"></div>
        <p style="margin-top:14px">Buscador y comparador independiente de becas, maestrías,
        doctorados y diplomados en Perú, Latinoamérica y el mundo.</p>
      </div>
      <div><h4>Explorar</h4><ul>
        <li><a href="{raiz}#/becas">Becas</a></li>
        <li><a href="{raiz}#/maestrias">Maestrías</a></li>
        <li><a href="{raiz}#/doctorados">Doctorados</a></li>
        <li><a href="{raiz}#/diplomados">Diplomados</a></li>
      </ul></div>
      <div><h4>Herramientas</h4><ul>
        <li><a href="{raiz}#/comparador">Comparador</a></li>
        <li><a href="{raiz}#/instituciones">Instituciones</a></li>
        <li><a href="{raiz}explorar/">Mapa del sitio</a></li>
      </ul></div>
      <div><h4>Verifica</h4><ul>
        <li><a href="https://enlinea.sunedu.gob.pe/" rel="noopener nofollow">Registro SUNEDU</a></li>
        <li><a href="https://www.gob.pe/pronabec" rel="noopener nofollow">PRONABEC</a></li>
        <li><a href="https://github.com/oprbguitar/becas" rel="noopener">Código abierto</a></li>
      </ul></div>
    </div>
    <div class="pie-abajo">
      <span>© {anio} Ruta Amauta · ruta.amauta.online</span>
      <span>Información referencial: verifica siempre en la fuente oficial.</span>
    </div>
  </div>
</footer>
</body>
</html>
"""


def pagina(ruta_rel, titulo, descripcion, miga, cuerpo, jsonld, og_tipo="website"):
    """Escribe una pagina completa en <ruta_rel>/index.html."""
    profundidad = len([p for p in ruta_rel.split("/") if p])
    raiz = "../" * profundidad if profundidad else ""
    canonica = f"{SITIO}/{ruta_rel}/" if ruta_rel else f"{SITIO}/"

    migas = " ".join(
        f'<a href="{e(u)}">{e(t)}</a><span>›</span>' if u else f"<span>{e(t)}</span>"
        for t, u in miga)

    salida = os.path.join(RAIZ, *ruta_rel.split("/")) if ruta_rel else RAIZ
    os.makedirs(salida, exist_ok=True)
    with open(os.path.join(salida, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(CABECERA.format(
            titulo=e(titulo), descripcion=e(descripcion), canonica=e(canonica),
            og_titulo=e(titulo.split(" | ")[0]), og_tipo=og_tipo, sitio=SITIO,
            raiz=raiz, miga=migas,
            jsonld=json.dumps(jsonld, ensure_ascii=False)))
        fh.write(cuerpo)
        fh.write(PIE.format(raiz=raiz, anio=datetime.now().year))
    return canonica


# ------------------------------------------------------------- fragmentos

def sello_html(estado):
    if estado not in SELLO:
        return ""
    texto, clase = SELLO[estado]
    return f'<span class="sello {clase}">{e(texto)}</span>'


def tabla_programas(programas, raiz="../../"):
    filas = []
    for p in sorted(programas, key=lambda x: x["nombre"]):
        filas.append(f"""<tr>
      <td><strong>{e(p['nombre'])}</strong></td>
      <td>{e(p['area'])}</td>
      <td>{e(duracion(p))}</td>
      <td>{e(p['modalidad'])}</td>
      <td class="precio-celda">{e(dinero(p))}</td>
    </tr>""")
    return f"""<div class="envoltura-tabla">
  <table class="tabla-datos">
    <thead><tr><th>Programa</th><th>Área</th><th>Duración</th><th>Modalidad</th><th>Costo referencial</th></tr></thead>
    <tbody>{''.join(filas)}</tbody>
  </table>
</div>"""


def rejilla_enlaces(items, clase="rejilla"):
    tarjetas = []
    for titulo, sub, url, extra in items:
        tarjetas.append(f"""<a class="tarjeta enlace-tarjeta" href="{e(url)}">
      <h3>{e(titulo)}</h3>
      <p class="institucion">{e(sub)}</p>
      {extra}
    </a>""")
    return f'<div class="{clase}">{"".join(tarjetas)}</div>'


# ------------------------------------------------------------- generacion

def main():
    becas = cargar("becas.json", [])
    instituciones = cargar("instituciones.json", [])
    enlaces = cargar("enlaces.json", {}) or {}
    programas = (cargar("maestrias.json", []) + cargar("doctorados.json", [])
                 + cargar("diplomados.json", []))

    enl_inst = enlaces.get("instituciones", {})
    enl_beca = enlaces.get("becas", {})
    for u in instituciones:
        info = enl_inst.get(u["id"])
        if info and info.get("url"):
            u["url_posgrado"] = info["url"]

    por_inst = {}
    for p in programas:
        por_inst.setdefault(p["institucion_id"], []).append(p)

    urls = []          # (loc, prioridad, cambio)
    hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # limpiar salidas previas para que no queden paginas huerfanas
    for carpeta in ("u", "pais", "area", "beca", "explorar"):
        ruta = os.path.join(RAIZ, carpeta)
        if os.path.isdir(ruta):
            shutil.rmtree(ruta)

    # ---------------------------------------------------- instituciones
    for u in instituciones:
        progs = por_inst.get(u["id"], [])
        if not progs:
            continue
        cuenta = {t: sum(1 for p in progs if p["tipo"] == t) for t in TIPOS}
        resumen = ", ".join(f"{n} {PLURAL[t]}" for t, n in cuenta.items() if n)
        slug_pais = baba(u["pais"])

        titulo = f"Posgrados en {u['nombre']} ({u['sigla']}) — {u['pais']} | Ruta Amauta"
        desc = (f"{resumen} en {u['nombre']}, {u['ciudad']} ({u['pais']}). "
                f"Costos referenciales, duración, modalidad y enlace oficial a "
                f"la escuela de posgrado.")

        bloques = []
        for t in ("maestria", "doctorado", "diplomado"):
            grupo = [p for p in progs if p["tipo"] == t]
            if not grupo:
                continue
            bloques.append(f"""<section class="seccion">
      <div class="seccion-cabecera"><h2>{len(grupo)} {PLURAL[t]}</h2>
        <a class="btn-texto" href="../../#/{PLURAL[t]}?institucion={e(u['nombre'])}">Filtrar en el buscador ›</a></div>
      {tabla_programas(grupo)}
    </section>""")

        cuerpo = f"""<div class="contenedor">
  <section class="ficha-cabecera">
    <div>
      <h1 class="titulo-pagina">{e(u['nombre'])}</h1>
      <p class="bajada">{e(u['ciudad'])}, {e(u['pais'])} · Universidad {e(u['tipo'].lower())}</p>
      <p style="margin:10px 0 0">{sello_html(u.get('sunedu'))}</p>
    </div>
    <div class="ficha-acciones">
      <a class="btn btn-primario" href="{e(u.get('url_posgrado') or u.get('web'))}"
         target="_blank" rel="noopener nofollow">Escuela de posgrado ↗</a>
      <a class="btn btn-linea" href="{e(u.get('web'))}" target="_blank" rel="noopener nofollow">Sitio institucional ↗</a>
    </div>
  </section>

  <div class="metricas">
    <div class="metrica"><div><b>{len(progs)}</b><span>Programas listados</span></div></div>
    <div class="metrica oliva"><div><b>{cuenta['maestria']}</b><span>Maestrías</span></div></div>
    <div class="metrica"><div><b>{cuenta['doctorado']}</b><span>Doctorados</span></div></div>
    <div class="metrica oliva"><div><b>{cuenta['diplomado']}</b><span>Diplomados</span></div></div>
  </div>

  {''.join(bloques)}

  <p class="nota-legal">Los costos son rangos referenciales de mercado, no precios
  oficiales. Confirma precio, fechas y requisitos en la web oficial de
  {e(u['nombre'])} antes de postular.</p>

  <p><a class="btn btn-oliva" href="../../pais/{slug_pais}/">Ver todo {e(u['pais'])}</a></p>
</div>"""

        jsonld = {
            "@context": "https://schema.org",
            "@type": "CollegeOrUniversity",
            "name": u["nombre"], "alternateName": u["sigla"],
            "url": u.get("web"),
            "address": {"@type": "PostalAddress",
                        "addressLocality": u["ciudad"], "addressCountry": u["pais"]},
            "subjectOf": {"@type": "ItemList", "numberOfItems": len(progs),
                          "itemListElement": [
                              {"@type": "ListItem", "position": i + 1,
                               "item": {"@type": "Course", "name": p["nombre"],
                                        "provider": {"@type": "Organization", "name": u["nombre"]}}}
                              for i, p in enumerate(sorted(progs, key=lambda x: x["nombre"])[:25])]},
        }
        loc = pagina(f"u/{u['id']}", titulo, desc,
                     [("Inicio", "../../"), ("Explorar", "../../explorar/"),
                      (u["pais"], f"../../pais/{slug_pais}/"), (u["sigla"], None)],
                     cuerpo, jsonld, og_tipo="profile")
        urls.append((loc, "0.7", "monthly"))

    # ------------------------------------------------------------ paises
    paises = sorted({u["pais"] for u in instituciones})
    for nombre_pais in paises:
        us = [u for u in instituciones if u["pais"] == nombre_pais]
        ids = {u["id"] for u in us}
        progs = [p for p in programas if p["institucion_id"] in ids]
        if not progs:
            continue
        cuenta = {t: sum(1 for p in progs if p["tipo"] == t) for t in TIPOS}
        becas_pais = [b for b in becas if b.get("pais") == nombre_pais]
        region = us[0].get("region", "")

        # El titular solo nombra los tipos que ese pais realmente tiene.
        presentes = [PLURAL[t] for t in ("maestria", "doctorado", "diplomado") if cuenta[t]]
        listado = (", ".join(presentes[:-1]) + " y " + presentes[-1]
                   if len(presentes) > 1 else presentes[0])
        detalle = ", ".join(f"{miles(cuenta[t])} {PLURAL[t]}"
                            for t in ("maestria", "doctorado", "diplomado") if cuenta[t])
        titulo = (f"{listado.capitalize()} en {nombre_pais} "
                  f"— {miles(len(progs))} programas | Ruta Amauta")
        desc = (f"{detalle} en {len(us)} universidades de {nombre_pais}. "
                f"Compara costos, duración y modalidad, y accede al sitio oficial "
                f"de cada programa.")

        tarjetas = []
        for u in sorted(us, key=lambda x: x["nombre"]):
            n = len(por_inst.get(u["id"], []))
            if not n:
                continue
            tarjetas.append((u["nombre"], f"{u['ciudad']} · {n} programas",
                             f"../../u/{u['id']}/", sello_html(u.get("sunedu"))))

        lista_becas = ""
        if becas_pais:
            enlaces_b = "".join(
                f'<li><a href="../../beca/{baba(b["id"])}/">{e(b["nombre"])}</a> '
                f'<span class="tenue">· {e(b.get("cobertura", ""))}</span></li>'
                for b in becas_pais)
            lista_becas = f"""<section class="seccion">
      <div class="seccion-cabecera"><h2>Becas para estudiar en {e(nombre_pais)}</h2></div>
      <ul class="lista-enlaces">{enlaces_b}</ul>
    </section>"""

        areas = {}
        for p in progs:
            areas[p["area"]] = areas.get(p["area"], 0) + 1
        chips = "".join(
            f'<a class="pastilla" href="../../area/{baba(a)}/">{e(a)} <b>{n}</b></a>'
            for a, n in sorted(areas.items(), key=lambda kv: -kv[1]))

        celdas = [(miles(cuenta[t]), TIPOS[t] + "s") for t in
                  ("maestria", "doctorado", "diplomado") if cuenta[t]]
        celdas.append((str(len(becas_pais)), "Becas"))
        metricas_pais = "".join(
            f'<div class="metrica {"oliva" if i % 2 else ""}">'
            f"<div><b>{v}</b><span>{k}</span></div></div>"
            for i, (v, k) in enumerate(celdas))

        cuerpo = f"""<div class="contenedor">
  <h1 class="titulo-pagina">Posgrados en {e(nombre_pais)}</h1>
  <p class="bajada">{miles(len(progs))} programas en {len(us)} universidades · {e(region)}</p>

  <div class="metricas">{metricas_pais}</div>

  <section class="seccion">
    <div class="seccion-cabecera"><h2>Áreas de estudio</h2></div>
    <div class="fila-filtros" style="border:0;padding:0;margin:0">{chips}</div>
  </section>

  <section class="seccion">
    <div class="seccion-cabecera"><h2>Universidades en {e(nombre_pais)}</h2>
      <a class="btn-texto" href="../../#/maestrias?pais={e(nombre_pais)}">Buscar y filtrar ›</a></div>
    {rejilla_enlaces(tarjetas)}
  </section>

  {lista_becas}
</div>"""

        jsonld = {
            "@context": "https://schema.org", "@type": "CollectionPage",
            "name": f"Posgrados en {nombre_pais}",
            "description": desc,
            "about": {"@type": "Country", "name": nombre_pais},
            "mainEntity": {"@type": "ItemList", "numberOfItems": len(tarjetas),
                           "itemListElement": [
                               {"@type": "ListItem", "position": i + 1, "name": t[0],
                                "url": f"{SITIO}/u/{u['id']}/"}
                               for i, (t, u) in enumerate(zip(tarjetas, us))][:50]},
        }
        loc = pagina(f"pais/{baba(nombre_pais)}", titulo, desc,
                     [("Inicio", "../../"), ("Explorar", "../../explorar/"),
                      (nombre_pais, None)], cuerpo, jsonld)
        urls.append((loc, "0.8", "weekly"))

    # ------------------------------------------------------------- areas
    areas = sorted({p["area"] for p in programas})
    for area in areas:
        progs = [p for p in programas if p["area"] == area]
        cuenta = {t: sum(1 for p in progs if p["tipo"] == t) for t in TIPOS}
        por_pais = {}
        for p in progs:
            por_pais[p["pais"]] = por_pais.get(p["pais"], 0) + 1

        titulo = f"{area}: maestrías, doctorados y diplomados | Ruta Amauta"
        desc = (f"{len(progs)} programas de {area.lower()} en "
                f"{len(por_pais)} países: {cuenta['maestria']} maestrías, "
                f"{cuenta['doctorado']} doctorados y {cuenta['diplomado']} diplomados. "
                f"Compara costos y modalidades.")

        chips = "".join(
            f'<a class="pastilla" href="../../pais/{baba(k)}/">{e(k)} <b>{v}</b></a>'
            for k, v in sorted(por_pais.items(), key=lambda kv: -kv[1])[:40])

        destacados = sorted(progs, key=lambda p: (not p.get("destacado"), p["nombre"]))[:24]
        tarjetas = [(p["nombre"], f"{p['institucion']} · {p['pais']}",
                     f"../../u/{p['institucion_id']}/",
                     f'<p class="meta-linea">{e(TIPOS[p["tipo"]])} · {e(duracion(p))} · {e(p["modalidad"])}</p>')
                    for p in destacados]

        cuerpo = f"""<div class="contenedor">
  <h1 class="titulo-pagina">{e(area)}</h1>
  <p class="bajada">{miles(len(progs))} programas de posgrado en {len(por_pais)} países</p>

  <div class="metricas">
    <div class="metrica"><div><b>{miles(cuenta['maestria'])}</b><span>Maestrías</span></div></div>
    <div class="metrica oliva"><div><b>{miles(cuenta['doctorado'])}</b><span>Doctorados</span></div></div>
    <div class="metrica"><div><b>{miles(cuenta['diplomado'])}</b><span>Diplomados</span></div></div>
    <div class="metrica oliva"><div><b>{len(por_pais)}</b><span>Países</span></div></div>
  </div>

  <section class="seccion">
    <div class="seccion-cabecera"><h2>Dónde estudiar {e(area.lower())}</h2></div>
    <div class="fila-filtros" style="border:0;padding:0;margin:0">{chips}</div>
  </section>

  <section class="seccion">
    <div class="seccion-cabecera"><h2>Programas destacados</h2>
      <a class="btn-texto" href="../../#/maestrias?area={e(area)}">Ver todos en el buscador ›</a></div>
    {rejilla_enlaces(tarjetas)}
  </section>
</div>"""

        jsonld = {"@context": "https://schema.org", "@type": "CollectionPage",
                  "name": area, "description": desc}
        loc = pagina(f"area/{baba(area)}", titulo, desc,
                     [("Inicio", "../../"), ("Explorar", "../../explorar/"), (area, None)],
                     cuerpo, jsonld)
        urls.append((loc, "0.7", "monthly"))

    # ------------------------------------------------------------- becas
    for b in becas:
        slug = baba(b["id"])
        info = enl_beca.get(b["id"], {})
        url_oficial = info.get("url") or b.get("url")
        incluye = [k.replace("_", " ") for k, v in (b.get("incluye") or {}).items() if v]

        titulo = f"{b['nombre']} — {b['organizacion']} | Ruta Amauta"
        desc = (b.get("descripcion") or
                f"Beca {b.get('cobertura', '').lower()} de {b['organizacion']} "
                f"para estudiar en {b.get('pais')}.")[:300]

        req = "".join(f"<li>{e(r)}</li>" for r in (b.get("requisitos") or []))
        inc = "".join(f'<span class="pastilla estatica">{e(i)}</span>' for i in incluye)
        niveles = ", ".join(b.get("niveles") or []) or "—"
        areas_b = ", ".join(b.get("areas") or []) or "Todas"

        cuerpo = f"""<div class="contenedor">
  <section class="ficha-cabecera">
    <div>
      <span class="insignia beca">Beca</span>
      <h1 class="titulo-pagina">{e(b['nombre'])}</h1>
      <p class="bajada">{e(b['organizacion'])} · {e(b.get('pais'))}</p>
    </div>
    <div class="ficha-acciones">
      <a class="btn btn-primario" href="{e(url_oficial)}" target="_blank" rel="noopener nofollow">Convocatoria oficial ↗</a>
    </div>
  </section>

  <p class="parrafo">{e(b.get('descripcion') or '')}</p>

  <div class="datos">
    <div class="dato"><span>Cobertura</span><b>{e(b.get('cobertura') or '—')}</b></div>
    <div class="dato"><span>Nivel</span><b>{e(niveles)}</b></div>
    <div class="dato"><span>País de destino</span><b>{e(b.get('pais') or '—')}</b></div>
    <div class="dato"><span>Modalidad</span><b>{e(b.get('modalidad') or '—')}</b></div>
    <div class="dato"><span>Duración</span><b>{e(duracion(b))}</b></div>
    <div class="dato"><span>Áreas</span><b>{e(areas_b)}</b></div>
    <div class="dato"><span>Apertura</span><b>{e(fecha_es(b.get('fecha_apertura')))}</b></div>
    <div class="dato"><span>Cierre</span><b>{e(fecha_es(b.get('fecha_cierre')))}</b></div>
  </div>

  {'<h2 class="titulo-seccion">La beca incluye</h2><div class="fila-chips">' + inc + '</div>' if inc else ''}
  {'<h2 class="titulo-seccion">Requisitos principales</h2><ul class="lista-requisitos">' + req + '</ul>' if req else ''}

  <p class="nota-legal">Las fechas son referenciales: las convocatorias son anuales y
  pueden cambiar. Confirma siempre plazos y requisitos en la convocatoria oficial.</p>

  <p><a class="btn btn-oliva" href="../../#/becas">Ver todas las becas</a></p>
</div>"""

        jsonld = {
            "@context": "https://schema.org",
            "@type": "EducationalOccupationalProgram",
            "name": b["nombre"],
            "programPrerequisites": b.get("requisitos") or [],
            "educationalProgramMode": b.get("modalidad"),
            "description": desc,
            "provider": {"@type": "Organization", "name": b["organizacion"]},
            "url": url_oficial,
        }
        loc = pagina(f"beca/{slug}", titulo, desc,
                     [("Inicio", "../../"), ("Explorar", "../../explorar/"),
                      ("Becas", "../../#/becas"), (b["nombre"], None)],
                     cuerpo, jsonld, og_tipo="article")
        urls.append((loc, "0.9", "weekly"))

    # ---------------------------------------------------------- explorar
    por_region = {}
    for u in instituciones:
        por_region.setdefault(u.get("region", "Otros"), set()).add(u["pais"])

    bloques_region = []
    for region in sorted(por_region):
        enlaces_p = "".join(
            f'<a class="pastilla" href="../pais/{baba(p)}/">{e(p)}</a>'
            for p in sorted(por_region[region]))
        bloques_region.append(f"""<section class="seccion">
      <div class="seccion-cabecera"><h2>{e(region)}</h2></div>
      <div class="fila-filtros" style="border:0;padding:0;margin:0">{enlaces_p}</div>
    </section>""")

    enlaces_area = "".join(
        f'<a class="pastilla" href="../area/{baba(a)}/">{e(a)}</a>' for a in areas)
    enlaces_beca = "".join(
        f'<li><a href="../beca/{baba(b["id"])}/">{e(b["nombre"])}</a> '
        f'<span class="tenue">· {e(b["organizacion"])}</span></li>'
        for b in sorted(becas, key=lambda x: x["nombre"]))

    cuerpo = f"""<div class="contenedor">
  <h1 class="titulo-pagina">Explorar Ruta Amauta</h1>
  <p class="bajada">{miles(len(programas))} programas de posgrado en
  {len(instituciones)} instituciones de {len(paises)} países, más
  {len(becas)} convocatorias de becas.</p>

  <section class="seccion">
    <div class="seccion-cabecera"><h2>Áreas de estudio</h2></div>
    <div class="fila-filtros" style="border:0;padding:0;margin:0">{enlaces_area}</div>
  </section>

  {''.join(bloques_region)}

  <section class="seccion">
    <div class="seccion-cabecera"><h2>Todas las becas</h2></div>
    <ul class="lista-enlaces dos-columnas">{enlaces_beca}</ul>
  </section>
</div>"""

    jsonld = {"@context": "https://schema.org", "@type": "CollectionPage",
              "name": "Explorar Ruta Amauta",
              "description": "Mapa completo de países, áreas, universidades y becas."}
    loc = pagina("explorar", "Explorar: países, áreas, universidades y becas | Ruta Amauta",
                 f"Mapa completo de Ruta Amauta: {len(paises)} países, {len(areas)} áreas "
                 f"de estudio, {len(instituciones)} instituciones y {len(becas)} becas.",
                 [("Inicio", "../"), ("Explorar", None)], cuerpo, jsonld)
    urls.append((loc, "0.9", "weekly"))

    # ---------------------------------------------------- sitemap y robots
    urls.insert(0, (f"{SITIO}/", "1.0", "daily"))
    cuerpos = "\n".join(
        f"  <url><loc>{u}</loc><lastmod>{hoy}</lastmod>"
        f"<changefreq>{c}</changefreq><priority>{p}</priority></url>"
        for u, p, c in urls)
    with open(os.path.join(RAIZ, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                 f"{cuerpos}\n</urlset>\n")

    with open(os.path.join(RAIZ, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"""# Ruta Amauta — https://ruta.amauta.online
User-agent: *
Allow: /
Disallow: /scraper/
Disallow: /imagenes/mockup design/

Sitemap: {SITIO}/sitemap.xml
""")

    print(f"  {len(urls)} páginas en sitemap.xml")
    print(f"  robots.txt escrito")


if __name__ == "__main__":
    main()
