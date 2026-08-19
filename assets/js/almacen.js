/**
 * Persistencia en el navegador (localStorage). No hay servidor ni cuentas:
 * las becas guardadas, el tema y los filtros viven solo en este dispositivo.
 */

const CLAVE_GUARDADAS = "becaradar.guardadas.v1";
const CLAVE_TEMA = "becaradar.tema";
const CLAVE_FILTROS = "becaradar.filtros.v1";

function leer(clave, porDefecto) {
  try {
    const crudo = localStorage.getItem(clave);
    return crudo ? JSON.parse(crudo) : porDefecto;
  } catch {
    return porDefecto;
  }
}

function escribir(clave, valor) {
  try {
    localStorage.setItem(clave, JSON.stringify(valor));
    return true;
  } catch {
    return false; // modo privado o cuota llena: la app sigue funcionando en memoria
  }
}

/* ------------------------------ Guardadas ------------------------------ */
let guardadas = new Map(Object.entries(leer(CLAVE_GUARDADAS, {})));
const oyentes = new Set();

function persistir() {
  escribir(CLAVE_GUARDADAS, Object.fromEntries(guardadas));
  oyentes.forEach((fn) => fn(guardadas));
}

export const almacen = {
  /** Se notifica a la interfaz cada vez que cambia la lista guardada. */
  alCambiar(fn) { oyentes.add(fn); fn(guardadas); return () => oyentes.delete(fn); },

  tiene: (id) => guardadas.has(id),
  lista: () => [...guardadas.values()],
  total: () => guardadas.size,

  alternar(beca) {
    if (guardadas.has(beca.id)) guardadas.delete(beca.id);
    else guardadas.set(beca.id, {
      id: beca.id, nombre: beca.nombre, organizacion: beca.organizacion,
      pais: beca.pais, url: beca.url, fecha_cierre: beca.fecha_cierre,
      guardadaEn: new Date().toISOString(),
    });
    persistir();
    return guardadas.has(beca.id);
  },

  quitar(id) { guardadas.delete(id); persistir(); },
  vaciar() { guardadas.clear(); persistir(); },

  exportar() {
    return JSON.stringify({
      app: "BecaRadar", version: 1, exportado: new Date().toISOString(),
      becas: [...guardadas.values()],
    }, null, 2);
  },

  /** Importa un archivo exportado previamente, fusionando sin duplicar. */
  importar(texto) {
    const datos = JSON.parse(texto);
    const entrantes = Array.isArray(datos) ? datos : datos.becas;
    if (!Array.isArray(entrantes)) throw new Error("Archivo no reconocido");
    let nuevas = 0;
    for (const b of entrantes) {
      if (b && typeof b.id === "string" && !guardadas.has(b.id)) { guardadas.set(b.id, b); nuevas++; }
    }
    persistir();
    return nuevas;
  },
};

/* --------------------------------- Tema -------------------------------- */
export const tema = {
  leer() {
    const guardado = leer(CLAVE_TEMA, null);
    if (guardado === "light" || guardado === "dark") return guardado;
    return matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  },
  aplicar(valor) {
    document.documentElement.dataset.theme = valor;
    escribir(CLAVE_TEMA, valor);
  },
};

/* ------------------------- Filtros (última sesión) --------------------- */
export const filtrosGuardados = {
  leer: () => leer(CLAVE_FILTROS, null),
  escribir: (estado) => escribir(CLAVE_FILTROS, estado),
};
