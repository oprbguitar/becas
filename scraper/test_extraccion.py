#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pruebas del extractor sin salir a internet.

Usan páginas de ejemplo que imitan la estructura real de una convocatoria,
para comprobar que el rastreador reconoce requisitos y fechas de cierre y que
descarta el ruido de la plantilla (menús, cookies, pies de página).

    python scraper/test_extraccion.py
"""
from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scrape import extraer_fecha_cierre, extraer_requisitos, es_requisito  # noqa: E402

FUTURO = date.today() + timedelta(days=90)

PAGINA_ES = f"""
<html><body>
  <nav><a href="/">Inicio</a> | <a href="/becas">Becas</a></nav>
  <div class="cookies">Usamos cookies para mejorar tu experiencia.</div>
  <h1>Convocatoria de Becas de Posgrado 2026</h1>
  <p>Compartir en redes</p>
  <h2>Requisitos de postulación</h2>
  <ul>
    <li>Ser de nacionalidad peruana y contar con documento de identidad vigente.</li>
    <li>Acreditar un promedio ponderado mínimo de 15 sobre 20 en los estudios de pregrado.</li>
    <li>Presentar carta de admisión de una universidad extranjera acreditada.</li>
    <li>No haber sido beneficiario de otra beca del Estado en los últimos cinco años.</li>
  </ul>
  <p>La fecha de cierre de la convocatoria es el {FUTURO.day} de
     {["enero","febrero","marzo","abril","mayo","junio","julio","agosto",
        "septiembre","octubre","noviembre","diciembre"][FUTURO.month - 1]} de {FUTURO.year}.</p>
  <footer>© 2026 Todos los derechos reservados. Política de privacidad.</footer>
</body></html>
"""

PAGINA_EN = f"""
<html><body>
  <header><a href="/login">Log in</a></header>
  <h2>Eligibility</h2>
  <ul>
    <li>Applicants must hold an undergraduate degree from a recognised institution.</li>
    <li>You must have at least two years of relevant work experience before applying.</li>
    <li>Applicants must be citizens of an eligible country listed on this page.</li>
  </ul>
  <p>The application deadline is {FUTURO.strftime('%d/%m/%Y')}.</p>
  <footer>All rights reserved.</footer>
</body></html>
"""

PAGINA_SIN_DATOS = "<html><body><h1>Página en mantenimiento</h1><p>Vuelve pronto.</p></body></html>"


def revisar(condicion: bool, mensaje: str) -> bool:
    print(f"  {'OK  ' if condicion else 'FALLA'} {mensaje}")
    return condicion


def main() -> int:
    ok = True
    print("Extracción en español:")
    reqs = extraer_requisitos(PAGINA_ES)
    ok &= revisar(len(reqs) >= 3, f"encuentra al menos 3 requisitos (encontró {len(reqs)})")
    ok &= revisar(any("nacionalidad peruana" in r for r in reqs), "reconoce el requisito de nacionalidad")
    ok &= revisar(not any("cookies" in r.lower() for r in reqs), "descarta el aviso de cookies")
    ok &= revisar(not any("derechos reservados" in r.lower() for r in reqs), "descarta el pie de página")
    ok &= revisar(extraer_fecha_cierre(PAGINA_ES) == FUTURO.isoformat(),
                  f"detecta la fecha de cierre en texto ({FUTURO.isoformat()})")

    print("Extracción en inglés:")
    reqs_en = extraer_requisitos(PAGINA_EN)
    ok &= revisar(len(reqs_en) >= 3, f"encuentra al menos 3 requisitos (encontró {len(reqs_en)})")
    ok &= revisar(extraer_fecha_cierre(PAGINA_EN) == FUTURO.isoformat(), "detecta la fecha en formato dd/mm/aaaa")

    print("Página sin datos útiles:")
    ok &= revisar(extraer_requisitos(PAGINA_SIN_DATOS) == [], "no inventa requisitos")
    ok &= revisar(extraer_fecha_cierre(PAGINA_SIN_DATOS) is None, "no inventa fechas")

    print("Clasificador de líneas:")
    ok &= revisar(es_requisito("Contar con grado de bachiller emitido por una universidad licenciada."),
                  "acepta una línea de requisito")
    ok &= revisar(not es_requisito("Inicio"), "rechaza una línea demasiado corta")
    ok &= revisar(not es_requisito("Aceptar cookies para continuar navegando en este sitio web oficial."),
                  "rechaza ruido de plantilla")

    print("\n" + ("Todas las pruebas pasaron." if ok else "Hay pruebas fallidas."))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
