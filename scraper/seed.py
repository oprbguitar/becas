# -*- coding: utf-8 -*-
"""Catalogo semilla de becas.

Este modulo es la unica fuente de verdad del catalogo base. El scraper
(scraper/scrape.py) toma cada entrada, visita `url_requisitos` y enriquece
la ficha con los requisitos y las fechas publicadas en el sitio oficial.

Las fechas del semillero son REFERENCIALES (convocatorias anuales); el
scraper las actualiza y la UI siempre enlaza a la convocatoria oficial.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "becas.json"

# Coordenadas (lat, lng) de la ciudad/pais destino para el filtro por distancia.
CIUDADES = {
    "Lima": (-12.0464, -77.0428), "Arequipa": (-16.409, -71.5375),
    "Cusco": (-13.5319, -71.9675), "Trujillo": (-8.109, -79.0215),
    "Bogota": (4.711, -74.0721), "Santiago": (-33.4489, -70.6693),
    "Buenos Aires": (-34.6037, -58.3816), "Sao Paulo": (-23.5505, -46.6333),
    "Ciudad de Mexico": (19.4326, -99.1332), "Monterrey": (25.6866, -100.3161),
    "Montevideo": (-34.9011, -56.1645), "Quito": (-0.1807, -78.4678),
    "Washington": (38.9072, -77.0369), "Boston": (42.3601, -71.0589),
    "Nueva York": (40.7128, -74.006), "Stanford": (37.4275, -122.1697),
    "Londres": (51.5074, -0.1278), "Cambridge": (52.2053, 0.1218),
    "Oxford": (51.752, -1.2577), "Edimburgo": (55.9533, -3.1883),
    "Madrid": (40.4168, -3.7038), "Barcelona": (41.3851, 2.1734),
    "Paris": (48.8566, 2.3522), "Berlin": (52.52, 13.405),
    "Bonn": (50.7374, 7.0982), "Munich": (48.1351, 11.582),
    "Bruselas": (50.8503, 4.3517), "Amsterdam": (52.3676, 4.9041),
    "La Haya": (52.0705, 4.3007), "Roma": (41.9028, 12.4964),
    "Milan": (45.4642, 9.19), "Zurich": (47.3769, 8.5417),
    "Berna": (46.948, 7.4474), "Viena": (48.2082, 16.3738),
    "Estocolmo": (59.3293, 18.0686), "Oslo": (59.9139, 10.7522),
    "Copenhague": (55.6761, 12.5683), "Helsinki": (60.1699, 24.9384),
    "Budapest": (47.4979, 19.0402), "Varsovia": (52.2297, 21.0122),
    "Praga": (50.0755, 14.4378), "Lisboa": (38.7223, -9.1393),
    "Ankara": (39.9334, 32.8597), "Estambul": (41.0082, 28.9784),
    "Moscu": (55.7558, 37.6173), "Pekin": (39.9042, 116.4074),
    "Shanghai": (31.2304, 121.4737), "Hong Kong": (22.3193, 114.1694),
    "Tokio": (35.6762, 139.6503), "Seul": (37.5665, 126.978),
    "Taipei": (25.033, 121.5654), "Singapur": (1.3521, 103.8198),
    "Nueva Delhi": (28.6139, 77.209), "Bangkok": (13.7563, 100.5018),
    "Yeda": (22.3095, 39.1077), "Abu Dabi": (24.4539, 54.3773),
    "Doha": (25.2854, 51.531), "Toronto": (43.6532, -79.3832),
    "Ottawa": (45.4215, -75.6972), "Melbourne": (-37.8136, 144.9631),
    "Canberra": (-35.2809, 149.13), "Wellington": (-41.2866, 174.7756),
    "Ciudad del Cabo": (-33.9249, 18.4241), "Nairobi": (-1.2921, 36.8219),
    "Global": (0.0, 0.0),
}


def slug(texto: str) -> str:
    txt = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", txt.lower()).strip("-")


BECAS: list[dict] = []


def b(nombre, organizacion, region, pais, ciudad, niveles, areas, cobertura,
      incluye, edad_min, edad_max, meses, apertura, cierre, costo_postulacion,
      idiomas, url, url_requisitos, descripcion, requisitos, modalidad="Presencial",
      destacada=False):
    """Registra una beca normalizada en el catalogo."""
    lat, lng = CIUDADES.get(ciudad, CIUDADES["Global"])
    BECAS.append({
        "id": slug(f"{nombre}-{organizacion}"),
        "nombre": nombre,
        "organizacion": organizacion,
        "region": region,
        "pais": pais,
        "ciudad": ciudad,
        "lat": lat,
        "lng": lng,
        "niveles": niveles,
        "areas": areas,
        "cobertura": cobertura,          # Completa | Parcial | Matricula | Estipendio
        "incluye": incluye,              # dict de booleanos
        "edad_min": edad_min,
        "edad_max": edad_max,
        "duracion_meses": meses,
        "fecha_apertura": apertura,
        "fecha_cierre": cierre,
        "costo_postulacion_usd": costo_postulacion,
        "idiomas": idiomas,
        "modalidad": modalidad,
        "url": url,
        "url_requisitos": url_requisitos,
        "descripcion": descripcion,
        "requisitos": requisitos,
        "destacada": destacada,
        "fuente": "semilla",
    })


def inc(matricula=False, manutencion=False, hospedaje=False, pasajes=False,
        seguro=False, idioma=False, laptop=False):
    return {
        "matricula": matricula, "manutencion": manutencion, "hospedaje": hospedaje,
        "pasajes": pasajes, "seguro": seguro, "curso_idioma": idioma, "equipos": laptop,
    }


# ---------------------------------------------------------------- Peru
b("Beca 18", "PRONABEC", "Perú", "Perú", "Lima", ["Pregrado"],
  ["Ingeniería", "Salud", "Ciencias", "Tecnología", "Negocios", "Educación"],
  "Completa", inc(True, True, True, True, True, False, True), 16, 22, 60,
  "2026-01-12", "2026-03-20", 0, ["Español"],
  "Https://www.gob.pe/pronabec", "Https://www.gob.pe/institución/pronabec/campa%C3%B1as/1246-beca-18",
  "Beca integral del Estado peruano para jóvenes de alto rendimiento en situación de pobreza que cursarán una carrera universitaria o técnica en universidades e institutos elegibles del país.",
  ["Nacionalidad peruana", "Alto rendimiento académico en secundaria",
   "Condición socioeconómica de pobreza o pobreza extrema (SISFOH)",
   "Haber culminado la secundaria en los últimos años según modalidad",
   "No contar con estudios superiores culminados"], destacada=True)

b("Beca Permanencia", "PRONABEC", "Perú", "Perú", "Lima", ["Pregrado"],
  ["Todas"], "Parcial", inc(True, True, False, False, False), 16, 30, 24,
  "2026-04-01", "2026-05-30", 0, ["Español"],
  "Https://www.gob.pe/pronabec", "Https://www.gob.pe/institución/pronabec/campa%C3%B1as/1247-beca-permanencia",
  "Subvención para estudiantes de universidades públicas en riesgo de abandonar sus estudios por motivos económicos.",
  ["Estudiar en universidad pública licenciada", "Estar entre el 3er y 8vo ciclo",
   "Promedio ponderado aprobatorio", "Clasificación socioeconómica de pobreza"])

b("Beca Generación del Bicentenario", "PRONABEC", "Perú", "Global", "Lima",
  ["Maestría", "Doctorado"],
  ["Ingeniería", "Ciencias", "Tecnología", "Salud", "Medio Ambiente", "Educación"],
  "Completa", inc(True, True, True, True, True), 22, 40, 24,
  "2026-02-15", "2026-04-25", 0, ["Español", "Inglés"],
  "Https://www.gob.pe/pronabec", "Https://www.gob.pe/institución/pronabec/campa%C3%B1as/1248-beca-generacion-del-bicentenario",
  "Financia estudios de posgrado en las mejores universidades del mundo para profesionales peruanos con compromiso de retorno al país.",
  ["Nacionalidad peruana", "Carta de admisión a universidad del top mundial",
   "Grado de bachiller", "Compromiso de retorno al Perú por 2 años"], destacada=True)

b("Becas de Posgrado PROCIENCIA", "CONCYTEC - PROCIENCIA", "Perú", "Perú", "Lima",
  ["Maestría", "Doctorado"], ["Ciencias", "Ingeniería", "Tecnología", "Salud"],
  "Completa", inc(True, True, False, False, True), 22, 45, 36,
  "2026-03-01", "2026-06-15", 0, ["Español"],
  "Https://prociencia.gob.pe/", "Https://prociencia.gob.pe/concursos/",
  "Financiamiento estatal para maestrías y doctorados en ciencia, tecnologia e innovación dictados en universidades peruanas acreditadas.",
  ["Investigador registrado en el CTI Vitae", "Admisión a programa acreditado",
   "Plan de tesis alineado a prioridades nacionales"])

b("Beca Hijos de Docentes", "PRONABEC", "Perú", "Perú", "Lima", ["Pregrado"],
  ["Todas"], "Completa", inc(True, True, True, False, True), 16, 25, 60,
  "2026-03-10", "2026-05-10", 0, ["Español"],
  "Https://www.gob.pe/pronabec", "Https://www.gob.pe/institución/pronabec/campa%C3%B1as",
  "Beca dirigida a hijos de docentes de instituciones educativas públicas con alto rendimiento académico.",
  ["Ser hijo de docente nombrado o contratado del sector público",
   "Alto rendimiento académico", "Ingresar a universidad o instituto elegible"])

# ---------------------------------------------------------- Latinoamerica
b("Becas OEA - Programa de Alianzas", "Organización de Estados Americanos",
  "Latinoamérica", "Varios", "Washington", ["Maestría", "Doctorado", "Curso corto"],
  ["Todas"], "Parcial", inc(True, False, False, False, False), 18, 60, 24,
  "2026-01-20", "2026-05-31", 0, ["Español", "Inglés", "Portugués"],
  "Https://www.oas.org/es/becas/", "Https://www.oas.org/es/becas/PAEC/default.asp",
  "Alianzas de la OEA con universidades de las Américas y Europa que otorgan descuentos de 30% a 100% en matrícula de posgrado.",
  ["Ser ciudadano o residente de un Estado miembro de la OEA",
   "Admisión al programa académico elegido", "Formulario OEA en línea"])

b("Becas Fundación Carolina", "Fundación Carolina", "Europa", "España", "Madrid",
  ["Maestría", "Doctorado", "Posdoctorado"], ["Todas"], "Completa",
  inc(True, True, False, True, True), 21, 45, 12,
  "2026-01-10", "2026-04-03", 0, ["Español"],
  "Https://www.fundacioncarolina.es/", "Https://www.fundacioncarolina.es/formación/",
  "Programa insignia de cooperación entre España y America Latina: más de 700 becas anuales de posgrado, doctorado y estancias cortas.",
  ["Nacionalidad de un país de America Latina miembro de la Comunidad Iberoamericana",
   "Título universitario de grado", "Preinscripcion en el programa académico",
   "Curriculum y carta de motivación"], destacada=True)

b("Becas AUIP de Movilidad Académica", "Asociación Universitaria Iberoamericana de Posgrado",
  "Europa", "España", "Madrid", ["Maestría", "Doctorado", "Intercambio"], ["Todas"],
  "Parcial", inc(False, False, False, True, False), 21, 60, 6,
  "2026-02-01", "2026-09-30", 0, ["Español"],
  "Https://www.auip.org/", "Https://www.auip.org/es/convocatorias-becas",
  "Ayudas de movilidad entre universidades iberoamericanas asociadas a la AUIP, con varias convocatorias al año.",
  ["Vinculo con universidad asociada a la AUIP", "Carta de aceptacion de la universidad de destino",
   "Plan de trabajo académico"])

b("Becas Santander", "Banco Santander - Santander Open Academy", "Global", "Varios",
  "Madrid", ["Pregrado", "Maestría", "Curso corto"],
  ["Tecnología", "Negocios", "Ingeniería", "Todas"], "Parcial",
  inc(True, False, False, False, False), 18, 65, 6,
  "2026-01-05", "2026-10-31", 0, ["Español", "Inglés", "Portugués"],
  "Https://www.santanderopenacademy.com/es/index.html",
  "Https://www.santanderopenacademy.com/es/programs.html",
  "Miles de becas de corta duración en habilidades digitales, idiomas, emprendimiento y movilidad internacional, con convocatorias abiertas todo el año.",
  ["Registro en la plataforma Santander Open Academy", "Cumplir los requisitos de cada programa",
   "No es necesario ser cliente del banco"], modalidad="Mixta")

b("Plataforma de Movilidad Estudiantil Alianza del Pacífico", "Alianza del Pacífico",
  "Latinoamérica", "Chile, Colombia, México, Perú", "Santiago",
  ["Pregrado", "Doctorado", "Intercambio"], ["Todas"], "Completa",
  inc(True, True, False, True, True), 18, 40, 5,
  "2026-03-01", "2026-06-15", 0, ["Español"],
  "Https://alianzapacifico.net/becas/", "Https://alianzapacifico.net/becas/",
  "Intercambio académico semestral entre los cuatro países de la Alianza del Pacífico, con dos convocatorias anuales.",
  ["Ser nacional de Chile, Colombia, México o Perú",
   "Haber cursado al menos el 50% del pregrado", "Promedio mínimo equivalente a 80/100"])

b("Becas de Posgrado CONAHCYT", "CONAHCYT México", "Latinoamérica", "México",
  "Ciudad de México", ["Maestría", "Doctorado"], ["Ciencias", "Ingeniería", "Salud", "Ciencias Sociales"],
  "Completa", inc(True, True, False, False, True), 21, 45, 24,
  "2026-02-01", "2026-05-30", 0, ["Español"],
  "Https://conahcyt.mx/", "Https://conahcyt.mx/becas_posgrados/becas-nacionales/",
  "Becas nacionales y al extranjero del sistema mexicano de ciencia para programas del Sistema Nacional de Posgrados.",
  ["Admisión a un programa del Sistema Nacional de Posgrados",
   "Dedicación exclusiva al programa", "Promedio mínimo de 8.0"])

b("Becas ANID Chile", "Agencia Nacional de investigación y Desarrollo", "Latinoamérica",
  "Chile", "Santiago", ["Maestría", "Doctorado"], ["Ciencias", "Ingeniería", "Ciencias Sociales", "Salud"],
  "Completa", inc(True, True, False, False, True), 21, 45, 48,
  "2026-04-01", "2026-07-15", 0, ["Español"],
  "Https://www.anid.cl/", "Https://www.anid.cl/concursos/",
  "Becas de magister y doctorado en Chile y en el extranjero financiadas por el Estado chileno, abiertas también a extranjeros en algunas líneas.",
  ["Grado académico previo", "Aceptacion en programa acreditado",
   "Curriculum y cartas de recomendación"])

b("Becas Fundación Botín", "Fundación Botín", "Europa", "España", "Madrid",
  ["Curso corto", "Maestría"], ["Ciencias Sociales", "Negocios", "Derecho"],
  "Completa", inc(True, True, True, True, True), 21, 35, 3,
  "2026-01-15", "2026-03-15", 0, ["Español"],
  "Https://fundacionbotin.org/", "Https://fundacionbotin.org/programas/talento-solidario/",
  "Programa de fortalecimiento para servidores públicos y lideres latinoamericanos, con formación en España y America Latina.",
  ["Ser funcionario público o profesional del sector público de America Latina",
   "Menos de 35 años", "Experiencia demostrable en gestión pública"])


# ---------------------------------------------------------------- Europa
b("Chevening Scholarships", "Gobierno del Reino Unido", "Europa", "Reino Unido",
  "Londres", ["Maestría"], ["Todas"], "Completa",
  inc(True, True, False, True, False), 21, 60, 12,
  "2026-08-05", "2026-11-04", 0, ["Inglés"],
  "Https://www.chevening.org/", "Https://www.chevening.org/scholarships/who-can-apply/eligibility/",
  "Beca del gobierno británico para lideres emergentes: cubre un master de un año en cualquier universidad del Reino Unido.",
  ["Ciudadania de un país elegible para Chevening", "Título universitario de grado",
   "Mínimo 2 años (2800 horas) de experiencia laboral",
   "Tres ofertas de admisión en universidades del Reino Unido",
   "Compromiso de retornar al país de origen por 2 años"], destacada=True)

b("Erasmus Mundus Joint Masters", "Comisión Europea", "Europa", "Union Europea",
  "Bruselas", ["Maestría"], ["Todas"], "Completa",
  inc(True, True, False, True, True), 20, 60, 24,
  "2025-10-01", "2026-01-15", 0, ["Inglés"],
  "Https://www.eacea.ec.europa.eu/scholarships/erasmus-mundus-catalogue_en",
  "Https://erasmus-plus.ec.europa.eu/opportunities/opportunities-for-individuals/students/erasmus-mundus-joint-masters-scholarships",
  "Maestrías conjuntas impartidas por consorcios de universidades europeas: se estudia en 2 o 3 países con beca integral.",
  ["Título de grado (o estar por obtenerlo)", "Dominio del inglés acreditado",
   "Postular directamente al consorcio del master elegido",
   "Se puede postular a un máximo de 3 programas por convocatoria"], destacada=True)

b("Becas DAAD para Posgrado", "Servicio Alemán de Intercambio académico", "Europa",
  "Alemania", "Bonn", ["Maestría", "Doctorado", "Posdoctorado"], ["Todas"],
  "Completa", inc(True, True, False, True, True, True), 21, 45, 24,
  "2026-06-01", "2026-10-15", 0, ["Inglés", "Alemán"],
  "Https://www.daad.de/en/", "Https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/",
  "El mayor programa de becas de Alemania: estipendio mensual, seguro, pasajes y curso de alemán para posgrado e investigación.",
  ["Título de grado obtenido hace menos de 6 años",
   "Al menos 2 años de experiencia profesional para programas de desarrollo",
   "Certificado de idioma según el programa", "Carta de motivación y plan de estudios"], destacada=True)

b("Beca Eiffel", "Ministerio de Europa y Asuntos Exteriores de Francia", "Europa",
  "Francia", "Paris", ["Maestría", "Doctorado"],
  ["Ingeniería", "Ciencias", "Derecho", "Negocios", "Ciencias Sociales"], "Completa",
  inc(False, True, False, True, True), 18, 30, 24,
  "2025-10-01", "2026-01-09", 0, ["Francés", "Inglés"],
  "Https://www.campusfrance.org/es/eiffel-programa-becas-excelencia",
  "Https://www.campusfrance.org/es/eiffel-programa-becas-excelencia",
  "Beca de excelencia del Estado francés. La postulación la realiza la institución francesa, no el estudiante.",
  ["Nacionalidad no francesa", "Máximo 25 años para master y 30 para doctorado",
   "Ser postulado por un establecimiento de educación superior francés",
   "Expediente académico sobresaliente"])

b("Swiss Government Excellence Scholarships", "Confederación Suiza", "Europa", "Suiza",
  "Berna", ["Maestría", "Doctorado", "Posdoctorado"], ["Todas"], "Completa",
  inc(True, True, False, True, True), 21, 35, 36,
  "2026-08-01", "2026-11-30", 0, ["Inglés", "Alemán", "Francés"],
  "Https://www.sbfi.admin.ch/sbfi/en/home/education/scholarships-and-grants/swiss-government-excellence-scholarships.html",
  "Https://www.sbfi.admin.ch/sbfi/en/home/education/scholarships-and-grants/swiss-government-excellence-scholarships.html",
  "Becas de investigación y doctorado en universidades públicas suizas, con estipendio mensual y seguro de salud.",
  ["Carta de aceptacion de un profesor supervisor en Suiza",
   "Título de maestría para doctorado", "Menos de 35 años",
   "Postular a traves de la embajada suiza del país de origen"])

b("Stipendium Hungaricum", "Gobierno de Hungría", "Europa", "Hungría", "Budapest",
  ["Pregrado", "Maestría", "Doctorado"], ["Todas"], "Completa",
  inc(True, True, True, False, True), 18, 45, 48,
  "2025-11-15", "2026-01-15", 0, ["Inglés", "Hungaro"],
  "Https://stipendiumhungaricum.hu/", "Https://stipendiumhungaricum.hu/about/",
  "Programa estatal hungaro que cubre matrícula, alojamiento y estipendio mensual para estudiantes de más de 90 países.",
  ["Nacionalidad de un país con acuerdo bilateral vigente",
   "Certificado de idioma según el programa", "Postulación doble: portal Tempus y entidad nacional"])

b("Beca MAEC-AECID", "Agencia Espanola de cooperación Internacional", "Europa",
  "España", "Madrid", ["Maestría", "Doctorado", "Curso corto"],
  ["Humanidades", "Arte y Diseño", "Ciencias Sociales", "Todas"], "Parcial",
  inc(True, True, False, False, True), 18, 40, 12,
  "2025-12-01", "2026-02-28", 0, ["Español"],
  "Https://www.aecid.gob.es/es/becas-y-lectorados",
  "Https://www.aecid.gob.es/es/becas-y-lectorados",
  "Becas del Estado español para estudios de posgrado, arte, música y cooperación en España.",
  ["Título universitario", "Nacionalidad de país elegible según la línea",
   "Certificado de español si corresponde"])

b("Gates Cambridge Scholarship", "Universidad de Cambridge", "Europa", "Reino Unido",
  "Cambridge", ["Maestría", "Doctorado"], ["Todas"], "Completa",
  inc(True, True, False, True, True), 20, 45, 48,
  "2025-09-10", "2026-01-07", 0, ["Inglés"],
  "Https://www.gatescambridge.org/", "Https://www.gatescambridge.org/apply/eligibility/",
  "Una de las becas más competitivas del mundo: posgrado completo en Cambridge para lideres con vocación de impacto social.",
  ["No tener nacionalidad britanica", "Postular a un posgrado de tiempo completo en Cambridge",
   "Excelencia académica sobresaliente", "Compromiso con la mejora de la vida de otros"], destacada=True)

b("Rhodes Scholarship", "Rhodes Trust - Universidad de Oxford", "Europa",
  "Reino Unido", "Oxford", ["Maestría", "Doctorado"], ["Todas"], "Completa",
  inc(True, True, False, True, True), 18, 28, 24,
  "2026-06-01", "2026-10-01", 0, ["Inglés"],
  "Https://www.rhodeshouse.ox.ac.uk/", "Https://www.rhodeshouse.ox.ac.uk/scholarships/the-rhodes-scholarship/",
  "Beca histórica para posgrado en Oxford, con circunscripciones por país o región.",
  ["Edad entre 18 y 28 años según circunscripción",
   "Grado universitario con excelencia académica",
   "Liderazgo, servicio y caracter demostrados"])

b("Holland Scholarship", "Gobierno de los Países Bajos", "Europa", "Países Bajos",
  "Amsterdam", ["Pregrado", "Maestría"], ["Todas"], "Parcial",
  inc(False, True, False, False, False), 17, 40, 12,
  "2025-10-01", "2026-02-01", 0, ["Inglés"],
  "Https://www.studyinnl.org/finances/holland-scholarship",
  "Https://www.studyinnl.org/finances/holland-scholarship",
  "Aporte único de 5.000 euros para el primer año de estudios en una universidad holandesa participante.",
  ["Nacionalidad de fuera del Espacio económico Europeo",
   "Primera vez estudiando en Países Bajos",
   "Postular en la universidad holandesa participante"])

b("Orange Knowledge Programme / OKP", "Nuffic - Países Bajos", "Europa",
  "Países Bajos", "La Haya", ["Maestría", "Curso corto"],
  ["Agricultura", "Salud", "Medio Ambiente", "Derecho", "Negocios"], "Completa",
  inc(True, True, False, True, True), 22, 45, 12,
  "2026-02-01", "2026-05-15", 0, ["Inglés"],
  "Https://www.nuffic.nl/en/subjects/scholarships",
  "Https://www.nuffic.nl/en/subjects/scholarships",
  "Becas neerlandesas de desarrollo profesional dirigidas a profesionales de países socios.",
  ["Nacionalidad de un país de la lista OKP", "Admisión al curso o master",
   "Carta de respaldo del empleador", "Nivel de inglés acreditado"])

b("Becas del Gobierno de Italia", "Ministero degli Affari Esteri de Italia", "Europa",
  "Italia", "Roma", ["Maestría", "Doctorado", "Curso corto"],
  ["Arte y Diseño", "Humanidades", "Ingeniería", "Ciencias"], "Parcial",
  inc(True, True, False, False, True), 18, 40, 9,
  "2026-04-01", "2026-06-15", 0, ["Italiano", "Inglés"],
  "Https://studyinitaly.esteri.it/", "Https://studyinitaly.esteri.it/en/call-for-procedure",
  "Becas anuales del Estado italiano para master, doctorado, cursos de arte, música y lengua italiana.",
  ["Título previo según nivel", "Certificado de italiano B2 o inglés B2",
   "Postulación en el portal Study in Italy"])

b("Becas del Gobierno de Turquía / Türkiye Bursları", "Gobierno de Turquía", "Europa",
  "Turquía", "Ankara", ["Pregrado", "Maestría", "Doctorado"], ["Todas"], "Completa",
  inc(True, True, True, True, True, True), 17, 45, 48,
  "2026-01-10", "2026-02-20", 0, ["Turco", "Inglés"],
  "Https://turkiyeburslari.gov.tr/", "Https://turkiyeburslari.gov.tr/en/page/prospective-students/requirements",
  "Beca integral turca: matrícula, alojamiento, estipendio, pasajes, seguro y un año de curso de turco.",
  ["Máximo 21 años para pregrado, 30 para maestría y 35 para doctorado",
   "Promedio mínimo de 70% (90% en medicina)",
   "No estar matriculado actualmente en una universidad turca"])

b("Becas del Gobierno de Polonia - NAWA", "Agencia Nacional de Intercambio académico",
  "Europa", "Polonia", "Varsovia", ["Maestría", "Doctorado", "Curso corto"],
  ["Ciencias", "Ingeniería", "Humanidades"], "Completa",
  inc(True, True, False, False, True, True), 18, 40, 24,
  "2026-03-01", "2026-05-30", 0, ["Inglés", "Polaco"],
  "Https://nawa.gov.pl/en/", "Https://nawa.gov.pl/en/students",
  "Programas NAWA de movilidad y posgrado en universidades polacas, incluido el programa Banach para America Latina.",
  ["Nacionalidad elegible según programa", "título previo",
   "Carta de aceptacion de la universidad polaca"])


# ------------------------------------------------------------ China / Asia
b("Chinese Government Scholarship / CSC", "China Scholarship Council", "China",
  "China", "Pekín", ["Pregrado", "Maestría", "Doctorado"], ["Todas"], "Completa",
  inc(True, True, True, False, True, True), 17, 40, 48,
  "2025-12-01", "2026-04-30", 0, ["Chino", "Inglés"],
  "Https://www.campuschina.org/", "Https://www.campuschina.org/scholarships/detail/2edd7ba5d29d4b7d99c88f9bd9bd0e4f.html",
  "Beca insignia del gobierno chino: matrícula, alojamiento en campus, estipendio mensual y seguro médico integral.",
  ["Máximo 25 años para pregrado, 35 para maestría y 40 para doctorado",
   "No tener nacionalidad china", "Certificado HSK o de inglés según el programa",
   "Postular por embajada, universidad china o institución designada"], destacada=True)

b("Confucius Institute Scholarship", "Centro CLEC - Instituto Confucio", "China",
  "China", "Pekín", ["Pregrado", "Maestría", "Curso corto"],
  ["Humanidades", "Educación"], "Completa",
  inc(True, True, True, False, True, True), 16, 35, 12,
  "2026-03-01", "2026-05-20", 0, ["Chino"],
  "Https://cis.chinese.cn/", "Https://cis.chinese.cn/en/",
  "Beca para estudiar lengua y cultura china o formarse como profesor de chino, desde cursos de un semestre hasta maestrías.",
  ["Nivel de HSK según la duración solicitada", "No tener nacionalidad china",
   "Recomendación de un Instituto Confucio o entidad autorizada"])

b("Beijing Government Scholarship", "Municipalidad de Pekín", "China", "China",
  "Pekín", ["Pregrado", "Maestría", "Doctorado"], ["Todas"], "Parcial",
  inc(True, False, False, False, False), 17, 40, 36,
  "2026-02-01", "2026-05-31", 0, ["Chino", "Inglés"],
  "Https://www.beijing.gov.cn/", "Http://www.studyinbeijing.org.cn/",
  "Beca municipal complementaria que cubre total o parcialmente la matrícula en universidades de Pekín.",
  ["Estar admitido en una universidad de Pekín participante",
   "Buen rendimiento académico", "Postular a traves de la universidad"])

b("Shanghai Government Scholarship", "Municipalidad de Shanghai", "China", "China",
  "Shanghai", ["Pregrado", "Maestría", "Doctorado"], ["Todas"], "Parcial",
  inc(True, True, False, False, True), 17, 40, 36,
  "2026-01-15", "2026-05-15", 0, ["Chino", "Inglés"],
  "Https://www.shanghai.gov.cn/", "Http://www.study-shanghai.org/",
  "Programa de becas de la ciudad de Shanghai con modalidades de cobertura total o parcial.",
  ["Admisión en universidad de Shanghai participante", "No tener nacionalidad china",
   "Certificado de idioma según el programa"])

b("Hong Kong PhD Fellowship Scheme", "Research Grants Council de Hong Kong", "Asia",
  "Hong Kong", "Hong Kong", ["Doctorado"], ["Ciencias", "Ingeniería", "Negocios", "Ciencias Sociales"],
  "Completa", inc(True, True, False, True, True), 21, 40, 36,
  "2025-09-01", "2025-12-01", 0, ["Inglés"],
  "Https://cerg1.ugc.edu.hk/hkpfs/", "Https://cerg1.ugc.edu.hk/hkpfs/",
  "Estipendio anual y apoyo a conferencias para doctorados en las universidades públicas de Hong Kong.",
  ["Excelencia académica y capacidad de investigación",
   "Postular en paralelo al programa de doctorado de la universidad",
   "Obtener un número de referencia HKPFS antes de postular"])

b("MEXT - Becas del Gobierno de Japón", "Ministerio de Educación de Japón", "Asia",
  "Japón", "Tokio", ["Pregrado", "Maestría", "Doctorado", "Técnico"], ["Todas"],
  "Completa", inc(True, True, False, True, False, True), 17, 35, 60,
  "2026-04-01", "2026-06-10", 0, ["Japonés", "Inglés"],
  "Https://www.studyinjapan.go.jp/en/", "Https://www.studyinjapan.go.jp/en/planning/scholarship/",
  "Beca del gobierno japonés con estipendio mensual, matrícula completa, pasajes y curso preparatorio de japonés.",
  ["Nacionalidad de país con relaciones diplomaticas con Japón",
   "Limite de edad según modalidad (usualmente menos de 35 años)",
   "Postular por embajada de Japón o por recomendación universitaria",
   "Examen escrito y entrevista"], destacada=True)

b("Global Korea Scholarship / GKS", "NIIED - Gobierno de Corea", "Asia",
  "Corea del Sur", "Seúl", ["Pregrado", "Maestría", "Doctorado"], ["Todas"],
  "Completa", inc(True, True, False, True, True, True), 17, 40, 48,
  "2026-02-01", "2026-03-25", 0, ["Coreano", "Inglés"],
  "Https://www.studyinkorea.go.kr/", "Https://www.studyinkorea.go.kr/en/scholarship/gks_info.do",
  "Beca coreana integral con un año de curso de coreano, matrícula, estipendio mensual, pasajes y seguro.",
  ["Menos de 25 años para pregrado y 40 para posgrado",
   "Promedio académico superior al 80%", "No tener nacionalidad coreana",
   "Buen estado de salud certificado"], destacada=True)

b("Taiwan ICDF Scholarship", "International Cooperation and Development Fund", "Asia",
  "Taiwán", "Taipéi", ["Pregrado", "Maestría", "Doctorado"],
  ["Ingeniería", "Agricultura", "Salud", "Negocios", "Medio Ambiente"], "Completa",
  inc(True, True, True, True, True), 18, 45, 48,
  "2026-01-01", "2026-03-15", 0, ["Inglés", "Chino"],
  "Https://www.icdf.org.tw/", "Https://www.icdf.org.tw/wSite/lp?ctNode=30317&mp=2",
  "Beca taiwanesa para países aliados y socios: matrícula, alojamiento, pasajes de ida y vuelta y estipendio.",
  ["Nacionalidad de un país socio del ICDF", "Título previo según nivel",
   "Inglés acreditado (TOEFL o IELTS)", "Postulación en línea y por embajada"])

b("Singapore International Graduate Award / SINGA", "A*STAR Singapur", "Asia",
  "Singapur", "Singapur", ["Doctorado"], ["Ciencias", "Ingeniería", "Tecnología", "Salud"],
  "Completa", inc(True, True, False, True, False), 21, 40, 48,
  "2026-01-01", "2026-06-01", 0, ["Inglés"],
  "Https://www.a-star.edu.sg/singa", "Https://www.a-star.edu.sg/singa/apply/eligibility",
  "Doctorado en biomedicina, ciencias fisicas e ingenieria en Singapur, con estipendio mensual y pasaje aéreo.",
  ["Título de grado con excelente rendimiento", "Buen dominio del inglés hablado y escrito",
   "Dos cartas de referencia académica"])

b("KAUST Fellowship", "King Abdullah University of Science and Technology", "Asia",
  "Arabia Saudita", "Yeda", ["Maestría", "Doctorado"],
  ["Ciencias", "Ingeniería", "Tecnología", "Medio Ambiente"], "Completa",
  inc(True, True, True, True, True), 20, 40, 48,
  "2025-09-01", "2026-01-31", 0, ["Inglés"],
  "Https://www.kaust.edu.sa/en/study/fellowships",
  "Https://www.kaust.edu.sa/en/study/admissions",
  "Beca integral automatica para todos los admitidos: matrícula, alojamiento en campus, estipendio y seguro médico.",
  ["Admisión al programa de posgrado de KAUST", "Título en ciencias o ingenieria",
   "Inglés acreditado", "Cartas de recomendación"])

b("Beca del Gobierno de India - ICCR", "Indian Council for Cultural Relations", "Asia",
  "India", "Nueva Delhi", ["Pregrado", "Maestría", "Doctorado"],
  ["Humanidades", "Ingeniería", "Ciencias", "Arte y Diseño"], "Completa",
  inc(True, True, True, False, False), 18, 40, 36,
  "2026-02-01", "2026-04-30", 0, ["Inglés", "Hindi"],
  "Https://www.iccr.gov.in/", "Https://a2ascholarships.iccr.gov.in/",
  "Programa indio de becas culturales y académicas con matrícula, alojamiento y estipendio mensual.",
  ["Nacionalidad elegible", "Certificados académicos apostillados",
   "Postulación en el portal A2A Scholarships"])

b("Asian Development Bank - Japan Scholarship Program", "Banco Asiático de Desarrollo",
  "Asia", "Varios", "Tokio", ["Maestría"],
  ["Negocios", "Medio Ambiente", "Ciencias Sociales", "Ingeniería"], "Completa",
  inc(True, True, True, True, True), 22, 35, 24,
  "2026-01-15", "2026-05-31", 0, ["Inglés"],
  "Https://www.adb.org/work-with-us/careers/japan-scholarship-program",
  "Https://www.adb.org/work-with-us/careers/japan-scholarship-program",
  "Maestrías en instituciones académicas de Asia y el Pacifico para profesionales de países miembros en desarrollo.",
  ["Nacionalidad de país miembro en desarrollo del BAD",
   "Al menos 2 años de experiencia laboral", "Menos de 35 años",
   "Admisión en una institución participante"])


# ------------------------------------------- Norteamerica / Oceania / Africa / Global
b("Fulbright Foreign Student Program", "Departamento de Estado de EE. UU.",
  "Norteamérica", "Estados Unidos", "Washington", ["Maestría", "Doctorado"],
  ["Todas"], "Completa", inc(True, True, False, True, True), 21, 45, 24,
  "2026-02-01", "2026-05-30", 0, ["Inglés"],
  "Https://foreign.fulbrightonline.org/", "Https://foreign.fulbrightonline.org/about/foreign-student-program",
  "Programa emblemático de intercambio de EE. UU.: posgrado completo con matrícula, manutención, pasajes y seguro.",
  ["Nacionalidad de país participante", "Título universitario de grado",
   "TOEFL o IELTS según la comisión del país",
   "Postular a traves de la comisión Fulbright o embajada local",
   "Compromiso de retorno al país de origen"], destacada=True)

b("Knight-Hennessy Scholars", "Universidad de Stanford", "Norteamérica",
  "Estados Unidos", "Stanford", ["Maestría", "Doctorado"], ["Todas"], "Completa",
  inc(True, True, False, True, True), 20, 45, 36,
  "2026-06-01", "2026-10-08", 0, ["Inglés"],
  "Https://knight-hennessy.stanford.edu/", "Https://knight-hennessy.stanford.edu/admission/eligibility",
  "Financia hasta tres años de cualquier posgrado en Stanford, con un programa de liderazgo propio.",
  ["Título de grado obtenido en los últimos años según politica vigente",
   "Postular en paralelo a un programa de posgrado de Stanford",
   "Liderazgo civico e independencia de pensamiento"], destacada=True)

b("Vanier Canada Graduate Scholarships", "Gobierno de Canadá", "Norteamérica",
  "Canadá", "Ottawa", ["Doctorado"], ["Ciencias", "Salud", "Ciencias Sociales", "Ingeniería"],
  "Completa", inc(False, True, False, False, False), 21, 45, 36,
  "2026-06-01", "2026-11-01", 0, ["Inglés", "Francés"],
  "Https://vanier.gc.ca/", "Https://vanier.gc.ca/en/nomination_process-processus_de_mise_en_candidature.html",
  "50.000 dólares canadienses por año durante tres años para doctorandos de excelencia en universidades canadienses.",
  ["Ser nominado por una universidad canadiense",
   "Excelencia académica y potencial de investigación",
   "Máximo 3 años de estudios doctorales completados"])

b("Australia Awards Scholarships", "Gobierno de Australia", "Oceanía", "Australia",
  "Canberra", ["Pregrado", "Maestría"], ["Todas"], "Completa",
  inc(True, True, True, True, True, True), 18, 45, 24,
  "2026-02-01", "2026-04-30", 0, ["Inglés"],
  "Https://www.dfat.gov.au/people-to-people/australia-awards",
  "Https://www.dfat.gov.au/people-to-people/australia-awards/australia-awards-scholarships",
  "Beca integral del gobierno australiano para profesionales de países socios, con apoyo académico y de reinserción.",
  ["Nacionalidad de un país participante", "Mínimo 18 años al iniciar",
   "Cumplir requisitos de inglés de la universidad",
   "Compromiso de retornar por al menos 2 años"])

b("Manaaki New Zealand Scholarships", "Gobierno de Nueva Zelanda", "Oceanía",
  "Nueva Zelanda", "Wellington", ["Maestría", "Doctorado"],
  ["Agricultura", "Medio Ambiente", "Negocios", "Salud", "Educación"], "Completa",
  inc(True, True, True, True, True), 18, 45, 24,
  "2026-02-01", "2026-03-28", 0, ["Inglés"],
  "Https://www.mfat.govt.nz/en/aid-and-development/new-zealand-scholarships",
  "Https://www.nzscholarships.govt.nz/",
  "Beca neozelandesa integral con matrícula, estipendio, alojamiento inicial, seguro y pasajes.",
  ["Nacionalidad de país elegible", "Al menos 2 años de experiencia laboral",
   "Compromiso de retorno por 2 años", "Inglés acreditado"])

b("Mastercard Foundation Scholars Program", "Mastercard Foundation", "África",
  "Varios", "Nairobi", ["Pregrado", "Maestría"], ["Todas"], "Completa",
  inc(True, True, True, True, True, True), 17, 35, 48,
  "2026-01-01", "2026-06-30", 0, ["Inglés", "Francés"],
  "Https://mastercardfdn.org/en/what-we-do/our-programs/mastercard-foundation-scholars-program/",
  "Https://mastercardfdn.org/en/what-we-do/our-programs/mastercard-foundation-scholars-program/",
  "Beca integral con mentoria y desarrollo de liderazgo, en universidades socias de África, America y Europa.",
  ["Excelencia académica con limitaciones económicas",
   "Compromiso de servicio a la comunidad",
   "Postular en una universidad socia del programa"])

b("Rotary Peace Fellowship", "Fundación Rotaria", "Global", "Varios", "Global",
  ["Maestría", "Curso corto"], ["Ciencias Sociales", "Derecho", "Educación"],
  "Completa", inc(True, True, True, True, False), 22, 60, 24,
  "2026-02-01", "2026-05-15", 0, ["Inglés"],
  "Https://www.rotary.org/en/our-programs/peace-fellowships",
  "Https://www.rotary.org/en/our-programs/peace-fellowships",
  "Maestrías y certificados en paz y resolución de conflictos en centros Rotary de todo el mundo.",
  ["Mínimo 3 años de experiencia en paz o desarrollo (5 para certificado)",
   "Dominio del inglés", "Compromiso con el servicio comunitario",
   "Endoso de un club o distrito rotario"])

b("Becas del Banco Mundial - Joint Japan/World Bank", "Banco Mundial", "Global",
  "Varios", "Washington", ["Maestría"],
  ["Negocios", "Ciencias Sociales", "Salud", "Medio Ambiente"], "Completa",
  inc(True, True, False, True, True), 22, 45, 24,
  "2026-02-01", "2026-05-25", 0, ["Inglés"],
  "Https://www.worldbank.org/en/programs/scholarships",
  "Https://www.worldbank.org/en/programs/scholarships",
  "Maestrías en desarrollo para profesionales de países miembros, en universidades socias de todo el mundo.",
  ["Nacionalidad de país miembro elegible", "Mínimo 3 años de experiencia en desarrollo",
   "Admisión en un programa participante", "No tener doble nacionalidad de país desarrollado"])

b("Green Talents Award", "Ministerio Federal de Educación e investigación de Alemania",
  "Europa", "Alemania", "Berlin", ["Maestría", "Doctorado", "Posdoctorado"],
  ["Medio Ambiente", "Ciencias", "Ingeniería"], "Completa",
  inc(False, True, True, True, True), 21, 40, 3,
  "2026-01-15", "2026-05-24", 0, ["Inglés"],
  "Https://www.greentalents.de/", "Https://www.greentalents.de/participate.php",
  "Premio a jóvenes investigadores en desarrollo sostenible: viaje científico por Alemania y estancia de investigación financiada.",
  ["Estudiante de maestría avanzada, doctorando o posdoctorado",
   "Investigación vinculada al desarrollo sostenible", "Inglés fluido"])

b("UNESCO Fellowships Programme", "UNESCO", "Global", "Varios", "Paris",
  ["Maestría", "Curso corto", "Posdoctorado"],
  ["Educación", "Ciencias", "Medio Ambiente", "Humanidades"], "Parcial",
  inc(True, True, False, True, False), 21, 50, 12,
  "2026-01-01", "2026-09-30", 0, ["Inglés", "Francés"],
  "Https://www.unesco.org/en/fellowships", "Https://www.unesco.org/en/fellowships",
  "Becas y co-becas de la UNESCO en áreas de su mandato, canalizadas por las comisiones nacionales.",
  ["Postulación a traves de la comisión Nacional de UNESCO del país",
   "Título previo según programa", "Dominio del idioma de instrucción"])

b("Becas BID - Programa de Pasantías y Estudios", "Banco Interamericano de Desarrollo",
  "Latinoamérica", "Varios", "Washington", ["Maestría", "Doctorado", "Curso corto"],
  ["Negocios", "Ciencias Sociales", "Ingeniería", "Medio Ambiente"], "Parcial",
  inc(False, True, False, True, False), 21, 45, 12,
  "2026-03-01", "2026-08-31", 0, ["Español", "Inglés"],
  "Https://www.iadb.org/es/quienes-somos/oportunidades-de-carrera",
  "Https://www.iadb.org/es/quienes-somos/oportunidades-de-carrera",
  "Programas del BID de pasantias, investigación y apoyo a estudios de posgrado para ciudadanos de la región.",
  ["Nacionalidad de país miembro del BID", "Estar matriculado en un posgrado",
   "Dominio de al menos dos idiomas oficiales del banco"])

b("Coursera / edX Financial Aid", "Coursera y edX", "Global", "En línea", "Global",
  ["Curso corto", "Técnico"], ["Tecnología", "Negocios", "Ciencias", "Todas"],
  "Matrícula", inc(True, False, False, False, False), 16, 99, 6,
  "2026-01-01", "2026-12-31", 0, ["Inglés", "Español"],
  "Https://www.coursera.org/", "Https://www.coursera.support/s/article/209819033-Apply-for-Financial-Aid-or-a-Scholarship",
  "Ayuda financiera permanente que cubre el costo de cursos y certificados profesionales en línea.",
  ["Solicitud de ayuda financiera dentro del curso",
   "Explicar la situación económica y el objetivo de aprendizaje",
   "Respuesta en aproximadamente 15 dias"], modalidad="Virtual")

b("Google Developer Scholarship", "Google", "Global", "En línea", "Global",
  ["Curso corto", "Técnico"], ["Tecnología", "Ingeniería"], "Matrícula",
  inc(True, False, False, False, False), 16, 99, 6,
  "2026-01-15", "2026-09-30", 0, ["Inglés", "Español"],
  "Https://grow.google/", "Https://grow.google/certificates/",
  "Becas y certificados profesionales de Google en desarrollo, analítica de datos, UX y soporte de TI.",
  ["Acceso a internet y dedicación semanal mínima",
   "Sin requisito de título previo", "Postulación en la plataforma del partner"],
  modalidad="Virtual")

b("Becas Erasmus+ KA171 Movilidad Internacional", "Comisión Europea", "Europa",
  "Union Europea", "Bruselas", ["Pregrado", "Maestría", "Doctorado", "Intercambio"],
  ["Todas"], "Parcial", inc(False, True, False, True, True), 18, 45, 6,
  "2026-02-01", "2026-06-30", 0, ["Inglés", "Español"],
  "Https://erasmus-plus.ec.europa.eu/", "Https://erasmus-plus.ec.europa.eu/opportunities/opportunities-for-individuals/students",
  "Estancias de un semestre en universidades europeas mediante convenios entre tu universidad y la institución europea.",
  ["Estar matriculado en una universidad con convenio Erasmus+ KA171",
   "Haber aprobado el primer año de estudios",
   "Nivel de idioma B1 o B2 según destino"])

b("Emile Boutmy Scholarship", "Sciences Po", "Europa", "Francia", "Paris",
  ["Pregrado", "Maestría"], ["Ciencias Sociales", "Derecho", "Negocios"], "Parcial",
  inc(True, False, False, False, False), 17, 35, 24,
  "2025-10-01", "2026-01-06", 0, ["Inglés", "Francés"],
  "Https://www.sciencespo.fr/students/en/fees-funding/scholarships-financial-aid.html",
  "Https://www.sciencespo.fr/students/en/fees-funding/emile-boutmy-scholarship.html",
  "Beca de Sciences Po para estudiantes de fuera de la Union Europea, entre exoneración parcial y total de matrícula.",
  ["Nacionalidad de fuera de la UE", "Primera postulación a Sciences Po",
   "Excelente expediente académico", "Solicitud dentro del formulario de admisión"])

b("Becas de la Universidad de Buenos Aires - Movilidad", "Universidad de Buenos Aires",
  "Latinoamérica", "Argentina", "Buenos Aires", ["Pregrado", "Maestría", "Intercambio"],
  ["Todas"], "Parcial", inc(False, True, True, False, False), 18, 40, 6,
  "2026-03-01", "2026-06-30", 0, ["Español"],
  "Https://www.uba.ar/internacionales/", "Https://www.uba.ar/internacionales/",
  "Programas de movilidad e intercambio de la UBA con universidades de America Latina y Europa.",
  ["Estudiante regular de universidad con convenio",
   "Promedio académico mínimo", "Postulación via oficina de relaciones internacionales"])

b("Becas Roberto Rocca", "Fundación Roberto Rocca (Tenaris - Ternium)", "Latinoamérica",
  "Varios", "Buenos Aires", ["Pregrado", "Maestría", "Doctorado"],
  ["Ingeniería", "Ciencias", "Tecnología"], "Parcial",
  inc(True, True, False, False, False), 18, 35, 24,
  "2026-04-01", "2026-07-31", 0, ["Español", "Inglés"],
  "Https://www.robertorocca.org/", "Https://www.robertorocca.org/es/education-program",
  "Becas para estudiantes de ingenieria y ciencias aplicadas en America Latina, y posgrados en el exterior.",
  ["Estudiar ingenieria o ciencias aplicadas",
   "Excelente desempeno académico", "Residir en un país donde opera el programa"])

b("Becas Tecnológico de Monterrey - Líderes del Mañana", "Tecnológico de Monterrey",
  "Latinoamérica", "México", "Monterrey", ["Pregrado"], ["Todas"], "Completa",
  inc(True, True, True, False, True, False, True), 16, 25, 48,
  "2026-01-15", "2026-04-30", 0, ["Español"],
  "Https://tec.mx/es/lideres-del-manana", "Https://tec.mx/es/lideres-del-manana",
  "Beca integral del Tec de Monterrey para jóvenes de alto potencial con recursos económicos limitados.",
  ["Excelencia académica y liderazgo comprobado", "Necesidad económica acreditada",
   "Proceso de selección con entrevistas y examen de admisión"])

b("Becas de Excelencia del Gobierno de Rusia", "Rossotrudnichestvo", "Europa", "Rusia",
  "Moscú", ["Pregrado", "Maestría", "Doctorado"],
  ["Ingeniería", "Ciencias", "Salud", "Humanidades"], "Completa",
  inc(True, True, True, False, False, True), 17, 40, 60,
  "2025-11-01", "2026-02-28", 0, ["Ruso", "Inglés"],
  "Https://education-in-russia.com/", "Https://education-in-russia.com/",
  "Cupos estatales rusos con matrícula gratuita, alojamiento en residencia y curso preparatorio de ruso.",
  ["Registro en el portal Education in Russia",
   "Documentos académicos traducidos", "Examen de selección en la representacion rusa"])

b("Becas de la Universidad de São Paulo - PEC-PG", "Gobierno de Brasil (CAPES/CNPq)",
  "Latinoamérica", "Brasil", "São Paulo", ["Maestría", "Doctorado"], ["Todas"],
  "Completa", inc(True, True, False, True, False), 21, 45, 48,
  "2026-02-01", "2026-05-31", 0, ["Portugués"],
  "Https://www.gov.br/capes/", "Https://www.gov.br/capes/pt-br/acesso-a-informacao/acoes-e-programas/bolsas",
  "Programa brasileno de posgrado para ciudadanos de países en desarrollo con acuerdo de cooperación.",
  ["Nacionalidad de país con acuerdo educativo o cultural con Brasil",
   "Certificado Celpe-Bras de portugués", "Carta de aceptacion del programa de posgrado"])


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(BECAS, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(BECAS)} becas escritas en {OUT}")


if __name__ == "__main__":
    main()
