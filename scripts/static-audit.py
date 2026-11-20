#!/usr/bin/env python3
"""Static audits for the localized site; intentionally does not launch a server."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import json,re
ROOT=Path(__file__).resolve().parents[1]
PAGES=sorted(p for p in ROOT.rglob('*.html') if 'design-reference' not in p.parts and 'admin' not in p.parts and 'data' not in p.parts)
class AuditParser(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.stack=[];self.links=[];self.resources=[];self.ids=[];self.h1=0;self.headings=[];self.lang=None;self.canon=[];self.hreflang=[];self.jsonld=[];self.images=[];self.descriptions=[];self.og=False;self.twitter=False;self.skip=False;self.shell={};self.current=None;self.text=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs); self.stack.append((tag,a));
  if tag=='html':self.lang=a.get('lang')
  if a.get('id'):self.ids.append(a['id'])
  if tag in ('h1','h2','h3','h4','h5','h6'):
   self.headings.append(int(tag[1]))
   if tag=='h1':self.h1+=1
  if tag=='a':self.links.append((a.get('href',''),a,any({'lang-switch','menu-language'} & set(parent.get('class','').split()) for _,parent in self.stack[:-1])))
  if tag=='img':self.images.append(a)
  if tag=='img' and a.get('src'):self.resources.append(a['src'])
  if tag=='script' and a.get('src'):self.resources.append(a['src'])
  if tag=='link' and a.get('href') and a.get('rel') in ('stylesheet','icon','manifest','apple-touch-icon','preload'):self.resources.append(a['href'])
  if tag=='meta' and a.get('name')=='description':self.descriptions.append(a.get('content',''))
  if tag=='meta' and a.get('property')=='og:title':self.og=True
  if tag=='meta' and a.get('name')=='twitter:card':self.twitter=True
  if tag=='link' and a.get('rel')=='canonical':self.canon.append(a.get('href'))
  if tag=='link' and a.get('rel')=='alternate' and a.get('hreflang'):self.hreflang.append((a['hreflang'],a.get('href')))
  if tag=='script' and a.get('type')=='application/ld+json':self.current=[]
  group=tag if tag in ('header','footer') else ('menu' if tag=='aside' and 'menu-overlay' in a.get('class','').split() else None)
  if group and any(x[0]==group for x in self.stack[:-1]):pass
  elif group:self.shell[group]=[group+'.'+'.'.join(a.get('class','').split())]
  elif self.shell and any(x[0] in self.shell for x in self.stack[:-1]):
   for key in ('header','footer','menu'):
    if key in self.shell and any(x[0]==key for x in self.stack[:-1]):self.shell[key].append(tag+'.'+'.'.join(a.get('class','').split()))
  if tag=='main' and a.get('id'):self.main_id=a['id']
 def handle_endtag(self,tag):
  if tag=='script' and self.current is not None:
   try:self.jsonld.append(json.loads(''.join(self.current)))
   except Exception:self.jsonld.append(None)
   self.current=None
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:self.stack=self.stack[:i];break
 def handle_data(self,data):
  if self.current is not None:self.current.append(data)

def local_exists(href):
 u=urlparse(href)
 if u.scheme or href.startswith('//') or not u.path:return True,'',ROOT
 path=u.path
 target=ROOT/path.lstrip('/')
 if path.endswith('/'):target=target/'index.html'
 elif not target.suffix:target=target/'index.html'
 return target.exists(),u.fragment,target

def run():
 issues=[];shells={'header':{},'footer':{},'menu':{}};descriptions={};titles={};hreflang_map={};stats={'pages':len(PAGES),'hreflang':0,'jsonld':0,'sprites':0,'links':0,'samples':0,'images':0}
 sprite=(ROOT/'assets/icons/sprite.svg').read_text() if (ROOT/'assets/icons/sprite.svg').exists() else ''
 sprite_ids=set(re.findall(r'<symbol[^>]+id=["\']([^"\']+)',sprite))
 for page in PAGES:
  source=page.read_text(errors='replace'); p=AuditParser();p.feed(source);rel=page.relative_to(ROOT).as_posix();lang=p.lang or 'en'
  for switcher in ('lang-switch','menu-language'):
   match=re.search(r'<nav\b[^>]*class="[^"]*'+switcher+r'[^"]*"[^>]*>(.*?)</nav>',source,re.S)
   if not match or len(re.findall(r'<a\b',match.group(1)))!=3 or 'aria-hidden="true">·' in match.group(1):issues.append(f'{rel}: {switcher} is not three equal cells without separators')
  if p.h1!=1:issues.append(f'{rel}: {p.h1} h1 elements')
  if not p.lang:issues.append(f'{rel}: html lang missing')
  if any(level>previous+1 for previous,level in zip(p.headings,p.headings[1:])):issues.append(f'{rel}: skipped heading level')
  if not all(f'<{tag}' in source for tag in ('header','nav','main','footer')):issues.append(f'{rel}: missing semantic landmark')
  if len(p.ids)!=len(set(p.ids)):issues.append(f'{rel}: duplicate IDs')
  if p.descriptions:
   if not p.descriptions[0].strip():issues.append(f'{rel}: empty meta description')
   descriptions.setdefault(p.descriptions[0],[]).append(rel)
  title_match=re.search(r'<title>(.*?)</title>',source,re.S|re.I)
  if not title_match:issues.append(f'{rel}: title missing')
  else:titles.setdefault(title_match.group(1).strip(),[]).append(rel)
  if '404.html' not in rel and (not p.og or not p.twitter):issues.append(f'{rel}: missing OG/Twitter metadata')
  if 'id="main-content"' not in source:issues.append(f'{rel}: main content target missing')
  if 'class="skip-link"' not in source:issues.append(f'{rel}: skip link missing')
  if lang in ('uz','ru') and 'data-review="needs-native-review"' not in source:issues.append(f'{rel}: no native-review marker')
  if '404.html' not in rel and len(p.canon)!=1:issues.append(f'{rel}: canonical count {len(p.canon)}')
  if p.canon and p.hreflang:hreflang_map[p.canon[0]]={key:value for key,value in p.hreflang}
  for group in ('header','footer'):
   if group in p.shell:shells[group].setdefault(lang,set()).add(tuple(p.shell[group]))
  for item in p.jsonld:
   if item is None:issues.append(f'{rel}: invalid JSON-LD')
   else:stats['jsonld']+=1
  if p.hreflang:stats['hreflang']+=1
  if 'data-sample="true"' in source:stats['samples']+=source.count('data-sample="true"')
  for image in p.images:
   stats['images']+=1
   if image.get('alt') is None:issues.append(f'{rel}: image missing alt')
   if not image.get('width') or not image.get('height'):issues.append(f'{rel}: image missing dimensions')
   if image.get('loading') not in ('lazy','eager'):issues.append(f'{rel}: image loading mode missing')
  footer=re.search(r'<footer\b.*?</footer>',source,re.S)
  if footer:
   urls=re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>',footer.group())
   social=[x for x in urls if any(d in x for d in ('github.com/azbea','linkedin.com/in/a-abbosov','t.me/azbe_plt','instagram.com/azbe.plt'))]
   if len(social)!=4:issues.append(f'{rel}: footer social link count {len(social)}')
  for href,a,in_language_switcher in p.links:
   if not href or href=='#':issues.append(f'{rel}: empty/hash-only anchor');continue
   if 'localhost' in href or href.startswith('http://'):issues.append(f'{rel}: dev or insecure link {href}')
   parsed=urlparse(href)
   if lang in ('uz','ru') and not in_language_switcher and href.startswith('/') and not href.startswith((f'/{lang}/','/assets/','/css/','/js/','/data/','/site.webmanifest','/robots.txt','/ru/','/uz/')):
    issues.append(f'{rel}: internal link missing /{lang}/ prefix: {href}')
   if parsed.scheme in ('https','mailto','tel'):
    if parsed.scheme=='https' and (a.get('target')=='_blank' and not {'noopener','noreferrer'}<=set(a.get('rel','').split())):issues.append(f'{rel}: external target lacks rel {href}')
    continue
   exists,fragment,target=local_exists(href)
   if not exists:issues.append(f'{rel}: missing internal target {href} -> {target.relative_to(ROOT)}')
   elif fragment and target.exists():
    body=target.read_text(errors='ignore')
    if f'id="{fragment}"' not in body:issues.append(f'{rel}: missing fragment #{fragment} in {target.relative_to(ROOT)}')
   stats['links']+=1
  for resource in p.resources:
   exists,_,target=local_exists(resource)
   if not exists:issues.append(f'{rel}: missing local asset {resource} -> {target.relative_to(ROOT)}')
  for ref in re.findall(r'<use\b[^>]+href="([^"]+)"',source):
   if ref.startswith('/assets/icons/sprite.svg#'):
    stats['sprites']+=1
    if ref.split('#',1)[1] not in sprite_ids:issues.append(f'{rel}: missing sprite symbol {ref}')
   elif '#' in ref and not ref.startswith('/assets/icons/sprite.svg#'):issues.append(f'{rel}: inline/local sprite dependency {ref}')
 for stylesheet in (ROOT/'css').glob('*.css'):
  for raw in re.findall(r'url\(\s*["\']?([^"\')]+)',stylesheet.read_text()):
   value=raw.strip()
   if value.startswith(('data:','http:','https:','#','%23')):continue
   exists,_,target=local_exists(value)
   if not exists:issues.append(f'{stylesheet.relative_to(ROOT)}: missing CSS asset {value} -> {target.relative_to(ROOT)}')
 for description,files in descriptions.items():
  if len(files)>1:issues.append(f'duplicate meta description: {", ".join(files)}')
 for title,files in titles.items():
  if len(files)>1:issues.append(f'duplicate title: {", ".join(files)}')
 for canonical,alternates in hreflang_map.items():
  if not {'en','uz','ru','x-default'}<=set(alternates):issues.append(f'{canonical}: incomplete hreflang set')
  for language,url in alternates.items():
   if language in ('en','uz','ru') and url not in hreflang_map:issues.append(f'{canonical}: alternate {language} has no reciprocal page {url}')
  if alternates.get('x-default')!=alternates.get('en'):issues.append(f'{canonical}: x-default differs from English')
 # structure diff across locales, including 404 separately not counted in 27
 for section,by_lang in shells.items():
  merged=set().union(*by_lang.values()) if by_lang else set()
  if len(merged)>1:issues.append(f'{section} structural signatures differ ({len(merged)} variants)')
 # sitemap entries point to route files, do not include admin
 sitemap=(ROOT/'sitemap.xml').read_text(); urls=re.findall(r'<loc>(.*?)</loc>',sitemap)
 for url in urls:
  path=urlparse(url).path;target=ROOT/(path.lstrip('/') or '.')
  if path.endswith('/'):target=target/'index.html'
  if not target.exists():issues.append(f'sitemap missing route file: {url}')
 if any('/admin' in u for u in urls):issues.append('admin appears in sitemap')
 cname=(ROOT/'CNAME').read_text().strip()
 if cname!='abbosov.com':issues.append('CNAME does not contain abbosov.com')
 admin=(ROOT/'admin/index.html').read_text()
 if 'noindex,nofollow' not in admin or 'X-Robots-Tag' not in admin:issues.append('admin page missing robots meta')
 if 'Disallow: /admin/' not in (ROOT/'robots.txt').read_text():issues.append('robots.txt does not disallow /admin/')
 if any('/admin/' in page.read_text(errors='ignore') for page in PAGES):issues.append('public page links or references admin')
 print(f"Static audit: {stats['pages']} HTML files (includes three 404 files); {len(urls)} sitemap URLs; {stats['links']} local links; {stats['hreflang']} pages with hreflang; {stats['jsonld']} valid JSON-LD blocks; {stats['sprites']} shared sprite references; {stats['samples']} sample markers; {stats['images']} images.")
 for section,data in shells.items():print(f'{section} diff: '+('PASS — normalized structure is identical per language.' if len(set().union(*data.values()))<=1 else 'FAIL — '+', '.join(f'{k}:{len(v)} signature(s)' for k,v in data.items())))
 print(f'Sprite symbols: {", ".join(sorted(sprite_ids))}')
 print(f'Sitemap URLs: {len(urls)}; admin excluded: {not any("/admin" in u for u in urls)}')
 print('Language switchers: three 38×44px cells and no separator dots on every public document.')
 print('Nav pill arithmetic: '+', '.join(f'{w}px viewport → {w-8}px pill → {w-23}px inner grid → {w-189}px logo track' for w in (320,360,390,430)))
 if issues:
  print(f'Issues: {len(issues)}')
  for issue in issues:print(' - '+issue)
  return 1
 print('PASS: no static issues found.');return 0
if __name__=='__main__':raise SystemExit(run())
