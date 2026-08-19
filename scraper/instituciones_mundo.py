# -*- coding: utf-8 -*-
"""Tercera tanda de la tabla semilla: cobertura mundial.

Suma paises que faltaban por completo -- Centroamerica y el Caribe, los paises
nordicos, Europa central y del este, Asia meridional y sudoriental, Oriente
Medio, Oceania y Africa -- ademas de mas universidades en los paises que ya
estaban.

Mismo formato de fila que scraper/instituciones.py:
  (id, nombre, sigla, pais, ciudad, dominio, ruta_posgrado, sunedu, tipo,
   nivel_costo, areas)
"""

# --- Centroamerica y el Caribe -----------------------------------------
CARIBE = [
 ("una-py","Universidad Nacional de Asunción","UNA","Paraguay","Asunción","una.py","/postgrado","extranjera","Pública",1,"AGR SAL DER EDU ING"),
 ("uca-py","Universidad Católica Nuestra Señora de la Asunción","UCA Paraguay","Paraguay","Asunción","universidadcatolica.edu.py","/posgrado","extranjera","Privada",2,"DER GES EDU SOC"),
 ("up-pa","Universidad de Panamá","UP Panamá","Panamá","Ciudad de Panamá","up.ac.pa","/posgrado","extranjera","Pública",1,"SAL DER EDU GES AMB"),
 ("utp-pa","Universidad Tecnológica de Panamá","UTP Panamá","Panamá","Ciudad de Panamá","utp.ac.pa","/posgrado","extranjera","Pública",2,"ING DAT AMB GES"),
 ("usac","Universidad de San Carlos de Guatemala","USAC","Guatemala","Ciudad de Guatemala","usac.edu.gt","/posgrado","extranjera","Pública",1,"SAL DER EDU AGR ING"),
 ("url-gt","Universidad Rafael Landívar","URL","Guatemala","Ciudad de Guatemala","url.edu.gt","/posgrados","extranjera","Privada",2,"DER GES EDU SOC"),
 ("uvg","Universidad del Valle de Guatemala","UVG","Guatemala","Ciudad de Guatemala","uvg.edu.gt","/posgrados","extranjera","Privada",2,"ING DAT AMB EDU"),
 ("ues","Universidad de El Salvador","UES","El Salvador","San Salvador","ues.edu.sv","/posgrado","extranjera","Pública",1,"SAL EDU ING DER"),
 ("uca-sv","Universidad Centroamericana José Simeón Cañas","UCA","El Salvador","San Salvador","uca.edu.sv","/posgrados","extranjera","Privada",2,"SOC DER GES EDU"),
 ("unah","Universidad Nacional Autónoma de Honduras","UNAH","Honduras","Tegucigalpa","unah.edu.hn","/posgrado","extranjera","Pública",1,"SAL DER EDU AGR"),
 ("unan","Universidad Nacional Autónoma de Nicaragua","UNAN-Managua","Nicaragua","Managua","unan.edu.ni","/posgrado","extranjera","Pública",1,"SAL EDU AGR SOC"),
 ("pucmm","Pontificia Universidad Católica Madre y Maestra","PUCMM","República Dominicana","Santiago de los Caballeros","pucmm.edu.do","/posgrado","extranjera","Privada",2,"GES DER EDU SAL"),
 ("intec","Instituto Tecnológico de Santo Domingo","INTEC","República Dominicana","Santo Domingo","intec.edu.do","/posgrado","extranjera","Privada",2,"ING GES SAL DAT"),
 ("uh-cu","Universidad de La Habana","UH","Cuba","La Habana","uh.cu","/posgrado","extranjera","Pública",1,"SOC ECO SAL EDU"),
 ("ucv-ve","Universidad Central de Venezuela","UCV","Venezuela","Caracas","ucv.ve","/postgrado","extranjera","Pública",1,"SAL DER ING SOC"),
 ("usb-ve","Universidad Simón Bolívar","USB","Venezuela","Caracas","usb.ve","/postgrado","extranjera","Pública",1,"ING DAT AMB GES"),
 ("upr","Universidad de Puerto Rico","UPR","Puerto Rico","San Juan","upr.edu","/estudios-graduados","extranjera","Pública",2,"SAL EDU ING SOC AMB"),
 ("umsa","Universidad Mayor de San Andrés","UMSA","Bolivia","La Paz","umsa.bo","/postgrado","extranjera","Pública",1,"SAL DER EDU ING AGR"),
 ("udg","Universidad de Guadalajara","UdeG","México","Guadalajara","udg.mx","/posgrados","extranjera","Pública",1,"SAL EDU ING SOC AMB"),
 ("uanl","Universidad Autónoma de Nuevo León","UANL","México","Monterrey","uanl.mx","/posgrado","extranjera","Pública",1,"ING SAL DER GES"),
]

# --- Europa -------------------------------------------------------------
EUROPA = [
 ("lund","Lunds universitet","Lund","Suecia","Lund","lu.se","/education/master","extranjera","Pública",2,"ING AMB SOC SAL DAT"),
 ("kth","KTH Royal Institute of Technology","KTH","Suecia","Estocolmo","kth.se","/en/studies/master","extranjera","Pública",2,"ING DAT AMB"),
 ("uppsala","Uppsala universitet","Uppsala","Suecia","Uppsala","uu.se","/en/study/masters","extranjera","Pública",2,"SAL SOC AMB DAT"),
 ("ntnu","Norwegian University of Science and Technology","NTNU","Noruega","Trondheim","ntnu.edu","/studies/master","extranjera","Pública",1,"ING AMB DAT"),
 ("uio","Universitetet i Oslo","UiO","Noruega","Oslo","uio.no","/english/studies/programmes/master","extranjera","Pública",1,"SOC SAL DER AMB"),
 ("ku-dk","Københavns Universitet","KU","Dinamarca","Copenhague","ku.dk","/studies/masters","extranjera","Pública",2,"SAL AGR SOC AMB DAT"),
 ("dtu","Technical University of Denmark","DTU","Dinamarca","Lyngby","dtu.dk","/english/education/graduate","extranjera","Pública",2,"ING DAT AMB"),
 ("aalto","Aalto University","Aalto","Finlandia","Espoo","aalto.fi","/en/study-at-aalto/masters-programmes","extranjera","Pública",2,"ING GES DAT COM"),
 ("helsinki","University of Helsinki","Helsinki","Finlandia","Helsinki","helsinki.fi","/en/admissions-and-education/masters-programmes","extranjera","Pública",2,"SAL EDU AMB SOC"),
 ("univie","Universität Wien","Uni Wien","Austria","Viena","univie.ac.at","/en/studying/master","extranjera","Pública",1,"SOC DER EDU SAL"),
 ("tuwien","TU Wien","TU Wien","Austria","Viena","tuwien.at","/en/studies/master","extranjera","Pública",1,"ING DAT AMB"),
 ("uw-pl","Uniwersytet Warszawski","UW","Polonia","Varsovia","uw.edu.pl","/en/studies","extranjera","Pública",1,"SOC ECO DER DAT"),
 ("agh","AGH University of Krakow","AGH","Polonia","Cracovia","agh.edu.pl","/en/education","extranjera","Pública",1,"ING DAT AMB"),
 ("cuni","Univerzita Karlova","Charles University","Chequia","Praga","cuni.cz","/UKEN-1.html","extranjera","Pública",1,"SAL SOC EDU DER"),
 ("elte","Eötvös Loránd University","ELTE","Hungría","Budapest","elte.hu","/en/programmes","extranjera","Pública",1,"EDU SOC DAT SAL"),
 ("ceu","Central European University","CEU","Austria","Viena","ceu.edu","/graduate-programs","extranjera","Privada",3,"POL SOC ECO DER"),
 ("uoa","National and Kapodistrian University of Athens","NKUA","Grecia","Atenas","uoa.gr","/en/studies","extranjera","Pública",1,"SAL SOC DER EDU"),
 ("unibuc","Universitatea din București","UB Bucarest","Rumanía","Bucarest","unibuc.ro","/en/masters","extranjera","Pública",1,"SOC EDU DER DAT"),
 ("epfl","EPFL","EPFL","Suiza","Lausana","epfl.ch","/education/master/","extranjera","Pública",3,"ING DAT AMB"),
 ("uzh","Universität Zürich","UZH","Suiza","Zúrich","uzh.ch","/en/studies/master.html","extranjera","Pública",3,"SAL ECO DER SOC"),
 ("ucd","University College Dublin","UCD","Irlanda","Dublín","ucd.ie","/graduatestudies/","extranjera","Pública",3,"GES AGR SAL DAT"),
 ("uva-nl","Universiteit van Amsterdam","UvA","Países Bajos","Ámsterdam","uva.nl","/en/programmes/masters","extranjera","Pública",3,"SOC COM ECO DAT"),
 ("eur","Erasmus University Rotterdam","EUR","Países Bajos","Róterdam","eur.nl","/en/master","extranjera","Pública",3,"ECO GES SAL POL"),
 ("leiden","Universiteit Leiden","Leiden","Países Bajos","Leiden","universiteitleiden.nl","/en/education/study-programmes","extranjera","Pública",3,"DER POL SOC SAL"),
 ("fu-berlin","Freie Universität Berlin","FU Berlin","Alemania","Berlín","fu-berlin.de","/en/studium/studienangebot","extranjera","Pública",1,"SOC POL EDU SAL"),
 ("rwth","RWTH Aachen University","RWTH","Alemania","Aquisgrán","rwth-aachen.de","/go/id/bdz/","extranjera","Pública",1,"ING DAT AMB"),
 ("sorbonne","Sorbonne Université","Sorbonne","Francia","París","sorbonne-universite.fr","/en/education","extranjera","Pública",2,"SAL SOC ING DAT"),
 ("psl","Université PSL","PSL","Francia","París","psl.eu","/en/education","extranjera","Pública",2,"ING SOC ECO DAT"),
 ("hec","HEC Paris","HEC","Francia","Jouy-en-Josas","hec.edu","/en/masters-programs","extranjera","Privada",4,"GES ECO DAT"),
 ("sapienza","Sapienza Università di Roma","Sapienza","Italia","Roma","uniroma1.it","/en/courses","extranjera","Pública",1,"ING SAL SOC AMB"),
 ("unibo","Università di Bologna","UniBo","Italia","Bolonia","unibo.it","/en/study/second-cycle-degree","extranjera","Pública",1,"DER SOC AGR COM"),
 ("ulisboa","Universidade de Lisboa","ULisboa","Portugal","Lisboa","ulisboa.pt","/en/education","extranjera","Pública",2,"ING SAL SOC AMB"),
 ("uc-pt","Universidade de Coimbra","UC","Portugal","Coímbra","uc.pt","/en/candidatos/mestrados","extranjera","Pública",2,"DER SOC SAL EDU"),
 ("ugent","Universiteit Gent","UGent","Bélgica","Gante","ugent.be","/en/education/degree","extranjera","Pública",2,"AGR AMB SAL ING"),
]

# --- Asia y Oriente Medio ----------------------------------------------
ASIA = [
 ("iitb","Indian Institute of Technology Bombay","IIT Bombay","India","Bombay","iitb.ac.in","/en/education/academic-programmes","extranjera","Pública",1,"ING DAT GES"),
 ("iisc","Indian Institute of Science","IISc","India","Bangalore","iisc.ac.in","/admissions/","extranjera","Pública",1,"ING DAT AMB SAL"),
 ("du-in","University of Delhi","DU","India","Nueva Delhi","du.ac.in","/index.php?page=post-graduate","extranjera","Pública",1,"SOC ECO EDU DER"),
 ("um-my","Universiti Malaya","UM","Malasia","Kuala Lumpur","um.edu.my","/study/postgraduate","extranjera","Pública",1,"ING SAL GES SOC"),
 ("chula","Chulalongkorn University","Chula","Tailandia","Bangkok","chula.ac.th","/en/academic/graduate/","extranjera","Pública",1,"SAL ING SOC GES"),
 ("ui-id","Universitas Indonesia","UI","Indonesia","Yakarta","ui.ac.id","/en/education/","extranjera","Pública",1,"SAL SOC ECO ING"),
 ("up-ph","University of the Philippines","UP","Filipinas","Quezon City","up.edu.ph","/index.php/academics/","extranjera","Pública",1,"SAL EDU AGR SOC"),
 ("hku","The University of Hong Kong","HKU","Hong Kong","Hong Kong","hku.hk","/study/taught-postgraduate","extranjera","Pública",3,"GES DER SAL EDU DAT"),
 ("hkust","Hong Kong University of Science and Technology","HKUST","Hong Kong","Hong Kong","hkust.edu.hk","/academics/postgraduate","extranjera","Pública",3,"ING DAT GES"),
 ("ntu-tw","National Taiwan University","NTU","Taiwán","Taipéi","ntu.edu.tw","/english/academics","extranjera","Pública",1,"ING SAL AGR DAT"),
 ("huji","The Hebrew University of Jerusalem","HUJI","Israel","Jerusalén","huji.ac.il","/en/study","extranjera","Pública",2,"SAL SOC AGR DAT"),
 ("technion","Technion — Israel Institute of Technology","Technion","Israel","Haifa","technion.ac.il","/en/graduate-studies/","extranjera","Pública",2,"ING DAT SAL"),
 ("ku-ae","Khalifa University","KU","Emiratos Árabes Unidos","Abu Dabi","ku.ac.ae","/graduate-programs/","extranjera","Pública",2,"ING DAT AMB"),
 ("kaust","King Abdullah University of Science and Technology","KAUST","Arabia Saudita","Thuwal","kaust.edu.sa","/en/study/graduate-programs","extranjera","Privada",2,"ING DAT AMB AGR"),
 ("qu-qa","Qatar University","QU","Qatar","Doha","qu.edu.qa","/study/graduate","extranjera","Pública",2,"ING GES EDU DER"),
 ("kyoto","Kyoto University","Kyoto U","Japón","Kioto","kyoto-u.ac.jp","/en/education-campus/education","extranjera","Pública",2,"ING SAL AMB SOC"),
 ("pku","Peking University","PKU","China","Pekín","pku.edu.cn","/en/admissions.html","extranjera","Pública",2,"SOC ECO DER SAL"),
 ("fudan","Fudan University","Fudan","China","Shanghái","fudan.edu.cn","/en/admissions","extranjera","Pública",2,"GES SAL SOC DAT"),
 ("snu","Seoul National University","SNU","Corea del Sur","Seúl","snu.ac.kr","/academics/graduate","extranjera","Pública",2,"ING SAL SOC EDU"),
 ("ntu-sg","Nanyang Technological University","NTU Singapore","Singapur","Singapur","ntu.edu.sg","/education/graduate-programmes","extranjera","Pública",3,"ING DAT GES COM"),
]

# --- Oceania ------------------------------------------------------------
OCEANIA = [
 ("auckland","University of Auckland","Auckland","Nueva Zelanda","Auckland","auckland.ac.nz","/en/study/study-options/postgraduate-study.html","extranjera","Pública",3,"GES SAL EDU AMB ING"),
 ("otago","University of Otago","Otago","Nueva Zelanda","Dunedin","otago.ac.nz","/study/postgraduate","extranjera","Pública",3,"SAL SOC AMB EDU"),
 ("unsw","UNSW Sydney","UNSW","Australia","Sídney","unsw.edu.au","/study/postgraduate","extranjera","Pública",3,"ING GES DAT AMB"),
 ("uq","The University of Queensland","UQ","Australia","Brisbane","uq.edu.au","/study/programs","extranjera","Pública",3,"SAL AGR AMB ING"),
 ("monash","Monash University","Monash","Australia","Melbourne","monash.edu","/study/courses","extranjera","Pública",3,"GES SAL EDU DAT"),
]

# --- Africa -------------------------------------------------------------
AFRICA = [
 ("uct","University of Cape Town","UCT","Sudáfrica","Ciudad del Cabo","uct.ac.za","/main/apply/postgraduate","extranjera","Pública",2,"SAL POL AMB ECO ING"),
 ("wits","University of the Witwatersrand","Wits","Sudáfrica","Johannesburgo","wits.ac.za","/postgraduate/","extranjera","Pública",2,"ING SAL SOC GES"),
 ("stellenbosch","Stellenbosch University","SU","Sudáfrica","Stellenbosch","sun.ac.za","/english/faculty/postgraduate","extranjera","Pública",2,"AGR AMB GES SAL"),
 ("cairo","Cairo University","CU","Egipto","El Cairo","cu.edu.eg","/Postgraduate","extranjera","Pública",1,"SAL DER ING EDU"),
 ("auc","The American University in Cairo","AUC","Egipto","El Cairo","aucegypt.edu","/admissions/graduate","extranjera","Privada",2,"GES POL COM DAT"),
 ("um5","Université Mohammed V de Rabat","UM5","Marruecos","Rabat","um5.ac.ma","/formations","extranjera","Pública",1,"DER SOC ING EDU"),
 ("aui","Al Akhawayn University","AUI","Marruecos","Ifrane","aui.ma","/academics/graduate-programs","extranjera","Privada",2,"GES DAT POL"),
 ("uonbi","University of Nairobi","UoN","Kenia","Nairobi","uonbi.ac.ke","/courses","extranjera","Pública",1,"SAL AGR EDU GES"),
 ("ug-gh","University of Ghana","UG","Ghana","Accra","ug.edu.gh","/graduate","extranjera","Pública",1,"SAL AGR SOC GES"),
 ("unilag","University of Lagos","UNILAG","Nigeria","Lagos","unilag.edu.ng","/postgraduate","extranjera","Pública",1,"GES ING SAL DER"),
]

# --- Mas Norteamerica ---------------------------------------------------
NORTEAMERICA = [
 ("berkeley","University of California, Berkeley","UC Berkeley","Estados Unidos","Berkeley, CA","berkeley.edu","/academics/graduate/","extranjera","Pública",4,"ING DAT POL AMB ECO"),
 ("umich","University of Michigan","U-M","Estados Unidos","Ann Arbor, MI","umich.edu","/academics/","extranjera","Pública",4,"SAL ING EDU POL DAT"),
 ("jhu","Johns Hopkins University","JHU","Estados Unidos","Baltimore, MD","jhu.edu","/admissions/graduate/","extranjera","Privada",4,"SAL POL ING DAT"),
 ("nyu","New York University","NYU","Estados Unidos","Nueva York","nyu.edu","/academics/graduate.html","extranjera","Privada",4,"COM DER GES SOC DAT"),
 ("ucla","University of California, Los Angeles","UCLA","Estados Unidos","Los Ángeles, CA","ucla.edu","/academics/graduate-programs","extranjera","Pública",4,"SAL EDU COM POL DAT"),
 ("ualberta","University of Alberta","U of A","Canadá","Edmonton","ualberta.ca","/graduate-studies/","extranjera","Pública",3,"AGR ING SAL AMB"),
 ("uwaterloo","University of Waterloo","Waterloo","Canadá","Waterloo","uwaterloo.ca","/graduate-studies/","extranjera","Pública",3,"DAT ING GES"),
]

MUNDIAL = CARIBE + EUROPA + ASIA + OCEANIA + AFRICA + NORTEAMERICA

REGION_MUNDIAL = {
 "Paraguay": "Latinoamérica", "Panamá": "Latinoamérica", "Guatemala": "Latinoamérica",
 "El Salvador": "Latinoamérica", "Honduras": "Latinoamérica", "Nicaragua": "Latinoamérica",
 "República Dominicana": "Latinoamérica", "Cuba": "Latinoamérica",
 "Venezuela": "Latinoamérica", "Puerto Rico": "Latinoamérica",
 "Suecia": "Europa", "Noruega": "Europa", "Dinamarca": "Europa", "Finlandia": "Europa",
 "Austria": "Europa", "Polonia": "Europa", "Chequia": "Europa", "Hungría": "Europa",
 "Grecia": "Europa", "Rumanía": "Europa",
 "India": "Asia", "Malasia": "Asia", "Tailandia": "Asia", "Indonesia": "Asia",
 "Filipinas": "Asia", "Hong Kong": "Asia", "Taiwán": "Asia", "Israel": "Asia",
 "Emiratos Árabes Unidos": "Asia", "Arabia Saudita": "Asia", "Qatar": "Asia",
 "Nueva Zelanda": "Oceanía",
 "Sudáfrica": "África", "Egipto": "África", "Marruecos": "África",
 "Kenia": "África", "Ghana": "África", "Nigeria": "África",
}

MONEDA_MUNDIAL = {
 "Paraguay": "USD", "Panamá": "USD", "Guatemala": "USD", "El Salvador": "USD",
 "Honduras": "USD", "Nicaragua": "USD", "República Dominicana": "USD",
 "Cuba": "USD", "Venezuela": "USD", "Puerto Rico": "USD",
 "Suecia": "SEK", "Noruega": "NOK", "Dinamarca": "DKK", "Finlandia": "EUR",
 "Austria": "EUR", "Polonia": "PLN", "Chequia": "CZK", "Hungría": "EUR",
 "Grecia": "EUR", "Rumanía": "EUR",
 "India": "INR", "Malasia": "MYR", "Tailandia": "THB", "Indonesia": "USD",
 "Filipinas": "PHP", "Hong Kong": "HKD", "Taiwán": "TWD", "Israel": "ILS",
 "Emiratos Árabes Unidos": "AED", "Arabia Saudita": "USD", "Qatar": "QAR",
 "Nueva Zelanda": "NZD",
 "Sudáfrica": "ZAR", "Egipto": "USD", "Marruecos": "MAD",
 "Kenia": "USD", "Ghana": "USD", "Nigeria": "USD",
}

# Tipos de cambio aproximados a USD, solo para ordenar y comparar rangos.
TASAS_MUNDIAL = {
 "SEK": 0.095, "NOK": 0.092, "DKK": 0.145, "PLN": 0.25, "CZK": 0.043,
 "INR": 0.012, "MYR": 0.22, "THB": 0.028, "PHP": 0.017, "HKD": 0.128,
 "TWD": 0.031, "ILS": 0.27, "AED": 0.272, "QAR": 0.275, "NZD": 0.60,
 "ZAR": 0.055, "MAD": 0.10,
}

IDIOMA_MUNDIAL = {
 "Suecia": "Inglés", "Noruega": "Inglés", "Dinamarca": "Inglés",
 "Finlandia": "Inglés", "Austria": "Inglés / Alemán", "Polonia": "Inglés",
 "Chequia": "Inglés", "Hungría": "Inglés", "Grecia": "Inglés / Griego",
 "Rumanía": "Inglés / Rumano",
 "India": "Inglés", "Malasia": "Inglés", "Tailandia": "Inglés",
 "Indonesia": "Inglés", "Filipinas": "Inglés", "Hong Kong": "Inglés",
 "Taiwán": "Inglés / Chino", "Israel": "Inglés", "Emiratos Árabes Unidos": "Inglés",
 "Arabia Saudita": "Inglés", "Qatar": "Inglés", "Nueva Zelanda": "Inglés",
 "Sudáfrica": "Inglés", "Egipto": "Inglés / Árabe", "Marruecos": "Francés / Inglés",
 "Kenia": "Inglés", "Ghana": "Inglés", "Nigeria": "Inglés",
 "Puerto Rico": "Español / Inglés", "Cuba": "Español",
}
