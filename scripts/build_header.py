#!/usr/bin/env python3
"""Build the self-contained kinetic header. Requires fonttools==4.68.0."""
from pathlib import Path
from math import sin, cos, pi
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
font = instantiateVariableFont(TTFont(ROOT / 'assets/fonts/SpaceGrotesk.ttf'), {'wght': 600})
glyphs = font.getGlyphSet()
cmap = font.getBestCmap()


def lettering(text, x, y, size, color, tracking=0):
    scale = size / font['head'].unitsPerEm
    paths = []
    for char in text:
        glyph = glyphs[cmap[ord(char)]]
        pen = SVGPathPen(glyphs)
        glyph.draw(pen)
        if pen.getCommands():
            paths.append(f'<path d="{pen.getCommands()}" transform="translate({x:.2f} {y}) scale({scale:.5f} {-scale:.5f})"/>')
        x += glyph.width * scale + tracking
    return f'<g fill="{color}">' + ''.join(paths) + '</g>'


def ribbon(v, phase):
    points = []
    # One continuous, half-twisted strip: an idea becoming something shareable.
    for i in range(121):
        u = 4 * pi * i / 120
        r = 102 + v * cos(u / 2)
        x, y, z = r * cos(u), r * sin(u), v * sin(u / 2)
        a = .68 + .36 * sin(phase)
        y, z = y * cos(a) - z * sin(a), y * sin(a) + z * cos(a)
        b = phase
        x, z = x * cos(b) + z * sin(b), -x * sin(b) + z * cos(b)
        c = -.48
        x, y = x * cos(c) - y * sin(c), x * sin(c) + y * cos(c)
        perspective = 650 / (650 - z)
        points.append(f'{x * perspective:.1f},{y * perspective:.1f}')
    return 'M' + 'L'.join(points) + 'Z'


def build_header():
    parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" role="img" aria-labelledby="title desc">
    <title id="title">xuan jing — Build. Share. Repeat.</title>
    <desc id="desc">A silver Möbius ribbon turns slowly beside the xuan jing wordmark on an ink-black background. Motion is replaced with a still composition when reduced motion is preferred.</desc>
    <style>
      .still { display: none; }
      @media (prefers-reduced-motion: reduce) {
        .motion { display: none; }
        .still { display: inline; }
      }
    </style>
    <defs>
      <linearGradient id="silver" x1="0" y1="0" x2="1" y2="1">
        <stop stop-color="#f3ede3"/><stop offset=".42" stop-color="#c5c5c2"/>
        <stop offset=".72" stop-color="#555a60"/><stop offset="1" stop-color="#b2bec4"/>
      </linearGradient>
    </defs>
    <rect width="1200" height="360" fill="#080a0d"/>
    ''']
    parts.append(lettering('xuan jing', 64, 204, 96, '#f2efe8', -2.5))
    parts.append(lettering('Build. Share. Repeat.', 69, 251, 24, '#a9acae', .15))
    parts.append('<g transform="translate(947 180)" fill="none" stroke-linejoin="round">')
    for group in ['still', 'motion']:
        parts.append(f'<g class="{group}">')
        for i in range(16):
            v = 3 + i * 2.8
            color = '#e7aa7a' if i == 15 else 'url(#silver)'
            width = 1.6 if i == 15 else .95
            parts.append(f'<path stroke="{color}" stroke-width="{width}" d="{ribbon(v, 0)}">')
            if group == 'motion':
                frames = [ribbon(v, 2 * pi * j / 32) for j in range(32)]
                frames.append(frames[0])
                parts.append('<animate attributeName="d" dur="18s" repeatCount="indefinite" values="' + ';'.join(frames) + '"/>')
            parts.append('</path>')
        parts.append('</g>')
    parts.append('</g></svg>\n')
    (ROOT / 'assets/xuan-jing.svg').write_text('\n'.join(parts))


if __name__ == "__main__":
    build_header()
