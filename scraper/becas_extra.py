# -*- coding: utf-8 -*-
"""Ampliacion del catalogo semilla de becas.

Se centra en los huecos que quedaban: mas convocatorias peruanas (estatales y
de universidades), mas Espana y algunas becas de posgrado de referencia
mundial que faltaban.

Mismo contrato que scraper/seed.py: este modulo expone `registrar(b, inc)` y
seed.py lo llama con sus propios ayudantes, de modo que las fichas quedan
normalizadas igual que las del catalogo original.

Las fechas son REFERENCIALES (las convocatorias son anuales). scraper/scrape.py
las actualiza contra la pagina oficial y scraper/validar_enlaces.py comprueba
que cada enlace abra.
"""


def registrar(b, inc):
    # ------------------------------------------------------------- Peru
    b("Beca Presidente de la República", "PRONABEC", "Perú", "Global", "Lima",
      ["Maestría", "Doctorado"],
      ["Ingeniería", "Ciencias", "Tecnología", "Salud", "Educación", "Negocios"],
      "Completa", inc(True, True, True, True, True), 22, 45, 24,
      "2026-03-02", "2026-05-29", 0, ["Español", "Inglés"],
      "https://www.gob.pe/pronabec",
      "https://www.gob.pe/institucion/pronabec/campa%C3%B1as/1249-beca-presidente-de-la-republica",
      "Financia maestrías y doctorados en universidades del top mundial para "
      "profesionales peruanos, con compromiso de retorno y servicio al país.",
      ["Nacionalidad peruana", "Carta de admisión a universidad del ranking exigido",
       "Grado de bachiller o título profesional",
       "Compromiso de retorno al Perú al terminar los estudios"], destacada=True)

    b("Beca Continuidad de Estudios Superiores", "PRONABEC", "Perú", "Perú", "Lima",
      ["Pregrado"], ["Todas"], "Completa", inc(True, True, False, False, True), 16, 35, 48,
      "2026-04-06", "2026-06-19", 0, ["Español"],
      "https://www.gob.pe/pronabec",
      "https://www.gob.pe/institucion/pronabec/campa%C3%B1as/1250-beca-continuidad-de-estudios",
      "Permite retomar y culminar estudios superiores interrumpidos por razones "
      "económicas en universidades e institutos elegibles del país.",
      ["Haber interrumpido los estudios superiores",
       "Clasificación socioeconómica de pobreza o pobreza extrema",
       "Vacante vigente en institución elegible"])

    b("Beca Vocación de Maestro", "PRONABEC", "Perú", "Perú", "Lima",
      ["Pregrado"], ["Educación"], "Completa", inc(True, True, True, False, True),
      16, 30, 60, "2026-02-09", "2026-04-17", 0, ["Español"],
      "https://www.gob.pe/pronabec",
      "https://www.gob.pe/institucion/pronabec/campa%C3%B1as/1251-beca-vocacion-de-maestro",
      "Beca integral para estudiar carreras de Educación en universidades e "
      "institutos pedagógicos licenciados del Perú.",
      ["Alto rendimiento en la educación secundaria",
       "Postular a una carrera de Educación en institución elegible",
       "Condición socioeconómica elegible"])

    b("Beca Perú", "PRONABEC", "Perú", "Perú", "Lima",
      ["Pregrado", "Técnico"], ["Todas"], "Parcial", inc(True, False, False, False, False),
      16, 30, 48, "2026-05-04", "2026-07-10", 0, ["Español"],
      "https://www.gob.pe/pronabec",
      "https://www.gob.pe/institucion/pronabec/campa%C3%B1as/1252-beca-peru",
      "Modalidad cofinanciada entre el Estado y universidades e institutos "
      "privados que ceden vacantes a estudiantes de alto rendimiento.",
      ["Alto rendimiento académico", "Postular a institución adherida al programa",
       "Condición socioeconómica elegible"])

    b("Beca Doble Oportunidad", "PRONABEC", "Perú", "Perú", "Lima",
      ["Técnico"], ["Tecnología", "Negocios", "Ingeniería"], "Completa",
      inc(True, True, False, False, True), 17, 25, 24,
      "2026-03-16", "2026-05-22", 0, ["Español"],
      "https://www.gob.pe/pronabec",
      "https://www.gob.pe/institucion/pronabec/campa%C3%B1as/1253-beca-doble-oportunidad",
      "Permite culminar la educación secundaria y obtener a la vez una "
      "certificación técnica en institutos de educación superior.",
      ["No haber culminado la secundaria", "Tener entre 17 y 25 años",
       "Condición socioeconómica de pobreza"])

    b("Becas de Doctorado PROCIENCIA", "CONCYTEC - PROCIENCIA", "Perú", "Perú", "Lima",
      ["Doctorado"], ["Ciencias", "Ingeniería", "Tecnología", "Salud", "Medio Ambiente"],
      "Completa", inc(True, True, False, False, True), 24, 50, 48,
      "2026-04-13", "2026-07-31", 0, ["Español"],
      "https://prociencia.gob.pe/", "https://prociencia.gob.pe/concursos/",
      "Financiamiento estatal para doctorados en ciencia y tecnología dictados "
      "en universidades peruanas con programas acreditados.",
      ["Registro vigente en CTI Vitae", "Admisión a doctorado acreditado",
       "Proyecto de tesis alineado a las prioridades nacionales de CTI"])

    b("Programa de Maestría Fulbright Perú", "Comisión Fulbright del Perú",
      "Norteamérica", "Estados Unidos", "Washington", ["Maestría"],
      ["Todas"], "Completa", inc(True, True, False, True, True), 22, 40, 24,
      "2026-02-02", "2026-05-15", 0, ["Inglés"],
      "https://www.fulbright.pe/", "https://www.fulbright.pe/becas/",
      "Beca del Gobierno de Estados Unidos para que profesionales peruanos "
      "cursen una maestría en universidades estadounidenses.",
      ["Nacionalidad peruana", "Grado de bachiller", "Dominio acreditado del inglés (TOEFL)",
       "Compromiso de retorno al Perú por dos años"], destacada=True)

    b("Becas de Posgrado PUCP", "Pontificia Universidad Católica del Perú",
      "Perú", "Perú", "Lima", ["Maestría", "Doctorado"], ["Todas"],
      "Parcial", inc(True, False, False, False, False), 22, 60, 24,
      "2026-01-12", "2026-03-13", 0, ["Español"],
      "https://posgrado.pucp.edu.pe/", "https://posgrado.pucp.edu.pe/becas-y-apoyo-financiero/",
      "Apoyo financiero de la Escuela de Posgrado de la PUCP: becas por mérito, "
      "media beca y descuentos para egresados y docentes.",
      ["Admisión a un programa de posgrado de la PUCP",
       "Expediente académico destacado", "Evaluación socioeconómica"])

    b("Fondo de Becas ESAN", "Universidad ESAN", "Perú", "Perú", "Lima",
      ["Maestría"], ["Negocios", "Tecnología", "Ingeniería"], "Parcial",
      inc(True, False, False, False, False), 23, 55, 24,
      "2026-02-16", "2026-04-24", 0, ["Español"],
      "https://www.esan.edu.pe/", "https://www.esan.edu.pe/maestrias",
      "Becas parciales y descuentos corporativos para las maestrías de ESAN, "
      "asignados por mérito académico y trayectoria profesional.",
      ["Admisión a una maestría de ESAN", "Experiencia profesional acreditada",
       "Entrevista personal"])

    b("Beca Excelencia CENTRUM PUCP", "CENTRUM PUCP Business School",
      "Perú", "Perú", "Lima", ["Maestría"], ["Negocios", "Economía"], "Parcial",
      inc(True, False, False, False, False), 24, 55, 24,
      "2026-03-09", "2026-05-08", 0, ["Español", "Inglés"],
      "https://centrum.pucp.edu.pe/", "https://centrum.pucp.edu.pe/maestrias/",
      "Descuentos por excelencia académica y convenios corporativos para los "
      "MBA y maestrías especializadas de CENTRUM PUCP.",
      ["Admisión al programa", "Promedio destacado en pregrado",
       "Mínimo de años de experiencia según el programa"])

    b("Becas de Posgrado Universidad del Pacífico", "Universidad del Pacífico",
      "Perú", "Perú", "Lima", ["Maestría"], ["Economía", "Negocios", "Políticas Públicas"],
      "Parcial", inc(True, False, False, False, False), 23, 50, 24,
      "2026-02-23", "2026-04-30", 0, ["Español"],
      "https://www.up.edu.pe/", "https://www.up.edu.pe/posgrado",
      "Becas por mérito y convenios institucionales para las maestrías de la "
      "Escuela de Posgrado de la Universidad del Pacífico.",
      ["Admisión a una maestría de la UP", "Expediente académico sobresaliente",
       "Sustento socioeconómico cuando aplique"])

    # ----------------------------------------------------------- Espana
    b("Becas de Posgrado Fundación \"la Caixa\"", "Fundación \"la Caixa\"",
      "Europa", "España", "Madrid", ["Maestría", "Doctorado"], ["Todas"],
      "Completa", inc(True, True, False, True, True), 22, 40, 24,
      "2026-01-19", "2026-04-08", 0, ["Español", "Inglés"],
      "https://fundacionlacaixa.org/", "https://fundacionlacaixa.org/es/becas-posgrado",
      "Una de las becas de posgrado más completas de España: cubre matrícula, "
      "manutención y viaje para estudiar en Europa o Norteamérica.",
      ["Expediente académico excelente", "Admisión o preadmisión al programa",
       "Nivel acreditado del idioma de estudio",
       "Proyecto personal y de retorno bien argumentado"], destacada=True)

    b("Becas Fundación Ramón Areces", "Fundación Ramón Areces", "Europa", "España",
      "Madrid", ["Maestría", "Doctorado"], ["Economía", "Ciencias", "Salud"],
      "Completa", inc(True, True, False, True, True), 22, 40, 24,
      "2026-02-02", "2026-04-17", 0, ["Español", "Inglés"],
      "https://www.fundacionareces.es/", "https://www.fundacionareces.es/fundacionareces/es/becas/",
      "Becas de ampliación de estudios en el extranjero en economía, ciencias "
      "de la vida y de la materia.",
      ["Titulación universitaria", "Admisión al centro de destino",
       "Dominio del idioma de estudio"])

    b("Becas Iberoamérica Santander Investigación", "Banco Santander",
      "Europa", "España", "Madrid", ["Maestría", "Doctorado"], ["Todas"],
      "Parcial", inc(False, True, False, True, False), 20, 45, 6,
      "2026-03-02", "2026-05-29", 0, ["Español", "Portugués"],
      "https://www.santanderopenacademy.com/",
      "https://www.santanderopenacademy.com/es/programs.html",
      "Movilidad académica de estudiantes y docentes entre universidades "
      "iberoamericanas de la red Santander.",
      ["Estar matriculado en una universidad de la red",
       "Aval de la universidad de origen", "Buen expediente académico"])

    b("Becas IE Foundation", "IE University", "Europa", "España", "Madrid",
      ["Maestría"], ["Negocios", "Tecnología", "Derecho", "Economía"], "Parcial",
      inc(True, False, False, False, False), 22, 45, 12,
      "2026-01-12", "2026-06-30", 0, ["Inglés", "Español"],
      "https://www.ie.edu/", "https://www.ie.edu/es/becas/",
      "Ayudas de la IE Foundation por mérito, liderazgo e impacto social para "
      "los másteres de IE University.",
      ["Admisión a un programa de IE University",
       "Expediente y trayectoria destacados", "Ensayo de motivación"])

    b("Becas UNIR para Latinoamérica", "Universidad Internacional de La Rioja",
      "Europa", "España", "Madrid", ["Maestría"], ["Educación", "Negocios", "Derecho"],
      "Parcial", inc(True, False, False, False, False), 21, 60, 12,
      "2026-01-05", "2026-12-15", 0, ["Español"],
      "https://www.unir.net/", "https://www.unir.net/becas-y-ayudas/",
      "Descuentos y ayudas al estudio para alumnos latinoamericanos en los "
      "másteres oficiales online de UNIR.",
      ["Titulación universitaria previa", "Matrícula en un máster oficial de UNIR",
       "Documentación académica apostillada"], modalidad="Online")

    # ------------------------------------------------------------ Mundo
    b("Clarendon Fund Scholarships", "University of Oxford", "Europa",
      "Reino Unido", "Oxford", ["Maestría", "Doctorado"], ["Todas"], "Completa",
      inc(True, True, False, False, False), 21, 45, 36,
      "2026-09-01", "2027-01-08", 0, ["Inglés"],
      "https://www.ox.ac.uk/clarendon", "https://www.ox.ac.uk/clarendon/applying",
      "Cubre matrícula completa y manutención para estudiantes de posgrado de "
      "excelencia en la Universidad de Oxford; no requiere postulación aparte.",
      ["Postular a un programa de posgrado elegible de Oxford",
       "Excelencia académica demostrable",
       "Cumplir los plazos de admisión de la universidad"], destacada=True)

    b("Knight-Hennessy Scholars", "Stanford University", "Norteamérica",
      "Estados Unidos", "Stanford", ["Maestría", "Doctorado"], ["Todas"],
      "Completa", inc(True, True, False, True, True), 21, 40, 36,
      "2026-06-10", "2026-10-08", 0, ["Inglés"],
      "https://knight-hennessy.stanford.edu/",
      "https://knight-hennessy.stanford.edu/admission",
      "Financia hasta tres años de cualquier posgrado de Stanford e incorpora "
      "al becario a un programa de formación en liderazgo.",
      ["Grado de bachiller obtenido en los últimos años",
       "Postulación paralela a un posgrado de Stanford",
       "Trayectoria de liderazgo e impacto"])

    b("Schwarzman Scholars", "Tsinghua University", "Asia", "China", "Global",
      ["Maestría"], ["Políticas Públicas", "Negocios", "Ciencias Sociales"],
      "Completa", inc(True, True, True, True, True), 20, 29, 12,
      "2026-04-01", "2026-09-24", 0, ["Inglés"],
      "https://www.schwarzmanscholars.org/",
      "https://www.schwarzmanscholars.org/admissions/",
      "Maestría de un año en Asuntos Globales en la Universidad de Tsinghua, "
      "con beca integral y residencia en Pekín.",
      ["Título universitario", "Menos de 29 años al iniciar el programa",
       "Inglés fluido", "Liderazgo demostrado"])

    b("Yenching Academy Scholarship", "Peking University", "Asia", "China",
      "Global", ["Maestría"], ["Ciencias Sociales", "Políticas Públicas", "Economía"],
      "Completa", inc(True, True, True, True, True), 20, 30, 24,
      "2026-08-17", "2026-12-04", 0, ["Inglés"],
      "https://yenchingacademy.pku.edu.cn/",
      "https://yenchingacademy.pku.edu.cn/ADMISSIONS.htm",
      "Maestría interdisciplinaria en Estudios sobre China en la Universidad de "
      "Pekín, con beca completa y alojamiento en el campus.",
      ["Título de pregrado", "Excelente expediente académico",
       "Interés acreditado en estudios sobre China"])

    b("Commonwealth Scholarships", "Commonwealth Scholarship Commission",
      "Europa", "Reino Unido", "Londres", ["Maestría", "Doctorado"],
      ["Desarrollo", "Salud", "Ingeniería", "Educación"], "Completa",
      inc(True, True, False, True, False), 22, 45, 12,
      "2026-09-15", "2026-12-17", 0, ["Inglés"],
      "https://cscuk.fcdo.gov.uk/", "https://cscuk.fcdo.gov.uk/scholarships/",
      "Becas del Reino Unido para ciudadanos de países de la Commonwealth y de "
      "países en desarrollo, orientadas al impacto en el país de origen.",
      ["Nacionalidad de un país elegible", "Título de pregrado con buena nota",
       "Postulación a través de la agencia nominadora del país"])

    b("Emerging Leaders in the Americas Program (ELAP)", "Gobierno de Canadá",
      "Norteamérica", "Canadá", "Global", ["Pregrado", "Maestría", "Doctorado"],
      ["Todas"], "Parcial", inc(False, True, False, True, False), 18, 40, 6,
      "2026-10-01", "2027-03-11", 0, ["Inglés", "Francés"],
      "https://www.educanada.ca/",
      "https://www.educanada.ca/scholarships-bourses/can/institutions/elap-pfla.aspx",
      "Movilidad académica de corta duración en instituciones canadienses para "
      "estudiantes de América Latina y el Caribe.",
      ["Estar matriculado en una institución de América Latina o el Caribe",
       "Acuerdo entre la institución de origen y la canadiense",
       "Postulación presentada por la institución canadiense"])

    b("Aga Khan Foundation International Scholarship Programme",
      "Aga Khan Foundation", "Global", "Global", "Global", ["Maestría", "Doctorado"],
      ["Todas"], "Parcial", inc(True, True, False, False, False), 22, 45, 24,
      "2026-01-05", "2026-03-31", 0, ["Inglés", "Francés"],
      "https://the.akdn/", "https://the.akdn/en/what-we-do/developing-human-capacity/education/international-scholarship-programme",
      "Mitad beca y mitad préstamo para estudios de posgrado de estudiantes con "
      "excelente historial académico y sin otros medios de financiamiento.",
      ["Residir en un país elegible del programa",
       "Admisión a un posgrado reconocido",
       "Demostrar necesidad financiera"])

    b("Becas Heinrich Böll Stiftung", "Heinrich-Böll-Stiftung", "Europa",
      "Alemania", "Berlin", ["Maestría", "Doctorado"],
      ["Medio Ambiente", "Ciencias Sociales", "Políticas Públicas"], "Completa",
      inc(True, True, False, False, True), 21, 40, 24,
      "2026-02-01", "2026-03-01", 0, ["Alemán", "Inglés"],
      "https://www.boell.de/", "https://www.boell.de/en/scholarships",
      "Becas para estudios de posgrado en Alemania dirigidas a personas con "
      "compromiso social, ecológico y democrático.",
      ["Admisión en una universidad alemana",
       "Compromiso político-social acreditado",
       "Conocimiento del idioma según el programa"])

    b("Becas Konrad-Adenauer-Stiftung", "Konrad-Adenauer-Stiftung", "Europa",
      "Alemania", "Bonn", ["Maestría", "Doctorado"],
      ["Políticas Públicas", "Derecho", "Economía", "Ciencias Sociales"],
      "Completa", inc(True, True, False, True, True), 21, 40, 24,
      "2026-05-04", "2026-07-15", 0, ["Alemán", "Inglés"],
      "https://www.kas.de/", "https://www.kas.de/en/scholarships",
      "Programa de becas para estudiantes internacionales de posgrado en "
      "Alemania, con formación complementaria en liderazgo y política.",
      ["Admisión a una universidad alemana", "Buen expediente académico",
       "Compromiso social y conocimientos de alemán"])

    b("Colfuturo — Programa Crédito Beca", "COLFUTURO", "Latinoamérica",
      "Colombia", "Bogota", ["Maestría", "Doctorado"], ["Todas"], "Parcial",
      inc(True, False, False, False, False), 21, 45, 24,
      "2026-01-26", "2026-04-24", 0, ["Español", "Inglés"],
      "https://www.colfuturo.org/", "https://www.colfuturo.org/financiacion-para-posgrados",
      "Crédito condonable para colombianos que cursan posgrados en el "
      "exterior; se convierte parcialmente en beca al regresar al país.",
      ["Nacionalidad colombiana", "Admisión a un posgrado en el exterior",
       "Codeudor y estudio de crédito aprobado"])

    b("Rotary Peace Fellowships", "The Rotary Foundation", "Global", "Global",
      "Global", ["Maestría"], ["Ciencias Sociales", "Políticas Públicas", "Desarrollo"],
      "Completa", inc(True, True, True, True, False), 24, 50, 24,
      "2026-02-02", "2026-05-15", 0, ["Inglés"],
      "https://www.rotary.org/", "https://www.rotary.org/en/our-programs/peace-fellowships",
      "Beca integral para una maestría en resolución de conflictos y "
      "construcción de paz en los centros Rotary Peace del mundo.",
      ["Experiencia profesional en desarrollo o resolución de conflictos",
       "Dominio del inglés", "Compromiso con la paz y el servicio comunitario"])
