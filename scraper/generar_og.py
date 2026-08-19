#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera la imagen de vista previa (Open Graph / Twitter Card).

1200x630 px sobre el crema de marca, con el logotipo, el nombre y el lema.
Es lo que se ve al compartir el enlace en WhatsApp, LinkedIn, X o Slack.

Uso:
    python scraper/generar_og.py
"""

import os

from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARCA = os.path.join(RAIZ, "imagenes", "banner.png")
DESTINO = os.path.join(RAIZ, "assets", "img", "compartir.png")

ANCHO, ALTO = 1200, 630
CREMA = (251, 245, 236)
TERRACOTA = (196, 85, 46)
OLIVA = (51, 52, 30)
SUAVE = (111, 106, 92)
ARENA = (217, 174, 122)

# Fuentes del sistema, con alternativas por si falta alguna.
CANDIDATAS_SERIF = ["georgia.ttf", "constan.ttf", "times.ttf", "DejaVuSerif.ttf"]
CANDIDATAS_SANS = ["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"]
DIRS = [r"C:\Windows\Fonts", "/usr/share/fonts/truetype/dejavu",
        "/usr/share/fonts/truetype/liberation", "/Library/Fonts"]


def fuente(candidatas, tam):
    for carpeta in DIRS:
        for nombre in candidatas:
            ruta = os.path.join(carpeta, nombre)
            if os.path.exists(ruta):
                try:
                    return ImageFont.truetype(ruta, tam)
                except OSError:
                    continue
    return ImageFont.load_default(tam)


def transparentar(img, umbral=238):
    img = img.convert("RGBA")
    pix = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pix[x, y]
            if r >= umbral and g >= umbral and b >= umbral:
                pix[x, y] = (r, g, b, 0)
    return img


def main():
    lienzo = Image.new("RGB", (ANCHO, ALTO), CREMA)
    dib = ImageDraw.Draw(lienzo)

    # Franja superior de marca.
    dib.rectangle([0, 0, ANCHO, 10], fill=TERRACOTA)

    # Logotipo recortado a su contenido.
    if os.path.exists(MARCA):
        logo = transparentar(Image.open(MARCA))
        caja = logo.getbbox()
        if caja:
            logo = logo.crop(caja)
        alto_logo = 132
        ancho_logo = int(logo.width * alto_logo / logo.height)
        logo = logo.resize((ancho_logo, alto_logo), Image.LANCZOS)
        lienzo.paste(logo, (86, 74), logo)

    f_titulo = fuente(CANDIDATAS_SERIF, 76)
    f_bajada = fuente(CANDIDATAS_SANS, 34)
    f_pie = fuente(CANDIDATAS_SANS, 27)

    dib.text((86, 262), "Tu ruta al conocimiento.", font=f_titulo, fill=OLIVA)
    dib.text((86, 366), "Becas, maestrías, doctorados y diplomados", font=f_bajada, fill=TERRACOTA)
    dib.text((86, 412), "en Perú, Latinoamérica y el mundo.", font=f_bajada, fill=SUAVE)

    # Separador y pie.
    dib.rectangle([86, 486, 400, 489], fill=ARENA)
    dib.text((86, 516), "Busca · compara · verifica el licenciamiento SUNEDU",
             font=f_pie, fill=SUAVE)
    dib.text((86, 556), "ruta.amauta.online", font=f_pie, fill=TERRACOTA)

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    lienzo.save(DESTINO, optimize=True, quality=90)
    print(f"  {os.path.relpath(DESTINO, RAIZ)}  {ANCHO}x{ALTO}")


if __name__ == "__main__":
    main()
