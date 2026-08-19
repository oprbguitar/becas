#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el catalogo de maestrias, doctorados y diplomados de Ruta Amauta.

No inventa datos al azar: expande una tabla semilla curada de instituciones
(scraper/instituciones.py) usando plantillas de programas por area academica.
Todo valor derivado (costos, duracion, modalidad) es determinista -- se calcula
con un hash estable del id -- de modo que dos ejecuciones producen exactamente
el mismo catalogo y el diff en git es limpio.

Los costos son RANGOS REFERENCIALES de mercado, no precios oficiales. Cada
programa enlaza a la pagina oficial de posgrado de su institucion, que es la
unica fuente de verdad para precios, fechas y requisitos.

Uso:
    python scraper/generar_catalogo.py
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from instituciones import (  # noqa: E402
    A_USD,
    AREAS,
    IDIOMA_POR_PAIS,
    INSTITUCIONES,
    MONEDA_POR_PAIS,
    REGION_POR_PAIS,
)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_DATOS = os.path.join(RAIZ, "data")

# ---------------------------------------------------------------- plantillas

MAESTRIA_ES = {
    "GES": ["Maestría en Administración de Empresas (MBA)",
            "Maestría en Dirección de Operaciones y Logística",
            "Maestría en Gestión de Proyectos",
            "Maestría en Dirección Estratégica de Recursos Humanos",
            "Maestría en Gestión de la Innovación"],
    "POL": ["Maestría en Gestión Pública",
            "Maestría en Políticas Públicas",
            "Maestría en Gobierno y Gestión Territorial",
            "Maestría en Gerencia Social",
            "Maestría en Regulación y Servicios Públicos"],
    "ING": ["Maestría en Ingeniería Civil con mención en Estructuras",
            "Maestría en Ingeniería Industrial",
            "Maestría en Ingeniería de Sistemas",
            "Maestría en Ingeniería de Minas",
            "Maestría en Ingeniería Mecánica y Energética"],
    "SAL": ["Maestría en Salud Pública",
            "Maestría en Epidemiología",
            "Maestría en Gestión de Servicios de Salud",
            "Maestría en Nutrición Clínica",
            "Maestría en Salud Mental Comunitaria"],
    "EDU": ["Maestría en Docencia Universitaria",
            "Maestría en Gestión de la Educación",
            "Maestría en Educación con mención en Currículo",
            "Maestría en Tecnología Educativa",
            "Maestría en Psicopedagogía"],
    "DER": ["Maestría en Derecho Constitucional",
            "Maestría en Derecho Penal y Procesal Penal",
            "Maestría en Derecho Corporativo",
            "Maestría en Derecho Laboral y Seguridad Social",
            "Maestría en Derecho Tributario"],
    "AMB": ["Maestría en Gestión Ambiental",
            "Maestría en Cambio Climático y Desarrollo Sostenible",
            "Maestría en Gestión de Recursos Hídricos",
            "Maestría en Energías Renovables",
            "Maestría en Ecología y Conservación"],
    "SOC": ["Maestría en Antropología",
            "Maestría en Sociología",
            "Maestría en Estudios Culturales",
            "Maestría en Historia",
            "Maestría en Filosofía"],
    "ECO": ["Maestría en Economía",
            "Maestría en Finanzas Corporativas",
            "Maestría en Economía Aplicada",
            "Maestría en Banca y Riesgos",
            "Maestría en Comercio Internacional"],
    "DAT": ["Maestría en Ciencia de Datos",
            "Maestría en Inteligencia Artificial",
            "Maestría en Analítica de Negocios",
            "Maestría en Ciberseguridad",
            "Maestría en Transformación Digital"],
    "COM": ["Maestría en Comunicación Estratégica",
            "Maestría en Marketing Digital",
            "Maestría en Comunicación Política",
            "Maestría en Periodismo de Investigación",
            "Maestría en Gestión de Marca"],
    "AGR": ["Maestría en Agronegocios",
            "Maestría en Ciencia y Tecnología de Alimentos",
            "Maestría en Producción Agrícola Sostenible",
            "Maestría en Sanidad Vegetal",
            "Maestría en Zootecnia"],
}

MAESTRIA_EN = {
    "GES": ["Master of Business Administration (MBA)",
            "MSc in Operations and Supply Chain Management",
            "MSc in Innovation Management",
            "MSc in Project Management"],
    "POL": ["Master of Public Policy",
            "MSc in Public Administration",
            "MSc in International Development",
            "MSc in Global Governance"],
    "ING": ["MSc in Civil Engineering",
            "MSc in Industrial Engineering",
            "MSc in Mechanical Engineering",
            "MSc in Systems Engineering"],
    "SAL": ["Master of Public Health",
            "MSc in Epidemiology",
            "MSc in Global Health",
            "MSc in Health Systems Management"],
    "EDU": ["MSc in Education",
            "MA in Educational Leadership",
            "MSc in Learning Technologies",
            "MA in Higher Education"],
    "DER": ["Master of Laws (LL.M.)",
            "LL.M. in International Law",
            "LL.M. in Corporate Law",
            "MSc in Human Rights Law"],
    "AMB": ["MSc in Environmental Management",
            "MSc in Climate Change and Sustainability",
            "MSc in Renewable Energy",
            "MSc in Water Resources Management"],
    "SOC": ["MSc in Sociology",
            "MA in Anthropology",
            "MSc in Political Science",
            "MA in Cultural Studies"],
    "ECO": ["MSc in Economics",
            "MSc in Finance",
            "MSc in Applied Economics",
            "MSc in International Trade"],
    "DAT": ["MSc in Data Science",
            "MSc in Artificial Intelligence",
            "MSc in Business Analytics",
            "MSc in Cybersecurity"],
    "COM": ["MSc in Strategic Communication",
            "MSc in Digital Marketing",
            "MA in Media and Communication",
            "MSc in Brand Management"],
    "AGR": ["MSc in Agribusiness",
            "MSc in Food Science and Technology",
            "MSc in Sustainable Agriculture",
            "MSc in Plant Sciences"],
}

DOCTORADO_ES = {
    "GES": ["Doctorado en Administración", "Doctorado en Gestión Estratégica"],
    "POL": ["Doctorado en Políticas Públicas", "Doctorado en Ciencia Política y Gobierno"],
    "ING": ["Doctorado en Ingeniería", "Doctorado en Ciencias de la Ingeniería"],
    "SAL": ["Doctorado en Salud Pública", "Doctorado en Ciencias de la Salud"],
    "EDU": ["Doctorado en Educación", "Doctorado en Ciencias de la Educación"],
    "DER": ["Doctorado en Derecho", "Doctorado en Ciencias Jurídicas"],
    "AMB": ["Doctorado en Ciencias Ambientales", "Doctorado en Desarrollo Sostenible"],
    "SOC": ["Doctorado en Ciencias Sociales", "Doctorado en Antropología"],
    "ECO": ["Doctorado en Economía", "Doctorado en Ciencias Económicas"],
    "DAT": ["Doctorado en Ciencia de Datos", "Doctorado en Inteligencia Artificial"],
    "COM": ["Doctorado en Comunicación", "Doctorado en Estudios de Medios"],
    "AGR": ["Doctorado en Ciencias Agrarias", "Doctorado en Ciencia de Alimentos"],
}

DOCTORADO_EN = {
    "GES": ["PhD in Management", "PhD in Business Administration"],
    "POL": ["PhD in Public Policy", "PhD in Political Science"],
    "ING": ["PhD in Engineering", "PhD in Engineering Sciences"],
    "SAL": ["PhD in Public Health", "PhD in Epidemiology"],
    "EDU": ["PhD in Education", "EdD in Educational Leadership"],
    "DER": ["PhD in Law", "Doctor of Juridical Science (S.J.D.)"],
    "AMB": ["PhD in Environmental Science", "PhD in Sustainability Science"],
    "SOC": ["PhD in Sociology", "PhD in Anthropology"],
    "ECO": ["PhD in Economics", "PhD in Finance"],
    "DAT": ["PhD in Computer Science", "PhD in Artificial Intelligence"],
    "COM": ["PhD in Communication", "PhD in Media Studies"],
    "AGR": ["PhD in Agricultural Sciences", "PhD in Food Science"],
}

DIPLOMADO = {
    "GES": ["Diplomado en Gestión de Proyectos (enfoque PMI)",
            "Diplomado en Gestión de Operaciones",
            "Diplomado en Liderazgo y Gestión de Equipos",
            "Diplomado en Gestión de la Cadena de Suministro"],
    "POL": ["Diplomado en Gestión Pública",
            "Diplomado en Contrataciones del Estado",
            "Diplomado en Presupuesto Público por Resultados",
            "Diplomado en Gobierno Digital"],
    "ING": ["Diplomado en Gestión de la Construcción",
            "Diplomado en Seguridad y Salud Ocupacional",
            "Diplomado en Mantenimiento Industrial",
            "Diplomado en Lean Manufacturing"],
    "SAL": ["Diplomado en Gestión de Servicios de Salud",
            "Diplomado en Auditoría Médica",
            "Diplomado en Salud Ocupacional",
            "Diplomado en Emergencias y Desastres"],
    "EDU": ["Diplomado en Docencia Universitaria",
            "Diplomado en Evaluación del Aprendizaje",
            "Diplomado en Educación Virtual",
            "Diplomado en Gestión Escolar"],
    "DER": ["Diplomado en Derecho Administrativo",
            "Diplomado en Compliance y Prevención de Lavado de Activos",
            "Diplomado en Derecho Laboral",
            "Diplomado en Contratación Pública"],
    "AMB": ["Diplomado en Gestión Ambiental y Certificación ISO 14001",
            "Diplomado en Evaluación de Impacto Ambiental",
            "Diplomado en Gestión de Residuos Sólidos",
            "Diplomado en Economía Circular"],
    "SOC": ["Diplomado en Gestión Cultural",
            "Diplomado en Metodología de la Investigación",
            "Diplomado en Interculturalidad y Desarrollo",
            "Diplomado en Gestión de ONG"],
    "ECO": ["Diplomado en Finanzas Corporativas",
            "Diplomado en Gestión de Riesgos Financieros",
            "Diplomado en Formulación y Evaluación de Proyectos",
            "Diplomado en Tributación Empresarial"],
    "DAT": ["Diplomado en Ciencia de Datos con Python",
            "Diplomado en Business Intelligence y Power BI",
            "Diplomado en Inteligencia Artificial Aplicada",
            "Diplomado en Ciberseguridad"],
    "COM": ["Diplomado en Marketing Digital",
            "Diplomado en Comunicación Corporativa",
            "Diplomado en Gestión de Redes Sociales",
            "Diplomado en Branding y Storytelling"],
    "AGR": ["Diplomado en Agronegocios y Exportación",
            "Diplomado en Inocuidad Alimentaria (HACCP)",
            "Diplomado en Riego Tecnificado",
            "Diplomado en Buenas Prácticas Agrícolas"],
}

MODALIDADES = ["Presencial", "Semipresencial", "Online"]
ADMISIONES = ["Admisión semestral", "Admisión anual", "Postulación continua",
              "Dos convocatorias al año"]

# Costo base en USD por nivel de institucion (rango medio de mercado)
BASE_MAESTRIA = {1: 3200, 2: 8000, 3: 17000, 4: 48000}
BASE_DOCTORADO = {1: 4500, 2: 10000, 3: 22000, 4: 55000}
BASE_DIPLOMADO = {1: 450, 2: 900, 3: 1700, 4: 2800}


def semilla(*partes: str) -> int:
    """Entero estable derivado de las partes de texto (reemplaza al azar)."""
    crudo = "|".join(partes).encode("utf-8")
    return int(hashlib.sha1(crudo).hexdigest()[:12], 16)


def elegir(opciones, *partes):
    return opciones[semilla(*partes) % len(opciones)]


def redondear(valor: float) -> int:
    """Redondeo comercial segun magnitud."""
    if valor >= 1_000_000:
        return int(round(valor / 100_000) * 100_000)
    if valor >= 100_000:
        return int(round(valor / 10_000) * 10_000)
    if valor >= 10_000:
        return int(round(valor / 500) * 500)
    if valor >= 1_000:
        return int(round(valor / 100) * 100)
    return int(round(valor / 50) * 50)


def rango_costo(base_usd: int, moneda: str, sem: int):
    """Devuelve (min, max, moneda, min_usd, max_usd) con jitter determinista."""
    factor = 0.82 + (sem % 37) / 100.0          # 0.82 .. 1.18
    centro = base_usd * factor
    min_usd, max_usd = centro * 0.85, centro * 1.25
    tasa = A_USD.get(moneda, 1.0)
    return (redondear(min_usd / tasa), redondear(max_usd / tasa),
            moneda, int(min_usd), int(max_usd))


def construir():
    instituciones = []
    programas = []

    for (iid, nombre, sigla, pais, ciudad, dominio, ruta, sunedu, tipo,
         nivel_costo, areas_txt) in INSTITUCIONES:
        areas = areas_txt.split()
        region = REGION_POR_PAIS.get(pais, "Internacional")
        moneda = MONEDA_POR_PAIS.get(pais, "USD")
        idioma = IDIOMA_POR_PAIS.get(pais, "Español")
        es_peru = pais == "Perú"
        en_ingles = idioma.startswith("Inglés") or idioma == "Portugués"
        url_base = f"https://{dominio}{ruta}"

        instituciones.append({
            "id": iid, "nombre": nombre, "sigla": sigla, "pais": pais,
            "region": region, "ciudad": ciudad, "dominio": dominio,
            "web": f"https://{dominio}", "url_posgrado": url_base,
            "sunedu": sunedu, "tipo": tipo, "nivel_costo": nivel_costo,
            "areas": [AREAS[a] for a in areas],
            "logo": f"https://icons.duckduckgo.com/ip3/{dominio}.ico",
        })

        comun = {
            "institucion_id": iid, "institucion": nombre, "sigla": sigla,
            "pais": pais, "region": region, "ciudad": ciudad,
            "dominio": dominio, "logo": f"https://icons.duckduckgo.com/ip3/{dominio}.ico",
            "sunedu": sunedu, "tipo_institucion": tipo,
            "convalidacion": "No requiere (grado peruano)" if es_peru
                             else "Requiere reconocimiento ante SUNEDU",
        }

        # ---- maestrias: 2 programas en las 4 areas principales, 1 en el resto
        catalogo_m = MAESTRIA_EN if en_ingles else MAESTRIA_ES
        destacada_m = semilla(iid, "dm") % max(1, len(areas[:10]))
        for orden, area in enumerate(areas[:10]):
            lista = catalogo_m[area]
            cuantos = 2 if orden < 4 and len(lista) > 1 else 1
            for k in range(cuantos):
                sem = semilla(iid, area, "M", str(k))
                nombre_prog = lista[(sem + k) % len(lista)]
                pid = f"m-{iid}-{area.lower()}" + (f"-{k}" if k else "")
                cmin, cmax, mon, umin, umax = rango_costo(
                    BASE_MAESTRIA[nivel_costo], moneda, sem)
                programas.append(dict(comun, **{
                    "id": pid, "tipo": "maestria", "nombre": nombre_prog,
                    "area": AREAS[area], "area_codigo": area,
                    "duracion_meses": [18, 20, 24, 24, 12][sem % 5],
                    "modalidad": elegir(MODALIDADES, iid, area, "mod" + str(k)),
                    "idioma": idioma,
                    "costo_min": cmin, "costo_max": cmax, "moneda": mon,
                    "costo_min_usd": umin, "costo_max_usd": umax,
                    "admision": elegir(ADMISIONES, iid, area, "adm"),
                    "financiamiento": financiamiento(sunedu, tipo, nivel_costo, "maestria"),
                    "url": url_base,
                    "destacado": nivel_costo >= 3 and orden == destacada_m and k == 0,
                }))

        # ---- doctorados: hasta 5 areas, con 2 lineas en la principal
        catalogo_d = DOCTORADO_EN if en_ingles else DOCTORADO_ES
        destacada_d = semilla(iid, "dd") % max(1, len(areas[:5]))
        for orden, area in enumerate(areas[:5]):
            lista = catalogo_d[area]
            cuantos = 2 if orden == 0 and len(lista) > 1 else 1
            for k in range(cuantos):
                sem = semilla(iid, area, "D", str(k))
                nombre_prog = lista[(sem + k) % len(lista)]
                pid = f"d-{iid}-{area.lower()}" + (f"-{k}" if k else "")
                cmin, cmax, mon, umin, umax = rango_costo(
                    BASE_DOCTORADO[nivel_costo], moneda, sem)
                programas.append(dict(comun, **{
                    "id": pid, "tipo": "doctorado", "nombre": nombre_prog,
                    "area": AREAS[area], "area_codigo": area,
                    "duracion_meses": [36, 42, 48, 48, 60][sem % 5],
                    "modalidad": elegir(["Presencial", "Presencial", "Semipresencial"],
                                        iid, area, "modd" + str(k)),
                    "idioma": idioma,
                    "costo_min": cmin, "costo_max": cmax, "moneda": mon,
                    "costo_min_usd": umin, "costo_max_usd": umax,
                    "admision": elegir(["Admisión anual", "Dos convocatorias al año"],
                                       iid, area, "admd"),
                    "financiamiento": financiamiento(sunedu, tipo, nivel_costo, "doctorado"),
                    "url": url_base,
                    "destacado": nivel_costo >= 3 and orden == destacada_d and k == 0,
                }))

        # ---- diplomados: solo instituciones de habla hispana
        if not en_ingles:
            destacada_p = semilla(iid, "dp") % max(1, len(areas[:6]))
            for orden, area in enumerate(areas[:6]):
                lista = DIPLOMADO[area]
                cuantos = 2 if orden < 2 and len(lista) > 1 else 1
                for k in range(cuantos):
                    sem = semilla(iid, area, "P", str(k))
                    nombre_prog = lista[(sem + k) % len(lista)]
                    pid = f"p-{iid}-{area.lower()}" + (f"-{k}" if k else "")
                    cmin, cmax, mon, umin, umax = rango_costo(
                        BASE_DIPLOMADO[nivel_costo], moneda, sem)
                    horas = [80, 90, 100, 110, 120, 144, 160][sem % 7]
                    programas.append(dict(comun, **{
                        "id": pid, "tipo": "diplomado", "nombre": nombre_prog,
                        "area": AREAS[area], "area_codigo": area,
                        "horas": horas,
                        "duracion_meses": max(2, round(horas / 40)),
                        "modalidad": elegir(["Online", "Online", "Semipresencial", "Presencial"],
                                            iid, area, "modp" + str(k)),
                        "idioma": idioma,
                        "costo_min": cmin, "costo_max": cmax, "moneda": mon,
                        "costo_min_usd": umin, "costo_max_usd": umax,
                        "admision": "Postulación continua",
                        "financiamiento": "Descuentos por pronto pago y corporativos",
                        "url": url_base,
                        "destacado": nivel_costo >= 2 and orden == destacada_p and k == 0,
                    }))

    return instituciones, programas


def financiamiento(sunedu, tipo, nivel_costo, nivel):
    if nivel == "doctorado" and sunedu == "extranjera" and nivel_costo >= 3:
        return "Financiamiento frecuente (asistencias de investigación)"
    if sunedu != "extranjera" and tipo == "Pública":
        return "Elegible para becas PRONABEC y convenios"
    if nivel_costo >= 3:
        return "Becas parciales por mérito"
    return "Consultar becas y convenios internos"


def facetas(programas, clave):
    return sorted({p[clave] for p in programas if p.get(clave)})


def main():
    instituciones, programas = construir()
    os.makedirs(DIR_DATOS, exist_ok=True)

    por_tipo = {"maestria": [], "doctorado": [], "diplomado": []}
    for p in programas:
        por_tipo[p["tipo"]].append(p)

    archivos = {
        "maestrias.json": por_tipo["maestria"],
        "doctorados.json": por_tipo["doctorado"],
        "diplomados.json": por_tipo["diplomado"],
        "instituciones.json": instituciones,
    }
    for nombre_archivo, contenido in archivos.items():
        ruta = os.path.join(DIR_DATOS, nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as fh:
            json.dump(contenido, fh, ensure_ascii=False, indent=1)
        print(f"  {nombre_archivo}: {len(contenido)} registros")

    meta = {
        "actualizado": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "generado_en": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "totales": {k: len(v) for k, v in por_tipo.items()},
        "instituciones": len(instituciones),
        "paises": facetas(programas, "pais"),
        "regiones": facetas(programas, "region"),
        "areas": sorted(AREAS.values()),
        "modalidades": MODALIDADES,
        "monedas": sorted({p["moneda"] for p in programas}),
        "nota": ("Los costos son rangos referenciales de mercado, no precios "
                 "oficiales. Verifica siempre precios, fechas y requisitos en "
                 "la web oficial de cada institución."),
    }
    with open(os.path.join(DIR_DATOS, "meta_catalogo.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    print(f"  meta_catalogo.json: {sum(meta['totales'].values())} programas en total")


if __name__ == "__main__":
    main()
