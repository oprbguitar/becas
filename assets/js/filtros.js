/**
 * Motor de filtros: define los grupos, construye el panel, mantiene el estado
 * (sincronizado con la URL y con localStorage) y filtra el catálogo.
 */
import { normalizar, diasHasta, distanciaKm, estadoConvocatoria } from "./utils.js";
import { filtrosGuardados } from "./almacen.js";

/** Estado inicial de todos los filtros. */
export const estadoPorDefecto = () => ({
  q: "",
  regiones: [], paises: [], areas: [], niveles: [], coberturas: [],
  idiomas: [], modalidades: [], incluye: [],
  estado: "",            // abierta | por-cerrar | proxima | cerrada
  cierraDesde: "", cierraHasta: "",
  edad: "",              // edad del postulante
  duracionMax: 0,        // 0 = sin límite (meses)
  costoMax: -1,          // -1 = sin límite (USD de postulación)
  distanciaMax: 0,       // 0 = sin límite (km desde mi ubicación)
  soloGuardadas: false,
  orden: "cierre",
});

export const estado = estadoPorDefecto();

/* ------------------------------------------------------------------ */
/*  Definición de los grupos del panel                                 */
/* ------------------------------------------------------------------ */

const ORDEN_REGIONES = ["Perú", "Latinoamérica", "Norteamérica", "Europa", "Asia", "China", "Oceanía", "África", "Global"];

const unicos = (becas, campo) => {
  const set = new Set();
  becas.forEach((b) => (Array.isArray(b[campo]) ? b[campo] : [b[campo]]).forEach((v) => v && set.add(v)));
  return [...set];
};

export const LLAVES_INCLUYE = [
  ["matricula", "Matrícula"],
  ["manutencion", "Manutención mensual"],
  ["hospedaje", "Hospedaje / alojamiento"],
  ["pasajes", "Pasajes aéreos"],
  ["seguro", "Seguro médico"],
  ["curso_idioma", "Curso de idioma"],
  ["equipos", "Equipos o laptop"],
];

/** Describe los grupos que se dibujan en el panel derecho. */
export function definirGrupos(becas) {
  return [
    {
      id: "regiones", titulo: "Región del mundo", tipo: "chips", campo: "regiones", abierto: true,
      opciones: ORDEN_REGIONES.filter((r) => becas.some((b) => b.region === r)),
    },
    {
      id: "areas", titulo: "Especialidad o área", tipo: "chips", campo: "areas", abierto: true,
      opciones: unicos(becas, "areas").sort((a, b) => a.localeCompare(b, "es")),
    },
    {
      id: "niveles", titulo: "Nivel de estudios", tipo: "chips", campo: "niveles", abierto: true,
      opciones: ["Técnico", "Pregrado", "Maestría", "Doctorado", "Posdoctorado", "Curso corto", "Intercambio"]
        .filter((n) => becas.some((b) => b.niveles.includes(n))),
    },
    {
      id: "coberturas", titulo: "Cobertura económica", tipo: "chips", campo: "coberturas",
      opciones: ["Completa", "Parcial", "Matrícula", "Estipendio"].filter((c) => becas.some((b) => b.cobertura === c)),
    },
    {
      id: "incluye", titulo: "La beca debe incluir", tipo: "interruptores", campo: "incluye",
      opciones: LLAVES_INCLUYE,
    },
    { id: "fechas", titulo: "Fechas de postulación", tipo: "fechas", abierto: true },
    { id: "perfil", titulo: "Tu perfil: edad y tiempo", tipo: "perfil" },
    { id: "costo", titulo: "Costo de postulación", tipo: "costo" },
    { id: "distancia", titulo: "Distancia desde tu ubicación", tipo: "distancia" },
    {
      id: "paises", titulo: "País de destino", tipo: "select", campo: "paises",
      opciones: unicos(becas, "pais").sort((a, b) => a.localeCompare(b, "es")),
    },
    {
      id: "idiomas", titulo: "Idioma de estudio", tipo: "chips", campo: "idiomas",
      opciones: unicos(becas, "idiomas").sort((a, b) => a.localeCompare(b, "es")),
    },
    {
      id: "modalidades", titulo: "Modalidad", tipo: "chips", campo: "modalidades",
      opciones: unicos(becas, "modalidad").sort((a, b) => a.localeCompare(b, "es")),
    },
  ];
}

/* ------------------------------------------------------------------ */
/*  Índice de búsqueda: se calcula una sola vez por beca               */
/* ------------------------------------------------------------------ */
export function indexar(becas) {
  for (const b of becas) {
    b._busqueda = normalizar([
      b.nombre, b.organizacion, b.pais, b.ciudad, b.region, b.descripcion,
      b.niveles.join(" "), b.areas.join(" "), b.idiomas.join(" "),
      (b.requisitos || []).join(" "),
    ].join(" "));
    b._estado = estadoConvocatoria(b).clave;
  }
  return becas;
}

/* ------------------------------------------------------------------ */
/*  Filtrado                                                           */
/* ------------------------------------------------------------------ */

const RANGO_COBERTURA = { Completa: 4, Parcial: 3, Estipendio: 2, "Matrícula": 1 };

/**
 * Aplica todos los filtros activos al catálogo.
 * @param {object[]} becas catálogo completo ya indexado
 * @param {object} f estado de filtros
 * @param {{lat:number,lng:number}|null} miUbicacion origen para el filtro de distancia
 * @param {(id:string)=>boolean} estaGuardada
 */
export function filtrar(becas, f, miUbicacion, estaGuardada) {
  const termino = normalizar(f.q.trim());
  const palabras = termino ? termino.split(/\s+/) : [];
  const edad = f.edad === "" ? null : Number(f.edad);

  return becas.filter((b) => {
    if (palabras.length && !palabras.every((p) => b._busqueda.includes(p))) return false;
    if (f.soloGuardadas && !estaGuardada(b.id)) return false;

    if (f.regiones.length && !f.regiones.includes(b.region)) return false;
    if (f.paises.length && !f.paises.includes(b.pais)) return false;
    if (f.niveles.length && !f.niveles.some((n) => b.niveles.includes(n))) return false;
    if (f.coberturas.length && !f.coberturas.includes(b.cobertura)) return false;
    if (f.modalidades.length && !f.modalidades.includes(b.modalidad)) return false;
    if (f.idiomas.length && !f.idiomas.some((i) => b.idiomas.includes(i))) return false;

    // "Todas" en el catálogo significa que la beca acepta cualquier especialidad
    if (f.areas.length && !b.areas.includes("Todas") && !f.areas.some((a) => b.areas.includes(a))) return false;

    if (f.incluye.length && !f.incluye.every((k) => b.incluye?.[k])) return false;
    if (f.estado && b._estado !== f.estado) return false;

    if (f.cierraDesde && (!b.fecha_cierre || b.fecha_cierre < f.cierraDesde)) return false;
    if (f.cierraHasta && (!b.fecha_cierre || b.fecha_cierre > f.cierraHasta)) return false;

    if (edad !== null && !Number.isNaN(edad)) {
      if (b.edad_min != null && edad < b.edad_min) return false;
      if (b.edad_max != null && edad > b.edad_max) return false;
    }

    if (f.duracionMax > 0 && b.duracion_meses > f.duracionMax) return false;
    if (f.costoMax >= 0 && (b.costo_postulacion_usd ?? 0) > f.costoMax) return false;

    if (f.distanciaMax > 0) {
      if (!miUbicacion) return false;
      b._distancia = distanciaKm(miUbicacion.lat, miUbicacion.lng, b.lat, b.lng);
      if (b._distancia > f.distanciaMax) return false;
    }
    return true;
  });
}

/** Ordena el resultado según el criterio elegido. */
export function ordenar(lista, criterio, miUbicacion) {
  const copia = [...lista];
  const lejos = 10 ** 9;
  const cmp = {
    cierre: (a, b) => (diasHasta(a.fecha_cierre) ?? lejos) - (diasHasta(b.fecha_cierre) ?? lejos),
    apertura: (a, b) => String(b.fecha_apertura).localeCompare(String(a.fecha_apertura)),
    nombre: (a, b) => a.nombre.localeCompare(b.nombre, "es"),
    cobertura: (a, b) => (RANGO_COBERTURA[b.cobertura] || 0) - (RANGO_COBERTURA[a.cobertura] || 0),
    duracion: (a, b) => (b.duracion_meses || 0) - (a.duracion_meses || 0),
    distancia: (a, b) => {
      if (!miUbicacion) return 0;
      const d = (x) => (x._distancia ??= distanciaKm(miUbicacion.lat, miUbicacion.lng, x.lat, x.lng));
      return d(a) - d(b);
    },
  }[criterio] || (() => 0);

  // Las convocatorias cerradas siempre bajan al final del listado
  return copia.sort((a, b) => {
    const ca = a._estado === "cerrada" ? 1 : 0;
    const cb = b._estado === "cerrada" ? 1 : 0;
    return ca - cb || cmp(a, b) || (b.destacada === true) - (a.destacada === true);
  });
}

/* ------------------------------------------------------------------ */
/*  Sincronización con la URL y con la última sesión                   */
/* ------------------------------------------------------------------ */

const LISTAS = ["regiones", "paises", "areas", "niveles", "coberturas", "idiomas", "modalidades", "incluye"];
const TEXTOS = ["q", "estado", "cierraDesde", "cierraHasta", "edad", "orden"];
const NUMEROS = ["duracionMax", "costoMax", "distanciaMax"];

export function leerURL(f) {
  const p = new URLSearchParams(location.search);
  if (![...p.keys()].length) return false;
  LISTAS.forEach((k) => { if (p.has(k)) f[k] = p.get(k).split("|").filter(Boolean); });
  TEXTOS.forEach((k) => { if (p.has(k)) f[k] = p.get(k); });
  NUMEROS.forEach((k) => { if (p.has(k)) f[k] = Number(p.get(k)); });
  if (p.has("soloGuardadas")) f.soloGuardadas = p.get("soloGuardadas") === "1";
  return true;
}

export function escribirURL(f) {
  const p = new URLSearchParams();
  LISTAS.forEach((k) => { if (f[k].length) p.set(k, f[k].join("|")); });
  TEXTOS.forEach((k) => { if (f[k]) p.set(k, f[k]); });
  NUMEROS.forEach((k) => { if (f[k] !== estadoPorDefecto()[k]) p.set(k, String(f[k])); });
  if (f.soloGuardadas) p.set("soloGuardadas", "1");
  const url = p.toString() ? `?${p}` : location.pathname;
  history.replaceState(null, "", url);
  filtrosGuardados.escribir(f);
}

export function restaurarSesion(f) {
  const previo = filtrosGuardados.leer();
  if (!previo) return false;
  Object.assign(f, { ...estadoPorDefecto(), ...previo, q: "" });
  return true;
}

/** Lista legible de los filtros activos, para los chips del listado. */
export function chipsActivos(f) {
  const chips = [];
  const etiquetaIncluye = Object.fromEntries(LLAVES_INCLUYE);
  LISTAS.forEach((k) => f[k].forEach((v) =>
    chips.push({ campo: k, valor: v, texto: k === "incluye" ? `Incluye ${etiquetaIncluye[v] || v}` : v })));
  if (f.q) chips.push({ campo: "q", valor: f.q, texto: `“${f.q}”` });
  if (f.estado) chips.push({ campo: "estado", valor: f.estado, texto: `Estado: ${f.estado.replace("-", " ")}` });
  if (f.cierraDesde) chips.push({ campo: "cierraDesde", valor: f.cierraDesde, texto: `Cierra desde ${f.cierraDesde}` });
  if (f.cierraHasta) chips.push({ campo: "cierraHasta", valor: f.cierraHasta, texto: `Cierra hasta ${f.cierraHasta}` });
  if (f.edad !== "") chips.push({ campo: "edad", valor: f.edad, texto: `${f.edad} años` });
  if (f.duracionMax > 0) chips.push({ campo: "duracionMax", valor: 0, texto: `Hasta ${f.duracionMax} meses` });
  if (f.costoMax >= 0) chips.push({ campo: "costoMax", valor: -1, texto: `Postulación ≤ US$ ${f.costoMax}` });
  if (f.distanciaMax > 0) chips.push({ campo: "distanciaMax", valor: 0, texto: `A menos de ${f.distanciaMax} km` });
  if (f.soloGuardadas) chips.push({ campo: "soloGuardadas", valor: false, texto: "Solo mis guardadas" });
  return chips;
}
