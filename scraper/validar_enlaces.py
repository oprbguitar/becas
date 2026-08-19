#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Valida que cada enlace del catalogo abra de verdad, y lo corrige si no.

Estrategia por institucion (rapida y con scraping real, no fuerza bruta):

    1. Prueba la ruta de posgrado declarada en la semilla (con y sin www).
    2. Si falla, abre la portada del dominio y **lee el HTML**: busca los
       enlaces cuyo texto o URL hablen de posgrado, maestria, doctorado,
       graduate, master... los puntua y comprueba los mejores.
    3. Si tampoco, se queda con la portada del dominio.
    4. Si el dominio no responde desde esta red, publica igual la portada
       oficial pero la marca como no verificada y guarda una busqueda
       restringida al dominio como salida alternativa. Nunca se publica un
       enlace de buscador como "sitio oficial".

Muchos sitios universitarios bloquean clientes automatizados y devuelven 403,
406, 418 o 429 aunque la pagina abra perfectamente en un navegador. Esos
codigos se tratan como "vivo pero protegido" y el enlace se conserva; solo se
descarta ante 404/410, DNS inexistente o timeout.

Las becas se comprueban igual: URL declarada -> portada del organismo ->
alternativa de busqueda.

El resultado va a data/enlaces.json, que consume
scraper/generar_catalogo.py: el catalogo publicado solo lleva enlaces
comprobados.

Uso:
    python scraper/validar_enlaces.py
    python scraper/validar_enlaces.py --limite 10 --hilos 8
    python scraper/validar_enlaces.py --solo-becas
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from urllib.parse import quote_plus, urljoin, urlparse

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from instituciones import INSTITUCIONES  # noqa: E402

try:
    from enlaces_manuales import BECAS as MANUAL_BECAS
    from enlaces_manuales import INSTITUCIONES as MANUAL_INST
except ImportError:      # el modulo de correcciones es opcional
    MANUAL_INST, MANUAL_BECAS = {}, {}

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_DATOS = os.path.join(RAIZ, "data")
SALIDA = os.path.join(DIR_DATOS, "enlaces.json")

CABECERAS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-PE,es;q=0.9,en;q=0.8",
}

BLOQUEO_BOT = {401, 403, 405, 406, 409, 418, 429, 503}
MUERTO = {400, 404, 410, 451, 500, 502}

TIEMPO = 16         # segundos por peticion
MAX_HTML = 300_000  # bytes de HTML a leer de la portada

# Palabras que delatan la seccion de posgrado, con su peso.
PISTAS = [
    ("escuela de posgrado", 10), ("escuela de postgrado", 10),
    ("posgrado", 8), ("postgrado", 8), ("pos-graduacao", 8),
    ("maestria", 7), ("maestrías", 7), ("maestrias", 7), ("magister", 6),
    ("doctorado", 6), ("master", 5), ("masteres", 7), ("másteres", 7),
    ("graduate", 6), ("postgraduate", 8), ("mba", 3), ("diplomado", 4),
]
RUIDO = ["noticia", "news", "blog", "evento", "login", "intranet", "campus-virtual",
         "facebook", "twitter", "instagram", "linkedin", "youtube", ".pdf"]

imprimir = threading.Lock()


def limpiar(texto: str) -> str:
    import unicodedata
    t = unicodedata.normalize("NFD", (texto or "").lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def sesion() -> requests.Session:
    s = requests.Session()
    s.headers.update(CABECERAS)
    return s


def probar(ses, url: str, traer_html=False) -> dict:
    """{estado: ok|protegido|muerto, codigo, url_final, html}"""
    try:
        r = ses.get(url, timeout=TIEMPO, allow_redirects=True, stream=True)
        codigo, final = r.status_code, r.url
        html = ""
        if traer_html and 200 <= codigo < 300:
            trozos, leidos = [], 0
            for t in r.iter_content(8192):
                trozos.append(t)
                leidos += len(t)
                if leidos >= MAX_HTML:
                    break
            html = b"".join(trozos).decode(r.encoding or "utf-8", "ignore")
        r.close()
        if 200 <= codigo < 300:
            return {"estado": "ok", "codigo": codigo, "url_final": final, "html": html}
        if codigo in BLOQUEO_BOT:
            return {"estado": "protegido", "codigo": codigo, "url_final": final, "html": ""}
        return {"estado": "muerto", "codigo": codigo, "url_final": final, "html": ""}
    except requests.RequestException as e:
        return {"estado": "muerto", "codigo": 0, "url_final": url, "html": "",
                "error": type(e).__name__}


def enlaces_de(html: str, base: str, dominio: str):
    """Devuelve candidatos de la portada ordenados por puntaje de 'posgrado'."""
    encontrados = {}
    for m in re.finditer(r'<a\b[^>]*href=["\']([^"\'#]+)["\'][^>]*>(.{0,160}?)</a>',
                         html, re.I | re.S):
        href, texto = m.group(1).strip(), re.sub(r"<[^>]+>", " ", m.group(2))
        if href.startswith(("mailto:", "tel:", "javascript:")):
            continue
        absoluta = urljoin(base, href)
        p = urlparse(absoluta)
        if p.scheme not in ("http", "https"):
            continue
        # solo dentro del mismo dominio o subdominios
        if dominio not in p.netloc:
            continue
        blanco = limpiar(texto + " " + p.path)
        if any(r in blanco for r in RUIDO):
            continue
        puntos = sum(peso for palabra, peso in PISTAS if palabra in blanco)
        if puntos:
            # una ruta corta suele ser la seccion, no una noticia suelta
            puntos += max(0, 4 - p.path.strip("/").count("/"))
            encontrados[absoluta] = max(puntos, encontrados.get(absoluta, 0))
    return [u for u, _ in sorted(encontrados.items(), key=lambda kv: -kv[1])]


def busqueda(dominio: str, texto: str) -> str:
    return "https://www.google.com/search?q=" + quote_plus(f"site:{dominio} {texto}")


def resolver_institucion(fila):
    iid, nombre, sigla, pais, ciudad, dominio, ruta = fila[:7]
    ses = sesion()
    protegido = None

    # 0. correccion manual: tiene prioridad sobre todo lo demas
    manual = MANUAL_INST.get(iid)
    if manual:
        r = probar(ses, manual)
        if r["estado"] == "ok":
            return iid, salida_ok(r["url_final"], r["codigo"], "manual")
        # verificada a mano: se publica aunque esta red no la alcance
        return iid, {"url": manual, "estado": "manual", "codigo": r["codigo"],
                     "nivel": "manual"}

    # 1. ruta declarada
    for host in (f"https://www.{dominio}", f"https://{dominio}"):
        if not ruta:
            break
        r = probar(ses, host + ruta)
        if r["estado"] == "ok":
            return iid, salida_ok(r["url_final"], r["codigo"], "declarada")
        if r["estado"] == "protegido" and protegido is None:
            protegido = (host + ruta, r["codigo"], "declarada")

    # 2. portada + lectura del HTML
    portada = None
    for host in (f"https://www.{dominio}", f"https://{dominio}"):
        r = probar(ses, host + "/", traer_html=True)
        if r["estado"] == "ok":
            portada = r
            break
        if r["estado"] == "protegido" and protegido is None:
            protegido = (host + "/", r["codigo"], "portada")

    if portada:
        for candidato in enlaces_de(portada["html"], portada["url_final"], dominio)[:4]:
            r = probar(ses, candidato)
            if r["estado"] == "ok":
                return iid, salida_ok(r["url_final"], r["codigo"], "descubierta")
            if r["estado"] == "protegido" and protegido is None:
                protegido = (candidato, r["codigo"], "descubierta")
        # 3. la portada al menos abre
        return iid, salida_ok(portada["url_final"], portada["codigo"], "portada")

    if protegido:
        url, codigo, nivel = protegido
        return iid, {"url": url, "estado": "protegido", "codigo": codigo, "nivel": nivel}

    # 4. El dominio no respondio desde esta red. No significa que este caido
    #    para el usuario final (muchas universidades bloquean centros de datos),
    #    asi que se publica la portada oficial y se marca como no verificada;
    #    la ficha ofrece ademas el boton de busqueda como salida garantizada.
    return iid, {"url": f"https://www.{dominio}/", "estado": "sin_respuesta",
                 "codigo": 0, "nivel": "portada",
                 "alternativa": busqueda(dominio, "posgrado maestría doctorado")}


def salida_ok(url, codigo, nivel):
    return {"url": url, "estado": "ok", "codigo": codigo, "nivel": nivel}


def resolver_beca(beca):
    ses = sesion()
    manual = MANUAL_BECAS.get(beca["id"])
    if manual:
        r = probar(ses, manual)
        estado = "ok" if r["estado"] == "ok" else "manual"
        return beca["id"], {"url": r["url_final"] if estado == "ok" else manual,
                            "estado": estado, "codigo": r["codigo"], "nivel": "manual"}

    url = (beca.get("url") or "").strip()
    url = url.replace("Https://", "https://").replace("Http://", "http://")
    if not url:
        return beca["id"], {"url": busqueda("gob.pe", beca["nombre"]),
                            "estado": "sin_respuesta", "codigo": 0, "nivel": "busqueda"}

    r = probar(ses, url)
    if r["estado"] == "ok":
        return beca["id"], salida_ok(r["url_final"], r["codigo"], "declarada")
    if r["estado"] == "protegido":
        return beca["id"], {"url": url, "estado": "protegido",
                            "codigo": r["codigo"], "nivel": "declarada"}

    host = urlparse(url).netloc
    if host:
        r2 = probar(ses, f"https://{host}/")
        if r2["estado"] == "ok":
            return beca["id"], salida_ok(r2["url_final"], r2["codigo"], "portada")
        if r2["estado"] == "protegido":
            return beca["id"], {"url": f"https://{host}/", "estado": "protegido",
                                "codigo": r2["codigo"], "nivel": "portada"}

    # El dominio no contesta desde esta red. La URL declarada la puso una
    # persona y apunta a la convocatoria concreta, asi que vale mas conservarla
    # que degradarla a la portada; se marca como no verificada y se guarda una
    # busqueda como salida alternativa.
    return beca["id"], {"url": url, "estado": "sin_respuesta", "codigo": 0,
                        "nivel": "declarada",
                        "alternativa": busqueda(host or "gob.pe", beca["nombre"])}


MARCA = {"ok": "OK ", "protegido": "BOT", "sin_respuesta": "-- ", "manual": "MAN"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limite", type=int, default=0)
    ap.add_argument("--hilos", type=int, default=14)
    ap.add_argument("--solo-becas", action="store_true")
    ap.add_argument("--solo-instituciones", action="store_true")
    args = ap.parse_args()

    previos = {}
    if os.path.exists(SALIDA):
        try:
            previos = json.load(open(SALIDA, encoding="utf-8"))
        except ValueError:
            previos = {}

    instituciones = dict(previos.get("instituciones", {}))
    becas_res = dict(previos.get("becas", {}))

    if not args.solo_becas:
        filas = INSTITUCIONES[: args.limite] if args.limite else INSTITUCIONES
        print(f"Validando {len(filas)} instituciones con {args.hilos} hilos…", flush=True)
        with ThreadPoolExecutor(max_workers=args.hilos) as pool:
            for n, (iid, res) in enumerate(pool.map(resolver_institucion, filas), 1):
                instituciones[iid] = res
                with imprimir:
                    print(f"  [{n:>3}/{len(filas)}] {MARCA[res['estado']]} {iid:<14} "
                          f"{res['nivel']:<11} {res['url'][:72]}", flush=True)

    if not args.solo_instituciones:
        ruta_becas = os.path.join(DIR_DATOS, "becas.json")
        if os.path.exists(ruta_becas):
            becas = json.load(open(ruta_becas, encoding="utf-8"))
            if args.limite:
                becas = becas[: args.limite]
            print(f"\nValidando {len(becas)} becas…", flush=True)
            with ThreadPoolExecutor(max_workers=args.hilos) as pool:
                for n, (bid, res) in enumerate(pool.map(resolver_beca, becas), 1):
                    becas_res[bid] = res
                    with imprimir:
                        print(f"  [{n:>3}/{len(becas)}] {MARCA[res['estado']]} {bid:<32} "
                              f"{res['url'][:62]}", flush=True)

    def cuenta(d):
        return {e: sum(1 for v in d.values() if v["estado"] == e)
                for e in ("ok", "manual", "protegido", "sin_respuesta")}

    salida = {
        "generado_en": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "resumen": {"instituciones": cuenta(instituciones), "becas": cuenta(becas_res)},
        "instituciones": instituciones,
        "becas": becas_res,
    }
    os.makedirs(DIR_DATOS, exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8") as fh:
        json.dump(salida, fh, ensure_ascii=False, indent=1, sort_keys=True)

    print("\nResumen:", json.dumps(salida["resumen"], ensure_ascii=False), flush=True)
    print(f"Guardado en {SALIDA}", flush=True)


if __name__ == "__main__":
    main()
