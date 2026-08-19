/**
 * Construcción del DOM: panel de filtros, tarjetas de beca y panel de guardadas.
 * Todo se crea con la API del navegador (sin innerHTML con datos externos).
 */
import { bandera, fechaLegible, diasHasta, estadoConvocatoria, distanciaKm } from "./utils.js";
import { LLAVES_INCLUYE } from "./filtros.js";

const el = (tag, clase, texto) => {
  const n = document.createElement(tag);
  if (clase) n.className = clase;
  if (texto != null) n.textContent = texto;
  return n;
};

/* ==================================================================== */
/*  PANEL DE FILTROS                                                     */
/* ==================================================================== */

/**
 * Dibuja el panel derecho.
 * @param {HTMLElement} raiz contenedor
 * @param {object[]} grupos definición de grupos
 * @param {object} f estado de filtros (se muta al interactuar)
 * @param {Function} alCambiar callback tras cada cambio
 * @param {object} api utilidades del anfitrión (geolocalización)
 */
export function construirFiltros(raiz, grupos, f, alCambiar, api) {
  raiz.textContent = "";
  const frag = document.createDocumentFragment();

  for (const g of grupos) {
    const cont = el("section", `fgrupo${g.abierto ? "" : " is-cerrado"}`);
    cont.dataset.grupo = g.id;

    const cab = el("button", "fgrupo__cab");
    cab.type = "button";
    cab.setAttribute("aria-expanded", String(!!g.abierto));
    cab.append(el("span", null, g.titulo));
    const contador = el("span", "fgrupo__n");
    contador.hidden = true;
    cab.append(contador);
    cab.insertAdjacentHTML("beforeend",
      '<svg class="fgrupo__flecha" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>');
    cab.addEventListener("click", () => {
      const cerrado = cont.classList.toggle("is-cerrado");
      cab.setAttribute("aria-expanded", String(!cerrado));
    });

    const cuerpo = el("div", "fgrupo__cuerpo");
    cuerpo.append(...cuerpoDeGrupo(g, f, alCambiar, api));

    cont.append(cab, cuerpo);
    frag.append(cont);
  }
  raiz.append(frag);
  actualizarContadores(raiz, f);
}

function cuerpoDeGrupo(g, f, alCambiar, api) {
  switch (g.tipo) {
    case "chips":         return [chips(g, f, alCambiar)];
    case "interruptores": return [interruptores(g, f, alCambiar)];
    case "select":        return [selectMultiple(g, f, alCambiar)];
    case "fechas":        return camposFecha(f, alCambiar);
    case "perfil":        return camposPerfil(f, alCambiar);
    case "costo":         return camposCosto(f, alCambiar);
    case "distancia":     return camposDistancia(f, alCambiar, api);
    default:              return [];
  }
}

function chips(g, f, alCambiar) {
  const caja = el("div", "opciones");
  for (const op of g.opciones) {
    const lab = el("label", "opcion");
    const inp = el("input");
    inp.type = "checkbox";
    inp.value = op;
    inp.checked = f[g.campo].includes(op);
    inp.addEventListener("change", () => {
      const lista = f[g.campo];
      const i = lista.indexOf(op);
      if (inp.checked && i < 0) lista.push(op);
      if (!inp.checked && i >= 0) lista.splice(i, 1);
      alCambiar();
    });
    lab.append(inp, el("span", null, op));
    caja.append(lab);
  }
  return caja;
}

function interruptores(g, f, alCambiar) {
  const caja = el("div", "opciones");
  caja.style.flexDirection = "column";
  caja.style.gap = "2px";
  for (const [clave, etiqueta] of g.opciones) {
    const lab = el("label", "interruptor");
    const inp = el("input");
    inp.type = "checkbox";
    inp.checked = f.incluye.includes(clave);
    inp.addEventListener("change", () => {
      const i = f.incluye.indexOf(clave);
      if (inp.checked && i < 0) f.incluye.push(clave);
      if (!inp.checked && i >= 0) f.incluye.splice(i, 1);
      alCambiar();
    });
    lab.append(inp, el("span", "interruptor__pista"), el("span", null, etiqueta));
    caja.append(lab);
  }
  return caja;
}

function selectMultiple(g, f, alCambiar) {
  const sel = el("select", "select");
  sel.append(new Option("Todos los países", ""));
  g.opciones.forEach((op) => sel.append(new Option(op, op)));
  sel.value = f[g.campo][0] || "";
  sel.addEventListener("change", () => {
    f[g.campo] = sel.value ? [sel.value] : [];
    alCambiar();
  });
  return sel;
}

function camposFecha(f, alCambiar) {
  const estadoSel = el("select", "select");
  [["", "Cualquier estado"], ["abierta", "Abiertas ahora"], ["por-cerrar", "Cierran en 15 días"],
   ["proxima", "Próximas a abrir"], ["cerrada", "Cerradas (referencia)"]]
    .forEach(([v, t]) => estadoSel.append(new Option(t, v)));
  estadoSel.value = f.estado;
  estadoSel.addEventListener("change", () => { f.estado = estadoSel.value; alCambiar(); });

  const fila = el("div", "fila");
  const desde = campoFecha("Cierra desde", f.cierraDesde, (v) => { f.cierraDesde = v; alCambiar(); });
  const hasta = campoFecha("Cierra hasta", f.cierraHasta, (v) => { f.cierraHasta = v; alCambiar(); });
  fila.append(desde, hasta);

  return [estadoSel, fila, el("p", "ayuda",
    "Las convocatorias se repiten cada año: si una ya cerró, sus fechas te sirven de referencia para la siguiente.")];
}

function campoFecha(etiqueta, valor, onInput) {
  const caja = el("div");
  const lab = el("label", "etiqueta", etiqueta);
  const inp = el("input", "campo");
  inp.type = "date";
  inp.value = valor || "";
  lab.htmlFor = inp.id = `f-${etiqueta.replace(/\s+/g, "-").toLowerCase()}`;
  inp.addEventListener("change", () => onInput(inp.value));
  caja.append(lab, inp);
  return caja;
}

function camposPerfil(f, alCambiar) {
  const cajaEdad = el("div");
  const labEdad = el("label", "etiqueta", "Tu edad (filtra por rango aceptado)");
  const edad = el("input", "campo");
  edad.type = "number";
  edad.min = "14"; edad.max = "99"; edad.placeholder = "Ej. 24";
  edad.value = f.edad;
  labEdad.htmlFor = edad.id = "f-edad";
  edad.addEventListener("input", () => { f.edad = edad.value; alCambiar(); });
  cajaEdad.append(labEdad, edad);

  const dur = deslizador({
    id: "f-duracion", etiqueta: "Duración máxima del programa",
    min: 0, max: 60, paso: 6, valor: f.duracionMax,
    formato: (v) => (v === 0 ? "Cualquier duración" : `Hasta ${v} meses (${(v / 12).toFixed(1)} años)`),
    alSoltar: (v) => { f.duracionMax = v; alCambiar(); },
  });
  return [cajaEdad, dur];
}

function camposCosto(f, alCambiar) {
  const d = deslizador({
    id: "f-costo", etiqueta: "Costo máximo de postular",
    min: -1, max: 300, paso: 10, valor: f.costoMax,
    formato: (v) => (v < 0 ? "Sin límite" : v === 0 ? "Solo becas gratuitas" : `Hasta US$ ${v}`),
    alSoltar: (v) => { f.costoMax = v; alCambiar(); },
  });
  return [d, el("p", "ayuda", "Casi todas las becas del catálogo son gratuitas de postular; el costo real de estudiar lo cubre la beca.")];
}

function camposDistancia(f, alCambiar, api) {
  const d = deslizador({
    id: "f-distancia", etiqueta: "Distancia máxima al destino",
    min: 0, max: 20000, paso: 500, valor: f.distanciaMax,
    formato: (v) => (v === 0 ? "Sin límite de distancia" : `A menos de ${v.toLocaleString("es")} km`),
    alSoltar: (v) => { f.distanciaMax = v; alCambiar(); },
  });

  const btn = el("button", "btn btn--soft btn--sm js-ripple", "Usar mi ubicación");
  btn.type = "button";
  const aviso = el("p", "ayuda", api.ubicacionTexto());
  btn.addEventListener("click", async () => {
    btn.disabled = true;
    btn.textContent = "Ubicando…";
    const ok = await api.pedirUbicacion();
    btn.disabled = false;
    btn.textContent = ok ? "Ubicación actualizada" : "Reintentar ubicación";
    aviso.textContent = api.ubicacionTexto();
    alCambiar();
  });

  const ciudad = el("select", "select");
  ciudad.append(new Option("O elige una ciudad de referencia", ""));
  api.ciudades().forEach(([nombre]) => ciudad.append(new Option(nombre, nombre)));
  ciudad.value = api.ciudadElegida();
  ciudad.addEventListener("change", () => {
    api.fijarCiudad(ciudad.value);
    aviso.textContent = api.ubicacionTexto();
    alCambiar();
  });

  return [d, btn, ciudad, aviso];
}

function deslizador({ id, etiqueta, min, max, paso, valor, formato, alSoltar }) {
  const caja = el("div", "rango");
  const lab = el("label", "etiqueta", etiqueta);
  const inp = el("input");
  inp.type = "range";
  inp.min = String(min); inp.max = String(max); inp.step = String(paso);
  inp.value = String(valor);
  lab.htmlFor = inp.id = id;
  const salida = el("output", "rango__valor", formato(Number(valor)));
  inp.addEventListener("input", () => { salida.textContent = formato(Number(inp.value)); });
  inp.addEventListener("change", () => alSoltar(Number(inp.value)));
  caja.append(lab, inp, salida);
  return caja;
}

/** Muestra en la cabecera de cada grupo cuántos filtros tiene activos. */
export function actualizarContadores(raiz, f) {
  const mapa = {
    regiones: f.regiones.length, areas: f.areas.length, niveles: f.niveles.length,
    coberturas: f.coberturas.length, incluye: f.incluye.length, paises: f.paises.length,
    idiomas: f.idiomas.length, modalidades: f.modalidades.length,
    fechas: (f.estado ? 1 : 0) + (f.cierraDesde ? 1 : 0) + (f.cierraHasta ? 1 : 0),
    perfil: (f.edad !== "" ? 1 : 0) + (f.duracionMax > 0 ? 1 : 0),
    costo: f.costoMax >= 0 ? 1 : 0,
    distancia: f.distanciaMax > 0 ? 1 : 0,
  };
  for (const [id, n] of Object.entries(mapa)) {
    const marca = raiz.querySelector(`[data-grupo="${id}"] .fgrupo__n`);
    if (!marca) continue;
    marca.hidden = n === 0;
    marca.textContent = String(n);
  }
}

/* ==================================================================== */
/*  TARJETA DE BECA                                                      */
/* ==================================================================== */

const PLANTILLA = () => document.getElementById("tpl-beca").content.firstElementChild;
const ETIQUETAS_INCLUYE = Object.fromEntries(LLAVES_INCLUYE);

export function crearTarjeta(beca, { guardada, alGuardar, miUbicacion, retardo = 0 }) {
  const n = PLANTILLA().cloneNode(true);
  n.style.setProperty("--retardo", `${retardo}ms`);
  n.dataset.id = beca.id;
  if (beca.destacada) n.classList.add("is-destacada");

  n.querySelector(".card__bandera").textContent = bandera(beca.pais);
  n.querySelector(".card__pais").textContent = `${beca.pais} · ${beca.region}`;
  n.querySelector(".card__titulo").textContent = beca.nombre;
  n.querySelector(".card__org").textContent = beca.organizacion;
  n.querySelector(".card__desc").textContent = beca.descripcion;

  // Etiquetas: nivel, cobertura y lo que incluye
  const tags = n.querySelector(".card__tags");
  const tag = (texto, tono = "") => {
    const li = el("li", `pill${tono ? ` pill--${tono}` : ""}`, texto);
    tags.append(li);
  };
  beca.niveles.slice(0, 3).forEach((x) => tag(x, "marca"));
  tag(`Cobertura ${beca.cobertura.toLowerCase()}`, beca.cobertura === "Completa" ? "exito" : "apoyo");
  Object.entries(beca.incluye || {})
    .filter(([, v]) => v)
    .slice(0, 3)
    .forEach(([k]) => tag(ETIQUETAS_INCLUYE[k] || k));

  // Datos clave
  const datos = n.querySelector(".card__datos");
  const dato = (titulo, valor) => {
    const d = el("div", "card__dato");
    d.append(el("dt", null, titulo), el("dd", null, valor));
    datos.append(d);
  };
  dato("Cierre", fechaLegible(beca.fecha_cierre));
  dato("Edad", beca.edad_min || beca.edad_max ? `${beca.edad_min ?? "—"} a ${beca.edad_max ?? "—"} años` : "Sin límite");
  dato("Duración", beca.duracion_meses ? `${beca.duracion_meses} meses` : "Variable");
  const distancia = miUbicacion ? distanciaKm(miUbicacion.lat, miUbicacion.lng, beca.lat, beca.lng) : null;
  dato(distancia != null ? "Distancia" : "Idioma",
       distancia != null ? `${distancia.toLocaleString("es")} km` : beca.idiomas.join(" / "));

  // Estado de la convocatoria + barra de tiempo restante
  const est = estadoConvocatoria(beca);
  const zona = n.querySelector(".card__estado");
  zona.append(el("span", `pill pill--${est.tono || "marca"}`, est.texto));
  const dias = diasHasta(beca.fecha_cierre);
  if (dias != null && dias >= 0) {
    const barra = el("div", "barra-tiempo");
    const relleno = el("div", "barra-tiempo__relleno");
    const pct = Math.max(4, Math.min(100, (dias / 180) * 100));
    relleno.style.width = `${pct}%`;
    if (dias <= 15) relleno.classList.add("is-baja");
    else if (dias <= 45) relleno.classList.add("is-media");
    barra.append(relleno);
    barra.title = `Faltan ${dias} días para el cierre`;
    zona.append(barra);
  }

  // Requisitos (los actualiza el rastreador automático)
  const req = beca.requisitos || [];
  n.querySelector(".card__req-n").textContent = `(${req.length})`;
  const lista = n.querySelector(".card__req-lista");
  req.forEach((r) => lista.append(el("li", null, r)));
  n.querySelector(".card__req-fuente").textContent = beca.requisitos_actualizados
    ? `Requisitos leídos de la web oficial el ${fechaLegible(beca.requisitos_actualizados)}.`
    : "Resumen de las bases oficiales. Confirma siempre en el enlace.";

  // Enlaces directos
  const postular = n.querySelector(".card__postular");
  postular.href = beca.url;
  postular.setAttribute("aria-label", `Postular a ${beca.nombre} (se abre en una pestaña nueva)`);
  const bases = n.querySelector(".card__requisitos");
  bases.href = beca.url_requisitos || beca.url;

  // Guardar / quitar
  const btn = n.querySelector(".card__guardar");
  aplicarEstadoGuardado(btn, guardada, beca.nombre);
  btn.addEventListener("click", () => {
    const ahora = alGuardar(beca);
    aplicarEstadoGuardado(btn, ahora, beca.nombre);
    btn.classList.remove("is-latiendo");
    void btn.offsetWidth;      // reinicia la animación
    btn.classList.add("is-latiendo");
  });

  return n;
}

function aplicarEstadoGuardado(btn, guardada, nombre) {
  btn.setAttribute("aria-pressed", String(guardada));
  btn.setAttribute("aria-label", `${guardada ? "Quitar" : "Guardar"} ${nombre} ${guardada ? "de" : "en"} mis becas`);
  btn.title = guardada ? "Quitar de mis becas" : "Guardar en mis becas";
}

/* ==================================================================== */
/*  PANEL DE GUARDADAS                                                   */
/* ==================================================================== */

export function pintarGuardadas(lista, contenedor, { alQuitar, alAbrir }) {
  contenedor.textContent = "";
  const frag = document.createDocumentFragment();
  const ordenadas = [...lista].sort(
    (a, b) => (diasHasta(a.fecha_cierre) ?? 1e9) - (diasHasta(b.fecha_cierre) ?? 1e9));

  for (const g of ordenadas) {
    const li = el("li", "guardada");
    li.dataset.id = g.id;

    const titulo = el("p", "guardada__nombre");
    const enlace = el("a", null, g.nombre);
    enlace.href = g.url;
    enlace.target = "_blank";
    enlace.rel = "noopener noreferrer";
    titulo.append(enlace);

    const est = estadoConvocatoria(g);
    const meta = el("p", "guardada__meta",
      `${bandera(g.pais)} ${g.pais} · ${fechaLegible(g.fecha_cierre, true)}`);
    const pill = el("span", `pill pill--sm pill--${est.tono || "marca"}`, est.texto);

    const quitar = el("button", "guardada__quitar", "×");
    quitar.type = "button";
    quitar.setAttribute("aria-label", `Quitar ${g.nombre} de mis becas`);
    quitar.addEventListener("click", () => {
      li.classList.add("is-saliendo");
      li.addEventListener("animationend", () => alQuitar(g.id), { once: true });
    });

    li.addEventListener("dblclick", () => alAbrir(g.id));
    li.append(titulo, meta, pill, quitar);
    frag.append(li);
  }
  contenedor.append(frag);
}
