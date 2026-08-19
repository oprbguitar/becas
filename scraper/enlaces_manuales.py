# -*- coding: utf-8 -*-
"""Correcciones manuales de enlaces.

scraper/validar_enlaces.py prueba estas URLs ANTES que ninguna otra. Si
responden bien, se publican; si el dominio no contesta desde la red donde
corre el validador, se publican igual marcadas como "manual", porque son
direcciones verificadas a mano.

Sirve para dos casos:
  * universidades cuyo dominio rechaza peticiones automatizadas o bloquea
    centros de datos, de modo que el descubrimiento automatico no las alcanza;
  * secciones de posgrado que viven en un subdominio que la portada no enlaza
    de forma evidente.

Anade aqui cualquier enlace que veas mal en el sitio y vuelve a correr:
    python scraper/validar_enlaces.py --solo-instituciones
"""

INSTITUCIONES = {
    # El subdominio www no existe en varios sitios peruanos.
    "centrum": "https://centrum.pucp.edu.pe/maestrias/",
    "unmsm": "https://unmsm.edu.pe/",
    "upch": "https://upch.edu.pe/",
    "unap-puno": "https://unap.edu.pe/",
    "unsch": "https://unsch.edu.pe/",
    # Portales que responden en otra ruta.
    "unal": "https://unal.edu.co/",
    "fgv": "https://portal.fgv.br/",
    "nova-pt": "https://www.unl.pt/en",
    "pucp": "https://posgrado.pucp.edu.pe/",
    "up": "https://www.up.edu.pe/programas/posgrado",
    "esan": "https://www.esan.edu.pe/maestrias",
    "usmp": "https://www.usmp.edu.pe/",
    "ucsm": "https://ucsm.edu.pe/escuela-de-postgrado/",
    "unir": "https://www.unir.net/educacion/masteres/",
    "oxford": "https://www.ox.ac.uk/admissions/graduate/courses",
    "columbia": "https://www.columbia.edu/content/academics",
    "melbourne": "https://study.unimelb.edu.au/find/?collection=find-a-course",
    "ub": "https://www.ub.edu/portal/web/economia-empresa/masteres-universitarios",
}

BECAS = {
    # Fichas de campana de PRONABEC en gob.pe.
    "beca-18-pronabec": "https://www.gob.pe/beca18",
}
