#!/usr/bin/env python3
"""Maakt de icoonbestanden uit 'Coco - transparant.png'.

Draai dit opnieuw als de bronafbeelding verandert:

    pip install pillow && python3 scripts/maak-iconen.py

De kleine formaten (het tabbladicoontje) zijn uitgesneden rond Coco's kop, want
de hele figuur wordt op 16 pixels een onherkenbare vlek. De grote formaten
gebruiken de hele figuur.
"""
from pathlib import Path

from PIL import Image

WORTEL = Path(__file__).resolve().parent.parent
BRON = WORTEL / "Coco - transparant.png"
ACHTERGROND = (244, 246, 249, 255)  # #F4F6F9, gelijk aan background_color in manifest.json

KOP = (270, 105, 770, 605)  # vierkant rond kop en bril
FIGUUR = (140, 80, 909, 953)  # de hele figuur, zonder lege rand


def op_achtergrond(afbeelding):
    vlak = Image.new("RGBA", afbeelding.size, ACHTERGROND)
    vlak.alpha_composite(afbeelding)
    return vlak


def vierkant(afbeelding, marge=0.0):
    """Plaatst de afbeelding gecentreerd op een doorzichtig vierkant."""
    zijde = round(max(afbeelding.size) * (1 + 2 * marge))
    vlak = Image.new("RGBA", (zijde, zijde), (0, 0, 0, 0))
    vlak.alpha_composite(afbeelding, ((zijde - afbeelding.width) // 2, (zijde - afbeelding.height) // 2))
    return vlak


def schaal(afbeelding, formaat):
    return afbeelding.resize((formaat, formaat), Image.LANCZOS)


def main():
    bron = Image.open(BRON).convert("RGBA")
    kop = bron.crop(KOP)
    figuur = vierkant(bron.crop(FIGUUR))

    # Tabblad: .ico met 16/32/48 voor oudere browsers, png voor de rest.
    schaal(kop, 48).save(WORTEL / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    schaal(kop, 32).save(WORTEL / "favicon-32.png")

    # iPhone-beginscherm: geen doorzichtigheid, iOS zet daar zwart achter.
    op_achtergrond(schaal(vierkant(bron.crop(FIGUUR), marge=0.06), 180)).convert("RGB").save(
        WORTEL / "apple-touch-icon.png"
    )

    # App-icoon (manifest).
    schaal(figuur, 512).save(WORTEL / "icon-512.png")
    # Maskable: extra ruimte eromheen, want Android snijdt de randen weg.
    op_achtergrond(schaal(vierkant(bron.crop(FIGUUR), marge=0.2), 192)).save(
        WORTEL / "icon-maskable-192.png"
    )

    for naam in ("favicon.ico", "favicon-32.png", "apple-touch-icon.png", "icon-512.png", "icon-maskable-192.png"):
        print(f"{naam}: {(WORTEL / naam).stat().st_size // 1024} kB")


if __name__ == "__main__":
    main()
