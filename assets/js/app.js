/**
 * BecaRadar — punto de entrada.
 * Carga el catálogo, conecta filtros, listado y panel de guardadas.
 */
import { retardar, porFrame, animarContador, activarOndas, fechaLegible } from "./utils.js";
import { almacen, tema } from "./almacen.js";
import {
  estado, estadoPorDefecto, definirGrupos, indexar, filtrar, ordenar,
  leerURL, escribirURL, restaurarSesion, chipsActivos,
} from "./filtros.js";
import { construirFiltros, actualizarContadores, crearTarjeta, pintarGuardadas } from "./interfaz.js";

const $ = (sel) => document.querySelector(sel);
const POR_PAGINA = 24;

const app = {
  becas: [],
  visibles: [],
  mostradas: 0,
  meta: {},
  miUbicacion: null,
  ciudadElegida: "",
  ciudades: [
    ["Lima, Perú", -12.0464, -77.0428], ["Arequipa, Perú", -16.409, -71.5375],
    ["Trujillo, Perú", -8.109, -79.0215], ["Bogotá, Colombia", 4.711, -74.0721],
    ["Santiago, Chile", -33.4489, -70.6693], ["Buenos Aires, Argentina", -34.6037, -58.3816],
    ["Ciudad de México", 19.4326, -99.1332], ["São Paulo, Brasil", -23.5505, -46.6333],
    ["Madrid, España", 40.4168, -3.7038], ["Miami, EE. UU.", 25.7617, -80.1918],
  ],
};

/* ---------------------------------------------------------------- Tema */
function iniciarTema() {
  tema.aplicar(tema.leer());
  $("#btn-tema").addEventListener("click", () => {
    const nuevo = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    tema.aplicar(nuevo);
  });
}

/* --------------------------------------------------------- Ubicación */
const apiUbicacion = {
  ciudades: () => app.ciudades,
  ciudadElegida: () => app.ciudadElegida,
  fijarCiudad(nombre) {
    app.ciudadElegida = nombre;
    const c = app.ciudades.find(([n]) => n === nombre);
    app.miUbicacion = c ? { lat: c[1], lng: c[2], etiqueta: nombre } : null;
  },
  ubicacionTexto() {
    if (!app.miUbicacion) return "Aún no defines desde dónde medir la distancia.";
    return `Midiendo distancias desde ${app.miUbicacion.etiqueta}.`;
  },
  pedirUbicacion() {
    return new Promise((resolve) => {
      if (!navigator.geolocation) return resolve(false);
      navigator.geolocation.getCurrentPosition(
        ({ coords }) => {
          app.miUbicacion = { lat: coords.latitude, lng: coords.longitude, etiqueta: "tu ubicación actual" };
          app.ciudadElegida = "";
          resolve(true);
        },
        () => resolve(false),
        { timeout: 8000, maximumAge: 600000 },
      );
    });
  },
};

/* ------------------------------------------------------ Carga de datos */
async function cargarCatalogo() {
  const grid = $("#grid-becas");
  grid.append(...Array.from({ length: 6 }, () => {
    const s = document.createElement("div");
    s.className = "skeleton";
    return s;
  }));

  const [becas, meta] = await Promise.all([
    fetch("data/becas.json", { cache: "no-cache" }).then((r) => r.json()),
    fetch("data/meta.json", { cache: "no-cache" }).then((r) => r.json()).catch(() => ({})),
  ]);
  app.becas = indexar(becas);
  app.meta = meta;
  grid.textContent = "";
}

/* --------------------------------------------------------- Render */
function render({ reiniciar = true } = {}) {
  if (reiniciar) {
    app.visibles = ordenar(
      filtrar(app.becas, estado, app.miUbicacion, (id) => almacen.tiene(id)),
      estado.orden, app.miUbicacion,
    );
    app.mostradas = 0;
    $("#grid-becas").textContent = "";
  }

  const grid = $("#grid-becas");
  const lote = app.visibles.slice(app.mostradas, app.mostradas + POR_PAGINA);
  const frag = document.createDocumentFragment();
  lote.forEach((beca, i) => frag.append(crearTarjeta(beca, {
    guardada: almacen.tiene(beca.id),
    alGuardar: alternarGuardado,
    miUbicacion: app.miUbicacion,
    retardo: Math.min(i * 28, 420),
  })));
  grid.append(frag);
  app.mostradas += lote.length;

  const total = app.visibles.length;
  $("#conteo").textContent = total;
  $("#conteo-movil").textContent = total;
  $("#conteo-total").textContent = total === app.becas.length ? "· catálogo completo" : `de ${app.becas.length}`;
  $("#resultados-vacio").hidden = total > 0;
  $("#cargar-mas").hidden = app.mostradas >= total;
  $("#btn-cargar-mas").textContent = `Ver ${Math.min(POR_PAGINA, total - app.mostradas)} becas más`;

  pintarChips();
  actualizarContadores($("#filtros"), estado);
  escribirURL(estado);
}

const renderDiferido = retardar(render, 160);

function pintarChips() {
  const cont = $("#chips-activos");
  cont.textContent = "";
  const chips = chipsActivos(estado);
  for (const c of chips) {
    const chip = document.createElement("span");
    chip.className = "chip-activo";
    chip.append(document.createTextNode(c.texto));
    const x = document.createElement("button");
    x.type = "button";
    x.textContent = "×";
    x.setAttribute("aria-label", `Quitar filtro ${c.texto}`);
    x.addEventListener("click", () => quitarFiltro(c));
    chip.append(x);
    cont.append(chip);
  }
  if (chips.length > 1) {
    const limpiar = document.createElement("button");
    limpiar.className = "btn btn--ghost btn--sm js-ripple";
    limpiar.textContent = "Limpiar todo";
    limpiar.addEventListener("click", limpiarFiltros);
    cont.append(limpiar);
  }
}

function quitarFiltro({ campo, valor }) {
  if (Array.isArray(estado[campo])) estado[campo] = estado[campo].filter((v) => v !== valor);
  else estado[campo] = valor;
  if (campo === "q") $("#q").value = "";
  reconstruirPanel();
  render();
}

function limpiarFiltros() {
  Object.assign(estado, estadoPorDefecto());
  $("#q").value = "";
  $("#btn-limpiar-q").hidden = true;
  $("#orden").value = estado.orden;
  reconstruirPanel();
  render();
}

function reconstruirPanel() {
  construirFiltros($("#filtros"), definirGrupos(app.becas), estado, renderDiferido, apiUbicacion);
}

/* ------------------------------------------------------- Guardadas */
function alternarGuardado(beca) {
  const guardada = almacen.alternar(beca);
  return guardada;
}

function sincronizarGuardadas() {
  const lista = almacen.lista();
  $("#contador-guardadas").textContent = lista.length;
  $("#guardadas-vacio").hidden = lista.length > 0;
  $("#guardadas-resumen").hidden = lista.length === 0;

  pintarGuardadas(lista, $("#lista-guardadas"), {
    alQuitar: (id) => almacen.quitar(id),
    alAbrir: (id) => irATarjeta(id),
  });

  if (lista.length) {
    const abiertas = lista.filter((g) => {
      const d = g.fecha_cierre ? (new Date(`${g.fecha_cierre}T12:00:00Z`) - Date.now()) / 86400000 : -1;
      return d >= 0;
    });
    $("#resumen-abiertas").textContent = `${abiertas.length} vigente${abiertas.length === 1 ? "" : "s"}`;
    const proxima = abiertas.sort((a, b) => a.fecha_cierre.localeCompare(b.fecha_cierre))[0];
    $("#resumen-proxima").textContent = proxima
      ? `Próximo cierre: ${fechaLegible(proxima.fecha_cierre, true)}`
      : "Sin cierres próximos";
  }

  // Refleja el estado en las tarjetas ya pintadas
  document.querySelectorAll(".card").forEach((card) => {
    const btn = card.querySelector(".card__guardar");
    const guardada = almacen.tiene(card.dataset.id);
    btn.setAttribute("aria-pressed", String(guardada));
  });

  if (estado.soloGuardadas) render();
}

function irATarjeta(id) {
  const card = document.querySelector(`.card[data-id="${CSS.escape(id)}"]`);
  if (!card) return;
  card.scrollIntoView({ behavior: "smooth", block: "center" });
  card.focus({ preventScroll: true });
}

/* --------------------------------------------------------- Portada */
function pintarPortada() {
  const hoy = new Date().toISOString().slice(0, 10);
  const paises = new Set(app.becas.map((b) => b.pais)).size;
  const abiertas = app.becas.filter((b) => b.fecha_cierre >= hoy && b.fecha_apertura <= hoy).length;
  const completas = app.becas.filter((b) => b.cobertura === "Completa").length;
  const nums = [...document.querySelectorAll("[data-contador]")];
  [app.becas.length, paises, abiertas, completas].forEach((v, i) => nums[i] && animarContador(nums[i], v));
  $("#hero-total").textContent = app.becas.length;
  $("#pie-total").textContent = app.becas.length;
  $("#pie-actualizado").textContent = app.meta.actualizado ? fechaLegible(app.meta.actualizado) : "—";

  const atajos = [
    { texto: "🇵🇪 Becas en Perú", aplicar: () => { estado.regiones = ["Perú"]; } },
    { texto: "🇨🇳 Estudiar en China", aplicar: () => { estado.regiones = ["China"]; } },
    { texto: "🇪🇺 Europa con beca completa", aplicar: () => { estado.regiones = ["Europa"]; estado.coberturas = ["Completa"]; } },
    { texto: "🎓 Maestrías 100% cubiertas", aplicar: () => { estado.niveles = ["Maestría"]; estado.coberturas = ["Completa"]; } },
    { texto: "⏳ Cierran este mes", aplicar: () => { estado.estado = "por-cerrar"; } },
    { texto: "✈️ Incluyen pasajes y hospedaje", aplicar: () => { estado.incluye = ["pasajes", "hospedaje"]; } },
    { texto: "💻 Cursos en línea gratis", aplicar: () => { estado.modalidades = ["Virtual"]; } },
    { texto: "🔖 Solo mis guardadas", aplicar: () => { estado.soloGuardadas = true; } },
  ];
  const cont = $("#atajos");
  atajos.forEach((a) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "atajo js-ripple";
    btn.textContent = a.texto;
    btn.addEventListener("click", () => {
      Object.assign(estado, estadoPorDefecto());
      a.aplicar();
      $("#q").value = "";
      reconstruirPanel();
      render();
      $("#resultados").scrollIntoView({ behavior: "smooth", block: "start" });
    });
    cont.append(btn);
  });
}

/* ------------------------------------------------------------ Eventos */
function conectarEventos() {
  const q = $("#q");
  const limpiarQ = $("#btn-limpiar-q");
  q.addEventListener("input", () => {
    estado.q = q.value;
    limpiarQ.hidden = !q.value;
    renderDiferido();
  });
  limpiarQ.addEventListener("click", () => {
    q.value = ""; estado.q = ""; limpiarQ.hidden = true; q.focus(); render();
  });
  $("#form-busqueda").addEventListener("submit", (e) => {
    e.preventDefault();
    q.blur();
    $("#resultados").scrollIntoView({ behavior: "smooth", block: "start" });
  });

  $("#orden").addEventListener("change", (e) => { estado.orden = e.target.value; render(); });
  $("#btn-cargar-mas").addEventListener("click", () => render({ reiniciar: false }));
  $("#btn-reset").addEventListener("click", limpiarFiltros);
  $("#btn-reset-vacio").addEventListener("click", limpiarFiltros);

  // Paneles deslizantes en pantallas pequeñas
  const overlay = $("#overlay");
  const abrir = (panel, boton) => {
    panel.classList.add("is-abierto");
    overlay.hidden = false;
    boton?.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
  };
  const cerrarTodo = () => {
    $("#panel-filtros").classList.remove("is-abierto");
    $("#panel-guardadas").classList.remove("is-abierto");
    overlay.hidden = true;
    $("#btn-abrir-filtros").setAttribute("aria-expanded", "false");
    $("#btn-abrir-guardadas").setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  };
  $("#btn-abrir-filtros").addEventListener("click", () => abrir($("#panel-filtros"), $("#btn-abrir-filtros")));
  $("#btn-filtros-flotante").addEventListener("click", () => abrir($("#panel-filtros")));
  $("#btn-abrir-guardadas").addEventListener("click", () => {
    if (matchMedia("(max-width: 860px)").matches) abrir($("#panel-guardadas"), $("#btn-abrir-guardadas"));
    else $("#panel-guardadas").scrollIntoView({ behavior: "smooth", block: "center" });
  });
  $("#btn-cerrar-filtros").addEventListener("click", cerrarTodo);
  $("#btn-cerrar-guardadas").addEventListener("click", cerrarTodo);
  $("#btn-aplicar-movil").addEventListener("click", cerrarTodo);
  overlay.addEventListener("click", cerrarTodo);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") cerrarTodo();
    if (e.key === "/" && document.activeElement !== q) { e.preventDefault(); q.focus(); }
  });

  // Exportar / importar / vaciar
  $("#btn-exportar").addEventListener("click", () => {
    const blob = new Blob([almacen.exportar()], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `mis-becas-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
  });
  $("#input-importar").addEventListener("change", async (e) => {
    const archivo = e.target.files?.[0];
    if (!archivo) return;
    try {
      const nuevas = almacen.importar(await archivo.text());
      avisar(`${nuevas} beca${nuevas === 1 ? "" : "s"} importada${nuevas === 1 ? "" : "s"}.`);
    } catch {
      avisar("No pudimos leer ese archivo.");
    }
    e.target.value = "";
  });
  $("#btn-vaciar").addEventListener("click", () => {
    if (almacen.total() && confirm("¿Quitar todas las becas guardadas de este navegador?")) almacen.vaciar();
  });

  // Barra de progreso de lectura + sombra de la cabecera
  const topbar = $("#topbar");
  const barra = $("#barra-progreso");
  addEventListener("scroll", porFrame(() => {
    const y = scrollY;
    topbar.classList.toggle("is-scrolled", y > 8);
    const alto = document.documentElement.scrollHeight - innerHeight;
    barra.style.width = `${alto > 0 ? (y / alto) * 100 : 0}%`;
  }), { passive: true });

  // Carga progresiva al llegar al final del listado
  const centinela = $("#cargar-mas");
  new IntersectionObserver((entradas) => {
    if (entradas[0].isIntersecting && !centinela.hidden) render({ reiniciar: false });
  }, { rootMargin: "300px" }).observe(centinela);
}

function avisar(texto) {
  const t = document.createElement("div");
  t.textContent = texto;
  t.setAttribute("role", "status");
  t.style.cssText = "position:fixed;left:50%;bottom:22px;transform:translateX(-50%);z-index:120;" +
    "padding:11px 18px;border-radius:999px;background:var(--texto);color:var(--fondo);" +
    "font-size:13px;font-weight:600;box-shadow:var(--sombra-md);animation:entrar .25s var(--curva)";
  document.body.append(t);
  setTimeout(() => t.remove(), 3200);
}

/* --------------------------------------------------------------- Inicio */
async function iniciar() {
  iniciarTema();
  activarOndas();
  try {
    await cargarCatalogo();
  } catch {
    $("#grid-becas").innerHTML =
      '<p class="vacio">No pudimos cargar el catálogo. Revisa tu conexión y recarga la página.</p>';
    return;
  }
  if (!leerURL(estado)) restaurarSesion(estado);
  $("#q").value = estado.q;
  $("#btn-limpiar-q").hidden = !estado.q;
  $("#orden").value = estado.orden;

  pintarPortada();
  reconstruirPanel();
  almacen.alCambiar(sincronizarGuardadas);
  conectarEventos();
  render();
}

iniciar();
