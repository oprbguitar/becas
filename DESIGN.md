# DESIGN.md — Ruta Amauta v3 «sobrio»

## Dirección

| Eje | Decisión | Origen |
|---|---|---|
| Composición | Página de producto: barra delgada, titular grande centrado, listas antes que tarjetas, bandas alternas (crema / blanco / oliva) | Pedido del autor: «minimalista, tipo Apple» |
| Color | Se conserva la paleta del logotipo: terracota `#C4552E`, oliva `#33341E`, arena `#D9AE7A` sobre crema `#FBF5EC` | Pedido del autor: «mantén los mismos colores y el logo» (prevalece sobre la paleta sugerida por `design-pick`) |
| Tipografía | Atkinson Hyperlegible (interfaz y titulares) + IBM Plex Mono (fechas, resoluciones, montos) | `design-pick` (legibilidad primero). Se retiraron Inter y Playfair Display |
| Forma | Radios 8 / 12 / 18 px; botones en cápsula; sin bordes en tarjetas, sombra mínima | Lenguaje tipo Apple pedido por el autor (prevalece sobre «0 px» de `design-pick`) |
| Movimiento | 160 ms, curva `cubic-bezier(.2,.7,.2,1)`; solo estado, foco y aparición del modal; `prefers-reduced-motion` lo anula | `design-pick` («seco») |
| Densidad | Media: la evidencia (fecha, resolución, fuente) siempre visible, sin adornos | Dominio: decisiones de dinero y validez legal |

Direcciones descartadas: (1) tablero denso tipo terminal, demasiado técnico
para postulantes; (2) maestro-detalle a dos paneles, rompía el flujo móvil de
las convocatorias desplegables.

## Tokens

Todos están en `:root` de `assets/css/estilos.css`:

- **Color:** `--crema`, `--crema-2`, `--blanco`, `--terracota(-osc|-suave)`,
  `--oliva(-2|-suave)`, `--arena(-suave)`, `--texto`, `--suave`, `--tenue`,
  `--borde(-fuerte)`, estados `--verde`, `--ambar`, `--rojo` (+ `-suave`).
- **Tipo:** `--t-12 … --t-56` (12, 13, 15, 17, 21, 28, 40, 56–64 fluido).
- **Espacio:** `--e-1 … --e-9` (4, 8, 12, 16, 24, 32, 48, 64, 96).
- **Forma:** `--r-sm 8`, `--r 12`, `--r-lg 18`, `--r-pastilla`.
- **Movimiento:** `--dur 160ms`, `--curva`.

## Semáforo de evidencia

`.estado` + clase: `abierta`/`verificado`/`licenciada` (verde),
`proxima`/`condicionado` (ámbar), `cerrada`/`pendiente`/`no_figura` (gris),
`no_compatible`/`denegada` (rojo). Es una convención de la interfaz, no una
norma oficial: el texto siempre acompaña al color.

## Estados

`:focus-visible` con contorno terracota en todo control; `hover` en enlaces de
barra, filas, botones, cápsulas y paginación; `active` con escala 0,98;
`aria-pressed` / `aria-current` para el control segmentado y la barra;
`disabled` al 45 % de opacidad; carga con esqueleto y texto «Cargando…».

## Responsive

Comprobado a 360, 768, 1280 y 1600 px. Bajo 860 px la barra pasa a menú
desplegable, la herramienta SUNEDU apila sus columnas y las filas de
convocatoria mueven la fecha bajo el título. Sin desplazamiento horizontal de
página (las tablas desplazan dentro de su contenedor).
