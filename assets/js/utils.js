/**
 * Utilidades compartidas: formato, fechas, geografía y micro-interacciones.
 * Sin dependencias externas: todo el portal es HTML + CSS + JS estándar.
 */

/** Agrupa llamadas seguidas en una sola (para el buscador en vivo). */
export function retardar(fn, ms = 180) {
  let id;
  return (...args) => {
    clearTimeout(id);
    id = setTimeout(() => fn(...args), ms);
  };
}

/** Ejecuta como máximo una vez por frame (para eventos de scroll). */
export function porFrame(fn) {
  let pendiente = false;
  return (...args) => {
    if (pendiente) return;
    pendiente = true;
    requestAnimationFrame(() => { pendiente = false; fn(...args); });
  };
}

/** Texto sin tildes ni mayúsculas, para comparar búsquedas. */
export function normalizar(txt = "") {
  return txt.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}

const FMT_FECHA = new Intl.DateTimeFormat("es", { day: "2-digit", month: "short", year: "numeric" });
const FMT_FECHA_CORTA = new Intl.DateTimeFormat("es", { day: "2-digit", month: "short" });

export function aFecha(iso) {
  if (!iso) return null;
  const d = new Date(`${iso}T12:00:00Z`);
  return Number.isNaN(d.getTime()) ? null : d;
}

export function fechaLegible(iso, corta = false) {
  const d = aFecha(iso);
  if (!d) return "Sin fecha";
  return (corta ? FMT_FECHA_CORTA : FMT_FECHA).format(d);
}

/** Días que faltan para una fecha (negativo si ya pasó). */
export function diasHasta(iso) {
  const d = aFecha(iso);
  if (!d) return null;
  const hoy = new Date();
  hoy.setHours(0, 0, 0, 0);
  return Math.round((d - hoy) / 86400000);
}

/**
 * Estado de la convocatoria en función de sus fechas.
 * Las convocatorias son anuales: si ya cerró, se asume que reabre el año próximo.
 */
export function estadoConvocatoria(beca) {
  const faltaCierre = diasHasta(beca.fecha_cierre);
  const faltaApertura = diasHasta(beca.fecha_apertura);
  if (faltaCierre === null) return { clave: "sin-fecha", texto: "Fechas por confirmar", tono: "" };
  if (faltaCierre < 0) return { clave: "cerrada", texto: "Cerrada · vuelve el próximo ciclo", tono: "peligro", dias: faltaCierre };
  if (faltaApertura !== null && faltaApertura > 0)
    return { clave: "proxima", texto: `Abre en ${faltaApertura} día${faltaApertura === 1 ? "" : "s"}`, tono: "alerta", dias: faltaCierre };
  if (faltaCierre <= 15)
    return { clave: "por-cerrar", texto: `¡Cierra en ${faltaCierre} día${faltaCierre === 1 ? "" : "s"}!`, tono: "peligro", dias: faltaCierre };
  return { clave: "abierta", texto: `Abierta · cierra en ${faltaCierre} días`, tono: "exito", dias: faltaCierre };
}

/** Distancia en kilómetros entre dos puntos geográficos (fórmula de Haversine). */
export function distanciaKm(lat1, lon1, lat2, lon2) {
  const R = 6371;
  const rad = (g) => (g * Math.PI) / 180;
  const dLat = rad(lat2 - lat1);
  const dLon = rad(lon2 - lon1);
  const a = Math.sin(dLat / 2) ** 2 +
            Math.cos(rad(lat1)) * Math.cos(rad(lat2)) * Math.sin(dLon / 2) ** 2;
  return Math.round(2 * R * Math.asin(Math.sqrt(a)));
}

/** Emoji de bandera a partir del nombre del país (solo decorativo). */
const BANDERAS = {
  "Perú": "🇵🇪", "México": "🇲🇽", "Chile": "🇨🇱", "Argentina": "🇦🇷", "Brasil": "🇧🇷",
  "Colombia": "🇨🇴", "Uruguay": "🇺🇾", "Ecuador": "🇪🇨", "Estados Unidos": "🇺🇸",
  "Canadá": "🇨🇦", "Reino Unido": "🇬🇧", "España": "🇪🇸", "Francia": "🇫🇷",
  "Alemania": "🇩🇪", "Italia": "🇮🇹", "Suiza": "🇨🇭", "Países Bajos": "🇳🇱",
  "Hungría": "🇭🇺", "Polonia": "🇵🇱", "Turquía": "🇹🇷", "Rusia": "🇷🇺",
  "China": "🇨🇳", "Hong Kong": "🇭🇰", "Japón": "🇯🇵", "Corea del Sur": "🇰🇷",
  "Taiwan": "🇹🇼", "Singapur": "🇸🇬", "India": "🇮🇳", "Arabia Saudita": "🇸🇦",
  "Australia": "🇦🇺", "Nueva Zelanda": "🇳🇿", "Unión Europea": "🇪🇺",
  "En línea": "💻", "Varios": "🌍",
};
export function bandera(pais) { return BANDERAS[pais] || "🌍"; }

/** Anima un número desde 0 hasta su valor final. */
export function animarContador(el, valor, ms = 900) {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) { el.textContent = valor; return; }
  const inicio = performance.now();
  const paso = (t) => {
    const p = Math.min(1, (t - inicio) / ms);
    el.textContent = Math.round(valor * (1 - Math.pow(1 - p, 3)));
    if (p < 1) requestAnimationFrame(paso);
  };
  requestAnimationFrame(paso);
}

/** Efecto de onda al pulsar cualquier elemento con la clase js-ripple. */
export function activarOndas(raiz = document) {
  raiz.addEventListener("pointerdown", (e) => {
    const btn = e.target.closest(".js-ripple, .card__guardar");
    if (!btn || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const r = btn.getBoundingClientRect();
    const d = Math.max(r.width, r.height);
    const onda = document.createElement("span");
    onda.className = "onda";
    onda.style.cssText = `width:${d}px;height:${d}px;left:${e.clientX - r.left - d / 2}px;top:${e.clientY - r.top - d / 2}px`;
    btn.appendChild(onda);
    onda.addEventListener("animationend", () => onda.remove());
  }, { passive: true });
}
