#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el favicon y los iconos de la PWA a partir de imagenes/logo.png.

Recorta el margen blanco del logotipo, vuelve transparente el fondo y exporta
los tamanos que necesitan el navegador, iOS y el manifest.

Uso:
    python scraper/generar_favicon.py
"""

import os

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEN = os.path.join(RAIZ, "imagenes", "logo.png")
DESTINO = os.path.join(RAIZ, "assets", "img")

UMBRAL_BLANCO = 238      # pixeles mas claros que esto se vuelven transparentes
MARGEN = 0.06            # aire alrededor del logotipo, en proporcion del lado


def transparentar(img: Image.Image) -> Image.Image:
    img = img.convert("RGBA")
    pix = img.load()
    ancho, alto = img.size
    for y in range(alto):
        for x in range(ancho):
            r, g, b, a = pix[x, y]
            if r >= UMBRAL_BLANCO and g >= UMBRAL_BLANCO and b >= UMBRAL_BLANCO:
                pix[x, y] = (r, g, b, 0)
    return img


def cuadrar(img: Image.Image) -> Image.Image:
    """Recorta al contenido visible y lo centra en un lienzo cuadrado."""
    caja = img.getbbox()
    if caja:
        img = img.crop(caja)
    lado = max(img.size)
    lado = int(lado * (1 + MARGEN * 2))
    lienzo = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    lienzo.paste(img, ((lado - img.width) // 2, (lado - img.height) // 2), img)
    return lienzo


def main():
    if not os.path.exists(ORIGEN):
        raise SystemExit(f"No encuentro {ORIGEN}")
    os.makedirs(DESTINO, exist_ok=True)

    base = cuadrar(transparentar(Image.open(ORIGEN)))

    # PNG transparentes para el navegador, iOS y el manifest.
    for lado in (32, 180, 192, 512):
        salida = os.path.join(DESTINO, f"icono-{lado}.png")
        base.resize((lado, lado), Image.LANCZOS).save(salida, optimize=True)
        print(f"  icono-{lado}.png")

    # .ico multiresolucion sobre crema, para pestanas de fondo claro.
    crema = Image.new("RGBA", base.size, (251, 245, 236, 255))
    crema.alpha_composite(base)
    crema.save(os.path.join(DESTINO, "favicon.ico"),
               sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print("  favicon.ico")

    # Version maskable: el icono sobre el crema de marca, con mas aire.
    lado = 512
    fondo = Image.new("RGBA", (lado, lado), (251, 245, 236, 255))
    logo = base.resize((int(lado * 0.72),) * 2, Image.LANCZOS)
    fondo.paste(logo, ((lado - logo.width) // 2, (lado - logo.height) // 2), logo)
    fondo.save(os.path.join(DESTINO, "icono-maskable-512.png"), optimize=True)
    print("  icono-maskable-512.png")


if __name__ == "__main__":
    main()
