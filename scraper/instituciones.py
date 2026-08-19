# -*- coding: utf-8 -*-
"""Tabla semilla de instituciones para el catalogo de posgrados.

Cada fila:
  (id, nombre, sigla, pais, ciudad, dominio, ruta_posgrado, sunedu, tipo, nivel_costo, areas)

sunedu:
  "licenciada"  -> universidad peruana con licencia institucional otorgada por SUNEDU
  "proceso"     -> licenciamiento o renovacion en tramite / por verificar en el registro
  "extranjera"  -> institucion no peruana: no aplica licenciamiento SUNEDU; el grado se
                   inscribe en Peru via reconocimiento o revalidacion ante SUNEDU

nivel_costo: 1 (publica economica) .. 4 (premium internacional)
areas: codigos separados por espacio (ver AREAS)
"""

AREAS = {
    "GES": "Gestión y Negocios",
    "POL": "Políticas Públicas y Gobierno",
    "ING": "Ingeniería y Tecnología",
    "SAL": "Ciencias de la Salud",
    "EDU": "Educación",
    "DER": "Derecho",
    "AMB": "Medio Ambiente y Sostenibilidad",
    "SOC": "Ciencias Sociales y Humanidades",
    "ECO": "Economía y Finanzas",
    "DAT": "Datos e Inteligencia Artificial",
    "COM": "Comunicación y Marketing",
    "AGR": "Agronomía y Alimentos",
}

# --- Peru ---------------------------------------------------------------
PERU = [
 ("pucp","Pontificia Universidad Católica del Perú","PUCP","Perú","Lima","pucp.edu.pe","/escuela-posgrado/","licenciada","Privada",3,"GES POL ING DER SOC EDU AMB DAT ECO COM"),
 ("unmsm","Universidad Nacional Mayor de San Marcos","UNMSM","Perú","Lima","unmsm.edu.pe","/posgrado","licenciada","Pública",1,"SAL SOC DER EDU ING ECO POL AGR"),
 ("uni","Universidad Nacional de Ingeniería","UNI","Perú","Lima","uni.edu.pe","/postgrado","licenciada","Pública",1,"ING AMB DAT GES"),
 ("unalm","Universidad Nacional Agraria La Molina","UNALM","Perú","Lima","unalm.edu.pe","/escuela-de-posgrado/","licenciada","Pública",1,"AGR AMB ING GES"),
 ("upch","Universidad Peruana Cayetano Heredia","UPCH","Perú","Lima","upch.edu.pe","/escuela-de-posgrado/","licenciada","Privada",3,"SAL AMB EDU GES DAT"),
 ("up","Universidad del Pacífico","UP","Perú","Lima","up.edu.pe","/posgrado","licenciada","Privada",3,"ECO GES POL DAT COM"),
 ("esan","Universidad ESAN","ESAN","Perú","Lima","esan.edu.pe","/maestrias","licenciada","Privada",3,"GES ECO DAT ING COM POL"),
 ("upc","Universidad Peruana de Ciencias Aplicadas","UPC","Perú","Lima","upc.edu.pe","/posgrado/","licenciada","Privada",3,"GES ING SAL DAT COM EDU"),
 ("ulima","Universidad de Lima","ULima","Perú","Lima","ulima.edu.pe","/posgrado","licenciada","Privada",3,"GES DER COM ING ECO"),
 ("usil","Universidad San Ignacio de Loyola","USIL","Perú","Lima","usil.edu.pe","/posgrado","licenciada","Privada",2,"GES EDU COM AGR DAT"),
 ("udep","Universidad de Piura","UDEP","Perú","Piura","udep.edu.pe","/posgrado/","licenciada","Privada",2,"GES DER EDU COM ING"),
 ("urp","Universidad Ricardo Palma","URP","Perú","Lima","urp.edu.pe","/escuela-de-posgrado/","licenciada","Privada",2,"ING SAL DER EDU GES"),
 ("usmp","Universidad de San Martín de Porres","USMP","Perú","Lima","usmp.edu.pe","/posgrado","licenciada","Privada",2,"SAL DER GES COM EDU"),
 ("unsa","Universidad Nacional de San Agustín de Arequipa","UNSA","Perú","Arequipa","unsa.edu.pe","/unidades-de-posgrado/","licenciada","Pública",1,"ING SAL DER EDU GES AMB"),
 ("unt","Universidad Nacional de Trujillo","UNT","Perú","Trujillo","unitru.edu.pe","/posgrado","licenciada","Pública",1,"SAL EDU ING AGR DER"),
 ("unsaac","Universidad Nacional de San Antonio Abad del Cusco","UNSAAC","Perú","Cusco","unsaac.edu.pe","/escuela-de-posgrado/","licenciada","Pública",1,"SOC AGR ING EDU AMB"),
 ("ucsm","Universidad Católica de Santa María","UCSM","Perú","Arequipa","ucsm.edu.pe","/escuela-de-postgrado/","licenciada","Privada",2,"SAL DER EDU GES ING"),
 ("ucsp","Universidad Católica San Pablo","UCSP","Perú","Arequipa","ucsp.edu.pe","/posgrado/","licenciada","Privada",2,"GES ING DER EDU"),
 ("utec","Universidad de Ingeniería y Tecnología","UTEC","Perú","Lima","utec.edu.pe","/posgrado","licenciada","Privada",3,"ING DAT AMB GES"),
 ("uarm","Universidad Antonio Ruiz de Montoya","UARM","Perú","Lima","uarm.edu.pe","/posgrado/","licenciada","Privada",2,"EDU SOC POL COM"),
 ("unfv","Universidad Nacional Federico Villarreal","UNFV","Perú","Lima","unfv.edu.pe","/posgrado","licenciada","Pública",1,"SAL DER EDU ING GES"),
 ("unprg","Universidad Nacional Pedro Ruiz Gallo","UNPRG","Perú","Lambayeque","unprg.edu.pe","/posgrado","licenciada","Pública",1,"ING EDU AGR SAL"),
 ("utp","Universidad Tecnológica del Perú","UTP","Perú","Lima","utp.edu.pe","/posgrado","licenciada","Privada",2,"ING GES DAT EDU"),
 ("ucv","Universidad César Vallejo","UCV","Perú","Trujillo","ucv.edu.pe","/posgrado/","licenciada","Privada",2,"EDU GES DER SAL ING"),
 ("upn","Universidad Privada del Norte","UPN","Perú","Trujillo","upn.edu.pe","/posgrado","licenciada","Privada",2,"GES ING EDU SAL"),
 ("unac","Universidad Nacional del Callao","UNAC","Perú","Callao","unac.edu.pe","/posgrado","licenciada","Pública",1,"ING GES AMB ECO"),
 ("unp","Universidad Nacional de Piura","UNP","Perú","Piura","unp.edu.pe","/posgrado","licenciada","Pública",1,"AGR ING EDU DER"),
 ("unjbg","Universidad Nacional Jorge Basadre Grohmann","UNJBG","Perú","Tacna","unjbg.edu.pe","/posgrado","licenciada","Pública",1,"ING EDU AGR SAL"),
 ("uncp","Universidad Nacional del Centro del Perú","UNCP","Perú","Huancayo","uncp.edu.pe","/posgrado","licenciada","Pública",1,"AGR EDU ING SAL"),
 ("continental","Universidad Continental","UC","Perú","Huancayo","continental.edu.pe","/posgrado/","licenciada","Privada",2,"GES EDU ING SAL DAT"),
 ("upsjb","Universidad Privada San Juan Bautista","UPSJB","Perú","Lima","upsjb.edu.pe","/posgrado","proceso","Privada",2,"SAL GES EDU"),
 ("unica","Universidad Nacional San Luis Gonzaga","UNICA","Perú","Ica","unica.edu.pe","/posgrado","proceso","Pública",1,"SAL EDU AGR ING"),
]

# --- Latinoamerica ------------------------------------------------------
LATAM = [
 ("uchile","Universidad de Chile","UChile","Chile","Santiago","uchile.cl","/postgrados","extranjera","Pública",2,"POL ING SAL SOC ECO EDU AMB DER"),
 ("puc-chile","Pontificia Universidad Católica de Chile","PUC Chile","Chile","Santiago","uc.cl","/postgrados","extranjera","Privada",3,"GES ING POL SAL EDU AMB DER SOC"),
 ("udec","Universidad de Concepción","UdeC","Chile","Concepción","udec.cl","/postgrado","extranjera","Privada",2,"ING AMB SAL AGR EDU"),
 ("usach","Universidad de Santiago de Chile","USACH","Chile","Santiago","usach.cl","/postgrado","extranjera","Pública",2,"ING DAT GES AMB"),
 ("uai","Universidad Adolfo Ibáñez","UAI","Chile","Santiago","uai.cl","/postgrados","extranjera","Privada",3,"GES ECO DAT POL"),
 ("uandes-co","Universidad de los Andes","Uniandes","Colombia","Bogotá","uniandes.edu.co","/programas/posgrados","extranjera","Privada",3,"POL GES ING ECO DER DAT AMB EDU"),
 ("unal","Universidad Nacional de Colombia","UNAL","Colombia","Bogotá","unal.edu.co","/programas/posgrado","extranjera","Pública",1,"ING SAL AGR SOC AMB EDU"),
 ("javeriana","Pontificia Universidad Javeriana","Javeriana","Colombia","Bogotá","javeriana.edu.co","/posgrados","extranjera","Privada",2,"SAL DER SOC EDU COM GES"),
 ("eafit","Universidad EAFIT","EAFIT","Colombia","Medellín","eafit.edu.co","/programas/posgrado","extranjera","Privada",2,"GES ING ECO DAT"),
 ("udea","Universidad de Antioquia","UdeA","Colombia","Medellín","udea.edu.co","/posgrados","extranjera","Pública",1,"SAL EDU ING SOC"),
 ("unam","Universidad Nacional Autónoma de México","UNAM","México","Ciudad de México","unam.mx","/posgrado","extranjera","Pública",1,"SOC ING SAL DER EDU AMB ECO POL"),
 ("tec","Tecnológico de Monterrey","Tec de Monterrey","México","Monterrey","tec.mx","/es/posgrados","extranjera","Privada",3,"GES ING DAT AMB EDU SAL"),
 ("itam","Instituto Tecnológico Autónomo de México","ITAM","México","Ciudad de México","itam.mx","/posgrados","extranjera","Privada",3,"ECO GES POL DER DAT"),
 ("ipn","Instituto Politécnico Nacional","IPN","México","Ciudad de México","ipn.mx","/posgrado","extranjera","Pública",1,"ING DAT SAL AMB"),
 ("udlap","Universidad de las Américas Puebla","UDLAP","México","Puebla","udlap.mx","/posgrados","extranjera","Privada",2,"GES COM EDU ING"),
 ("uba","Universidad de Buenos Aires","UBA","Argentina","Buenos Aires","uba.ar","/posgrados","extranjera","Pública",1,"DER SAL SOC ECO EDU ING"),
 ("utdt","Universidad Torcuato Di Tella","UTDT","Argentina","Buenos Aires","utdt.edu","/posgrados","extranjera","Privada",3,"ECO POL GES DAT DER"),
 ("austral","Universidad Austral","Austral","Argentina","Buenos Aires","austral.edu.ar","/posgrados","extranjera","Privada",2,"GES DER COM SAL"),
 ("unc-ar","Universidad Nacional de Córdoba","UNC","Argentina","Córdoba","unc.edu.ar","/posgrados","extranjera","Pública",1,"SAL AGR SOC ING EDU"),
 ("usp","Universidade de São Paulo","USP","Brasil","São Paulo","usp.br","/pos-graduacao","extranjera","Pública",1,"ING SAL AGR SOC AMB DAT ECO"),
 ("unicamp","Universidade Estadual de Campinas","Unicamp","Brasil","Campinas","unicamp.br","/pos-graduacao","extranjera","Pública",1,"ING DAT SAL AMB"),
 ("fgv","Fundação Getulio Vargas","FGV","Brasil","São Paulo","fgv.br","/pos-graduacao","extranjera","Privada",3,"ECO GES POL DER DAT"),
 ("ufrj","Universidade Federal do Rio de Janeiro","UFRJ","Brasil","Río de Janeiro","ufrj.br","/pos-graduacao","extranjera","Pública",1,"ING SAL AMB SOC"),
 ("ucr","Universidad de Costa Rica","UCR","Costa Rica","San José","ucr.ac.cr","/posgrado","extranjera","Pública",1,"SAL EDU AMB SOC ING"),
 ("tec-cr","Tecnológico de Costa Rica","TEC","Costa Rica","Cartago","tec.ac.cr","/posgrados","extranjera","Pública",2,"ING AMB GES DAT"),
 ("usfq","Universidad San Francisco de Quito","USFQ","Ecuador","Quito","usfq.edu.ec","/es/programas/posgrados","extranjera","Privada",2,"GES AMB SAL COM"),
 ("flacso-ec","FLACSO Ecuador","FLACSO","Ecuador","Quito","flacso.edu.ec","/posgrados","extranjera","Privada",2,"SOC POL ECO AMB"),
 ("udelar","Universidad de la República","UdelaR","Uruguay","Montevideo","udelar.edu.uy","/posgrados","extranjera","Pública",1,"SAL SOC ING AGR"),
 ("ort-uy","Universidad ORT Uruguay","ORT","Uruguay","Montevideo","ort.edu.uy","/posgrados","extranjera","Privada",2,"GES DAT ING COM"),
 ("upb-bo","Universidad Privada Boliviana","UPB","Bolivia","La Paz","upb.edu","/posgrado","extranjera","Privada",2,"GES ING DAT ECO"),
 ("incae","INCAE Business School","INCAE","Costa Rica","Alajuela","incae.edu","/es/programas","extranjera","Privada",3,"GES ECO AMB POL"),
]

# --- Resto del mundo ----------------------------------------------------
MUNDO = [
 ("ucm","Universidad Complutense de Madrid","UCM","España","Madrid","ucm.es","/estudios/masteres","extranjera","Pública",2,"DER SOC SAL EDU COM ECO"),
 ("ub","Universitat de Barcelona","UB","España","Barcelona","ub.edu","/estudios/masteres-universitarios","extranjera","Pública",2,"SAL AMB SOC EDU DAT"),
 ("uab","Universitat Autònoma de Barcelona","UAB","España","Barcelona","uab.cat","/estudiar/masteres-oficiales","extranjera","Pública",2,"COM SOC AMB ING EDU"),
 ("upm","Universidad Politécnica de Madrid","UPM","España","Madrid","upm.es","/Estudios/Masteres","extranjera","Pública",2,"ING DAT AMB AGR"),
 ("ie","IE University","IE","España","Madrid","ie.edu","/es/programas","extranjera","Privada",4,"GES ECO DAT POL COM DER"),
 ("esade","ESADE","ESADE","España","Barcelona","esade.edu","/es/programas","extranjera","Privada",4,"GES ECO DER DAT"),
 ("unir","Universidad Internacional de La Rioja","UNIR","España","Logroño","unir.net","/educacion/masteres/","extranjera","Privada",2,"EDU GES DER COM SAL DAT"),
 ("usal","Universidad de Salamanca","USAL","España","Salamanca","usal.es","/masteres-universitarios","extranjera","Pública",2,"SOC DER EDU SAL"),
 ("oxford","University of Oxford","Oxford","Reino Unido","Oxford","ox.ac.uk","/admissions/graduate/courses","extranjera","Privada",4,"POL SAL SOC DER ECO AMB DAT"),
 ("cambridge","University of Cambridge","Cambridge","Reino Unido","Cambridge","cam.ac.uk","/postgraduate/courses","extranjera","Privada",4,"ING SAL SOC ECO DAT AMB"),
 ("lse","London School of Economics and Political Science","LSE","Reino Unido","Londres","lse.ac.uk","/programmes/search-courses","extranjera","Privada",4,"ECO POL SOC DER DAT"),
 ("edinburgh","The University of Edinburgh","Edinburgh","Reino Unido","Edimburgo","ed.ac.uk","/studying/postgraduate","extranjera","Pública",3,"SAL DAT AMB EDU SOC"),
 ("manchester","The University of Manchester","Manchester","Reino Unido","Mánchester","manchester.ac.uk","/study/masters/courses","extranjera","Pública",3,"ING GES SAL DAT AMB"),
 ("harvard","Harvard University","Harvard","Estados Unidos","Cambridge, MA","harvard.edu","/programs/","extranjera","Privada",4,"POL SAL DER EDU ECO GES"),
 ("mit","Massachusetts Institute of Technology","MIT","Estados Unidos","Cambridge, MA","mit.edu","/education/graduate-education/","extranjera","Privada",4,"ING DAT GES AMB ECO"),
 ("stanford","Stanford University","Stanford","Estados Unidos","Stanford, CA","stanford.edu","/academics/","extranjera","Privada",4,"ING DAT GES SAL EDU"),
 ("columbia","Columbia University","Columbia","Estados Unidos","Nueva York","columbia.edu","/content/academics","extranjera","Privada",4,"POL DER COM SAL ECO AMB"),
 ("georgetown","Georgetown University","Georgetown","Estados Unidos","Washington D.C.","georgetown.edu","/academics/","extranjera","Privada",4,"POL DER SOC ECO"),
 ("toronto","University of Toronto","U of T","Canadá","Toronto","utoronto.ca","/academics/graduate-studies","extranjera","Pública",3,"SAL ING DAT EDU POL"),
 ("ubc","University of British Columbia","UBC","Canadá","Vancouver","ubc.ca","/programs/","extranjera","Pública",3,"AMB ING SAL EDU DAT"),
 ("mcgill","McGill University","McGill","Canadá","Montreal","mcgill.ca","/gradapplicants/programs","extranjera","Pública",3,"SAL ING SOC DER"),
 ("melbourne","The University of Melbourne","Melbourne","Australia","Melbourne","unimelb.edu.au","/study/graduate","extranjera","Pública",3,"POL SAL ING EDU AMB DAT"),
 ("sydney","The University of Sydney","Sydney","Australia","Sídney","sydney.edu.au","/courses/","extranjera","Pública",3,"SAL GES ING AMB EDU"),
 ("anu","Australian National University","ANU","Australia","Canberra","anu.edu.au","/study/study-options","extranjera","Pública",3,"POL SOC AMB DAT ECO"),
 ("eth","ETH Zürich","ETH","Suiza","Zúrich","ethz.ch","/en/studies/master.html","extranjera","Pública",3,"ING DAT AMB AGR"),
 ("tudelft","Delft University of Technology","TU Delft","Países Bajos","Delft","tudelft.nl","/en/education/programmes/masters","extranjera","Pública",3,"ING DAT AMB GES"),
 ("wur","Wageningen University & Research","WUR","Países Bajos","Wageningen","wur.nl","/en/education-programmes/master.htm","extranjera","Pública",3,"AGR AMB SAL DAT"),
 ("sciencespo","Sciences Po","Sciences Po","Francia","París","sciencespo.fr","/en/education/","extranjera","Privada",3,"POL SOC ECO COM DER"),
 ("bocconi","Università Bocconi","Bocconi","Italia","Milán","unibocconi.it","/en/programs","extranjera","Privada",3,"ECO GES DAT DER"),
 ("nus","National University of Singapore","NUS","Singapur","Singapur","nus.edu.sg","/education/graduate-programmes","extranjera","Pública",3,"ING DAT GES POL AMB"),
 ("tokyo","The University of Tokyo","UTokyo","Japón","Tokio","u-tokyo.ac.jp","/en/academics/graduate.html","extranjera","Pública",2,"ING SAL AMB DAT SOC"),
 ("tsinghua","Tsinghua University","Tsinghua","China","Pekín","tsinghua.edu.cn","/en/Admissions.htm","extranjera","Pública",2,"ING DAT GES AMB"),
 ("kaist","KAIST","KAIST","Corea del Sur","Daejeon","kaist.ac.kr","/en/html/edu/","extranjera","Pública",2,"ING DAT GES"),
]

INSTITUCIONES = PERU + LATAM + MUNDO

REGION_POR_PAIS = {
 "Perú": "Perú",
 "Chile": "Latinoamérica", "Colombia": "Latinoamérica", "México": "Latinoamérica",
 "Argentina": "Latinoamérica", "Brasil": "Latinoamérica", "Costa Rica": "Latinoamérica",
 "Ecuador": "Latinoamérica", "Uruguay": "Latinoamérica", "Bolivia": "Latinoamérica",
 "España": "Europa", "Reino Unido": "Europa", "Suiza": "Europa", "Países Bajos": "Europa",
 "Francia": "Europa", "Italia": "Europa",
 "Estados Unidos": "Norteamérica", "Canadá": "Norteamérica",
 "Australia": "Oceanía",
 "Singapur": "Asia", "Japón": "Asia", "China": "Asia", "Corea del Sur": "Asia",
}

MONEDA_POR_PAIS = {
 "Perú": "PEN", "Chile": "CLP", "Colombia": "COP", "México": "MXN", "Argentina": "USD",
 "Brasil": "BRL", "Costa Rica": "USD", "Ecuador": "USD", "Uruguay": "USD", "Bolivia": "USD",
 "España": "EUR", "Reino Unido": "GBP", "Suiza": "CHF", "Países Bajos": "EUR",
 "Francia": "EUR", "Italia": "EUR", "Estados Unidos": "USD", "Canadá": "CAD",
 "Australia": "AUD", "Singapur": "SGD", "Japón": "USD", "China": "USD", "Corea del Sur": "USD",
}

# Tipo de cambio aproximado a USD. Solo se usa para ordenar y comparar rangos.
A_USD = {"PEN": 0.27, "CLP": 0.0011, "COP": 0.00025, "MXN": 0.055, "BRL": 0.18,
         "EUR": 1.08, "GBP": 1.27, "CHF": 1.12, "CAD": 0.73, "AUD": 0.66,
         "SGD": 0.74, "USD": 1.0}

IDIOMA_POR_PAIS = {
 "Reino Unido": "Inglés", "Estados Unidos": "Inglés", "Canadá": "Inglés",
 "Australia": "Inglés", "Singapur": "Inglés", "Países Bajos": "Inglés",
 "Suiza": "Inglés", "Japón": "Inglés", "China": "Inglés", "Corea del Sur": "Inglés",
 "Brasil": "Portugués", "Francia": "Francés / Inglés", "Italia": "Inglés",
}
