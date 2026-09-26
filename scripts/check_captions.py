#!/usr/bin/env python3
"""Read-only SRT checks. Exit 1 on errors; reading-speed warnings need review."""
import argparse
import html
import json
import re
from pathlib import Path

STAMP = r"(\d{2,}):([0-5]\d):([0-5]\d)[,.](\d{3})"
TIMING = re.compile(rf"^{STAMP}\s+-->\s+{STAMP}$")


def milliseconds(groups):
    h, m, s, ms = map(int, groups)
    return ((h * 60 + m) * 60 + s) * 1000 + ms


def check(text, duration=None, font=None, max_width=1500, max_cps=25):
    errors, warnings, widths = [], [], []
    blocks = re.split(r"\n[ \t]*\n", text.lstrip('\ufeff').replace('\r\n', '\n').strip())
    if not text.strip():
        return {'cues': 0, 'errors': ['No subtitle cues found.'], 'warnings': [], 'width_checked': font is not None}
    previous_end = 0
    for number, block in enumerate(blocks, 1):
        lines = block.splitlines()
        prefix = f'Cue {number}'
        if len(lines) < 3 or lines[0].strip() != str(number):
            errors.append(f'{prefix}: expected sequential index, timing, and text.')
            continue
        match = TIMING.fullmatch(lines[1].strip())
        if not match:
            errors.append(f'{prefix}: invalid SRT timestamp.')
            continue
        groups = match.groups()
        start, end = milliseconds(groups[:4]), milliseconds(groups[4:])
        if end <= start:
            errors.append(f'{prefix}: end must follow start.')
        if start < previous_end:
            errors.append(f'{prefix}: overlaps an earlier cue or is out of order.')
        previous_end = max(previous_end, end)
        if duration is not None and end > round(duration * 1000):
            errors.append(f'{prefix}: extends beyond video duration.')
        visible_lines = lines[2:]
        if len(visible_lines) != 1:
            errors.append(f'{prefix}: has {len(visible_lines)} lines; expected one.')
        plain = html.unescape(re.sub(r'<[^>]+>', '', ' '.join(visible_lines))).strip()
        if not plain:
            errors.append(f'{prefix}: empty displayed text.')
        if font is not None:
            width = float(font.getlength(plain))
            widths.append(width)
            if width > max_width:
                errors.append(f'{prefix}: {width:.1f}px exceeds {max_width}px safe width.')
        if end > start:
            cps = len(plain) / ((end - start) / 1000)
            if cps > max_cps:
                warnings.append(f'{prefix}: {cps:.1f} characters/s; review reading time.')
    return {'cues': len(blocks), 'errors': errors, 'warnings': warnings,
            'width_checked': font is not None,
            'maximum_width_px': round(max(widths), 1) if widths else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('srt', type=Path)
    parser.add_argument('--duration', type=float, help='Full video duration in seconds')
    parser.add_argument('--font', type=Path, help='Exact font used in the rendered captions; needs Pillow')
    parser.add_argument('--font-size', type=int, default=34)
    parser.add_argument('--max-width', type=float, default=1500)
    parser.add_argument('--max-cps', type=float, default=25)
    args = parser.parse_args()
    if min(args.font_size, args.max_width, args.max_cps) <= 0 or (args.duration is not None and args.duration <= 0):
        parser.error('Font size, width, CPS and duration must be positive.')
    font = None
    try:
        if args.font:
            from PIL import ImageFont
            font = ImageFont.truetype(str(args.font), args.font_size)
        report = check(args.srt.read_text(encoding='utf-8-sig'), args.duration, font, args.max_width, args.max_cps)
    except (OSError, UnicodeError, ImportError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(1 if report['errors'] else 0)


if __name__ == '__main__':
    main()
