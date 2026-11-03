"""Descarga las listas oficiales de SUNEDU y las contrasta con el catálogo.

Produce data/sunedu.json con:
  - las universidades y escuelas de posgrado licenciadas (con enlace a la
    resolución de licenciamiento),
  - las universidades con licencia denegada (con su resolución),
  - el cruce de cada institución peruana de data/instituciones.json contra
    esas listas, para que la interfaz muestre la evidencia y no solo una
    etiqueta.

Uso:
    python scraper/sunedu_listas.py            # descarga y cruza
    python scraper/sunedu_listas.py --local DIR # usa lic.html y den.html ya descargados

Si SUNEDU no responde, el script conserva el último data/sunedu.json y lo
marca como desactualizado en lugar de borrarlo.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "data" / "sunedu.json"

URL_LICENCIADAS = "https://www.sunedu.gob.pe/lista-de-universidades-licenciadas/"
URL_DENEGADAS = "https://www.sunedu.gob.pe/lista-de-universidades-denegadas/"
AGENTE = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/130.0 Safari/537.36 RutaAmauta/1.0")

# Nombres del catálogo que no coinciden literalmente con el de SUNEDU.
ALIAS = {
    "centrum pucp business school": "pontificia universidad catolica del peru",
    "universidad nacional de san agustin de arequipa": "universidad nacional de san agustin",
    "universidad nacional toribio rodriguez de mendoza": (
        "universidad nacional toribio rodriguez de mendoza de amazonas"),
}


def clave(nombre: str) -> str:
    txt = unicodedata.normalize("NFD", nombre.lower())
    txt = "".join(c for c in txt if unicodedata.category(c) != "Mn")
    txt = re.sub(r"\b(s\.?a\.?c\.?|s\.?a\.?)\b", " ", txt)
    txt = re.sub(r"[^a-z0-9 ]+", " ", txt)
    return re.sub(r"\s+", " ", txt).strip()


def limpiar(celda: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", celda)).replace("\xa0", " ").strip()


def leer_tablas(texto: str) -> list[list[dict]]:
    """Cada tabla es una lista de filas {texto: [...], enlaces: [...]}."""
    tablas = []
    for tabla in re.findall(r"<table[^>]*>(.*?)</table>", texto, re.S):
        filas = []
        for fila in re.findall(r"<tr[^>]*>(.*?)</tr>", tabla, re.S):
            celdas = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", fila, re.S)
            if not celdas:
                continue
            filas.append({
                "texto": [re.sub(r"\s+", " ", limpiar(c)) for c in celdas],
                "enlaces": [re.findall(r'href="([^"]+)"', c) for c in celdas],
            })
        tablas.append(filas)
    return tablas


def fecha_iso(ddmmaaaa: str) -> str | None:
    m = re.match(r"(\d{2})-(\d{2})-(\d{4})", ddmmaaaa)
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else None


def numero_resolucion(url: str) -> str | None:
    m = re.search(r"(\d{2,4})[-_](20\d\d)[-_]sunedu[-_]cd", url, re.I)
    return f"{int(m.group(1)):03d}-{m.group(2)}-SUNEDU/CD" if m else None


def parsear_licenciadas(texto: str) -> tuple[list[dict], dict]:
    registros = []
    for tabla in leer_tablas(texto):
        if not tabla:
            continue
        cabecera = " ".join(tabla[0]["texto"]).upper()
        tipo = "escuela_posgrado" if "ESCUELA" in cabecera else "universidad"
        for fila in tabla[1:]:
            t, e = fila["texto"], fila["enlaces"]
            if len(t) < 5:
                continue
            url = (e[2] or [None])[0]
            dep_prov = t[3].split("/")
            registros.append({
                "nombre": t[0], "tipo": tipo, "estado": "licenciada",
                "fecha": fecha_iso(t[1]), "resolucion_url": url,
                "resolucion": numero_resolucion(url or ""),
                "departamento": dep_prov[0].strip(),
                "provincia": dep_prov[-1].strip(), "gestion": t[4],
                # La lista de licenciadas a veces enlaza una resolución
                # denegatoria (caso Universidad Tecnológica de los Andes):
                # se señala para revisión, sin cambiar el estado publicado.
                "observacion": ("El enlace de la resolución alude a una denegatoria; "
                                "revisar actos posteriores.")
                if url and "denegar" in url.lower() else None,
            })
    m = re.search(r"(\d+)\s+universidades cuentan con licencia institucional vigente", texto)
    # La página no rotula la fecha de corte en texto plano; se usa la fecha
    # de última modificación que declara su propio JSON-LD.
    corte = re.search(r'"dateModified":"(20\d\d-\d\d-\d\d)', texto)
    return registros, {
        "declaradas": int(m.group(1)) if m else None,
        "corte": corte.group(1) if corte else None,
    }


def parsear_denegadas(texto: str) -> tuple[list[dict], dict]:
    registros = []
    for tabla in leer_tablas(texto):
        if not tabla:
            continue
        cabecera = " ".join(tabla[0]["texto"]).upper()
        tipo = "escuela_posgrado" if "ESCUELA" in cabecera else "universidad"
        for fila in tabla[1:]:
            t, e = fila["texto"], fila["enlaces"]
            if len(t) < 4:
                continue
            url = (e[2] or [None])[0]
            registros.append({
                "nombre": t[0], "tipo": tipo, "estado": "denegada",
                "fecha": fecha_iso(t[1]), "resolucion_url": url,
                "resolucion": numero_resolucion(url or ""), "gestion": t[3],
            })
    m = re.search(r"(\d+)\s+universidades y (\d+) escuelas de posgrado se encuentran con "
                  r"licencia institucional denegada", texto)
    return registros, {"declaradas": int(m.group(1)) + int(m.group(2)) if m else None}


def descargar(url: str) -> str:
    import requests
    r = requests.get(url, headers={"User-Agent": AGENTE}, timeout=40)
    r.raise_for_status()
    return r.content.decode("utf-8", errors="replace")


def cruzar(instituciones: list[dict], licenciadas: list[dict],
           denegadas: list[dict]) -> dict:
    indice = {clave(r["nombre"]): r for r in denegadas}
    indice.update({clave(r["nombre"]): r for r in licenciadas})
    cruce = {}
    for inst in instituciones:
        if inst.get("pais") != "Perú":
            continue
        k = clave(inst["nombre"])
        k = ALIAS.get(k, k)
        oficial = indice.get(k)
        if oficial is None:  # coincidencia parcial: el nombre oficial contiene al del catálogo
            candidatos = [r for kk, r in indice.items() if k in kk or kk in k]
            oficial = candidatos[0] if len(candidatos) == 1 else None
        if oficial is None:
            resultado = "no_figura"
        elif oficial["estado"] == "licenciada":
            resultado = "licenciada"
        else:
            resultado = "denegada"
        cruce[inst["id"]] = {
            "catalogo": inst.get("sunedu"),
            "oficial": resultado,
            "nombre_oficial": oficial["nombre"] if oficial else None,
            "fecha": oficial["fecha"] if oficial else None,
            "resolucion": oficial.get("resolucion") if oficial else None,
            "resolucion_url": oficial.get("resolucion_url") if oficial else None,
            "observacion": oficial.get("observacion") if oficial else None,
            "discrepancia": (resultado == "licenciada") != (inst.get("sunedu") == "licenciada"),
            "via": "alias" if k != clave(inst["nombre"]) else "nombre",
        }
    return cruce


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--local", type=Path, help="Carpeta con lic.html y den.html")
    args = ap.parse_args()

    hoy = datetime.now(timezone(timedelta(hours=-5)))  # hora de Lima
    try:
        if args.local:
            t_lic = (args.local / "lic.html").read_text(encoding="utf-8", errors="replace")
            t_den = (args.local / "den.html").read_text(encoding="utf-8", errors="replace")
        else:
            t_lic, t_den = descargar(URL_LICENCIADAS), descargar(URL_DENEGADAS)
    except Exception as error:  # noqa: BLE001 — cualquier fallo de red conserva el último dato
        print(f"SUNEDU no respondió: {error}", file=sys.stderr)
        if SALIDA.exists():
            previo = json.loads(SALIDA.read_text(encoding="utf-8"))
            previo["estado_fuente"] = "desactualizado"
            previo["ultimo_error"] = f"{hoy:%Y-%m-%d}: {error}"[:300]
            SALIDA.write_text(json.dumps(previo, ensure_ascii=False, indent=1) + "\n",
                              encoding="utf-8")
        return 0

    licenciadas, info_lic = parsear_licenciadas(t_lic)
    denegadas, info_den = parsear_denegadas(t_den)
    if len(licenciadas) < 80:
        print(f"Solo se leyeron {len(licenciadas)} licenciadas: formato inesperado.",
              file=sys.stderr)
        return 1

    instituciones = json.loads((RAIZ / "data" / "instituciones.json").read_text(encoding="utf-8"))
    cruce = cruzar(instituciones, licenciadas, denegadas)

    salida = {
        "consultado": f"{hoy:%Y-%m-%d}",
        "estado_fuente": "vigente",
        "fuentes": {"licenciadas": URL_LICENCIADAS, "denegadas": URL_DENEGADAS},
        "corte_licenciadas": info_lic["corte"],
        "declaradas_licenciadas": info_lic["declaradas"],
        "declaradas_denegadas": info_den["declaradas"],
        "licenciadas": licenciadas,
        "denegadas": denegadas,
        "cruce_catalogo": cruce,
    }
    SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    disc = [k for k, v in cruce.items() if v["discrepancia"] or v["oficial"] == "no_figura"]
    print(f"Licenciadas: {len(licenciadas)} (SUNEDU declara {info_lic['declaradas']}, "
          f"corte {info_lic['corte']}) · denegadas: {len(denegadas)}")
    print(f"Instituciones peruanas cruzadas: {len(cruce)} · a revisar: {len(disc)} {disc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
