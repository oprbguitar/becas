#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rastreador de convocatorias de BecaRadar.

Se ejecuta en GitHub Actions (ver .github/workflows/actualizar-becas.yml), no en
el navegador del usuario ni con ayuda de un modelo: es un script determinista.

Qué hace, beca por beca:
  1. Visita la URL de bases oficiales declarada en el semillero.
  2. Verifica que el enlace siga vivo (para no mandar a nadie a un 404).
  3. Extrae los requisitos publicados (listas y párrafos con lenguaje de requisito).
  4. Detecta fechas de cierre visibles en la página.
  5. Fusiona lo encontrado sobre la ficha del semillero. Si algo falla, la ficha
     original se conserva intacta: el portal nunca se queda sin datos.

Uso:
    python scraper/scrape.py                 # rastrea todo y escribe data/
    python scraper/scrape.py --limite 5      # prueba rápida
    python scraper/scrape.py --sin-red       # solo regenera desde el semillero
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seed import BECAS as SEMILLA  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SALIDA_BECAS = ROOT / "data" / "becas.json"
SALIDA_META = ROOT / "data" / "meta.json"

AGENTE = (
    "Mozilla/5.0 (compatible; BecaRadarBot/1.0; "
    "+https://github.com/oprbguitar/becas) requests"
)
TIEMPO_LIMITE = 20
PAUSA_POR_DOMINIO = 1.5      # cortesía: no golpear el mismo servidor
HILOS = 6

# Palabras que delatan una línea de requisito en español, inglés o portugués.
PISTAS_REQUISITO = (
    "requisito", "requiere", "deberá", "debera", "debe ", "acredit", "presentar",
    "postulante", "aplicante", "elegib", "podrán postular", "no haber", "haber ",
    "contar con", "edad", "años", "certificado", "título", "titulo", "grado de",
    "promedio", "nacionalidad", "carta de", "experiencia",
    "requirement", "eligib", "must ", "should have", "applicants", "at least",
    "hold a", "degree", "proficiency", "citizen",
)
RUIDO = (
    "cookie", "javascript", "iniciar sesión", "log in", "sign up", "newsletter",
    "©", "todos los derechos", "all rights reserved", "política de privacidad",
    "privacy policy", "menú", "menu", "compartir", "share this",
)

MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10,
    "noviembre": 11, "diciembre": 12,
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
}

_ultimo_acceso: dict[str, float] = {}


# --------------------------------------------------------------------- red
def esperar_turno(url: str) -> None:
    """Impone una pausa mínima entre peticiones al mismo dominio."""
    dominio = urlparse(url).netloc
    ahora = time.monotonic()
    previo = _ultimo_acceso.get(dominio, 0.0)
    espera = PAUSA_POR_DOMINIO - (ahora - previo)
    if espera > 0:
        time.sleep(espera)
    _ultimo_acceso[dominio] = time.monotonic()


def descargar(url: str) -> tuple[int, str]:
    """Devuelve (código HTTP, html). Código 0 si la petición falló."""
    esperar_turno(url)
    try:
        r = requests.get(
            url, timeout=TIEMPO_LIMITE, allow_redirects=True,
            headers={"User-Agent": AGENTE, "Accept-Language": "es,en;q=0.8"},
        )
        tipo = r.headers.get("content-type", "")
        return r.status_code, r.text if "html" in tipo or not tipo else ""
    except requests.RequestException:
        return 0, ""


# ----------------------------------------------------------------- parseo
def limpiar(texto: str) -> str:
    return re.sub(r"\s+", " ", texto or "").strip(" •-–—·\t\n\r")


def es_requisito(texto: str) -> bool:
    t = texto.lower()
    if not (35 <= len(texto) <= 260):
        return False
    if any(r in t for r in RUIDO):
        return False
    if texto.count("|") > 1 or texto.count("·") > 2:
        return False
    return any(p in t for p in PISTAS_REQUISITO)


def extraer_requisitos(html: str, maximo: int = 8) -> list[str]:
    """Saca de la página las líneas que parecen requisitos de postulación."""
    sopa = BeautifulSoup(html, "html.parser")
    for basura in sopa(["script", "style", "nav", "footer", "header", "form", "noscript"]):
        basura.decompose()

    candidatos: list[str] = []
    for nodo in sopa.find_all(["li", "p"]):
        texto = limpiar(nodo.get_text(" ", strip=True))
        if es_requisito(texto):
            candidatos.append(texto)

    # Prioriza las líneas que están dentro de una sección de requisitos
    seccion: list[str] = []
    for cab in sopa.find_all(["h1", "h2", "h3", "h4", "strong"]):
        titulo = limpiar(cab.get_text(" ", strip=True)).lower()
        if not any(k in titulo for k in ("requisit", "eligib", "quién puede", "who can", "requirement", "bases")):
            continue
        for hermano in cab.find_all_next(["li", "p", "h2", "h3"], limit=40):
            if hermano.name in ("h2", "h3") and hermano is not cab:
                break
            texto = limpiar(hermano.get_text(" ", strip=True))
            if 25 <= len(texto) <= 260 and not any(r in texto.lower() for r in RUIDO):
                seccion.append(texto)

    vistos: set[str] = set()
    salida: list[str] = []
    for texto in seccion + candidatos:
        clave = texto.lower()[:70]
        if clave in vistos:
            continue
        vistos.add(clave)
        salida.append(texto)
        if len(salida) >= maximo:
            break
    return salida


def extraer_fecha_cierre(html: str) -> str | None:
    """Busca una fecha límite futura mencionada cerca de la palabra 'cierre'."""
    texto = limpiar(BeautifulSoup(html, "html.parser").get_text(" ", strip=True)).lower()
    ventanas = []
    for m in re.finditer(r"(cierre|cierra|plazo|deadline|hasta el|closes?|fecha límite|fecha limite)", texto):
        ventanas.append(texto[m.start(): m.start() + 160])
    hoy = date.today()
    candidatas: list[date] = []
    for v in ventanas:
        candidatas += _fechas_en(v)
    futuras = [f for f in candidatas if hoy <= f <= date(hoy.year + 2, 12, 31)]
    return min(futuras).isoformat() if futuras else None


def _fechas_en(txt: str) -> list[date]:
    encontradas: list[date] = []
    for d, m, a in re.findall(r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b", txt):
        try:
            encontradas.append(date(int(a), int(m), int(d)))
        except ValueError:
            pass
    for a, m, d in re.findall(r"\b(\d{4})-(\d{2})-(\d{2})\b", txt):
        try:
            encontradas.append(date(int(a), int(m), int(d)))
        except ValueError:
            pass
    patron_es = r"\b(\d{1,2})\s+de\s+([a-záéíóú]+)\s+(?:de\s+)?(\d{4})"
    for d, mes, a in re.findall(patron_es, txt):
        if mes in MESES:
            try:
                encontradas.append(date(int(a), MESES[mes], int(d)))
            except ValueError:
                pass
    patron_en = r"\b(\d{1,2})\s+([a-z]+)\s+(\d{4})|\b([a-z]+)\s+(\d{1,2}),?\s+(\d{4})"
    for g in re.findall(patron_en, txt):
        d1, mes1, a1, mes2, d2, a2 = g
        mes, d, a = (mes1, d1, a1) if mes1 else (mes2, d2, a2)
        if mes in MESES:
            try:
                encontradas.append(date(int(a), MESES[mes], int(d)))
            except ValueError:
                pass
    return encontradas


# -------------------------------------------------------------- proceso
def enriquecer(beca: dict) -> dict:
    """Devuelve una copia de la ficha con lo que se pudo leer de la web oficial."""
    ficha = dict(beca)
    url = beca.get("url_requisitos") or beca.get("url")
    codigo, html = descargar(url)
    ficha["enlace_verificado"] = date.today().isoformat()
    ficha["enlace_ok"] = codigo in (200, 201, 202, 203)

    if not html:
        ficha["fuente"] = "semilla"
        return ficha

    requisitos = extraer_requisitos(html)
    if len(requisitos) >= 3:
        ficha["requisitos"] = requisitos
        ficha["requisitos_actualizados"] = date.today().isoformat()
        ficha["fuente"] = "web-oficial"

    cierre = extraer_fecha_cierre(html)
    if cierre:
        ficha["fecha_cierre_detectada"] = cierre
        # Solo se adopta si la del semillero ya venció: evita pisar datos buenos
        if beca.get("fecha_cierre", "") < date.today().isoformat():
            ficha["fecha_cierre"] = cierre
    return ficha


def main() -> int:
    ap = argparse.ArgumentParser(description="Actualiza el catálogo de becas.")
    ap.add_argument("--limite", type=int, default=0, help="rastrea solo las N primeras")
    ap.add_argument("--sin-red", action="store_true", help="no descarga nada, solo regenera")
    args = ap.parse_args()

    becas = [dict(b) for b in SEMILLA]
    if args.limite:
        objetivo, resto = becas[: args.limite], becas[args.limite:]
    else:
        objetivo, resto = becas, []

    resultados: list[dict] = []
    if args.sin_red:
        resultados = objetivo
    else:
        print(f"Rastreando {len(objetivo)} convocatorias…", flush=True)
        with ThreadPoolExecutor(max_workers=HILOS) as pool:
            tareas = {pool.submit(enriquecer, b): b for b in objetivo}
            for i, tarea in enumerate(as_completed(tareas), 1):
                base = tareas[tarea]
                try:
                    ficha = tarea.result()
                except Exception as err:                      # noqa: BLE001
                    print(f"  ! {base['nombre']}: {err}")
                    ficha = base
                resultados.append(ficha)
                marca = "OK " if ficha.get("fuente") == "web-oficial" else "-- "
                print(f"  {marca}[{i}/{len(objetivo)}] {ficha['nombre'][:52]}", flush=True)

    # Conserva el orden original del semillero
    posicion = {b["id"]: i for i, b in enumerate(SEMILLA)}
    catalogo = sorted(resultados + resto, key=lambda b: posicion.get(b["id"], 999))

    SALIDA_BECAS.parent.mkdir(parents=True, exist_ok=True)
    SALIDA_BECAS.write_text(json.dumps(catalogo, ensure_ascii=False, indent=1), encoding="utf-8")

    meta = {
        "actualizado": date.today().isoformat(),
        "generado_en": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "total": len(catalogo),
        "con_requisitos_de_la_web": sum(1 for b in catalogo if b.get("fuente") == "web-oficial"),
        "enlaces_ok": sum(1 for b in catalogo if b.get("enlace_ok")),
        "regiones": sorted({b["region"] for b in catalogo}),
        "paises": sorted({b["pais"] for b in catalogo}),
    }
    SALIDA_META.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"\nCatálogo: {meta['total']} becas · "
          f"{meta['con_requisitos_de_la_web']} con requisitos leídos de la web · "
          f"{meta['enlaces_ok']} enlaces verificados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
