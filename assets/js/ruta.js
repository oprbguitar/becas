/* Ruta Amauta — buscador y comparador de oportunidades académicas.
   Aplicación de una sola página, sin dependencias, servida como estático.  */
(() => {
'use strict';

/* ============================================================ utilidades */

const $ = (sel, raiz = document) => raiz.querySelector(sel);
const $$ = (sel, raiz = document) => [...raiz.querySelectorAll(sel)];

const normalizar = (txt) => (txt || '')
  .toString().toLowerCase()
  .normalize('NFD').replace(/[̀-ͯ]/g, '');

const escapar = (txt) => (txt == null ? '' : String(txt))
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;').replace(/'/g, '&#39;');

const numero = (n) => new Intl.NumberFormat('es-PE').format(Math.round(n || 0));

const SIMBOLO = { PEN: 'S/', USD: 'US$', EUR: '€', GBP: '£', CLP: 'CLP$',
                  COP: 'COP$', MXN: 'MX$', BRL: 'R$', CAD: 'CA$', AUD: 'AU$',
                  CHF: 'CHF', SGD: 'SG$' };

const dinero = (min, max, moneda) => {
  if (min == null) return '—';
  const s = SIMBOLO[moneda] || (moneda + ' ');
  return `${s} ${numero(min)} – ${numero(max)}`;
};

const duracion = (item) => {
  if (item.horas) return `${item.horas} horas`;
  const m = item.duracion_meses;
  if (!m) return '—';
  if (m % 12 === 0 && m >= 12) return `${m / 12} ${m === 12 ? 'año' : 'años'}`;
  return `${m} meses`;
};

const fecha = (iso) => {
  if (!iso) return '—';
  const d = new Date(iso + 'T12:00:00');
  if (isNaN(d)) return iso;
  return d.toLocaleDateString('es-PE', { day: '2-digit', month: 'short', year: 'numeric' });
};

const diasPara = (iso) => {
  if (!iso) return null;
  const d = new Date(iso + 'T12:00:00');
  if (isNaN(d)) return null;
  return Math.ceil((d - new Date()) / 86400000);
};

const dominioDe = (url) => {
  try { return new URL(url).hostname.replace(/^www\./, ''); } catch { return ''; }
};

const iniciales = (nombre) => (nombre || '?')
  .split(/\s+/).filter(p => p.length > 3).slice(0, 2)
  .map(p => p[0].toUpperCase()).join('') || (nombre || '?')[0].toUpperCase();

/* ------------------------------------------------------------- iconos */

const I = {
  lupa: '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
  flecha: '<path d="M9 6l6 6-6 6"/>',
  marcador: '<path d="M6 3h12v18l-6-4.5L6 21z"/>',
  reloj: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  globo: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18a15 15 0 0 1 0-18"/>',
  pin: '<path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
  banco: '<path d="M3 10h18M5 10v9M19 10v9M9 10v9M15 10v9M3 21h18M12 3l9 5H3z"/>',
  birrete: '<path d="M2 8l10-5 10 5-10 5z"/><path d="M6 10.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-5.5"/>',
  libro: '<path d="M4 4h7a3 3 0 0 1 3 3v13a2.5 2.5 0 0 0-2.5-2H4z"/><path d="M20 4h-4a3 3 0 0 0-3 3v13a2.5 2.5 0 0 1 2.5-2H20z"/>',
  diploma: '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
  maletin: '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2"/>',
  calendario: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
  moneda: '<circle cx="12" cy="12" r="9"/><path d="M12 7v10M9.5 9.5h4a1.75 1.75 0 0 1 0 3.5h-3a1.75 1.75 0 0 0 0 3.5h4"/>',
  wifi: '<path d="M5 12.5a10 10 0 0 1 14 0M8 16a6 6 0 0 1 8 0"/><circle cx="12" cy="19.5" r="1"/>',
  escudo: '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="m9 12 2 2 4-4"/>',
  balanza: '<path d="M12 3v18M3 7h18M6 7l-3 7h6zM18 7l-3 7h6z"/>',
  chispa: '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
  info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
  x: '<path d="M6 6l12 12M18 6L6 18"/>',
  mas: '<path d="M12 5v14M5 12h14"/>',
  enlace: '<path d="M14 4h6v6"/><path d="M20 4l-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
  idioma: '<path d="M3 5h11M9 3v2c0 5-2.5 8-6 10"/><path d="M6 11c1.5 3 4 5 7 6"/><path d="M13 21l4.5-11 4.5 11M15 17h6"/>',
  filtro: '<path d="M3 5h18l-7 8v6l-4 2v-8z"/>',
  estrella: '<path d="m12 3 2.6 5.6 6 .8-4.4 4.2 1.1 6-5.3-3-5.3 3 1.1-6L3.4 9.4l6-.8z"/>',
  usuarios: '<circle cx="9" cy="8" r="3.5"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 20c0-2.4-1-4.5-2.5-5.6"/>',
  hoja: '<path d="M5 19c8 2 14-3 14-11V5h-3C8 5 3 11 5 19z"/><path d="M5 19c1-5 4-8 9-10"/>',
};

const ico = (nombre, tam = 16, extra = '') =>
  `<svg width="${tam}" height="${tam}" viewBox="0 0 24 24" fill="none" stroke="currentColor" ` +
  `stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" ${extra}>${I[nombre] || ''}</svg>`;

/* ============================================================== estado */

const ALMACEN = {
  favoritos: new Set(JSON.parse(localStorage.getItem('ra:favoritos') || '[]')),
  comparador: JSON.parse(localStorage.getItem('ra:comparador') || '[]'),
  guardar() {
    localStorage.setItem('ra:favoritos', JSON.stringify([...this.favoritos]));
    localStorage.setItem('ra:comparador', JSON.stringify(this.comparador));
    pintarGlobos();
  },
  alternarFavorito(id) {
    this.favoritos.has(id) ? this.favoritos.delete(id) : this.favoritos.add(id);
    this.guardar();
  },
  alternarComparador(id) {
    const i = this.comparador.indexOf(id);
    if (i >= 0) this.comparador.splice(i, 1);
    else if (this.comparador.length < 4) this.comparador.push(id);
    else return false;
    this.guardar();
    return true;
  },
};

const DATOS = { items: [], porId: new Map(), meta: null, instituciones: [], listo: false };

/* ================================================= carga y normalización */

const ETIQUETA_SUNEDU = {
  licenciada: { texto: 'Licenciada por SUNEDU', clase: 'ok' },
  proceso: { texto: 'Licenciamiento en trámite', clase: 'proceso' },
  extranjera: { texto: 'Extranjera · reconocimiento SUNEDU', clase: 'ext' },
};

function normalizarBeca(b) {
  const dom = dominioDe(b.url);
  return {
    id: b.id, tipo: 'beca', nombre: b.nombre,
    institucion: b.organizacion, sigla: b.organizacion,
    pais: b.pais, region: b.region, ciudad: b.ciudad || '',
    area: (b.areas && b.areas[0]) || 'Todas', areas: b.areas || [],
    niveles: b.niveles || [], modalidad: b.modalidad || 'Presencial',
    idioma: (b.idiomas || ['Español']).join(' / '),
    duracion_meses: b.duracion_meses, cobertura: b.cobertura,
    incluye: b.incluye || {}, fecha_cierre: b.fecha_cierre, fecha_apertura: b.fecha_apertura,
    costo_min: null, costo_max: null, moneda: null,
    costo_min_usd: 0, costo_max_usd: 0,
    sunedu: b.pais === 'Perú' ? 'licenciada' : 'extranjera',
    convalidacion: b.pais === 'Perú' ? 'No requiere (Perú)' : 'Según universidad de destino',
    financiamiento: b.cobertura === 'Completa' ? 'Beca completa' : 'Beca parcial',
    admision: b.fecha_cierre ? 'Cierre ' + fecha(b.fecha_cierre) : 'Consultar convocatoria',
    descripcion: b.descripcion, requisitos: b.requisitos || [],
    url: b.url, url_requisitos: b.url_requisitos, url_busqueda: b.url_requisitos || b.url,
    dominio: dom, logo: dom ? `https://icons.duckduckgo.com/ip3/${dom}.ico` : '',
    destacado: !!b.destacada, tipo_institucion: 'Organización',
  };
}

async function cargar() {
  const pedir = async (ruta, respaldo) => {
    try {
      const r = await fetch(ruta, { cache: 'no-cache' });
      if (!r.ok) throw new Error(r.status);
      return await r.json();
    } catch { return respaldo; }
  };

  const [becas, maestrias, doctorados, diplomados, instituciones, meta] = await Promise.all([
    pedir('data/becas.json', []),
    pedir('data/maestrias.json', []),
    pedir('data/doctorados.json', []),
    pedir('data/diplomados.json', []),
    pedir('data/instituciones.json', []),
    pedir('data/meta_catalogo.json', null),
  ]);

  DATOS.items = [
    ...becas.map(normalizarBeca),
    ...maestrias, ...doctorados, ...diplomados,
  ];
  DATOS.items.forEach(it => {
    it.buscable = normalizar([it.nombre, it.institucion, it.sigla, it.pais,
                              it.ciudad, it.area, (it.areas || []).join(' ')].join(' '));
    DATOS.porId.set(it.id, it);
  });
  DATOS.instituciones = instituciones;
  DATOS.meta = meta;
  DATOS.listo = true;

  if (meta && meta.actualizado) {
    $('#pie-actualizado').textContent = 'Catálogo actualizado: ' + fecha(meta.actualizado);
  }
}

const porTipo = (t) => DATOS.items.filter(i => i.tipo === t);
const unicos = (items, clave) => [...new Set(items.map(i => i[clave]).filter(Boolean))].sort(
  (a, b) => a.localeCompare(b, 'es'));

/* ========================================================= componentes */

// El logotipo se resuelve desde el dominio oficial de la institución.
// Si el servicio de iconos falla se prueba una alternativa y, en último
// término, queda visible el monograma con las iniciales.
function marcaLogo(item, tam = 52) {
  const dom = item.dominio || '';
  const alt = escapar(item.sigla || item.institucion || '');
  const respaldo = dom ? `https://www.google.com/s2/favicons?domain=${encodeURIComponent(dom)}&sz=64` : '';
  const img = dom
    ? `<img src="https://icons.duckduckgo.com/ip3/${escapar(dom)}.ico" alt="${alt}" loading="lazy"
            data-respaldo="${escapar(respaldo)}"
            onerror="if(this.dataset.respaldo){this.src=this.dataset.respaldo;this.dataset.respaldo='';}else{this.style.display='none';}">`
    : '';
  return `<div class="logo" style="width:${tam}px;height:${tam}px" title="${escapar(item.institucion)}">${escapar(iniciales(item.sigla || item.institucion))}${img}</div>`;
}

function selloSunedu(item) {
  const e = ETIQUETA_SUNEDU[item.sunedu];
  if (!e) return '';
  return `<span class="sello ${e.clase}">${ico('escudo', 13)} ${escapar(e.texto)}</span>`;
}

function tarjeta(item) {
  const fav = ALMACEN.favoritos.has(item.id);
  const enComp = ALMACEN.comparador.includes(item.id);
  const esBeca = item.tipo === 'beca';
  const nombreTipo = { beca: 'Beca', maestria: 'Maestría', doctorado: 'Doctorado', diplomado: 'Diplomado' }[item.tipo];

  const dias = esBeca ? diasPara(item.fecha_cierre) : null;
  const urgencia = dias != null && dias >= 0 && dias <= 30
    ? `<span style="color:var(--terracota);font-weight:600">Cierra en ${dias} d</span>` : '';

  const meta = esBeca
    ? [`<span>${ico('pin', 14)} ${escapar(item.pais)}</span>`,
       `<span>${ico('birrete', 14)} ${escapar((item.niveles || []).join(', ') || item.area)}</span>`,
       `<span>${ico('calendario', 14)} ${fecha(item.fecha_cierre)}</span>`]
    : [`<span>${ico('pin', 14)} ${escapar(item.pais)}</span>`,
       `<span>${ico(item.modalidad === 'Online' ? 'wifi' : 'banco', 14)} ${escapar(item.modalidad)}</span>`,
       `<span>${ico('reloj', 14)} ${duracion(item)}</span>`];

  const pie = esBeca
    ? `<div class="precio">${escapar(item.cobertura || 'Beca')}<small>Cobertura</small></div>`
    : `<div class="precio">${dinero(item.costo_min, item.costo_max, item.moneda)}<small>Referencial</small></div>`;

  return `
  <article class="tarjeta tarjeta-alto" data-id="${escapar(item.id)}">
    <div class="tarjeta-sup">
      ${marcaLogo(item)}
      <div style="min-width:0;flex:1">
        <span class="insignia ${item.tipo}">${nombreTipo}</span>
        ${urgencia ? `<div style="font-size:12px;margin-top:5px">${urgencia}</div>` : ''}
      </div>
      <button class="marcador ${fav ? 'activo' : ''}" data-accion="favorito" data-id="${escapar(item.id)}"
              title="${fav ? 'Quitar de favoritos' : 'Guardar en favoritos'}" aria-label="Favorito">
        ${ico('marcador', 19, fav ? 'fill="currentColor"' : '')}
      </button>
    </div>
    <h3><a href="#/programa/${encodeURIComponent(item.id)}">${escapar(item.nombre)}</a></h3>
    <p class="institucion">${escapar(item.institucion)}${item.ciudad ? ' · ' + escapar(item.ciudad) : ''}</p>
    <div class="meta">${meta.join('')}</div>
    <div style="margin-bottom:10px">${selloSunedu(item)}</div>
    <div class="tarjeta-pie">
      ${pie}
      <div class="acciones-tarjeta">
        <button class="mini ${enComp ? 'en-comparador' : ''}" data-accion="comparar" data-id="${escapar(item.id)}">
          ${ico('balanza', 13)} ${enComp ? 'Añadido' : 'Comparar'}
        </button>
        <button class="mini lleno" data-accion="ver" data-id="${escapar(item.id)}">Ver</button>
      </div>
    </div>
  </article>`;
}

function vacio(titulo, texto) {
  return `<div class="vacio">
    ${ico('lupa', 44)}
    <h3>${escapar(titulo)}</h3>
    <p>${escapar(texto)}</p>
  </div>`;
}

function paginacion(pagina, totalPaginas) {
  if (totalPaginas <= 1) return '';
  const btn = (p, txt, extra = '') =>
    `<button data-pagina="${p}" class="${p === pagina ? 'activa' : ''}" ${extra}>${txt}</button>`;
  const partes = [btn(pagina - 1, '‹', pagina === 1 ? 'disabled' : '')];
  const vistos = new Set([1, totalPaginas, pagina, pagina - 1, pagina + 1]);
  let previo = 0;
  [...vistos].filter(p => p >= 1 && p <= totalPaginas).sort((a, b) => a - b).forEach(p => {
    if (p - previo > 1) partes.push('<button class="puntos" disabled>…</button>');
    partes.push(btn(p, p));
    previo = p;
  });
  partes.push(btn(pagina + 1, '›', pagina === totalPaginas ? 'disabled' : ''));
  return `<div class="paginacion">${partes.join('')}</div>`;
}

/* ========================================================= filtrado */

const FILTROS = {};   // estado por vista

function filtrosDe(vista) {
  if (!FILTROS[vista]) FILTROS[vista] = { q: '', pagina: 1, orden: 'relevancia' };
  return FILTROS[vista];
}

function aplicarFiltros(items, f) {
  const q = normalizar(f.q).split(/\s+/).filter(Boolean);
  let res = items.filter(it => {
    if (q.length && !q.every(t => it.buscable.includes(t))) return false;
    if (f.pais && it.pais !== f.pais) return false;
    if (f.region && it.region !== f.region) return false;
    if (f.area && it.area !== f.area && !(it.areas || []).includes(f.area)) return false;
    if (f.modalidad && it.modalidad !== f.modalidad) return false;
    if (f.idioma && !(it.idioma || '').includes(f.idioma)) return false;
    if (f.sunedu && it.sunedu !== f.sunedu) return false;
    if (f.institucion && it.institucion !== f.institucion) return false;
    if (f.tipoInst && it.tipo_institucion !== f.tipoInst) return false;
    if (f.cobertura && it.cobertura !== f.cobertura) return false;
    if (f.nivel && !(it.niveles || []).includes(f.nivel)) return false;
    if (f.costoMax && it.costo_max_usd > +f.costoMax) return false;
    if (f.duracionMax && (it.duracion_meses || 0) > +f.duracionMax) return false;
    if (f.soloAbiertas && it.fecha_cierre) {
      const d = diasPara(it.fecha_cierre);
      if (d == null || d < 0) return false;
    }
    return true;
  });

  const ordenes = {
    relevancia: (a, b) => (b.destacado - a.destacado) || a.nombre.localeCompare(b.nombre, 'es'),
    nombre: (a, b) => a.nombre.localeCompare(b.nombre, 'es'),
    costoAsc: (a, b) => (a.costo_min_usd || 0) - (b.costo_min_usd || 0),
    costoDesc: (a, b) => (b.costo_max_usd || 0) - (a.costo_max_usd || 0),
    duracion: (a, b) => (a.duracion_meses || 999) - (b.duracion_meses || 999),
    cierre: (a, b) => {
      const da = diasPara(a.fecha_cierre), db = diasPara(b.fecha_cierre);
      const va = da == null || da < 0 ? 1e9 : da, vb = db == null || db < 0 ? 1e9 : db;
      return va - vb;
    },
    pais: (a, b) => a.pais.localeCompare(b.pais, 'es'),
  };
  res.sort(ordenes[f.orden] || ordenes.relevancia);
  return res;
}

function opciones(lista, valor, etiquetaTodos) {
  return [`<option value="">${escapar(etiquetaTodos)}</option>`]
    .concat(lista.map(v => `<option value="${escapar(v)}" ${v === valor ? 'selected' : ''}>${escapar(v)}</option>`))
    .join('');
}

/* ============================================================== vistas */

function portada({ titulo, resalte, bajada, lema }) {
  return `
  <section class="portada">
    <img class="portada-arte" src="assets/img/logo.png" alt="" aria-hidden="true">
    <div class="contenedor portada-texto">
      <h1 class="titulo">${titulo.replace('{r}', `<em>${escapar(resalte)}</em>`)}</h1>
      <p class="bajada">${escapar(bajada)}</p>
      ${lema ? `<p class="lema">${escapar(lema)}</p>` : ''}
    </div>
  </section>`;
}

function metricas(lista) {
  return `<div class="contenedor"><div class="metricas">` + lista.map((m, i) => `
    <div class="metrica ${i % 2 ? 'oliva' : ''}">
      <div class="metrica-icono">${ico(m.icono, 22)}</div>
      <div><b>${m.valor}</b><span>${escapar(m.texto)}</span></div>
    </div>`).join('') + `</div></div>`;
}

/* ---------------------------------------------------------- inicio */

function vistaInicio() {
  const total = DATOS.items.length;
  const paises = new Set(DATOS.items.map(i => i.pais)).size;
  const insts = DATOS.instituciones.length;
  // Mezcla equilibrada: dos oportunidades destacadas de cada tipo.
  const destacados = ['beca', 'maestria', 'doctorado', 'diplomado']
    .flatMap(t => DATOS.items.filter(i => i.destacado && i.tipo === t).slice(0, 2));

  const rutas = [
    { ruta: 'becas', icono: 'birrete', titulo: 'Becas', texto: 'Financiamiento completo y parcial para estudiar.', n: porTipo('beca').length },
    { ruta: 'maestrias', icono: 'libro', titulo: 'Maestrías', texto: 'Programas en Perú, Latinoamérica y el mundo.', n: porTipo('maestria').length },
    { ruta: 'doctorados', icono: 'diploma', titulo: 'Doctorados', texto: 'Investigación de alto nivel y financiamiento.', n: porTipo('doctorado').length },
    { ruta: 'diplomados', icono: 'maletin', titulo: 'Diplomados', texto: 'Formación corta para actualizar competencias.', n: porTipo('diplomado').length },
  ];

  return portada({
    titulo: 'Tu {r} al conocimiento.', resalte: 'ruta',
    bajada: 'Becas, posgrados y oportunidades para avanzar.',
    lema: 'No te desactualices. Avanza hoy.',
  }) + `
  <div class="contenedor" style="position:relative">
    <form class="buscador-portada" id="form-inicio">
      <div class="campo-busqueda">
        ${ico('lupa', 19)}
        <input type="text" id="q-inicio" placeholder="Busca por programa, país, universidad o área…"
               autocomplete="off" aria-label="Buscar">
      </div>
      <button class="btn btn-primario btn-alto" type="submit">Explorar</button>
    </form>

    <div class="rutas">
      ${rutas.map(r => `
        <a class="ruta" href="#/${r.ruta}">
          <div class="ruta-icono">${ico(r.icono, 24)}</div>
          <div style="min-width:0">
            <h3>${r.titulo}</h3>
            <p>${r.texto}</p>
          </div>
          <span class="ruta-flecha">${ico('flecha', 20)}</span>
        </a>`).join('')}
    </div>
  </div>` +
  metricas([
    { icono: 'maletin', valor: numero(total), texto: 'Oportunidades disponibles' },
    { icono: 'globo', valor: numero(paises), texto: 'Países' },
    { icono: 'banco', valor: numero(insts), texto: 'Instituciones' },
    { icono: 'marcador', valor: numero(ALMACEN.favoritos.size), texto: 'Guardados por ti' },
  ]) + `
  <div class="contenedor seccion">
    <div class="seccion-cabecera">
      <h2>Oportunidades destacadas</h2>
      <a class="btn-texto" href="#/maestrias">Ver todas ${ico('flecha', 14)}</a>
    </div>
    <div class="rejilla cuatro">${destacados.map(tarjeta).join('')}</div>
  </div>

  <div class="contenedor seccion">
    <div class="panel-filtros">
      <div class="fila-filtros" style="margin:0;padding:0;border:0">
        <span class="etiqueta-fila">${ico('pin', 13)} Rutas destacadas</span>
        <a class="pastilla" href="#/maestrias?sunedu=licenciada">${ico('escudo', 14)} Licenciadas SUNEDU</a>
        <a class="pastilla" href="#/maestrias?pais=Perú">${ico('pin', 14)} Perú</a>
        <a class="pastilla" href="#/maestrias?region=Latinoamérica">${ico('globo', 14)} Latinoamérica</a>
        <a class="pastilla" href="#/diplomados?modalidad=Online">${ico('wifi', 14)} Online</a>
        <a class="pastilla" href="#/becas?cobertura=Completa">${ico('estrella', 14)} Becas completas</a>
      </div>
    </div>
  </div>

  <div class="aviso-legal">${ico('info', 15)} Los programas se actualizan constantemente. Revisa siempre la información oficial de cada institución.</div>`;
}

/* ---------------------------------------------------------- listados */

const CONFIG_VISTA = {
  becas: {
    tipo: 'beca', titulo: '{r} para avanzar.', resalte: 'Becas',
    bajada: 'Encuentra financiamiento para estudiar en Perú y el mundo.',
    lema: 'Impulsa tu futuro.',
  },
  maestrias: {
    tipo: 'maestria', titulo: '{r} con propósito.', resalte: 'Maestrías',
    bajada: 'Programas para especializarte y crecer profesionalmente.',
    lema: 'Especialízate con claridad.',
  },
  doctorados: {
    tipo: 'doctorado', titulo: '{r} para liderar investigación.', resalte: 'Doctorados',
    bajada: 'Programas de alto nivel, financiamiento y líneas de investigación.',
    lema: 'Investiga. Lidera. Transforma.',
  },
  diplomados: {
    tipo: 'diplomado', titulo: '{r} para mantenerte vigente.', resalte: 'Diplomados',
    bajada: 'Formación práctica y rápida para actualizar tus competencias.',
    lema: 'Actualízate sin detenerte.',
  },
};

function vistaListado(vista) {
  const cfg = CONFIG_VISTA[vista];
  const base = porTipo(cfg.tipo);
  const f = filtrosDe(vista);
  const resultados = aplicarFiltros(base, f);

  const porPagina = 12;
  const totalPaginas = Math.max(1, Math.ceil(resultados.length / porPagina));
  if (f.pagina > totalPaginas) f.pagina = 1;
  const pagina = resultados.slice((f.pagina - 1) * porPagina, f.pagina * porPagina);

  const esBeca = cfg.tipo === 'beca';
  const online = base.filter(i => i.modalidad === 'Online').length;
  const abiertas = base.filter(i => { const d = diasPara(i.fecha_cierre); return d != null && d >= 0; }).length;

  const met = esBeca
    ? [{ icono: 'birrete', valor: numero(base.length), texto: 'Becas en catálogo' },
       { icono: 'calendario', valor: numero(abiertas), texto: 'Con convocatoria vigente' },
       { icono: 'globo', valor: numero(new Set(base.map(i => i.pais)).size), texto: 'Países' },
       { icono: 'estrella', valor: numero(base.filter(i => i.cobertura === 'Completa').length), texto: 'Cobertura completa' }]
    : [{ icono: 'libro', valor: numero(base.length), texto: 'Programas disponibles' },
       { icono: 'banco', valor: numero(new Set(base.map(i => i.institucion)).size), texto: 'Instituciones' },
       { icono: 'globo', valor: numero(new Set(base.map(i => i.pais)).size), texto: 'Países' },
       { icono: 'wifi', valor: Math.round(online / Math.max(1, base.length) * 100) + '%', texto: 'Programas online' }];

  const listaPaises = unicos(base, 'pais');
  const listaAreas = unicos(base, 'area');
  const listaRegiones = unicos(base, 'region');
  const listaModalidad = unicos(base, 'modalidad');
  const listaInst = unicos(base, 'institucion');

  const filtrosBecas = `
    <div class="campo"><label>Cobertura</label>
      <select data-f="cobertura">${opciones(unicos(base, 'cobertura'), f.cobertura, 'Todas las coberturas')}</select></div>
    <div class="campo"><label>Nivel de estudios</label>
      <select data-f="nivel">${opciones([...new Set(base.flatMap(i => i.niveles || []))].sort(), f.nivel, 'Todos los niveles')}</select></div>`;

  const filtrosPrograma = `
    <div class="campo"><label>Licenciamiento</label>
      <select data-f="sunedu">
        <option value="">Todos</option>
        <option value="licenciada" ${f.sunedu === 'licenciada' ? 'selected' : ''}>Licenciada por SUNEDU</option>
        <option value="proceso" ${f.sunedu === 'proceso' ? 'selected' : ''}>En trámite / por verificar</option>
        <option value="extranjera" ${f.sunedu === 'extranjera' ? 'selected' : ''}>Extranjera (reconocimiento)</option>
      </select></div>
    <div class="campo"><label>Costo máximo (US$)</label>
      <select data-f="costoMax">
        <option value="">Cualquier rango</option>
        ${[2000, 5000, 10000, 20000, 40000, 80000].map(v =>
          `<option value="${v}" ${String(f.costoMax) === String(v) ? 'selected' : ''}>Hasta US$ ${numero(v)}</option>`).join('')}
      </select></div>`;

  return portada({ titulo: cfg.titulo, resalte: cfg.resalte, bajada: cfg.bajada, lema: cfg.lema })
    + metricas(met) + `
  <div class="contenedor seccion" id="resultados">
    <form class="panel-filtros" id="form-filtros" data-vista="${vista}">
      <div class="rejilla-filtros">
        <div class="campo ancho-2"><label>Palabra clave</label>
          <div class="campo-busqueda-linea">${ico('lupa', 17)}
            <input type="text" data-f="q" value="${escapar(f.q)}" placeholder="Ej. gestión pública, salud, ingeniería…" autocomplete="off">
          </div>
        </div>
        <div class="campo"><label>País</label>
          <select data-f="pais">${opciones(listaPaises, f.pais, 'Todos los países')}</select></div>
        <div class="campo"><label>Región</label>
          <select data-f="region">${opciones(listaRegiones, f.region, 'Todas las regiones')}</select></div>
        <div class="campo"><label>Área de estudio</label>
          <select data-f="area">${opciones(listaAreas, f.area, 'Todas las áreas')}</select></div>
        <div class="campo"><label>Modalidad</label>
          <select data-f="modalidad">${opciones(listaModalidad, f.modalidad, 'Todas las modalidades')}</select></div>
        ${esBeca ? filtrosBecas : filtrosPrograma}
        <div class="campo"><label>Institución</label>
          <select data-f="institucion">${opciones(listaInst, f.institucion, 'Todas las instituciones')}</select></div>
      </div>

      <div class="fila-filtros">
        <span class="etiqueta-fila">${ico('filtro', 13)} Filtros rápidos</span>
        <button type="button" class="pastilla ${f.pais === 'Perú' ? 'activa' : ''}" data-rapido="pais" data-valor="Perú">${ico('pin', 14)} Perú</button>
        <button type="button" class="pastilla ${f.region === 'Latinoamérica' ? 'activa' : ''}" data-rapido="region" data-valor="Latinoamérica">${ico('globo', 14)} Latinoamérica</button>
        <button type="button" class="pastilla ${f.modalidad === 'Online' ? 'activa' : ''}" data-rapido="modalidad" data-valor="Online">${ico('wifi', 14)} Online</button>
        ${esBeca
          ? `<button type="button" class="pastilla ${f.cobertura === 'Completa' ? 'activa' : ''}" data-rapido="cobertura" data-valor="Completa">${ico('estrella', 14)} Completas</button>
             <button type="button" class="pastilla ${f.soloAbiertas ? 'activa' : ''}" data-rapido="soloAbiertas" data-valor="1">${ico('calendario', 14)} Vigentes</button>`
          : `<button type="button" class="pastilla ${f.sunedu === 'licenciada' ? 'activa' : ''}" data-rapido="sunedu" data-valor="licenciada">${ico('escudo', 14)} Licenciadas SUNEDU</button>`}
        <button type="button" class="btn-texto" data-limpiar>Limpiar filtros</button>
        <div class="derecha">
          <label for="orden">Ordenar por</label>
          <select id="orden" data-f="orden">
            <option value="relevancia" ${f.orden === 'relevancia' ? 'selected' : ''}>Más relevantes</option>
            ${esBeca ? `<option value="cierre" ${f.orden === 'cierre' ? 'selected' : ''}>Cierre más próximo</option>` : ''}
            ${!esBeca ? `<option value="costoAsc" ${f.orden === 'costoAsc' ? 'selected' : ''}>Menor costo</option>
                         <option value="costoDesc" ${f.orden === 'costoDesc' ? 'selected' : ''}>Mayor costo</option>
                         <option value="duracion" ${f.orden === 'duracion' ? 'selected' : ''}>Menor duración</option>` : ''}
            <option value="nombre" ${f.orden === 'nombre' ? 'selected' : ''}>Nombre (A–Z)</option>
            <option value="pais" ${f.orden === 'pais' ? 'selected' : ''}>País</option>
          </select>
        </div>
      </div>
    </form>

    <div class="barra-resultados">
      <p class="conteo">Mostrando <b>${numero(pagina.length)}</b> de <b>${numero(resultados.length)}</b> resultados</p>
    </div>

    ${resultados.length
      ? `<div class="rejilla">${pagina.map(tarjeta).join('')}</div>` + paginacion(f.pagina, totalPaginas)
      : vacio('Sin resultados', 'Prueba con menos filtros o una palabra clave más general.')}
  </div>

  <div class="aviso-legal">${ico('info', 15)} Costos y fechas son referenciales. Verifica siempre en la web oficial de la institución.</div>`;
}

/* ---------------------------------------------------------- favoritos */

function vistaFavoritos() {
  const guardados = [...ALMACEN.favoritos].map(id => DATOS.porId.get(id)).filter(Boolean);
  const f = filtrosDe('favoritos');
  const filtrados = f.tipo ? guardados.filter(i => i.tipo === f.tipo) : guardados;
  const pestanas = [['', 'Todos'], ['beca', 'Becas'], ['maestria', 'Maestrías'],
                    ['doctorado', 'Doctorados'], ['diplomado', 'Diplomados']];

  return portada({
    titulo: 'Tus {r}, en un solo lugar.', resalte: 'favoritos',
    bajada: 'Guarda, organiza y revisa oportunidades antes de decidir.',
    lema: 'Guarda hoy. Decide mejor.',
  }) + `
  <div class="contenedor seccion">
    <div class="fila-filtros" style="margin:0 0 18px;padding:0;border:0">
      ${pestanas.map(([v, t]) => `
        <button class="pastilla ${f.tipo === v || (!f.tipo && !v) ? 'activa' : ''}" data-pestana="${v}">${escapar(t)}</button>`).join('')}
      <div class="derecha">
        <a class="btn btn-oliva" href="#/comparador">${ico('balanza', 16)} Ir al comparador</a>
      </div>
    </div>
    ${guardados.length
      ? metricasSimples([
          { icono: 'marcador', valor: numero(guardados.length), texto: 'Guardados totales' },
          { icono: 'balanza', valor: numero(ALMACEN.comparador.length), texto: 'En el comparador' },
          { icono: 'globo', valor: numero(new Set(guardados.map(i => i.pais)).size), texto: 'Países' },
          { icono: 'banco', valor: numero(new Set(guardados.map(i => i.institucion)).size), texto: 'Instituciones' },
        ]) : ''}
    ${filtrados.length
      ? `<div class="rejilla" style="margin-top:18px">${filtrados.map(tarjeta).join('')}</div>`
      : vacio('Todavía no guardas nada',
              'Usa el marcador de cada tarjeta para guardar programas y compararlos después.')}
  </div>`;
}

function metricasSimples(lista) {
  return `<div class="metricas">` + lista.map((m, i) => `
    <div class="metrica ${i % 2 ? 'oliva' : ''}">
      <div class="metrica-icono">${ico(m.icono, 22)}</div>
      <div><b>${m.valor}</b><span>${escapar(m.texto)}</span></div>
    </div>`).join('') + `</div>`;
}

/* ---------------------------------------------------------- comparador */

function puntaje(item, conjunto) {
  // Compatibilidad relativa dentro del conjunto comparado: costo, duración,
  // flexibilidad de modalidad y respaldo institucional.
  const costos = conjunto.map(i => i.costo_max_usd || 0);
  const maxCosto = Math.max(...costos, 1);
  const duraciones = conjunto.map(i => i.duracion_meses || 0);
  const maxDur = Math.max(...duraciones, 1);

  let p = 100;
  p -= ((item.costo_max_usd || 0) / maxCosto) * 26;
  p -= ((item.duracion_meses || 0) / maxDur) * 16;
  if (item.modalidad === 'Online') p += 5;
  else if (item.modalidad === 'Semipresencial') p += 3;
  if (item.sunedu === 'licenciada') p += 4;
  if (item.sunedu === 'proceso') p -= 6;
  if (item.tipo === 'beca') p += 6;
  return Math.max(52, Math.min(98, Math.round(p)));
}

function anillo(valor) {
  const r = 16, c = 2 * Math.PI * r;
  const color = valor >= 90 ? 'var(--verde)' : valor >= 78 ? 'var(--oliva)' : 'var(--ambar)';
  return `<span class="anillo">
    <svg width="42" height="42" viewBox="0 0 42 42">
      <circle cx="21" cy="21" r="${r}" fill="none" stroke="var(--borde)" stroke-width="4"/>
      <circle cx="21" cy="21" r="${r}" fill="none" stroke="${color}" stroke-width="4"
        stroke-dasharray="${(c * valor / 100).toFixed(1)} ${c.toFixed(1)}"
        stroke-linecap="round" transform="rotate(-90 21 21)"/>
      <text x="21" y="24.5" text-anchor="middle" font-size="11" font-weight="700" fill="${color}">${valor}%</text>
    </svg>
    <span class="valor" style="color:${color}">${valor >= 90 ? 'Excelente' : valor >= 78 ? 'Muy bueno' : 'Bueno'}</span>
  </span>`;
}

function vistaComparador() {
  const sel = ALMACEN.comparador.map(id => DATOS.porId.get(id)).filter(Boolean);

  const bandeja = `
    <div class="bandeja-comparador">
      <div class="bandeja-titulo">Selecciona hasta 4 programas para comparar</div>
      ${sel.map((it, i) => `
        <div class="ficha-comparador">
          <span class="ficha-num">${i + 1}</span>
          ${marcaLogo(it, 34)}
          <span class="nombre">${escapar(it.nombre)}</span>
          <button class="quitar" data-accion="comparar" data-id="${escapar(it.id)}" aria-label="Quitar">${ico('x', 16)}</button>
        </div>`).join('')}
      ${sel.length < 4 ? `<a class="ficha-vacia" href="#/maestrias">${ico('mas', 16)} Añadir programa</a>` : ''}
    </div>`;

  if (!sel.length) {
    return portada({
      titulo: 'Compara y {r} mejor.', resalte: 'elige',
      bajada: 'Visualiza diferencias clave antes de tomar una decisión.',
      lema: 'Compara mejor. Elige seguro.',
    }) + `<div class="contenedor seccion">${bandeja}
      ${vacio('Aún no hay programas para comparar',
              'Pulsa “Comparar” en cualquier tarjeta para añadirla aquí.')}</div>`;
  }

  const filas = [
    ['banco', 'Institución', it => escapar(it.institucion)],
    ['pin', 'País / ciudad', it => escapar(it.pais + (it.ciudad ? ' · ' + it.ciudad : ''))],
    ['birrete', 'Tipo', it => ({ beca: 'Beca', maestria: 'Maestría', doctorado: 'Doctorado', diplomado: 'Diplomado' })[it.tipo]],
    ['libro', 'Área', it => escapar(it.area)],
    ['reloj', 'Duración', it => duracion(it)],
    ['wifi', 'Modalidad', it => escapar(it.modalidad)],
    ['idioma', 'Idioma', it => escapar(it.idioma || '—')],
    ['moneda', 'Costo referencial', it => it.tipo === 'beca'
        ? `<span class="tc-mejor">Cubierto por la beca</span>`
        : dinero(it.costo_min, it.costo_max, it.moneda), true],
    ['estrella', 'Financiamiento', it => escapar(it.financiamiento || '—')],
    ['escudo', 'Licenciamiento', it => selloSunedu(it) || '—'],
    ['escudo', 'Convalidación en Perú', it => escapar(it.convalidacion || '—')],
    ['calendario', 'Admisión', it => escapar(it.admision || '—')],
  ];

  const cols = `240px repeat(${sel.length}, minmax(190px, 1fr))`;
  const minUsd = Math.min(...sel.filter(i => i.costo_max_usd).map(i => i.costo_max_usd));

  const tabla = `
    <div class="envoltura-scroll">
      <div class="tabla-comparador">
        <div class="tc-fila tc-cabecera" style="grid-template-columns:${cols}">
          <div class="tc-celda tc-etiqueta">${ico('balanza', 16)} Programa</div>
          ${sel.map(it => `
            <div class="tc-celda">
              <div class="tc-titulo">${marcaLogo(it, 40)}
                <div style="min-width:0">
                  <h4>${escapar(it.nombre)}</h4>
                  <small>${escapar(it.sigla || it.institucion)}</small>
                </div>
              </div>
            </div>`).join('')}
        </div>
        ${filas.map(([icono, etiqueta, valor, destacada]) => `
          <div class="tc-fila ${destacada ? 'destacada' : ''}" style="grid-template-columns:${cols}">
            <div class="tc-celda tc-etiqueta">${ico(icono, 16)} ${escapar(etiqueta)}</div>
            ${sel.map(it => {
              const v = valor(it);
              const mejor = destacada && it.costo_max_usd && it.costo_max_usd === minUsd;
              return `<div class="tc-celda ${mejor ? 'tc-mejor' : ''}">${v}</div>`;
            }).join('')}
          </div>`).join('')}
        <div class="tc-fila" style="grid-template-columns:${cols}">
          <div class="tc-celda tc-etiqueta">${ico('estrella', 16)} Compatibilidad</div>
          ${sel.map(it => `<div class="tc-celda">${anillo(puntaje(it, sel))}</div>`).join('')}
        </div>
        <div class="tc-fila" style="grid-template-columns:${cols}">
          <div class="tc-celda tc-etiqueta">${ico('enlace', 16)} Sitio oficial</div>
          ${sel.map(it => `<div class="tc-celda"><a class="mini lleno" href="${escapar(it.url)}" target="_blank" rel="noopener">Abrir ${ico('enlace', 12)}</a></div>`).join('')}
        </div>
      </div>
    </div>`;

  const barato = sel.slice().sort((a, b) => (a.costo_max_usd || 0) - (b.costo_max_usd || 0))[0];
  const rapido = sel.slice().sort((a, b) => (a.duracion_meses || 999) - (b.duracion_meses || 999))[0];
  const flexible = sel.slice().sort((a, b) =>
    ({ Online: 0, Semipresencial: 1, Presencial: 2 })[a.modalidad] -
    ({ Online: 0, Semipresencial: 1, Presencial: 2 })[b.modalidad])[0];
  const mejorPuntaje = sel.slice().sort((a, b) => puntaje(b, sel) - puntaje(a, sel))[0];

  const reco = (icono, titulo, item, nota) => `
    <div class="reco">
      <div class="reco-icono">${ico(icono, 17)}</div>
      <div style="min-width:0">
        <b>${escapar(titulo)}</b>
        <span><a href="#/programa/${encodeURIComponent(item.id)}" style="color:var(--terracota);font-weight:600">${escapar(item.nombre)}</a></span>
        <span style="color:var(--tenue)">${escapar(item.sigla || item.institucion)}</span>
        <span>${escapar(nota)}</span>
      </div>
    </div>`;

  return portada({
    titulo: 'Compara y {r} mejor.', resalte: 'elige',
    bajada: 'Visualiza diferencias clave antes de tomar una decisión.',
    lema: 'Compara mejor. Elige seguro.',
  }) + `
  <div class="contenedor seccion">
    ${bandeja}
    <div style="display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:20px" class="rejilla-comparador">
      ${tabla}
      <aside class="panel-recomendacion">
        <h3>${ico('chispa', 19)} Recomendación rápida</h3>
        ${reco('moneda', 'Mejor costo', barato, barato.tipo === 'beca'
          ? 'La beca cubre el costo del programa.'
          : `Rango más bajo del conjunto: ${dinero(barato.costo_min, barato.costo_max, barato.moneda)}.`)}
        ${reco('reloj', 'Menor duración', rapido, `${duracion(rapido)} — llegas antes al grado.`)}
        ${reco('wifi', 'Más flexible', flexible, `Modalidad ${flexible.modalidad.toLowerCase()}.`)}
        ${reco('estrella', 'Mejor equilibrio', mejorPuntaje, `Compatibilidad ${puntaje(mejorPuntaje, sel)}% según costo, duración y respaldo.`)}
        <button class="btn btn-linea" style="width:100%;margin-top:14px" data-vaciar-comparador>Vaciar comparador</button>
      </aside>
    </div>
  </div>
  <div class="aviso-legal">${ico('escudo', 15)} La información se actualiza constantemente. Verifica siempre en la fuente oficial.</div>`;
}

/* ---------------------------------------------------------- instituciones */

function vistaInstituciones() {
  const f = filtrosDe('instituciones');
  const q = normalizar(f.q);
  const lista = DATOS.instituciones.filter(u =>
    (!q || normalizar(u.nombre + ' ' + u.sigla + ' ' + u.pais).includes(q)) &&
    (!f.pais || u.pais === f.pais) &&
    (!f.sunedu || u.sunedu === f.sunedu));

  return portada({
    titulo: '{r} verificadas.', resalte: 'Instituciones',
    bajada: 'Universidades y escuelas con su estado de licenciamiento y enlace oficial.',
    lema: 'Confirma antes de postular.',
  }) + `
  <div class="contenedor seccion">
    <form class="panel-filtros" id="form-filtros" data-vista="instituciones">
      <div class="rejilla-filtros">
        <div class="campo ancho-2"><label>Buscar institución</label>
          <div class="campo-busqueda-linea">${ico('lupa', 17)}
            <input type="text" data-f="q" value="${escapar(f.q || '')}" placeholder="Nombre o sigla…"></div></div>
        <div class="campo"><label>País</label>
          <select data-f="pais">${opciones(unicos(DATOS.instituciones, 'pais'), f.pais, 'Todos los países')}</select></div>
        <div class="campo"><label>Licenciamiento</label>
          <select data-f="sunedu">
            <option value="">Todos</option>
            <option value="licenciada" ${f.sunedu === 'licenciada' ? 'selected' : ''}>Licenciada por SUNEDU</option>
            <option value="proceso" ${f.sunedu === 'proceso' ? 'selected' : ''}>En trámite / por verificar</option>
            <option value="extranjera" ${f.sunedu === 'extranjera' ? 'selected' : ''}>Extranjera</option>
          </select></div>
      </div>
    </form>
    <p class="conteo" style="margin-bottom:14px">Mostrando <b>${numero(lista.length)}</b> instituciones</p>
    <div class="rejilla">
      ${lista.map(u => `
        <article class="tarjeta">
          <div class="tarjeta-sup">${marcaLogo(u)}
            <div style="min-width:0;flex:1">
              <h3 style="font-size:15.5px;margin:0">${escapar(u.nombre)}</h3>
              <p class="institucion" style="margin:2px 0 0">${escapar(u.ciudad)}, ${escapar(u.pais)}</p>
            </div>
          </div>
          <div style="margin-bottom:10px">${selloSunedu(u)}</div>
          <div class="meta">${(u.areas || []).slice(0, 4).map(a => `<span>${ico('libro', 13)} ${escapar(a)}</span>`).join('')}</div>
          <div class="tarjeta-pie">
            <span style="font-size:12.5px;color:var(--suave)">${escapar(u.tipo)}</span>
            <a class="mini lleno" href="${escapar(u.url_posgrado)}" target="_blank" rel="noopener">Posgrado ${ico('enlace', 12)}</a>
          </div>
        </article>`).join('')}
    </div>
    ${lista.length ? '' : vacio('Sin coincidencias', 'Ajusta la búsqueda o el filtro de país.')}
  </div>
  <div class="aviso-legal">${ico('escudo', 15)} Verifica el estado oficial de licenciamiento en el registro de SUNEDU.</div>`;
}

/* ---------------------------------------------------------- ficha (modal) */

function abrirFicha(id) {
  const it = DATOS.porId.get(id);
  if (!it) return;
  const esBeca = it.tipo === 'beca';
  const nombreTipo = { beca: 'Beca', maestria: 'Maestría', doctorado: 'Doctorado', diplomado: 'Diplomado' }[it.tipo];
  const fav = ALMACEN.favoritos.has(it.id);
  const enComp = ALMACEN.comparador.includes(it.id);

  const datos = esBeca
    ? [['Organización', it.institucion], ['País', it.pais], ['Cobertura', it.cobertura || '—'],
       ['Niveles', (it.niveles || []).join(', ') || '—'], ['Modalidad', it.modalidad],
       ['Duración', duracion(it)], ['Apertura', fecha(it.fecha_apertura)], ['Cierre', fecha(it.fecha_cierre)]]
    : [['Institución', it.institucion], ['País / ciudad', it.pais + (it.ciudad ? ' · ' + it.ciudad : '')],
       ['Área', it.area], ['Modalidad', it.modalidad], ['Duración', duracion(it)],
       ['Idioma', it.idioma], ['Costo referencial', dinero(it.costo_min, it.costo_max, it.moneda)],
       ['Admisión', it.admision], ['Financiamiento', it.financiamiento],
       ['Convalidación en Perú', it.convalidacion]];

  const incluye = esBeca && it.incluye
    ? Object.entries(it.incluye).filter(([, v]) => v).map(([k]) =>
        `<span class="pastilla" style="pointer-events:none">${ico('escudo', 13)} ${escapar(k.replace('_', ' '))}</span>`).join('')
    : '';

  const velo = document.createElement('div');
  velo.className = 'velo';
  velo.innerHTML = `
    <div class="modal" role="dialog" aria-modal="true" aria-label="${escapar(it.nombre)}">
      <button class="cerrar" data-cerrar aria-label="Cerrar">${ico('x', 18)}</button>
      <div class="modal-cabecera">
        <div class="sup">${marcaLogo(it, 60)}
          <div style="min-width:0">
            <span class="insignia ${it.tipo}">${nombreTipo}</span>
            <h2>${escapar(it.nombre)}</h2>
            <p style="margin:0;color:var(--suave);font-size:14px">${escapar(it.institucion)}</p>
            <div style="margin-top:9px">${selloSunedu(it)}</div>
          </div>
        </div>
      </div>
      <div class="modal-cuerpo">
        ${it.descripcion ? `<p style="margin:0 0 18px;color:var(--oliva-2);line-height:1.6">${escapar(it.descripcion)}</p>` : ''}
        <div class="datos">
          ${datos.map(([k, v]) => `<div class="dato"><span>${escapar(k)}</span><b>${escapar(v || '—')}</b></div>`).join('')}
        </div>
        ${incluye ? `<h4 style="font-family:var(--display);margin:0 0 10px">La beca incluye</h4>
          <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px">${incluye}</div>` : ''}
        ${(it.requisitos || []).length ? `<h4 style="font-family:var(--display);margin:0 0 10px">Requisitos principales</h4>
          <ul style="margin:0 0 18px;padding-left:20px;color:var(--oliva-2);line-height:1.7;font-size:14px">
            ${it.requisitos.map(r => `<li>${escapar(r)}</li>`).join('')}</ul>` : ''}
        <div class="modal-acciones">
          <a class="btn btn-primario" href="${escapar(it.url)}" target="_blank" rel="noopener">
            ${ico('enlace', 16)} Ir al sitio oficial</a>
          ${it.url_busqueda && it.url_busqueda !== it.url
            ? `<a class="btn btn-linea" href="${escapar(it.url_busqueda)}" target="_blank" rel="noopener">
                 ${ico('lupa', 16)} Buscar el programa</a>` : ''}
          <button class="btn btn-linea" data-accion="favorito" data-id="${escapar(it.id)}">
            ${ico('marcador', 16, fav ? 'fill="currentColor"' : '')} ${fav ? 'Guardado' : 'Guardar'}</button>
          <button class="btn ${enComp ? 'btn-oliva' : 'btn-linea'}" data-accion="comparar" data-id="${escapar(it.id)}">
            ${ico('balanza', 16)} ${enComp ? 'En el comparador' : 'Comparar'}</button>
        </div>
        <div class="aviso">${ico('info', 15)}
          <span>Ruta Amauta es un directorio independiente. Los costos, fechas y requisitos mostrados
          son referenciales: confirma siempre la información en la web oficial de la institución
          antes de postular o pagar.</span>
        </div>
      </div>
    </div>`;

  velo.addEventListener('click', (e) => {
    if (e.target === velo || e.target.closest('[data-cerrar]')) cerrarFicha();
  });
  document.body.appendChild(velo);
  document.body.style.overflow = 'hidden';
}

function cerrarFicha() {
  const v = $('.velo');
  if (v) v.remove();
  document.body.style.overflow = '';
  if (location.hash.startsWith('#/programa/')) history.back();
}

/* ============================================================== router */

const VISTAS = {
  inicio: vistaInicio, becas: () => vistaListado('becas'),
  maestrias: () => vistaListado('maestrias'), doctorados: () => vistaListado('doctorados'),
  diplomados: () => vistaListado('diplomados'), favoritos: vistaFavoritos,
  comparador: vistaComparador, instituciones: vistaInstituciones,
};

function leerRuta() {
  const bruto = location.hash.replace(/^#\/?/, '') || 'inicio';
  const [camino, consulta] = bruto.split('?');
  const partes = camino.split('/').filter(Boolean);
  return { vista: partes[0] || 'inicio', param: partes[1] ? decodeURIComponent(partes[1]) : null,
           params: new URLSearchParams(consulta || '') };
}

function pintar() {
  const { vista, param, params } = leerRuta();

  if (vista === 'programa' && param) {
    // la ficha se muestra sobre la última vista renderizada
    if (!$('#vista').dataset.pintado) { $('#vista').innerHTML = vistaInicio(); $('#vista').dataset.pintado = '1'; }
    if (!$('.velo')) abrirFicha(param);
    return;
  }
  cerrarModalSilencioso();

  const render = VISTAS[vista] || VISTAS.inicio;
  const nombreVista = VISTAS[vista] ? vista : 'inicio';

  // parámetros de URL -> filtros (enlaces de rutas destacadas)
  if ([...params.keys()].length && CONFIG_VISTA[nombreVista]) {
    const f = filtrosDe(nombreVista);
    params.forEach((v, k) => { f[k] = v; });
    f.pagina = 1;
  }

  $('#vista').innerHTML = render();
  $('#vista').dataset.pintado = '1';
  $$('.nav a').forEach(a => a.classList.toggle('activo', a.dataset.ruta === nombreVista));
  $('#nav').classList.remove('abierto');
  pintarGlobos();
  window.scrollTo({ top: 0, behavior: 'instant' in window ? 'instant' : 'auto' });
}

function cerrarModalSilencioso() {
  const v = $('.velo');
  if (v) { v.remove(); document.body.style.overflow = ''; }
}

function pintarGlobos() {
  const gf = $('#globo-favoritos'), gc = $('#globo-comparador');
  if (gf) { gf.textContent = ALMACEN.favoritos.size; gf.classList.toggle('oculto', !ALMACEN.favoritos.size); }
  if (gc) { gc.textContent = ALMACEN.comparador.length; gc.classList.toggle('oculto', !ALMACEN.comparador.length); }
}

/* ============================================================== eventos */

document.addEventListener('click', (e) => {
  const btnMenu = e.target.closest('#btn-menu');
  if (btnMenu) { $('#nav').classList.toggle('abierto'); return; }

  const arriba = e.target.closest('#btn-buscar-arriba');
  if (arriba) {
    const campo = $('[data-f="q"]') || $('#q-inicio');
    if (campo) { campo.focus(); campo.scrollIntoView({ block: 'center', behavior: 'smooth' }); }
    else location.hash = '#/maestrias';
    return;
  }

  const acc = e.target.closest('[data-accion]');
  if (acc) {
    const { accion, id } = acc.dataset;
    if (accion === 'favorito') { ALMACEN.alternarFavorito(id); actualizarTrasCambio(id); }
    if (accion === 'comparar') {
      if (!ALMACEN.alternarComparador(id)) alert('El comparador admite hasta 4 programas. Quita uno para añadir otro.');
      else actualizarTrasCambio(id);
    }
    if (accion === 'ver') location.hash = '#/programa/' + encodeURIComponent(id);
    return;
  }

  const rapido = e.target.closest('[data-rapido]');
  if (rapido) {
    const vista = rapido.closest('[data-vista]').dataset.vista;
    const f = filtrosDe(vista);
    const clave = rapido.dataset.rapido, valor = rapido.dataset.valor;
    f[clave] = f[clave] === valor ? '' : valor;
    f.pagina = 1;
    pintar();
    return;
  }

  if (e.target.closest('[data-limpiar]')) {
    const vista = e.target.closest('[data-vista]').dataset.vista;
    FILTROS[vista] = { q: '', pagina: 1, orden: 'relevancia' };
    pintar();
    return;
  }

  const pestana = e.target.closest('[data-pestana]');
  if (pestana) { filtrosDe('favoritos').tipo = pestana.dataset.pestana; pintar(); return; }

  if (e.target.closest('[data-vaciar-comparador]')) {
    ALMACEN.comparador = []; ALMACEN.guardar(); pintar(); return;
  }

  const pag = e.target.closest('[data-pagina]');
  if (pag && !pag.disabled) {
    const vista = leerRuta().vista;
    filtrosDe(vista).pagina = +pag.dataset.pagina;
    pintar();
    $('#resultados')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
});

// Las vistas que dependen del estado se repintan; en los listados solo se
// actualizan los botones afectados, para no perder el scroll ni el foco.
function actualizarTrasCambio(id) {
  const v = leerRuta().vista;
  if (v === 'favoritos' || v === 'comparador') { pintar(); return; }

  const fav = ALMACEN.favoritos.has(id);
  const enComp = ALMACEN.comparador.includes(id);

  $$(`[data-accion="favorito"][data-id="${CSS.escape(id)}"]`).forEach(b => {
    b.classList.toggle('activo', fav);
    const esBotonModal = b.classList.contains('btn');
    b.innerHTML = ico('marcador', esBotonModal ? 16 : 19, fav ? 'fill="currentColor"' : '')
      + (esBotonModal ? (fav ? ' Guardado' : ' Guardar') : '');
    b.title = fav ? 'Quitar de favoritos' : 'Guardar en favoritos';
  });

  $$(`[data-accion="comparar"][data-id="${CSS.escape(id)}"]`).forEach(b => {
    if (b.classList.contains('quitar')) return;
    const esBotonModal = b.classList.contains('btn');
    b.classList.toggle(esBotonModal ? 'btn-oliva' : 'en-comparador', enComp);
    b.classList.toggle('btn-linea', esBotonModal && !enComp);
    b.innerHTML = ico('balanza', esBotonModal ? 16 : 13) + ' ' +
      (enComp ? (esBotonModal ? 'En el comparador' : 'Añadido') : 'Comparar');
  });

  pintarGlobos();
}

document.addEventListener('change', (e) => {
  const campo = e.target.closest('[data-f]');
  if (!campo) return;
  const cont = campo.closest('[data-vista]');
  if (!cont) return;
  const f = filtrosDe(cont.dataset.vista);
  f[campo.dataset.f] = campo.value;
  f.pagina = 1;
  pintar();
});

let temporizador;
document.addEventListener('input', (e) => {
  const campo = e.target.closest('input[data-f="q"]');
  if (!campo) return;
  const cont = campo.closest('[data-vista]');
  if (!cont) return;
  clearTimeout(temporizador);
  temporizador = setTimeout(() => {
    const f = filtrosDe(cont.dataset.vista);
    f.q = campo.value;
    f.pagina = 1;
    pintar();
    const nuevo = $(`[data-vista="${cont.dataset.vista}"] input[data-f="q"]`);
    if (nuevo) { nuevo.focus(); nuevo.setSelectionRange(nuevo.value.length, nuevo.value.length); }
  }, 260);
});

document.addEventListener('submit', (e) => {
  if (e.target.id === 'form-inicio') {
    e.preventDefault();
    const q = $('#q-inicio').value.trim();
    filtrosDe('maestrias').q = q;
    filtrosDe('becas').q = q;
    location.hash = '#/maestrias';
  }
  if (e.target.id === 'form-filtros') e.preventDefault();
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && $('.velo')) cerrarFicha();
});

window.addEventListener('hashchange', pintar);

/* =============================================================== inicio */

$('#anio').textContent = new Date().getFullYear();

cargar().then(() => {
  pintar();
}).catch(err => {
  console.error(err);
  $('#vista').innerHTML = `<div class="contenedor seccion">${
    vacio('No se pudo cargar el catálogo', 'Recarga la página en unos segundos.')}</div>`;
});

})();
