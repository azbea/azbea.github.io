#!/usr/bin/env python3
"""Static SEO and image audit for abbosov.com. Does not start a server or browser."""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://abbosov.com'
SAME_AS = ['https://github.com/azbea','https://linkedin.com/in/a-abbosov','https://t.me/azbe_plt','https://instagram.com/azbe.plt']

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title=''; self.title_on=False; self.h1s=[]; self.h1_on=False; self.meta=[]; self.links=[]; self.imgs=[]; self.canonical=[]; self.hreflangs=[]; self.jsonlds=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='title': self.title_on=True
        if tag=='h1': self.h1s.append(''); self.h1_on=True
        if tag=='meta': self.meta.append(a)
        if tag=='link':
            rel=a.get('rel','').lower().split()
            if 'canonical' in rel:self.canonical.append(a.get('href',''))
            if 'alternate' in rel and a.get('hreflang'):self.hreflangs.append((a['hreflang'],a.get('href','')))
        if tag=='a' and a.get('href'):self.links.append(a['href'])
        if tag=='img':self.imgs.append(a)
        if tag=='script' and a.get('type')=='application/ld+json':self.jsonlds.append('')
        if tag=='script' and a.get('type')=='application/ld+json':self.jsonld_on=True
    def handle_endtag(self, tag):
        if tag=='title':self.title_on=False
        if tag=='h1':self.h1_on=False
        if tag=='script' and getattr(self,'jsonld_on',False):self.jsonld_on=False
    def handle_data(self,data):
        if self.title_on:self.title+=data
        if self.h1_on and self.h1s:self.h1s[-1]+=data
        if getattr(self,'jsonld_on',False) and self.jsonlds:self.jsonlds[-1]+=data

def err(msg): return 'FAIL '+msg
def ok(msg): return 'PASS '+msg
def local_file(url):
    u=urlparse(url)
    if u.scheme in ('http','https'):
        if u.netloc!='abbosov.com':return None
    elif u.scheme in ('mailto','tel','data','javascript') or not u.path:return None
    path=u.path.lstrip('/')
    if not path or u.path.endswith('/'):path += 'index.html'
    return ROOT/path

def check_page(p):
    raw=p.read_text(errors='replace'); parser=PageParser(); parser.feed(raw)
    meta_desc=[m.get('content','').strip() for m in parser.meta if m.get('name','').lower()=='description']
    robots=[m.get('content','').lower() for m in parser.meta if m.get('name','').lower()=='robots']
    title=parser.title.strip(); relpath=p.relative_to(ROOT); lang='ru' if relpath.parts[0]=='ru' else 'uz' if relpath.parts[0]=='uz' else 'en'
    canonical=parser.canonical[0] if len(parser.canonical)==1 else ''
    tests=[]
    h1_expected={'en':'Azizbek Abbosov','uz':'Azizbek Abbosov','ru':'Азизбек Аббосов'}
    h1_value=' '.join(parser.h1s[0].split()) if parser.h1s else ''
    h1_name_ok=(h1_expected[lang] in h1_value)
    if p.name=='404.html':h1_name_ok=True
    relparts=p.relative_to(ROOT).parts
    if p.name=='index.html' and len(relparts)==1:
        intro_expected={'en':'Azizbek Abbosov is a pilot student at Korea Aerospace University, an aviation enthusiast, traveler and developer from Tashkent, Uzbekistan. This is his official website.','uz':'Azizbek Abbosov — Toshkentlik, Koreya Aerokosmik Universitetida uchuvchilik boʻyicha tahsil olayotgan talaba, aviatsiya ishqibozi, sayohatchi va dasturchi. Bu uning rasmiy veb-sayti.','ru':'Азизбек Аббосов — студент-пилот Корейского аэрокосмического университета, энтузиаст авиации, путешественник и разработчик из Ташкента, Узбекистан. Это его официальный сайт.'}
        hm=re.search(r'<h1\b[^>]*>.*?</h1>\s*<p\b[^>]*class="[^"]*lead[^"]*"[^>]*>(.*?)</p>',raw,re.S)
        intro=' '.join(re.sub(r'<[^>]+>',' ',hm.group(1)).split()) if hm else ''
        h1_name_ok=h1_name_ok and intro==intro_expected[lang]
    tests.append(len(title)<=60 and len(title)>0 and len(parser.h1s)==1 and h1_name_ok)
    tests.append(len(meta_desc)==1 and 70<=len(meta_desc[0])<=155)
    is404=p.name=='404.html'
    if not is404:
        tests.append(len(parser.canonical)==1 and canonical.startswith(SITE+'/'))
        expected={('en',''):SITE+'/',('uz',''):SITE+'/uz/',('ru',''):SITE+'/ru/'}
        route=p.parent.name if p.parent.name!='.' else ''
        if route=='index.html': route=''
        if p.name=='index.html' and p.parent==ROOT:route=''
        # map localized page route
        pref='' if lang=='en' else lang+'/'
        rel=str(p.relative_to(ROOT))
        route=rel[len(pref):] if rel.startswith(pref) else rel
        route='' if route=='index.html' else route.removesuffix('/index.html').removesuffix('/index.html')
        route=route.removesuffix('/index.html')
        prefix='/' if not route else '/'+route.strip('/')+'/'
        expected={'en':SITE+prefix,'uz':SITE+'/uz'+prefix,'ru':SITE+'/ru'+prefix}
        href=dict(parser.hreflangs)
        tests[2] = tests[2] and canonical == expected[lang]
        tests.append(set(href)=={'en','uz','ru','x-default'} and href.get(lang)==expected[lang] and href.get('x-default')==expected['en'] and all(href.get(k)==expected[k] for k in ('en','uz','ru')))
        tests.append(bool(robots) and 'noindex' in robots[0] if 'journal' in relpath.parts else bool(robots) and 'noindex' not in robots[0] and 'max-image-preview:large' in robots[0])
    else:
        tests.append(bool(robots) and 'noindex' in robots[0] and any(h in ('/','/uz/','/ru/') for h in parser.links))
    image_ok=True
    for im in parser.imgs:
        if not im.get('alt','').strip() or len(im.get('alt',''))>125 or not im.get('width','').isdigit() or not im.get('height','').isdigit():image_ok=False
        for candidate in [im.get('src','')]+[x.split()[0] for x in im.get('srcset','').split(',') if x.strip()]:
            f=local_file(candidate)
            if candidate.startswith('http://'):image_ok=False
            if candidate and candidate.startswith('/') and (f is None or not f.is_file()):image_ok=False
            if candidate.lower().endswith(('.webp','.jpg','.jpeg')) and 'azizbek-abbosov' not in Path(candidate).name:image_ok=False
    tests.append(image_ok)
    ld_ok=True
    for block in parser.jsonlds:
        try:d=json.loads(block)
        except Exception:ld_ok=False;continue
        graph=d.get('@graph',[]); ids={x.get('@id') for x in graph if isinstance(x,dict) and x.get('@id')}
        def refs(x):
            nonlocal ld_ok
            if isinstance(x,dict):
                if set(x)=={'@id'} and x['@id'].startswith(SITE+'/') and x['@id'] not in ids:ld_ok=False
                for v in x.values():refs(v)
            elif isinstance(x,list):
                for v in x:refs(v)
        refs(graph)
        persons=[n for n in graph if isinstance(n,dict) and n.get('@type')=='Person']
        expected_desc='Azizbek Abbosov is a pilot student at Korea Aerospace University, an aviation enthusiast, traveler and developer from Tashkent, Uzbekistan.'
        for person in persons:
            if person.get('@id')!='https://abbosov.com/#person' or person.get('name')!='Azizbek Abbosov' or person.get('alternateName')!=['Азизбек Аббосов','Azizbek Abbosov','azbea'] or person.get('sameAs')!=SAME_AS or person.get('description')!=expected_desc:ld_ok=False
            if person.get('email')!='mailto:abbosov.dev@gmail.com' or person.get('homeLocation',{}).get('name')!='Tashkent, Uzbekistan' or person.get('address',{}).get('addressLocality')!='Tashkent':ld_ok=False
            if person.get('affiliation',{}).get('name')!='Korea Aerospace University' or person.get('alumniOf',{}).get('name')!='Chust District Polytechnic No. 2':ld_ok=False
            if any(k in person for k in ('jobTitle','worksFor','award','birthDate')):ld_ok=False
        if not persons and not is404:ld_ok=False
        for node in graph:
            if isinstance(node,dict) and node.get('@type')=='WebSite' and node.get('@id')!='https://abbosov.com/#website':ld_ok=False
            if isinstance(node,dict) and node.get('@type')=='ImageObject':
                u=node.get('contentUrl','');f=local_file(u)
                if not u.startswith(SITE+'/') or not f or not f.is_file() or not node.get('width') or not node.get('height'):ld_ok=False
    if not parser.jsonlds and not is404:ld_ok=False
    tests.append(ld_ok)
    links_ok=True
    for link in parser.links:
        if link.startswith('http://'):links_ok=False
        f=local_file(link)
        if f and not f.exists():links_ok=False
    tests.append(links_ok)
    textlow=raw.lower()
    tests.append(not bool(re.search(r'\b(?:lorem|todo|example\.com|placeholder|draft|remains to be confirmed)\b',textlow)) and not any('  ' in h for h in parser.h1s))
    return all(tests),title,tests

def PageParserImages(source):
    parser=PageParser();parser.feed(source);return [i.get('src','') for i in parser.imgs]

public=sorted(p for p in ROOT.rglob('*.html') if 'design-reference' not in p.parts and 'admin' not in p.parts and p.name!='selftest.html')
rows=[];all_titles=[];all_desc=[]
for p in public:
    passed,title,checks=check_page(p);rows.append((str(p.relative_to(ROOT)),passed,checks));all_titles.append(title)
    q=PageParser();q.feed(p.read_text(errors='replace'));all_desc.extend(m.get('content','').strip() for m in q.meta if m.get('name','').lower()=='description')
print('STATIC SEO AUDIT — no browser/server used')
print(f"{'Page':40} {'Result':8} {'Title/desc':11} {'Canon/hreflang':15} {'Robots':8} {'JSON-LD':8} {'Images':8} {'Links/text':11}")
for name,passed,c in rows:
    # columns reflect core combined assertions, then details encoded in check positions
    vals=['PASS' if v else 'FAIL' for v in c]
    print(f"{name:40} {'PASS' if passed else 'FAIL':8} {vals[0]+'/'+vals[1]:11} {(vals[2]+'/'+vals[3]) if len(c)>3 else 'n/a':15} {(vals[4] if len(c)>4 else vals[2]):8} {(vals[6] if len(c)>6 else vals[5]):8} {vals[5]:8} {vals[-2]+'/'+vals[-1]:11}")
# Sitemap URL/image checks without a web server.
xml=(ROOT/'sitemap.xml').read_text()
url_locs=re.findall(r'<loc>(https://abbosov\.com/[^<]+)</loc>',xml)
indexable=[]
for p in public:
    raw=p.read_text(errors='replace')
    if p.name=='404.html':continue
    m=re.search(r'<link rel="canonical" href="([^"]+)"',raw)
    r=re.search(r'<meta name="robots" content="([^"]+)"',raw)
    if m and (not r or 'noindex' not in r.group(1)):indexable.append(m.group(1))
sitemap_pages=[u for u in url_locs if '<image:loc>' not in u]
unique_ok=len(all_titles)==len(set(all_titles)) and len(all_desc)==len(set(all_desc))
# Regex loc extraction includes image locs; classify root-level page paths only.
page_urls=set(re.findall(r'<url>\s*<loc>(https://abbosov\.com/[^<]*)</loc>',xml))
expected=set(indexable)
image_urls=re.findall(r'<image:loc>(https://abbosov\.com/[^<]+)</image:loc>',xml)
image_ok=all(local_file(url.replace(SITE,'')) and local_file(url.replace(SITE,'')).is_file() for url in image_urls)
image_association_ok=True
for block in re.findall(r'<url>(.*?)</url>',xml,re.S):
    page_loc=re.search(r'<loc>(https://abbosov\.com/[^<]*)</loc>',block)
    if not page_loc:continue
    path=urlparse(page_loc.group(1)).path
    file=local_file(path)
    if not file or not file.exists():image_association_ok=False;continue
    source=file.read_text(errors='replace')
    visible=[]
    for src in re.findall(r'<img\b[^>]*\bsrc="([^"]+)"',source):
        if src.startswith('/assets/images/') and src.lower().endswith(('.webp','.jpg','.jpeg','.png')) and src not in visible:visible.append(src)
    listed=[u.replace(SITE,'') for u in re.findall(r'<image:loc>(https://abbosov\.com/[^<]+)</image:loc>',block)]
    if set(visible)!=set(listed):image_association_ok=False
sitemap_ok=page_urls==expected and image_ok and image_association_ok and 'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"' in xml
print(f"Unique titles/descriptions: {'PASS' if unique_ok else 'FAIL'} — {len(set(all_titles))}/{len(all_titles)} titles, {len(set(all_desc))}/{len(all_desc)} descriptions")
print(f"Sitemap: {'PASS' if sitemap_ok else 'FAIL'} — {len(page_urls)} page URLs, {len(image_urls)} image URLs; page set exact={page_urls==expected}; image files exist={image_ok}; image/page mapping correct={image_association_ok}")
assets_ok=all((ROOT/x).is_file() for x in ['assets/images/og-image.jpg','assets/images/prof.jpg']) and (ROOT/'assets/images/og-image.jpg').stat().st_size<300000
print(f"Legacy image URLs: {'PASS' if assets_ok else 'FAIL'} — og-image.jpg and prof.jpg exist; OG under 300 KB")
admin_ok=True
for p in (ROOT/'admin').glob('*.html'):
    s=p.read_text(errors='replace').lower()
    if 'name="robots" content="noindex,nofollow"' not in s:admin_ok=False
print(f"Admin robots: {'PASS' if admin_ok else 'FAIL'} — noindex,nofollow")
# Source image outputs should not carry EXIF/GPS.
import subprocess
outputs=[p for folder in ['assets/images/people','assets/images/education','assets/images/gallery'] for p in (ROOT/folder).glob('*.webp')]
try:
    probe=subprocess.run(['exiftool','-s','-EXIF:all','-GPS:all',*map(str,outputs)],capture_output=True,text=True,check=False)
    exif_ok=not bool(re.search(r'GPS\s*:',probe.stdout)) and not bool(re.search(r'EXIF\s*:',probe.stdout))
except FileNotFoundError:exif_ok=False
print(f"Image metadata: {'PASS' if exif_ok else 'FAIL'} — EXIF/GPS absent from {len(outputs)} WebP outputs")
# Cross-locale class-name regression.
class_ok=not any(x in (ROOT/f).read_text() for f in ['uz/about/index.html','uz/experience/index.html','ru/about/index.html','ru/experience/index.html'] for x in ['tajriba-','опыт-','maʼlumot-strip'])
print(f"Localized CSS classes: {'PASS' if class_ok else 'FAIL'}")
robots_txt=(ROOT/'robots.txt').read_text()
robots_ok='Allow: /' in robots_txt and 'Disallow: /admin/' in robots_txt and 'Sitemap: https://abbosov.com/sitemap.xml' in robots_txt
print(f"robots.txt: {'PASS' if robots_ok else 'FAIL'} — Allow root, disallow admin, sitemap reference")
ignore=(ROOT/'.gitignore').read_text()
required_ignore=['.DS_Store','my-photos/','design-reference/','MASTER_PROJECT_PROMPT.md','CODEX_*.md','*_REPORT.md','scripts/','data/private*']
ignore_ok=all(x in ignore.splitlines() for x in required_ignore) and 'CNAME' not in ignore.splitlines() and not (ROOT/'CNAME').exists()
print(f"Test-repo housekeeping: {'PASS' if ignore_ok else 'FAIL'} — required ignores present; CNAME absent and not ignored")
try:
    xmlcheck=subprocess.run(['xmllint','--noout',str(ROOT/'sitemap.xml')],capture_output=True,text=True,check=False)
    xml_ok=xmlcheck.returncode==0
except FileNotFoundError:xml_ok=False
print(f"Sitemap XML: {'PASS' if xml_ok else 'FAIL'} — well-formed XML")
# Home/about page images are the owner-selected portraits; gallery must have six clean images or more.
gallery_ok=all(sum(1 for im in PageParserImages((ROOT/(('' if l=='en' else l+'/')+'gallery/index.html')).read_text()) if '/assets/images/' in im and im.lower().endswith('.webp'))>=6 for l in ('en','uz','ru'))
print(f"Gallery indexability: {'PASS' if gallery_ok else 'FAIL'} — at least six WebP images per language")
print(f"OVERALL: {'PASS' if all(r[1] for r in rows) and sitemap_ok and assets_ok and admin_ok and exif_ok and class_ok and unique_ok and robots_ok and ignore_ok and xml_ok and gallery_ok else 'FAIL'} — {sum(r[1] for r in rows)}/{len(rows)} HTML pages")
sys.exit(0 if all(r[1] for r in rows) and sitemap_ok and assets_ok and admin_ok and exif_ok and class_ok and unique_ok and robots_ok and ignore_ok and xml_ok and gallery_ok else 1)
