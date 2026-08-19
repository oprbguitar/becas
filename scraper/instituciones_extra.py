# -*- coding: utf-8 -*-
"""Ampliacion de la tabla semilla: mas universidades peruanas (publicas y
privadas), mas Espana y mas destinos de posgrado.

Mismo formato de fila que scraper/instituciones.py:
  (id, nombre, sigla, pais, ciudad, dominio, ruta_posgrado, sunedu, tipo,
   nivel_costo, areas)

Las rutas de posgrado son las declaradas; scraper/validar_enlaces.py las
comprueba contra el sitio real y las corrige antes de generar el catalogo.
"""

PERU_2 = [
 ("centrum","CENTRUM PUCP Business School","CENTRUM","Perú","Lima","centrum.pucp.edu.pe","/maestrias/","licenciada","Privada",3,"GES ECO POL DAT COM AMB"),
 ("ucsur","Universidad Científica del Sur","UCSUR","Perú","Lima","cientifica.edu.pe","/posgrado","licenciada","Privada",2,"SAL AMB GES AGR EDU"),
 ("upao","Universidad Privada Antenor Orrego","UPAO","Perú","Trujillo","upao.edu.pe","/posgrado","licenciada","Privada",2,"SAL DER ING EDU GES"),
 ("upeu","Universidad Peruana Unión","UPeU","Perú","Lima","upeu.edu.pe","/posgrado","licenciada","Privada",2,"EDU SAL GES ING"),
 ("ucss","Universidad Católica Sedes Sapientiae","UCSS","Perú","Lima","ucss.edu.pe","/posgrado","licenciada","Privada",2,"EDU SOC GES AGR"),
 ("unife","Universidad Femenina del Sagrado Corazón","UNIFÉ","Perú","Lima","unife.edu.pe","/posgrado","licenciada","Privada",2,"EDU SOC DER COM"),
 ("uac","Universidad Andina del Cusco","UAC","Perú","Cusco","uandina.edu.pe","/posgrado","licenciada","Privada",2,"DER SAL GES EDU"),
 ("uss","Universidad Señor de Sipán","USS","Perú","Chiclayo","uss.edu.pe","/posgrado","licenciada","Privada",2,"DER GES EDU ING SAL"),
 ("upt","Universidad Privada de Tacna","UPT","Perú","Tacna","upt.edu.pe","/posgrado","licenciada","Privada",2,"DER GES ING EDU"),
 ("umch","Universidad Marcelino Champagnat","UMCH","Perú","Lima","umch.edu.pe","/posgrado","licenciada","Privada",2,"EDU SOC"),
 ("uladech","Universidad Católica Los Ángeles de Chimbote","ULADECH","Perú","Chimbote","uladech.edu.pe","/posgrado","licenciada","Privada",1,"DER EDU SAL GES"),
 ("uwiener","Universidad Privada Norbert Wiener","UPNW","Perú","Lima","uwiener.edu.pe","/posgrado","licenciada","Privada",2,"SAL GES EDU DAT"),
 ("unc","Universidad Nacional de Cajamarca","UNC","Perú","Cajamarca","unc.edu.pe","/posgrado","licenciada","Pública",1,"AGR ING SAL EDU AMB"),
 ("unasam","Universidad Nacional Santiago Antúnez de Mayolo","UNASAM","Perú","Huaraz","unasam.edu.pe","/posgrado","licenciada","Pública",1,"ING AMB AGR EDU"),
 ("unapiquitos","Universidad Nacional de la Amazonía Peruana","UNAP","Perú","Iquitos","unapiquitos.edu.pe","/posgrado","licenciada","Pública",1,"AMB SAL AGR EDU"),
 ("unas","Universidad Nacional Agraria de la Selva","UNAS","Perú","Tingo María","unas.edu.pe","/posgrado","licenciada","Pública",1,"AGR AMB ING"),
 ("unu","Universidad Nacional de Ucayali","UNU","Perú","Pucallpa","unu.edu.pe","/posgrado","licenciada","Pública",1,"AGR AMB EDU SAL"),
 ("unheval","Universidad Nacional Hermilio Valdizán","UNHEVAL","Perú","Huánuco","unheval.edu.pe","/posgrado","licenciada","Pública",1,"EDU SAL DER ING"),
 ("unsch","Universidad Nacional de San Cristóbal de Huamanga","UNSCH","Perú","Ayacucho","unsch.edu.pe","/posgrado","licenciada","Pública",1,"AGR EDU ING SOC"),
 ("unap-puno","Universidad Nacional del Altiplano","UNA Puno","Perú","Puno","unap.edu.pe","/posgrado","licenciada","Pública",1,"AGR EDU ING AMB SAL"),
 ("untumbes","Universidad Nacional de Tumbes","UNTUMBES","Perú","Tumbes","untumbes.edu.pe","/posgrado","licenciada","Pública",1,"AGR AMB SAL EDU"),
 ("unjfsc","Universidad Nacional José Faustino Sánchez Carrión","UNJFSC","Perú","Huacho","unjfsc.edu.pe","/posgrado","licenciada","Pública",1,"EDU DER ING AGR"),
 ("untrm","Universidad Nacional Toribio Rodríguez de Mendoza","UNTRM","Perú","Chachapoyas","untrm.edu.pe","/posgrado","licenciada","Pública",1,"AGR AMB SAL EDU"),
 ("unh","Universidad Nacional de Huancavelica","UNH","Perú","Huancavelica","unh.edu.pe","/posgrado","licenciada","Pública",1,"EDU AGR SAL ING"),
 ("undac","Universidad Nacional Daniel Alcides Carrión","UNDAC","Perú","Cerro de Pasco","undac.edu.pe","/posgrado","licenciada","Pública",1,"ING AMB EDU SAL"),
 ("unamba","Universidad Nacional Micaela Bastidas de Apurímac","UNAMBA","Perú","Abancay","unamba.edu.pe","/posgrado","licenciada","Pública",1,"AGR ING EDU"),
 ("unsm","Universidad Nacional de San Martín","UNSM","Perú","Tarapoto","unsm.edu.pe","/posgrado","licenciada","Pública",1,"AGR AMB SAL EDU"),
 ("unia","Universidad Nacional Intercultural de la Amazonía","UNIA","Perú","Pucallpa","unia.edu.pe","/posgrado","licenciada","Pública",1,"AGR SOC EDU"),
]

ESPANA_2 = [
 ("ugr","Universidad de Granada","UGR","España","Granada","ugr.es","/estudios/masteres","extranjera","Pública",2,"EDU SAL SOC DER AMB ING"),
 ("upv","Universitat Politècnica de València","UPV","España","Valencia","upv.es","/estudios/masteres","extranjera","Pública",2,"ING DAT AGR AMB GES"),
 ("us-sevilla","Universidad de Sevilla","US","España","Sevilla","us.es","/estudios/master","extranjera","Pública",2,"ING SAL EDU DER SOC"),
 ("uc3m","Universidad Carlos III de Madrid","UC3M","España","Madrid","uc3m.es","/master","extranjera","Pública",2,"ECO DER DAT ING COM"),
 ("uam","Universidad Autónoma de Madrid","UAM","España","Madrid","uam.es","/estudios/masteres","extranjera","Pública",2,"SAL SOC DER EDU AMB"),
 ("unav","Universidad de Navarra","UNAV","España","Pamplona","unav.edu","/estudios/masteres","extranjera","Privada",3,"SAL COM DER GES EDU"),
 ("comillas","Universidad Pontificia Comillas ICADE","Comillas","España","Madrid","comillas.edu","/es/masteres","extranjera","Privada",3,"DER ECO GES ING SOC"),
 ("uoc","Universitat Oberta de Catalunya","UOC","España","Barcelona","uoc.edu","/es/estudios/masters","extranjera","Privada",2,"EDU DAT GES COM SOC"),
 ("uv","Universitat de València","UV","España","Valencia","uv.es","/estudis/masteres","extranjera","Pública",2,"SAL EDU SOC ECO AMB"),
 ("ehu","Universidad del País Vasco","UPV/EHU","España","Bilbao","ehu.eus","/es/master","extranjera","Pública",2,"ING SOC EDU AMB SAL"),
 ("uah","Universidad de Alcalá","UAH","España","Alcalá de Henares","uah.es","/es/estudios/master","extranjera","Pública",2,"EDU DER SAL SOC"),
 ("unizar","Universidad de Zaragoza","Unizar","España","Zaragoza","unizar.es","/estudios/master","extranjera","Pública",2,"ING AGR SAL EDU"),
 ("uned","Universidad Nacional de Educación a Distancia","UNED","España","Madrid","uned.es","/universidad/inicio/estudios/masteres.html","extranjera","Pública",1,"EDU DER SOC ECO DAT"),
 ("uem","Universidad Europea de Madrid","UEM","España","Madrid","universidadeuropea.com","/es/masteres/","extranjera","Privada",3,"SAL GES COM DER DAT"),
]

MUNDO_2 = [
 ("ucl","University College London","UCL","Reino Unido","Londres","ucl.ac.uk","/prospective-students/graduate","extranjera","Pública",4,"SAL ING EDU SOC DAT AMB"),
 ("kcl","Kings College London","KCL","Reino Unido","Londres","kcl.ac.uk","/study/postgraduate","extranjera","Pública",4,"SAL DER SOC POL DAT"),
 ("tum","Technische Universität München","TUM","Alemania","Múnich","tum.de","/en/studies/degree-programs","extranjera","Pública",2,"ING DAT AMB AGR"),
 ("heidelberg","Universität Heidelberg","Heidelberg","Alemania","Heidelberg","uni-heidelberg.de","/en/study","extranjera","Pública",2,"SAL SOC AMB DAT"),
 ("kuleuven","KU Leuven","KU Leuven","Bélgica","Lovaina","kuleuven.be","/en/study/master","extranjera","Pública",2,"ING SAL AMB SOC DAT"),
 ("polimi","Politecnico di Milano","PoliMi","Italia","Milán","polimi.it","/en/programmes","extranjera","Pública",3,"ING DAT AMB COM"),
 ("tcd","Trinity College Dublin","Trinity","Irlanda","Dublín","tcd.ie","/courses/postgraduate/","extranjera","Pública",3,"SAL SOC DAT ECO"),
 ("uach-cl","Universidad Austral de Chile","UACh","Chile","Valdivia","uach.cl","/postgrado","extranjera","Privada",2,"AGR AMB SAL EDU"),
 ("urosario","Universidad del Rosario","UR","Colombia","Bogotá","urosario.edu.co","/posgrados/","extranjera","Privada",2,"DER POL SAL ECO GES"),
 ("uninorte","Universidad del Norte","Uninorte","Colombia","Barranquilla","uninorte.edu.co","/web/posgrados","extranjera","Privada",2,"ING SAL EDU GES DAT"),
 ("palermo","Universidad de Palermo","UP Palermo","Argentina","Buenos Aires","palermo.edu","/posgrados/","extranjera","Privada",2,"COM GES DER DAT"),
 ("puc-rio","Pontifícia Universidade Católica do Rio de Janeiro","PUC-Rio","Brasil","Río de Janeiro","puc-rio.br","/ensinopesq/ccpg/","extranjera","Privada",2,"ING ECO SOC DAT"),
 ("nova-pt","Universidade Nova de Lisboa","NOVA","Portugal","Lisboa","unl.pt","/en/education","extranjera","Pública",2,"ECO GES DAT SAL SOC"),
 ("uporto","Universidade do Porto","U.Porto","Portugal","Oporto","up.pt","/en/study/masters","extranjera","Pública",2,"ING SAL AMB EDU"),
]

EXTRA = PERU_2 + ESPANA_2 + MUNDO_2

REGION_EXTRA = {"Alemania": "Europa", "Bélgica": "Europa",
                "Irlanda": "Europa", "Portugal": "Europa"}
MONEDA_EXTRA = {"Alemania": "EUR", "Bélgica": "EUR",
                "Irlanda": "EUR", "Portugal": "EUR"}
IDIOMA_EXTRA = {"Alemania": "Inglés / Alemán", "Bélgica": "Inglés",
                "Irlanda": "Inglés", "Portugal": "Portugués"}
