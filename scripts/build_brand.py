#!/usr/bin/env python3
"""Build the vector brand family; install fonttools==4.68.0 first."""
import argparse
from pathlib import Path
from xml.sax.saxutils import escape
from build_header import lettering, ribbon

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/brand'
PROJECTS = [
    ('profile', ['xuan jing'], 'Build. Share. Repeat.', 0),
    ('job-filter', ['Job Filter'], 'Find your shortlist.', .34),
    ('open-source-starter', ['Open Source', 'Starter'], 'Start with good habits.', 1.02),
    ('community', ['Open-source', 'Workshop'], 'Build together.', 2.75),
    ('codex-workspace', ['Codex', 'Workspace'], 'Market research. In the open.', 3.5),
    ('prpc', ['PRPC'], 'Learning how systems connect.', 5.4),
]


def svg_start(width, height, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
<defs><linearGradient id="silver" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f3ede3"/><stop offset=".42" stop-color="#c5c5c2"/><stop offset=".72" stop-color="#555a60"/><stop offset="1" stop-color="#b2bec4"/></linearGradient></defs>
<rect width="{width}" height="{height}" fill="#080a0d"/>'''


def mark(x, y, scale, phase, compact=False):
    parts = [f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke-linecap="round" stroke-linejoin="round">']
    values = [3, 13, 23, 33, 45] if compact else [3 + i * 2.8 for i in range(16)]
    for i, v in enumerate(values):
        edge = i == len(values) - 1
        color = '#e7aa7a' if edge else ('#f2efe8' if compact else 'url(#silver)')
        width = (5.5 if edge else 4) if compact else (1.6 if edge else .95)
        parts.append(f'<path d="{ribbon(v, phase)}" stroke="{color}" stroke-width="{width}"/>')
    return ''.join(parts) + '</g>'


def cover(lines, subtitle, phase=0):
    parts = [svg_start(1280, 640, ' / '.join(lines) + ' — xuan jing')]
    y = 286 if len(lines) == 1 else 246
    for line in lines:
        # Keep every title in its allotted column, including future projects.
        size = min(80, 1000 / max(len(line), 1))
        parts.append(lettering(line, 72, y, size, '#f2efe8', -1.8))
        y += 88
    parts.append(lettering(subtitle, 76, y - 26, 25, '#a9acae'))
    parts.append(mark(988, 304, 1.65, phase))
    parts.append(lettering('xuan jing', 76, 566, 29, '#e7aa7a', -.45))
    parts.append('</svg>\n')
    return '\n'.join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--title', help='Custom cover title; use | for a line break')
    parser.add_argument('--subtitle', default='Build. Share. Repeat.')
    parser.add_argument('--output', type=Path, help='Custom .svg output path')
    args = parser.parse_args()
    if args.title:
        if not args.output or args.output.suffix != '.svg':
            parser.error('--title requires an --output ending in .svg')
        lines = args.title.split('|')
        if len(lines) > 2 or any(not line or len(line) > 24 for line in lines):
            parser.error('Use one or two title lines, each with 1–24 characters')
        if len(args.subtitle) > 45:
            parser.error('Keep the subtitle at 45 characters or fewer')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(cover(lines, args.subtitle))
        return
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'avatar.svg').write_text(svg_start(512, 512, 'xuan jing — Möbius mark') + mark(230, 249, 1.38, .18, compact=True) + '</svg>\n')
    for slug, lines, subtitle, phase in PROJECTS:
        (OUT / f'{slug}.svg').write_text(cover(lines, subtitle, phase))


if __name__ == '__main__':
    main()
