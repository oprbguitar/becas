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

// Búsqueda restringida al dominio oficial: salida garantizada cuando el
// enlace directo no se pudo comprobar.
const busquedaEn = (dominio, texto) => dominio
  ? 'https://www.google.com/search?q=' + encodeURIComponent(`site:${dominio} "${texto}"`)
  : 'https://www.google.com/search?q=' + encodeURIComponent(texto);

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
  copiar: '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3"/>',
  correo: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
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

const DATOS = { items: [], porId: new Map(), meta: null, instituciones: [], listo: false,
                sunedu: null, convocatorias: null, verificados: null, guia: null };

// Contrapartes con tratado que publica SUNEDU en su página del procedimiento
// de reconocimiento de grados extranjeros (consultada el 02/11/2026).
const TRATADO = new Set(['Alemania', 'Argentina', 'Austria', 'Bélgica', 'Brasil', 'Bolivia',
  'Bulgaria', 'Canadá', 'Croacia', 'Chile', 'China', 'Chipre', 'Colombia', 'Corea del Sur',
  'Costa Rica', 'Cuba', 'Dinamarca', 'Ecuador', 'El Salvador', 'Eslovaquia', 'Eslovenia',
  'España', 'Estonia', 'Estados Unidos', 'Finlandia', 'Francia', 'Grecia', 'Honduras', 'Hungría',
  'India', 'Irlanda', 'Islandia', 'Italia', 'Japón', 'Letonia', 'Liechtenstein', 'Lituania',
  'Luxemburgo', 'Malta', 'Marruecos', 'México', 'Nicaragua', 'Noruega', 'Países Bajos', 'Panamá',
  'Paraguay', 'Polonia', 'Portugal', 'Reino Unido', 'República Checa', 'Rumania', 'Rusia',
  'Santa Sede', 'Singapur', 'Serbia', 'Suecia', 'Suiza', 'Ucrania', 'Uruguay', 'Venezuela']);

const URL_SUNEDU = {
  licenciadas: 'https://www.sunedu.gob.pe/lista-de-universidades-licenciadas/',
  denegadas: 'https://www.sunedu.gob.pe/lista-de-universidades-denegadas/',
  extranjeros: 'https://www.sunedu.gob.pe/procedimiento-de-reconocimiento-de-grados-y-titulos-extranjeros/',
  lista2025: 'https://www.gob.pe/institucion/sunedu/normas-legales/7682493-00004-2026-sunedu-ds-dirgratu',
  ruct: 'https://www.educacion.gob.es/ruct/consultauniversidades?actual=universidades',
  presencialPeru: 'https://www.sunedu.gob.pe/sobre-grados-titulos-emitidos-universidades-extranjeras-estudios-realizados-territorio-peruano-12-02-2020/',
  correo: 'consultasreconocimiento@sunedu.gob.pe',
};

/* ================================================= carga y normalización */

const ETIQUETA_SUNEDU = {
  licenciada: { texto: 'Licenciada por SUNEDU', clase: 'ok' },
  proceso: { texto: 'Licenciamiento en trámite', clase: 'proceso' },
  extranjera: { texto: 'Extranjera · ruta SUNEDU por verificar', clase: 'ext' },
  tratado: { texto: 'Extranjera · país con tratado', clase: 'ext' },
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
    url: b.url, url_requisitos: b.url_requisitos,
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

  const [becas, maestrias, doctorados, diplomados, instituciones, meta, enlaces,
         sunedu, convocatorias, verificados] =
    await Promise.all([
      pedir('data/becas.json', []),
      pedir('data/maestrias.json', []),
      pedir('data/doctorados.json', []),
      pedir('data/diplomados.json', []),
      pedir('data/instituciones.json', []),
      pedir('data/meta_catalogo.json', null),
      pedir('data/enlaces.json', null),
      pedir('data/sunedu.json', null),
      pedir('data/convocatorias.json', null),
      pedir('data/programas_verificados.json', null),
    ]);
  DATOS.sunedu = sunedu;
  DATOS.convocatorias = convocatorias;
  DATOS.verificados = verificados;
  const cruce = (sunedu && sunedu.cruce_catalogo) || {};

  DATOS.items = [
    ...becas.map(normalizarBeca),
    ...maestrias, ...doctorados, ...diplomados,
  ];

  // scraper/validar_enlaces.py comprueba cada destino y, si la ruta declarada
  // no abre, descubre la sección real de posgrado leyendo la portada. Aquí se
  // aplica ese informe, de modo que el sitio nunca publique un enlace roto.
  const porInst = (enlaces && enlaces.instituciones) || {};
  const porBeca = (enlaces && enlaces.becas) || {};
  DATOS.enlaces = enlaces;

  const aplicar = (it, info) => {
    if (!info) return;
    if (info.url) it.url = info.url;
    it.enlace_estado = info.estado;
    it.enlace_nivel = info.nivel;
    if (info.alternativa) it.url_alternativa = info.alternativa;
  };

  // El estado SUNEDU que se muestra es el de la lista oficial, no el de la
  // semilla: scraper/sunedu_listas.py deja el cruce en data/sunedu.json.
  const oficial = (it, idInst) => {
    const c = cruce[idInst];
    if (c) {
      it.sunedu_cruce = c;
      it.sunedu = c.oficial === 'licenciada' ? 'licenciada' : 'proceso';
    } else if (it.pais && it.pais !== 'Perú' && it.sunedu === 'extranjera' && TRATADO.has(it.pais)) {
      it.sunedu = 'tratado';
    }
  };

  DATOS.items.forEach(it => {
    aplicar(it, it.tipo === 'beca' ? porBeca[it.id] : porInst[it.institucion_id]);
    if (it.tipo !== 'beca') oficial(it, it.institucion_id);
    it.url_busqueda = it.url_alternativa || busquedaEn(it.dominio, it.nombre);
    it.buscable = normalizar([it.nombre, it.institucion, it.sigla, it.pais,
                              it.ciudad, it.area, (it.areas || []).join(' ')].join(' '));
    DATOS.porId.set(it.id, it);
  });

  instituciones.forEach(u => {
    const info = porInst[u.id];
    if (info && info.url) { u.url_posgrado = info.url; u.enlace_estado = info.estado; }
    oficial(u, u.id);
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

// Estado de comprobación del enlace, según data/enlaces.json.
const ETIQUETA_ENLACE = {
  ok: { texto: 'Enlace comprobado', clase: 'ok' },
  manual: { texto: 'Enlace verificado a mano', clase: 'ok' },
  protegido: { texto: 'Enlace activo (el sitio bloquea robots)', clase: 'ext' },
  sin_respuesta: { texto: 'Enlace sin comprobar', clase: 'proceso' },
};

function selloEnlace(item) {
  const e = ETIQUETA_ENLACE[item.enlace_estado];
  if (!e) return '';
  return `<span class="sello ${e.clase}">${ico('enlace', 13)} ${escapar(e.texto)}</span>`;
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
    if (f.sunedu && it.sunedu !== f.sunedu && !(f.sunedu === 'extranjera' && it.sunedu === 'tratado')) return false;
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

function portada({ titulo, resalte, bajada, lema, antetitulo, clase = '' }) {
  return `
  <section class="portada ${clase}">
    <div class="contenedor portada-texto">
      ${antetitulo ? `<p class="antetitulo">${antetitulo}</p>` : ''}
      <h1 class="titulo">${titulo.replace('{r}', `<em>${escapar(resalte)}</em>`)}</h1>
      <p class="bajada">${escapar(bajada)}</p>
      ${lema ? `<p class="lema">${escapar(lema)}</p>` : ''}
    </div>
  </section>`;
}

/* ---------------------------------------------------------- inicio */

function vistaInicio() {
  const total = DATOS.items.length;
  const paises = new Set(DATOS.items.map(i => i.pais)).size;
  const insts = DATOS.instituciones.length;
  // Las becas ya tienen su propia sección con fechas verificadas; aquí solo
  // posgrados, uno peruano y otro extranjero por tipo cuando existan.
  const destacados = ['maestria', 'doctorado']
    .flatMap(t => [DATOS.items.find(i => i.destacado && i.tipo === t && i.pais === 'Perú'),
                   DATOS.items.find(i => i.destacado && i.tipo === t && i.pais !== 'Perú')])
    .filter(Boolean).slice(0, 4);
  const abiertas = convocatoriasOrdenadas().filter(c => estadoConv(c) === 'abierta').slice(0, 4);
  const sun = DATOS.sunedu;

  const explorar = [
    { ruta: 'becas', titulo: 'Becas', texto: 'Financiamiento completo y parcial', n: porTipo('beca').length },
    { ruta: 'maestrias', titulo: 'Maestrías', texto: 'Perú, Latinoamérica y el mundo', n: porTipo('maestria').length },
    { ruta: 'doctorados', titulo: 'Doctorados', texto: 'Investigación y financiamiento', n: porTipo('doctorado').length },
    { ruta: 'diplomados', titulo: 'Diplomados', texto: 'Formación corta y vigente', n: porTipo('diplomado').length },
  ];

  return portada({
    titulo: 'Tu {r} al conocimiento.', resalte: 'ruta',
    bajada: 'Convocatorias verificadas, becas y posgrados para peruanos, con el contraste SUNEDU a la vista antes de postular o pagar.',
  }) + `
  <div class="contenedor centro">
    <form class="buscador-portada" id="form-inicio" role="search">
      <div class="campo-busqueda">
        ${ico('lupa', 19)}
        <input type="search" id="q-inicio" placeholder="Programa, país, universidad o área"
               autocomplete="off" aria-label="Buscar en el catálogo">
      </div>
      <button class="btn btn-primario btn-alto" type="submit">Buscar</button>
    </form>
    <p class="cifras-portada"><b>${numero(total)}</b> oportunidades · <b>${numero(paises)}</b> países · <b>${numero(insts)}</b> instituciones</p>
  </div>

  <section class="seccion">
    <div class="contenedor">
      <div class="seccion-cabecera">
        <div>
          <h2>Convocatorias abiertas ahora</h2>
          <p class="subtitulo-bloque">Fechas leídas en la fuente oficial${DATOS.convocatorias ? ' el ' + fecha(DATOS.convocatorias.consultado) : ''}.</p>
        </div>
        <a class="btn-texto" href="#/convocatorias">Ver todas ${ico('flecha', 14)}</a>
      </div>
      ${abiertas.length ? `<div class="lista-filas">${abiertas.map(filaConvocatoria).join('')}</div>`
        : vacio('Sin convocatorias abiertas', 'Revisa las próximas en la sección Convocatorias.')}
    </div>
  </section>

  <section class="seccion banda-oscura">
    <div class="contenedor herramienta">
      <div>
        <h2 class="titulo-bloque">¿Tu universidad está licenciada?</h2>
        <p class="subtitulo-bloque">Consulta directa contra la lista oficial de SUNEDU, con el número y el enlace de la resolución.</p>
        ${sun ? `<div class="cifras-sunedu">
          <div><b>${sun.declaradas_licenciadas || sun.licenciadas.length}</b><span>licenciadas</span></div>
          <div><b>${sun.denegadas.length}</b><span>con licencia denegada</span></div>
          <div><b>${fecha(sun.corte_licenciadas)}</b><span>corte de la lista</span></div>
        </div>` : ''}
      </div>
      <div>
        ${buscadorSunedu('inicio')}
        <p style="margin:12px 0 0"><a class="btn-texto" style="color:var(--arena)" href="#/sunedu">Ruta para grados extranjeros ${ico('flecha', 14)}</a></p>
      </div>
    </div>
  </section>

  <section class="seccion">
    <div class="contenedor">
      <div class="seccion-cabecera"><h2>Explora el catálogo</h2></div>
      <nav class="explorar" aria-label="Tipos de programa">
        ${explorar.map(r => `
          <a href="#/${r.ruta}"><span class="cifra">${numero(r.n)}</span><b>${r.titulo}</b><span>${r.texto}</span></a>`).join('')}
      </nav>
      <p class="aviso-legal" style="justify-content:flex-start;padding:12px 0 0">${ico('info', 14)} Maestrías, doctorados y diplomados del catálogo son fichas exploratorias por área: confirma en la fuente oficial que el programa exista y su precio.</p>
    </div>
  </section>

  <section class="seccion" style="padding-top:0">
    <div class="contenedor">
      <div class="seccion-cabecera"><h2>Destacados</h2>
        <a class="btn-texto" href="#/maestrias">Ver posgrados ${ico('flecha', 14)}</a></div>
      <div class="rejilla cuatro">${destacados.map(tarjeta).join('')}</div>
    </div>
  </section>`;
}

/* ---------------------------------------------------------- listados */

const CONFIG_VISTA = {
  becas: {
    tipo: 'beca', titulo: '{r}.', resalte: 'Becas',
    bajada: 'Encuentra financiamiento para estudiar en Perú y el mundo.',
  },
  maestrias: {
    tipo: 'maestria', titulo: '{r}.', resalte: 'Maestrías',
    bajada: 'Programas para especializarte y crecer profesionalmente.',
  },
  doctorados: {
    tipo: 'doctorado', titulo: '{r}.', resalte: 'Doctorados',
    bajada: 'Programas de alto nivel, financiamiento y líneas de investigación.',
  },
  diplomados: {
    tipo: 'diplomado', titulo: '{r}.', resalte: 'Diplomados',
    bajada: 'Formación práctica y rápida para actualizar tus competencias.',
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
        <option value="tratado" ${f.sunedu === 'tratado' ? 'selected' : ''}>Extranjera · país con tratado</option>
        <option value="extranjera" ${f.sunedu === 'extranjera' ? 'selected' : ''}>Extranjera (todas)</option>
      </select></div>
    <div class="campo"><label>Costo máximo (US$)</label>
      <select data-f="costoMax">
        <option value="">Cualquier rango</option>
        ${[2000, 5000, 10000, 20000, 40000, 80000].map(v =>
          `<option value="${v}" ${String(f.costoMax) === String(v) ? 'selected' : ''}>Hasta US$ ${numero(v)}</option>`).join('')}
      </select></div>`;

  const segmento = esBeca ? '' : `
    <div class="contenedor centro" style="margin-bottom:24px">
      <nav class="segmentado" aria-label="Tipo de posgrado">
        ${['maestrias', 'doctorados', 'diplomados'].map(v => `
          <a href="#/${v}" ${v === vista ? 'aria-current="page"' : ''}>${CONFIG_VISTA[v].resalte}<span class="n">${numero(porTipo(CONFIG_VISTA[v].tipo).length)}</span></a>`).join('')}
      </nav>
    </div>`;

  return portada({ titulo: cfg.titulo, resalte: cfg.resalte, bajada: cfg.bajada, clase: 'compacta' })
    + segmento + `
  <div class="contenedor" id="resultados" style="padding-bottom:48px">
    ${esBeca ? `<div class="aviso neutro" style="margin:0 0 20px">${ico('calendario', 15)}
      <span>Este catálogo se rastrea cada semana. Para fechas leídas hoy en la fuente oficial, revisa
      <a class="btn-texto" href="#/convocatorias">Convocatorias vigentes</a>.</span></div>`
    : `<div class="aviso neutro" style="margin:0 0 20px">${ico('info', 15)}
      <span>Fichas exploratorias: se generan por área a partir de instituciones verificadas; el costo es un rango
      referencial y el enlace lleva a la escuela de posgrado. El estado SUNEDU sí es oficial. Las fichas con
      evidencia completa están en <a class="btn-texto" href="#/sunedu">Contraste SUNEDU</a>.</span></div>`}
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
          : `<button type="button" class="pastilla ${f.sunedu === 'licenciada' ? 'activa' : ''}" data-rapido="sunedu" data-valor="licenciada">${ico('escudo', 14)} Licenciadas SUNEDU</button>
             <button type="button" class="pastilla ${f.sunedu === 'tratado' ? 'activa' : ''}" data-rapido="sunedu" data-valor="tratado">${ico('globo', 14)} País con tratado</button>`}
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
  </div>`;
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
    clase: 'compacta',
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
      ? `<p class="conteo"><b>${numero(guardados.length)}</b> guardados · <b>${numero(ALMACEN.comparador.length)}</b> en el comparador · <b>${numero(new Set(guardados.map(i => i.pais)).size)}</b> países</p>` : ''}
    ${filtrados.length
      ? `<div class="rejilla" style="margin-top:18px">${filtrados.map(tarjeta).join('')}</div>`
      : vacio('Todavía no guardas nada',
              'Usa el marcador de cada tarjeta para guardar programas y compararlos después.')}
  </div>`;
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
      clase: 'compacta',
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
    clase: 'compacta',
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
    (!f.sunedu || u.sunedu === f.sunedu || (f.sunedu === 'extranjera' && u.sunedu === 'tratado')));

  return portada({
    titulo: '{r} verificadas.', resalte: 'Instituciones',
    bajada: 'Universidades y escuelas con su estado de licenciamiento y enlace oficial.',
    clase: 'compacta',
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

/* ---------------------------------------------------------- convocatorias */

const ETIQUETA_ESTADO = { abierta: 'Abierta', proxima: 'Próxima', cerrada: 'Cerrada' };

// El estado guardado se recalcula con la fecha de hoy: una convocatoria
// "abierta" cuyo cierre ya pasó se muestra cerrada sin esperar al rastreo.
function estadoConv(c) {
  if (c.estado === 'abierta' && c.cierre && diasPara(c.cierre) < 0) return 'cerrada';
  return c.estado;
}

function convocatoriasOrdenadas() {
  const lista = (DATOS.convocatorias && DATOS.convocatorias.convocatorias) || [];
  const peso = { abierta: 0, proxima: 1, cerrada: 2 };
  return [...lista].sort((a, b) => {
    const ea = estadoConv(a), eb = estadoConv(b);
    if (ea !== eb) return peso[ea] - peso[eb];
    if (ea === 'cerrada') return (b.cierre || '').localeCompare(a.cierre || '');
    return (a.cierre || '9').localeCompare(b.cierre || '9');
  });
}

function filaConvocatoria(c) {
  const est = estadoConv(c);
  const dias = c.cierre ? diasPara(c.cierre) : null;
  const quedan = est === 'abierta' && dias != null
    ? `<span class="quedan">${dias === 0 ? 'Cierra hoy' : dias === 1 ? 'Queda 1 día' : `Quedan ${dias} días`}</span>` : '';
  return `
  <details class="fila-conv">
    <summary>
      <span class="estado ${est}">${ETIQUETA_ESTADO[est] || est}</span>
      <div style="min-width:0">
        <h3>${escapar(c.nombre)}</h3>
        <p class="org">${escapar(c.organizacion)} · ${escapar(c.pais)} · ${escapar(c.niveles.join(', '))}</p>
      </div>
      <div class="cierre">${c.cierre ? `<b>${fecha(c.cierre)}</b>` : '<b>Por confirmar</b>'}${quedan || (c.cierre ? 'cierre' : '')}</div>
      <span class="chev">${ico('flecha', 18)}</span>
    </summary>
    <div class="detalle-conv">
      <div>
        ${c.cronograma.length ? `<h4>Cronograma</h4><ul class="cronograma">${c.cronograma.map(([k, v]) =>
          `<li><span>${escapar(k)}</span><span>${escapar(v)}</span></li>`).join('')}</ul>` : ''}
        ${c.cierre_hora ? `<p class="procedencia">${ico('reloj', 13)} ${escapar(c.cierre_hora)}</p>` : ''}
        <h4>Requisitos principales</h4>
        <ul>${c.requisitos.map(r => `<li>${escapar(r)}</li>`).join('')}</ul>
      </div>
      <div>
        <h4>Cupos</h4><p>${escapar(c.cupos)}</p>
        ${c.observaciones ? `<h4>Observaciones</h4><p>${escapar(c.observaciones)}</p>` : ''}
        <div class="modal-acciones" style="margin-bottom:12px">
          <a class="btn btn-primario" href="${escapar(c.url)}" target="_blank" rel="noopener">${ico('enlace', 15)} Fuente oficial</a>
        </div>
        ${c.documentos.length ? `<div class="fuentes-ev" style="margin-bottom:12px">${c.documentos.map(([t, u]) =>
          `<a href="${escapar(u)}" target="_blank" rel="noopener">${escapar(t)} ${ico('enlace', 12)}</a>`).join('')}</div>` : ''}
        <p class="procedencia">Fuente: ${escapar(c.fuente_tipo)} · consultada el ${fecha(c.consultado)}</p>
      </div>
    </div>
  </details>`;
}

function vistaConvocatorias() {
  const datos = DATOS.convocatorias;
  if (!datos) return `<div class="contenedor seccion">${vacio('Sin datos de convocatorias', 'No se pudo leer data/convocatorias.json.')}</div>`;
  const f = filtrosDe('convocatorias');
  const todas = convocatoriasOrdenadas();
  const n = (e) => todas.filter(c => estadoConv(c) === e).length;
  const filtro = f.estado || 'abierta';
  const lista = filtro === 'todas' ? todas : todas.filter(c => estadoConv(c) === filtro);
  const opcionesEstado = [['abierta', 'Abiertas', n('abierta')], ['proxima', 'Próximas', n('proxima')],
                          ['cerrada', 'Cerradas', n('cerrada')], ['todas', 'Todas', todas.length]];

  return portada({
    titulo: 'Convocatorias {r}.', resalte: 'vigentes', clase: 'compacta',
    bajada: 'Maestrías, doctorados, becas y cursos para peruanos, en el Perú y en el extranjero. Cada fecha se leyó en la fuente oficial.',
  }) + `
  <div class="contenedor centro" style="margin-bottom:24px">
    <div class="segmentado" role="group" aria-label="Estado de la convocatoria">
      ${opcionesEstado.map(([v, t, k]) =>
        `<button type="button" data-conv-estado="${v}" aria-pressed="${filtro === v}">${t}<span class="n">${k}</span></button>`).join('')}
    </div>
  </div>
  <div class="contenedor" style="padding-bottom:24px">
    ${lista.length ? `<div class="lista-filas">${lista.map(filaConvocatoria).join('')}</div>`
      : vacio('Nada en este estado', 'Prueba con otra pestaña.')}
    <div class="aviso neutro">${ico('info', 15)}
      <span><b>Cómo se verificó (${fecha(datos.consultado)}).</b> ${escapar(datos.metodo)} ${escapar(datos.nota)}</span>
    </div>
  </div>`;
}

/* ---------------------------------------------------------- SUNEDU */

function buscarSunedu(texto) {
  const sun = DATOS.sunedu;
  const q = normalizar(texto).trim();
  if (!sun || q.length < 3) return [];
  const palabras = q.split(/\s+/);
  return [...sun.licenciadas, ...sun.denegadas]
    .filter(r => { const n = normalizar(r.nombre); return palabras.every(p => n.includes(p)); })
    .slice(0, 6);
}

function resultadoSunedu(texto) {
  const sun = DATOS.sunedu;
  if (!sun) return `<p class="vacio-res">No se pudo cargar la lista oficial.</p>`;
  if (normalizar(texto).trim().length < 3) {
    return `<p class="vacio-res">Escribe al menos tres letras del nombre: «Continental», «San Marcos», «Callao»…</p>`;
  }
  const hallados = buscarSunedu(texto);
  if (!hallados.length) {
    return `<span class="estado no_figura">No figura</span>
      <h3>Sin coincidencias en las listas de SUNEDU</h3>
      <p style="color:var(--suave);margin:0">Puede tratarse de un instituto, una filial o un nombre distinto.
      Revisa la <a class="btn-texto" href="${URL_SUNEDU.licenciadas}" target="_blank" rel="noopener">lista oficial</a>.</p>`;
  }
  const r = hallados[0];
  const otros = hallados.slice(1);
  const lic = r.estado === 'licenciada';
  return `
    <span class="estado ${r.estado}">${lic ? 'Licenciada' : 'Licencia denegada'}</span>
    <h3>${escapar(r.nombre)}</h3>
    <dl class="pares">
      <dt>${lic ? 'Licenciada el' : 'Resolución publicada'}</dt><dd class="mono">${fecha(r.fecha)}</dd>
      ${r.resolucion ? `<dt>Resolución</dt><dd class="mono">${escapar(r.resolucion)}</dd>` : ''}
      ${r.departamento ? `<dt>Ubicación</dt><dd>${escapar(r.provincia)}, ${escapar(r.departamento)}</dd>` : ''}
      <dt>Gestión</dt><dd>${escapar(r.gestion)}${r.tipo === 'escuela_posgrado' ? ' · escuela de posgrado' : ''}</dd>
    </dl>
    ${r.observacion ? `<div class="aviso alerta" style="margin:0 0 12px">${ico('info', 15)}<span>${escapar(r.observacion)}</span></div>` : ''}
    ${!lic ? `<div class="aviso" style="margin:0 0 12px">${ico('info', 15)}<span>Una denegatoria histórica no equivale necesariamente a su estado de hoy: revisa actos posteriores.</span></div>` : ''}
    <div class="fuentes-ev">
      ${r.resolucion_url ? `<a href="${escapar(r.resolucion_url)}" target="_blank" rel="noopener">Ver resolución ${ico('enlace', 12)}</a>` : ''}
      <a href="${lic ? URL_SUNEDU.licenciadas : URL_SUNEDU.denegadas}" target="_blank" rel="noopener">Lista oficial ${ico('enlace', 12)}</a>
    </div>
    <p class="procedencia" style="margin:12px 0 0">Lista con corte al ${fecha(sun.corte_licenciadas)} · consultada el ${fecha(sun.consultado)}${sun.estado_fuente === 'desactualizado' ? ' · <b>desactualizada</b>' : ''}</p>
    ${otros.length ? `<p class="procedencia" style="margin:8px 0 0">También coincide: ${otros.map(o =>
      `<button type="button" class="btn-texto" data-sunedu-elige="${escapar(o.nombre)}">${escapar(o.nombre)}</button>`).join(' · ')}</p>` : ''}`;
}

function buscadorSunedu(lugar) {
  const sun = DATOS.sunedu;
  const nombres = sun ? [...sun.licenciadas, ...sun.denegadas].map(r => r.nombre) : [];
  return `
    <div class="campo-busqueda" style="box-shadow:none">
      ${ico('escudo', 18)}
      <input type="search" data-sunedu-q="${lugar}" list="lista-sunedu-${lugar}" autocomplete="off"
             placeholder="Nombre de la universidad" aria-label="Buscar universidad en la lista de SUNEDU">
      <datalist id="lista-sunedu-${lugar}">${nombres.map(n => `<option value="${escapar(n)}">`).join('')}</datalist>
    </div>
    <div class="resultado-sunedu" data-sunedu-res="${lugar}" aria-live="polite" style="margin-top:12px;color:var(--texto)">
      ${resultadoSunedu('')}
    </div>`;
}

// Evaluación de la ruta de reconocimiento de un grado extranjero. Solo
// combina reglas publicadas por SUNEDU; nunca afirma un reconocimiento.
function evaluarRuta({ pais, titulo, modalidad }) {
  const items = [];
  const conTratado = TRATADO.has(pais);

  if (titulo === 'certificado') {
    items.push(['no_compatible', 'Tipo de documento', 'Un certificado de curso o diplomado no equivale por sí mismo a un grado universitario de maestría o doctorado.']);
  } else if (titulo === 'propio') {
    items.push(pais === 'España'
      ? ['no_compatible', 'Tipo de documento', 'Los títulos propios otorgados en España no serán reconocidos por la SUNEDU. Solo los títulos oficiales, expedidos a nombre del Rey.']
      : ['condicionado', 'Tipo de documento', 'Confirma con la autoridad educativa del país que el diploma sea un grado oficial y no un título propio o de educación continua.']);
  } else if (titulo === 'oficial') {
    items.push(['condicionado', 'Tipo de documento', pais === 'España'
      ? 'Comprueba el programa en el RUCT de España: debe figurar como título oficial.'
      : 'Declarado oficial: comprueba el registro de la autoridad educativa del país de origen.']);
  } else {
    items.push(['pendiente', 'Tipo de documento', 'Pide a la institución el nombre exacto del grado y si es oficial, propio o de educación continua.']);
  }

  if (!pais) {
    items.push(['pendiente', 'Vía por tratado', 'Elige el país donde se emite el diploma.']);
  } else if (conTratado) {
    items.push(['condicionado', 'Vía por tratado', `${pais} figura en la lista de contrapartes con tratado que publica SUNEDU. Revisa el alcance concreto del tratado: no todos los diplomas quedan cubiertos.`
      + (pais === 'Paraguay' ? ' El acuerdo con Paraguay no habilita por sí mismo el ejercicio profesional.' : '')]);
  } else {
    items.push(['pendiente', 'Vía por tratado', `${pais} no figura en la lista de tratados. Eso no excluye el grado: corresponde evaluar la vía del criterio de calidad.`]);
  }

  items.push([conTratado ? 'pendiente' : 'condicionado', 'Criterio de calidad',
    'Busca la universidad en el Anexo I de la RD 00004-2026-SUNEDU-DS-DIRGRATU (lista referida a 2025, entre las 500 primeras de QS, ARWU, THE o SIR). La tabla de la página de SUNEDU es para 2023: es histórica. Se aplica la lista vigente a la fecha de matrícula o de emisión del diploma.']);

  if (modalidad === 'presencial_pe') {
    items.push(['no_compatible', 'Lugar de estudios', 'SUNEDU publicó una advertencia sobre estudios presenciales en territorio peruano por universidades extranjeras. Pide confirmación escrita antes de pagar.']);
  } else if (modalidad === 'virtual') {
    items.push(['condicionado', 'Lugar de estudios', 'Programa virtual: formula la consulta a SUNEDU con el detalle exacto de la modalidad y de dónde se imparten los estudios.']);
  } else if (modalidad === 'presencial_ext') {
    items.push(['verificado', 'Lugar de estudios', 'Estudios presenciales en el país de origen: sin advertencia específica de SUNEDU.']);
  } else {
    items.push(['pendiente', 'Lugar de estudios', 'Indica la modalidad y el país donde se cursan los estudios.']);
  }

  const bloqueo = items.some(i => i[0] === 'no_compatible');
  const veredicto = bloqueo
    ? ['no_compatible', 'No compatible con evidencia']
    : conTratado && titulo === 'oficial'
      ? ['condicionado', 'Ruta de reconocimiento identificada']
      : ['pendiente', 'Pendiente de evidencia'];
  return { items, veredicto };
}

const ETIQUETA_EVIDENCIA = { verificado: 'Verificado', condicionado: 'Con condiciones', pendiente: 'Pendiente', no_compatible: 'No compatible' };

function htmlRuta(entrada) {
  const { items, veredicto } = evaluarRuta(entrada);
  return `
    <span class="estado ${veredicto[0]}">${ETIQUETA_EVIDENCIA[veredicto[0]]}</span>
    <h3>${veredicto[1]}</h3>
    <ul class="lista-chequeo">${items.map(([e, t, x]) => `
      <li><div><b>${t}</b><span class="estado ${e}">${ETIQUETA_EVIDENCIA[e]}</span></div><span>${escapar(x)}</span></li>`).join('')}</ul>
    <div class="aviso neutro">${ico('escudo', 15)}<span>La aprobación final corresponde a SUNEDU, que evalúa cada diploma
      individualmente; no otorga avales generales a programas extranjeros. Plazo máximo de evaluación: 30 días hábiles.</span></div>
    <div class="fuentes-ev" style="margin-top:12px">
      <a href="${URL_SUNEDU.extranjeros}" target="_blank" rel="noopener">Procedimiento SUNEDU ${ico('enlace', 12)}</a>
      <a href="${URL_SUNEDU.lista2025}" target="_blank" rel="noopener">RD 00004-2026 (lista 2025) ${ico('enlace', 12)}</a>
      ${entrada.pais === 'España' ? `<a href="${URL_SUNEDU.ruct}" target="_blank" rel="noopener">RUCT España ${ico('enlace', 12)}</a>` : ''}
      ${entrada.modalidad === 'presencial_pe' ? `<a href="${URL_SUNEDU.presencialPeru}" target="_blank" rel="noopener">Advertencia SUNEDU ${ico('enlace', 12)}</a>` : ''}
    </div>`;
}

const CARTA = { institucion: '', pais: '', programa: '', grado: '', caracter: '', modalidad: '', matricula: '', enlace: '', nombre: '' };

// Plantilla tomada literalmente de la guía de referencia; cada campo vacío
// conserva su marcador entre corchetes.
function textoCarta() {
  const v = (k, marcador) => (CARTA[k] || '').trim() || marcador;
  return `Asunto: Consulta previa sobre reconocimiento de grado extranjero

Señores de SUNEDU:

Solicito orientación sobre la posibilidad de solicitar el reconocimiento en el Perú del grado que obtendría en el siguiente programa:

- Institución que otorgará el grado: ${v('institucion', '[nombre completo]')}.
- País de origen: ${v('pais', '[país]')}.
- Programa: ${v('programa', '[nombre completo]')}.
- Grado o título exacto que se otorgará: ${v('grado', '[denominación]')}.
- Carácter del título: ${v('caracter', '[oficial / propio / por confirmar]')}.
- Modalidad y lugar de estudios: ${v('modalidad', '[virtual, presencial o semipresencial; indicar país]')}.
- Fecha prevista de matrícula: ${v('matricula', '[fecha]')}.
- Enlace oficial del programa: ${v('enlace', '[enlace]')}.

Agradeceré indicar qué criterio de reconocimiento resultaría aplicable, qué lista y resolución corresponde consultar según la fecha de matrícula y qué documentos adicionales debería verificar antes de iniciar los estudios.

Atentamente,
${v('nombre', '[Nombre completo]')}`;
}

function enlaceCorreo() {
  const [asunto, ...cuerpo] = textoCarta().split('\n');
  return `mailto:${URL_SUNEDU.correo}?subject=${encodeURIComponent(asunto.replace('Asunto: ', ''))}&body=${encodeURIComponent(cuerpo.join('\n').trim())}`;
}

function fichaEvidencia(p) {
  const nombres = { institucion: 'Institución', programa: 'Programa y diploma', ruta_sunedu: 'Ruta SUNEDU',
                    admision: 'Admisión (Ing. Industrial)', oferta: 'Oferta y costo' };
  const pr = p.precio;
  const precio = pr.total
    ? `<b>${SIMBOLO[pr.moneda] || pr.moneda} ${numero(pr.total)}</b><span>${pr.tipo === 'publicado' ? 'total publicado' : 'total calculado'}</span>`
    : `<b>Precio no publicado</b><span>no se trata como cero</span>`;
  return `
  <article class="evidencia">
    <div class="evidencia-cab">
      <div>
        <h3>${escapar(p.nombre)}</h3>
        <p class="institucion">${escapar(p.universidad)} · ${escapar(p.pais)}</p>
      </div>
      <div class="precio-ev">${precio}</div>
    </div>
    <div class="verificaciones">
      ${Object.entries(nombres).map(([k, t]) => {
        const v = p.verificaciones[k];
        return `<div><h4>${t}</h4><span class="estado ${v.estado}">${ETIQUETA_EVIDENCIA[v.estado]}</span><br>${escapar(v.texto)}</div>`;
      }).join('')}
    </div>
    <p class="detalle-costo"><b>Grado:</b> ${escapar(p.grado)} · <b>Modalidad:</b> ${escapar(p.modalidad)} · <b>Inicio:</b> ${escapar(p.inicio)}</p>
    ${pr.componentes.length ? `<p class="detalle-costo"><b>Costo:</b> ${pr.componentes.map(([k, x]) => `${escapar(k)}: ${escapar(x)}`).join(' · ')}</p>` : ''}
    ${pr.nota ? `<p class="detalle-costo">${escapar(pr.nota)}</p>` : ''}
    ${p.relacionados ? `<p class="detalle-costo">${escapar(p.relacionados)}</p>` : ''}
    <div class="fuentes-ev">${p.fuentes.map(([t, u]) => `<a href="${escapar(u)}" target="_blank" rel="noopener">${escapar(t)} ${ico('enlace', 12)}</a>`).join('')}
      <span class="procedencia">Revisado el ${fecha(p.consultado)}</span></div>
  </article>`;
}

async function cargarGuia() {
  if (DATOS.guia != null) return DATOS.guia;
  try {
    const r = await fetch('data/guia-sunedu.html', { cache: 'no-cache' });
    DATOS.guia = r.ok ? await r.text() : '';
  } catch { DATOS.guia = ''; }
  return DATOS.guia;
}

function htmlGuia(texto) {
  if (!texto) return `<p class="cargando">No se pudo cargar la guía.</p>`;
  const plantilla = document.createElement('template');
  plantilla.innerHTML = texto;
  return [...plantilla.content.querySelectorAll('.guia-bloque')].map((b, i) => `
    <details ${i === 0 ? 'open' : ''}>
      <summary>${escapar(b.querySelector('h2')?.textContent || 'Sección')} ${ico('flecha', 18)}</summary>
      ${b.outerHTML}
    </details>`).join('');
}

function vistaSunedu() {
  const sun = DATOS.sunedu;
  const ver = (DATOS.verificados && DATOS.verificados.programas) || [];
  const cruce = sun ? Object.values(sun.cruce_catalogo) : [];
  const coinciden = cruce.filter(c => c.oficial === 'licenciada' && !c.discrepancia).length;
  const corregidas = cruce.filter(c => c.discrepancia);
  const paises = [...new Set([...TRATADO, ...DATOS.instituciones.map(u => u.pais)])]
    .filter(p => p && p !== 'Perú').sort((a, b) => a.localeCompare(b, 'es'));
  const f = filtrosDe('sunedu');
  const entrada = { pais: f.pais || '', titulo: f.titulo || '', modalidad: f.modalidad || '' };
  const secciones = [['s-peru', 'Universidad peruana'], ['s-ext', 'Grado extranjero'],
                     ['s-fichas', 'Fichas con evidencia'], ['carta-sunedu', 'Consulta previa'], ['s-guia', 'Guía']];

  setTimeout(async () => {
    const destino = $('#guia-texto');
    if (destino) destino.innerHTML = htmlGuia(await cargarGuia());
  });

  return portada({
    titulo: 'Contraste {r}.', resalte: 'SUNEDU', clase: 'compacta',
    bajada: 'La licencia de una universidad, la validez de un programa y el reconocimiento de un futuro diploma son tres cosas distintas. Aquí se verifican por separado.',
  }) + `
  <div class="contenedor centro" style="margin-bottom:8px">
    <nav class="segmentado" aria-label="Secciones">
      ${secciones.map(([id, t]) => `<button type="button" data-ir="${id}">${t}</button>`).join('')}
    </nav>
  </div>

  <section class="seccion" id="s-peru">
    <div class="contenedor herramienta">
      <div>
        <h2 class="titulo-bloque">1. Universidad peruana</h2>
        <p class="subtitulo-bloque">SUNEDU otorga una licencia institucional y publica la resolución. La licencia, por sí sola, no responde por la filial, la modalidad ni el programa.</p>
        ${sun ? `<div class="cifras-sunedu">
          <div><b>${sun.licenciadas.filter(r => r.tipo === 'universidad').length}</b><span>universidades licenciadas</span></div>
          <div><b>${sun.licenciadas.filter(r => r.tipo === 'escuela_posgrado').length}</b><span>escuelas de posgrado</span></div>
          <div><b>${sun.denegadas.length}</b><span>con licencia denegada</span></div>
        </div>
        <p class="procedencia" style="margin-top:16px">Corte de SUNEDU: ${fecha(sun.corte_licenciadas)} · consultado el ${fecha(sun.consultado)} con <span class="mono">scraper/sunedu_listas.py</span></p>
        <div class="aviso neutro">${ico('balanza', 15)}<span><b>Cruce con el catálogo:</b> ${coinciden} de ${cruce.length} universidades peruanas coinciden con la lista oficial.
          ${corregidas.length ? `${corregidas.length} figuraban «en trámite» y SUNEDU las lista como licenciadas: ${corregidas.map(c => escapar(c.nombre_oficial)).join(' y ')}. El portal ya muestra el dato oficial.` : ''}</span></div>` : ''}
      </div>
      <div>${buscadorSunedu('sunedu')}</div>
    </div>
  </section>

  <section class="seccion banda" id="s-ext">
    <div class="contenedor herramienta">
      <div>
        <h2 class="titulo-bloque">2. Grado extranjero</h2>
        <p class="subtitulo-bloque">SUNEDU no certifica a las universidades del mundo: evalúa cada diploma. Hay dos vías, criterio de calidad o tratado, más la oficialidad del grado en su país.</p>
        <form class="rejilla-filtros" style="grid-template-columns:1fr;margin-top:24px" data-vista="sunedu" id="form-ruta">
          <div class="campo"><label for="ruta-pais">País que emite el diploma</label>
            <select id="ruta-pais" data-f="pais">${opciones(paises, entrada.pais, 'Elige un país')}</select></div>
          <div class="campo"><label for="ruta-titulo">Tipo de documento que recibirás</label>
            <select id="ruta-titulo" data-f="titulo">
              ${[['', 'No lo sé todavía'], ['oficial', 'Grado oficial (maestro, magíster, máster oficial, doctor)'],
                 ['propio', 'Título propio de la universidad'], ['certificado', 'Certificado, diploma o curso de educación continua']]
                .map(([v, t]) => `<option value="${v}" ${entrada.titulo === v ? 'selected' : ''}>${t}</option>`).join('')}
            </select></div>
          <div class="campo"><label for="ruta-modalidad">Modalidad y lugar de estudios</label>
            <select id="ruta-modalidad" data-f="modalidad">
              ${[['', 'No lo sé todavía'], ['presencial_ext', 'Presencial en el país de origen'],
                 ['virtual', 'Virtual'], ['presencial_pe', 'Presencial en el Perú']]
                .map(([v, t]) => `<option value="${v}" ${entrada.modalidad === v ? 'selected' : ''}>${t}</option>`).join('')}
            </select></div>
        </form>
      </div>
      <div class="resultado-sunedu" aria-live="polite">${htmlRuta(entrada)}</div>
    </div>
  </section>

  <section class="seccion" id="s-fichas">
    <div class="contenedor">
      <div class="seccion-cabecera"><div>
        <h2>3. Fichas con evidencia</h2>
        <p class="subtitulo-bloque">Programas reales revisados el ${DATOS.verificados ? fecha(DATOS.verificados.consultado) : '—'}, con cinco verificaciones separadas. Perfil: ${escapar((DATOS.verificados && DATOS.verificados.perfil) || '')}</p>
      </div></div>
      ${ver.map(fichaEvidencia).join('')}
    </div>
  </section>

  <section class="seccion banda" id="carta-sunedu">
    <div class="contenedor herramienta">
      <div>
        <h2 class="titulo-bloque">4. Consulta previa a SUNEDU</h2>
        <p class="subtitulo-bloque">Solicita respuesta escrita antes de pagar. Completa los datos y envía el texto a <span class="mono">${URL_SUNEDU.correo}</span>, o llama a la central (01) 500-3930.</p>
        <form class="form-carta" id="form-carta" style="margin-top:24px">
          ${[['institucion', 'Institución que otorgará el grado', 'ancho-2'], ['pais', 'País de origen', ''],
             ['matricula', 'Fecha prevista de matrícula', ''], ['programa', 'Programa', 'ancho-2'],
             ['grado', 'Grado o título exacto', 'ancho-2'], ['caracter', 'Carácter del título', ''],
             ['modalidad', 'Modalidad y lugar de estudios', ''], ['enlace', 'Enlace oficial del programa', 'ancho-2'],
             ['nombre', 'Tu nombre completo', 'ancho-2']]
            .map(([k, t, c]) => `<div class="campo ${c}"><label for="carta-${k}">${t}</label>
              <input type="text" id="carta-${k}" data-carta="${k}" value="${escapar(CARTA[k])}" autocomplete="off"></div>`).join('')}
        </form>
      </div>
      <div>
        <pre class="carta" id="texto-carta">${escapar(textoCarta())}</pre>
        <div class="acciones-carta">
          <button type="button" class="btn btn-primario" data-copiar-carta>${ico('copiar', 15)} Copiar texto</button>
          <a class="btn btn-linea" id="correo-carta" href="${escapar(enlaceCorreo())}">${ico('correo', 15)} Abrir en mi correo</a>
        </div>
      </div>
    </div>
  </section>

  <section class="seccion" id="s-guia">
    <div class="contenedor">
      <div class="seccion-cabecera"><div>
        <h2>5. Guía de verificación</h2>
        <p class="subtitulo-bloque">Texto de referencia íntegro, con sus fuentes oficiales.</p>
      </div></div>
      <div class="guia" id="guia-texto"><p class="cargando">Cargando la guía…</p></div>
    </div>
  </section>`;
}

/* ---------------------------------------------------------- contraste en la ficha */

function contrasteFicha(it) {
  if (it.tipo === 'beca') return '';
  const c = it.sunedu_cruce;
  if (c) {
    const lic = c.oficial === 'licenciada';
    return `<div class="contraste ${lic ? 'ok' : 'alerta'}">
      <h4>Contraste SUNEDU · institución</h4>
      <p><span class="estado ${c.oficial}">${lic ? 'Licenciada' : c.oficial === 'denegada' ? 'Licencia denegada' : 'No figura en la lista'}</span></p>
      ${c.nombre_oficial ? `<p>${escapar(c.nombre_oficial)}${c.fecha ? ` · desde el <span class="mono">${fecha(c.fecha)}</span>` : ''}${c.resolucion ? ` · Res. <span class="mono">${escapar(c.resolucion)}</span>` : ''}</p>` : ''}
      ${c.resolucion_url ? `<p class="fuentes-ev"><a href="${escapar(c.resolucion_url)}" target="_blank" rel="noopener">Ver resolución ${ico('enlace', 12)}</a></p>` : ''}
      <p class="procedencia">La licencia es institucional: no acredita por sí sola este programa, su sede ni su modalidad.</p>
    </div>`;
  }
  if (it.pais && it.pais !== 'Perú') {
    const t = TRATADO.has(it.pais);
    return `<div class="contraste condicionado">
      <h4>Contraste SUNEDU · grado extranjero</h4>
      <p><span class="estado ${t ? 'condicionado' : 'pendiente'}">${t ? 'País con tratado' : 'Sin tratado: evaluar criterio de calidad'}</span></p>
      <p>${t ? `${escapar(it.pais)} figura en la lista de contrapartes con tratado de SUNEDU. Ruta identificada, no garantizada.`
             : 'Busca la universidad en el Anexo I de la RD 00004-2026 (lista 2025).'}${it.pais === 'España' ? ' Verifica que sea título oficial en el RUCT: los títulos propios no se reconocen.' : ''}</p>
      <p class="fuentes-ev"><a href="#/sunedu">Evaluar la ruta completa ${ico('flecha', 12)}</a></p>
    </div>`;
  }
  return '';
}

/* ---------------------------------------------------------- ficha (modal) */

// El texto del botón dice a dónde lleva realmente el enlace comprobado.
function etiquetaEnlace(it) {
  if (it.tipo === 'beca') return 'Ir a la convocatoria oficial';
  if (['declarada', 'descubierta', 'manual'].includes(it.enlace_nivel))
    return 'Ir a la escuela de posgrado';
  return 'Ir al sitio oficial';
}

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
            <span class="insignia ${it.tipo}">${nombreTipo}${esBeca ? '' : ' · ficha exploratoria'}</span>
            <h2>${escapar(it.nombre)}</h2>
            <p style="margin:0;color:var(--suave);font-size:14px">${escapar(it.institucion)}</p>
            <div style="margin-top:9px;display:flex;gap:8px;flex-wrap:wrap">
              ${selloSunedu(it)}${selloEnlace(it)}
            </div>
          </div>
        </div>
      </div>
      <div class="modal-cuerpo">
        ${it.descripcion ? `<p style="margin:0 0 18px;color:var(--oliva-2);line-height:1.6">${escapar(it.descripcion)}</p>` : ''}
        ${contrasteFicha(it)}
        <div class="datos">
          ${datos.map(([k, v]) => `<div class="dato"><span>${escapar(k)}</span><b>${escapar(v || '—')}</b></div>`).join('')}
        </div>
        ${incluye ? `<h4 style="margin:0 0 10px">La beca incluye</h4>
          <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px">${incluye}</div>` : ''}
        ${(it.requisitos || []).length ? `<h4 style="margin:0 0 10px">Requisitos principales</h4>
          <ul style="margin:0 0 18px;padding-left:20px;color:var(--oliva-2);line-height:1.7;font-size:14px">
            ${it.requisitos.map(r => `<li>${escapar(r)}</li>`).join('')}</ul>` : ''}
        <div class="modal-acciones">
          <a class="btn btn-primario" href="${escapar(it.url)}" target="_blank" rel="noopener">
            ${ico('enlace', 16)} ${etiquetaEnlace(it)}</a>
          <a class="btn btn-linea" href="${escapar(it.url_busqueda)}" target="_blank" rel="noopener">
            ${ico('lupa', 16)} Buscar el programa</a>
          <button class="btn btn-linea" data-accion="favorito" data-id="${escapar(it.id)}">
            ${ico('marcador', 16, fav ? 'fill="currentColor"' : '')} ${fav ? 'Guardado' : 'Guardar'}</button>
          <button class="btn ${enComp ? 'btn-oliva' : 'btn-linea'}" data-accion="comparar" data-id="${escapar(it.id)}">
            ${ico('balanza', 16)} ${enComp ? 'En el comparador' : 'Comparar'}</button>
        </div>
        ${it.enlace_estado === 'sin_respuesta' ? `
          <div class="aviso" style="background:var(--ambar-suave);color:#7A5A22">
            ${ico('info', 15)}
            <span>No pudimos comprobar este enlace automáticamente (el sitio no
            respondió a nuestra verificación). Te llevamos a la portada oficial;
            si no encuentras el programa, usa <b>Buscar el programa</b>.</span>
          </div>` : ''}
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
  convocatorias: vistaConvocatorias, sunedu: vistaSunedu,
};

// Vistas que comparten un mismo enlace de la barra superior.
const GRUPO_NAV = { maestrias: 'posgrados', doctorados: 'posgrados', diplomados: 'posgrados' };

function leerRuta() {
  const bruto = location.hash.replace(/^#\/?/, '') || 'inicio';
  const [camino, consulta] = bruto.split('?');
  const partes = camino.split('/').filter(Boolean);
  return { vista: partes[0] || 'inicio', param: partes[1] ? decodeURIComponent(partes[1]) : null,
           params: new URLSearchParams(consulta || '') };
}

const META_VISTA = {
  inicio: ['Ruta Amauta — Buscador de becas, maestrías, doctorados y diplomados',
    'Busca y compara becas, maestrías, doctorados y diplomados en Perú, Latinoamérica y el mundo. Filtra por país, área, modalidad, costo y licenciamiento SUNEDU.'],
  becas: ['Becas para estudiar en Perú y el mundo | Ruta Amauta',
    'Convocatorias de becas completas y parciales para pregrado y posgrado, con cobertura, requisitos y fecha de cierre. Enlace directo a la convocatoria oficial.'],
  maestrias: ['Maestrías en Perú, Latinoamérica y el mundo | Ruta Amauta',
    'Compara maestrías por país, área, modalidad y costo. Verifica el licenciamiento SUNEDU y accede a la escuela de posgrado oficial de cada universidad.'],
  doctorados: ['Doctorados y programas de investigación | Ruta Amauta',
    'Doctorados en Perú y el extranjero: duración, líneas de investigación, financiamiento y enlace oficial a cada programa.'],
  diplomados: ['Diplomados y cursos de especialización | Ruta Amauta',
    'Diplomados presenciales, semipresenciales y online para actualizar tus competencias, con horas, costo referencial e institución.'],
  favoritos: ['Tus programas guardados | Ruta Amauta',
    'Revisa y organiza las oportunidades académicas que guardaste antes de decidir.'],
  comparador: ['Comparador de programas de posgrado | Ruta Amauta',
    'Compara hasta cuatro programas lado a lado: costo, duración, modalidad, financiamiento y licenciamiento.'],
  convocatorias: ['Convocatorias vigentes verificadas para peruanos | Ruta Amauta',
    'Becas, maestrías, doctorados y cursos con convocatoria abierta o próxima, con fechas leídas en la fuente oficial: PRONABEC, Erasmus Mundus, Eiffel, Gates Cambridge, OEA y más.'],
  sunedu: ['Contraste SUNEDU: licenciamiento y grados extranjeros | Ruta Amauta',
    'Consulta si una universidad peruana está licenciada con su resolución, evalúa la ruta de reconocimiento de un grado extranjero y redacta tu consulta previa a SUNEDU.'],
  instituciones: ['Universidades e instituciones verificadas | Ruta Amauta',
    'Universidades de Perú y el mundo con su estado de licenciamiento SUNEDU y enlace comprobado a su escuela de posgrado.'],
};

function actualizarMetadatos(vista, item) {
  let [titulo, descripcion] = META_VISTA[vista] || META_VISTA.inicio;
  if (item) {
    titulo = `${item.nombre} — ${item.institucion} | Ruta Amauta`;
    descripcion = item.descripcion
      || `${item.area} en ${item.institucion} (${item.pais}). ${duracion(item)}, modalidad ${item.modalidad.toLowerCase()}.`;
  }
  document.title = titulo;
  const meta = $('meta[name="description"]');
  if (meta) meta.setAttribute('content', descripcion.slice(0, 300));
  const canon = $('link[rel="canonical"]');
  if (canon) canon.setAttribute('href', 'https://ruta.amauta.online/' + location.hash);
}

function pintar() {
  const { vista, param, params } = leerRuta();

  if (vista === 'programa' && param) {
    // la ficha se muestra sobre la última vista renderizada
    if (!$('#vista').dataset.pintado) { $('#vista').innerHTML = vistaInicio(); $('#vista').dataset.pintado = '1'; }
    if (!$('.velo')) abrirFicha(param);
    actualizarMetadatos('inicio', DATOS.porId.get(param));
    return;
  }
  cerrarModalSilencioso();

  const render = VISTAS[vista] || VISTAS.inicio;
  const nombreVista = VISTAS[vista] ? vista : 'inicio';

  // Parámetros de URL -> filtros. Se parte de cero para que un enlace
  // compartido muestre exactamente lo que anuncia y no arrastre los filtros
  // que el visitante tuviera puestos antes.
  if ([...params.keys()].length && CONFIG_VISTA[nombreVista]) {
    FILTROS[nombreVista] = { q: '', pagina: 1, orden: 'relevancia' };
    const f = FILTROS[nombreVista];
    params.forEach((v, k) => { f[k] = v; });
  }

  $('#vista').innerHTML = render();
  $('#vista').dataset.pintado = '1';
  actualizarMetadatos(nombreVista);
  const grupo = GRUPO_NAV[nombreVista] || nombreVista;
  $$('.nav a').forEach(a => {
    const activo = a.dataset.ruta === grupo;
    a.classList.toggle('activo', activo);
    if (activo) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
  });
  $('#nav').classList.remove('abierto');
  $('#btn-menu')?.setAttribute('aria-expanded', 'false');
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
  if (btnMenu) {
    const abierto = $('#nav').classList.toggle('abierto');
    btnMenu.setAttribute('aria-expanded', String(abierto));
    return;
  }

  const estadoConvBtn = e.target.closest('[data-conv-estado]');
  if (estadoConvBtn) { filtrosDe('convocatorias').estado = estadoConvBtn.dataset.convEstado; pintar(); return; }

  const ir = e.target.closest('[data-ir]');
  if (ir) { document.getElementById(ir.dataset.ir)?.scrollIntoView({ behavior: 'smooth', block: 'start' }); return; }

  const elige = e.target.closest('[data-sunedu-elige]');
  if (elige) {
    const caja = elige.closest('[data-sunedu-res]');
    const campo = $(`[data-sunedu-q="${caja.dataset.suneduRes}"]`);
    campo.value = elige.dataset.suneduElige;
    caja.innerHTML = resultadoSunedu(campo.value);
    return;
  }

  if (e.target.closest('[data-copiar-carta]')) {
    const btn = e.target.closest('[data-copiar-carta]');
    const listo = () => { btn.innerHTML = ico('escudo', 15) + ' Copiado'; setTimeout(() => { btn.innerHTML = ico('copiar', 15) + ' Copiar texto'; }, 1800); };
    if (navigator.clipboard) navigator.clipboard.writeText(textoCarta()).then(listo, () => {});
    return;
  }

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
  if (cont.dataset.vista === 'sunedu') {
    if (campo.dataset.f === 'pais' && !CARTA.pais) CARTA.pais = campo.value;
    const panel = cont.closest('.herramienta').querySelector('.resultado-sunedu');
    panel.innerHTML = htmlRuta({ pais: f.pais || '', titulo: f.titulo || '', modalidad: f.modalidad || '' });
    return;
  }
  pintar();
});

let temporizador;
document.addEventListener('input', (e) => {
  // Verificador SUNEDU y carta: se actualiza solo su panel, sin repintar.
  const qSunedu = e.target.closest('[data-sunedu-q]');
  if (qSunedu) {
    const caja = $(`[data-sunedu-res="${qSunedu.dataset.suneduQ}"]`);
    if (caja) caja.innerHTML = resultadoSunedu(qSunedu.value);
    return;
  }
  const campoCarta = e.target.closest('[data-carta]');
  if (campoCarta) {
    CARTA[campoCarta.dataset.carta] = campoCarta.value;
    $('#texto-carta').textContent = textoCarta();
    $('#correo-carta').setAttribute('href', enlaceCorreo());
    return;
  }

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
  if (['form-filtros', 'form-ruta', 'form-carta'].includes(e.target.id)) e.preventDefault();
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
