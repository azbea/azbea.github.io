#!/usr/bin/env python3
"""Static checks for the curated photo integration. Does not start a server or browser."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LANGS = {"en": "", "uz": "uz/", "ru": "ru/"}
EXPECTED = {
    "aviation-hall", "aircraft-display-detail", "aircraft-exhibition-portrait",
    "flight-helmet-display", "aircraft-outdoor-display", "cockpit-simulator",
    "illuminated-pavilion", "river-skyline-night", "riverside-park",
    "river-sunset", "shoreline-portrait", "city-street-portrait",
    "library-atrium", "riverside-bridge-portrait",
}
errors = []

def check(condition, message):
    if not condition:
        errors.append(message)

class ImgParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.images = []; self.sources = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img": self.images.append(attrs)
        if tag == "source": self.sources.append(attrs)

def local_paths(value):
    if not value: return []
    paths=[]
    for item in value.split(','):
        candidate=item.strip().split()[0]
        if candidate.startswith('/') and not candidate.startswith('//'):
            paths.append(candidate)
    return paths

originals = [p for p in (ROOT/'my-photos').iterdir() if p.is_file() and p.suffix.lower() in {'.jpg','.jpeg','.png','.webp','.avif'}]
check(len(originals) == 40, f"expected 40 original photos (including four education originals), found {len(originals)}")
for lang, folder in LANGS.items():
    p=ROOT/folder/'gallery/index.html'; parser=ImgParser(); parser.feed(p.read_text())
    check(len(parser.images)==14, f"{p.relative_to(ROOT)}: expected 14 images, got {len(parser.images)}")
    stems=set()
    for img in parser.images:
        src=img.get('src',''); match=re.search(r'/photos/([a-z0-9-]+)-(?:\d+)\.jpg$',src)
        if match: stems.add(match.group(1))
        check(bool(img.get('alt','').strip()), f"{p.relative_to(ROOT)}: missing alt on {src}")
        check(img.get('loading')=='lazy' and img.get('decoding')=='async', f"{p.relative_to(ROOT)}: lazy/async attributes missing on {src}")
        check(bool(img.get('width')) and bool(img.get('height')), f"{p.relative_to(ROOT)}: dimensions missing on {src}")
    check(stems==EXPECTED, f"{p.relative_to(ROOT)}: expected image set mismatch ({sorted(stems)})")
    check('gallery-placeholder' not in p.read_text(), f"{p.relative_to(ROOT)}: placeholder remains")
    check('name="robots" content="noindex' not in p.read_text(), f"{p.relative_to(ROOT)}: Gallery still noindex")
    for attrs in parser.images+parser.sources:
        for key in ('src','srcset'):
            for uri in local_paths(attrs.get(key,'')):
                check((ROOT/uri.lstrip('/')).is_file(), f"{p.relative_to(ROOT)}: missing asset {uri}")
    for page, stem in ((f'{folder}about/index.html','riverside-bridge-portrait'),(f'{folder}experience/index.html','river-sunset')):
        file=ROOT/page; parser=ImgParser(); parser.feed(file.read_text())
        matches=[i for i in parser.images if f'/photos/{stem}-' in i.get('src','')]
        check(len(matches)==1, f"{page}: expected exactly one {stem} contextual photo")
        if matches:
            check(bool(matches[0].get('alt','').strip()), f"{page}: missing contextual alt")
            for uri in local_paths(matches[0].get('src',''))+local_paths(matches[0].get('srcset','')):
                check((ROOT/uri.lstrip('/')).is_file(), f"{page}: missing asset {uri}")

sitemap=(ROOT/'sitemap.xml').read_text()
check(sitemap.count('<loc>https://abbosov.com/gallery/</loc>')==1,'sitemap English Gallery URL missing or duplicated')
for lang,url in (("en","https://abbosov.com/gallery/"),("uz","https://abbosov.com/uz/gallery/"),("ru","https://abbosov.com/ru/gallery/")):
    check(f'<loc>{url}</loc>' in sitemap,f'sitemap missing {lang} Gallery URL')
    block=re.search(r'<url>\s*<loc>'+re.escape(url)+r'</loc>[\s\S]*?</url>',sitemap)
    check(bool(block),f'{url}: sitemap URL block missing')
    if block:
        for alt,target in (("en","https://abbosov.com/gallery/"),("uz","https://abbosov.com/uz/gallery/"),("ru","https://abbosov.com/ru/gallery/"),("x-default","https://abbosov.com/gallery/")):
            check(f'hreflang="{alt}" href="{target}"' in block.group(0),f'{url}: incorrect/missing {alt} alternate')

photo_dir=ROOT/'assets/images/photos'
for stem in EXPECTED:
    check(any(photo_dir.glob(stem+'-*.webp')), f'{stem}: WebP derivative missing')
    check(any(photo_dir.glob(stem+'-*.jpg')), f'{stem}: JPEG fallback missing')

if errors:
    print(f'FAIL: {len(errors)} issue(s)')
    for e in errors: print(' -',e)
    sys.exit(1)
print(f'PASS: {len(originals)} originals retained; 14 unique optimized photos in each of 3 Gallery pages; 6 contextual placements; all referenced local assets exist; sitemap XML and Gallery alternates valid.')
