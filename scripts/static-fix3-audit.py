#!/usr/bin/env python3
"""Static structural and asset checks for FIX3. Does not launch a server/browser."""
from html.parser import HTMLParser
from pathlib import Path
import re, sys, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
SYMBOLS={'github':'https://github.com/azbea','linkedin':'https://linkedin.com/in/a-abbosov','telegram':'https://t.me/azbe_plt','instagram':'https://instagram.com/azbe.plt'}
class Node:
 def __init__(self,tag,attrs,parent=None): self.tag=tag;self.attrs=dict(attrs);self.children=[];self.parent=parent; self.text=''
 def classes(self): return tuple(sorted(self.attrs.get('class','').split()))
class Parser(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=True);self.root=Node('document',[]);self.stack=[self.root];self.symbols=[];self.uses=[]
 def handle_starttag(self,t,a):
  n=Node(t,a,self.stack[-1]);self.stack[-1].children.append(n)
  if t=='use': self.uses.append(n.attrs.get('href',''))
  if t=='symbol': self.symbols.append(n.attrs.get('id',''))
  if t not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr','use'}: self.stack.append(n)
 def handle_startendtag(self,t,a): self.handle_starttag(t,a); self.handle_endtag(t)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t: self.stack=self.stack[:i];break
 def handle_data(self,d): self.stack[-1].text+=d

def descendants(n):
 yield n
 for c in n.children: yield from descendants(c)
def norm(n):
 attrs=tuple(sorted(n.attrs))
 return (n.tag,n.classes(),attrs,tuple(norm(c) for c in n.children))
def hasclass(n,c): return c in n.classes()
def parse(p):
 h=Parser();h.feed(p.read_text());return h
pages=sorted(p for p in ROOT.rglob('*.html') if not {'admin','design-reference','data'}&set(p.relative_to(ROOT).parts))
parsed={p:parse(p) for p in pages}
# Verify nine translated page structures, including all link row containers.
print('STRUCTURE — page, EN/UZ/RU component signatures')
fail=0
routes=['','about','education','experience','developer','timeline','journal','gallery','future']
def langpath(lang,route):
 parts=[]
 if lang!='en': parts.append(lang)
 if route: parts.append(route)
 parts.append('index.html')
 return ROOT.joinpath(*parts)
def containers(parser):
 return [n for n in descendants(parser.root) if (n.tag=='nav' and any(hasclass(n,c) for c in ('soc','route-links','next-page'))) or hasclass(n,'affordance-list')]
for route in routes:
 ps=[langpath(l,route) for l in ('en','uz','ru')]
 sigs=[]
 for p in ps:
  sigs.append(tuple(norm(n) for n in containers(parsed[p])))
 lang_ok=[True,sigs[1]==sigs[0],sigs[2]==sigs[0]]
 ok=all(lang_ok)
 # Icon groups are link-row adjacent components; compare their complete normalized trees too.
 for component in ('footer-social','menu-social'):
  group_sigs=[]
  for p in ps:
   group_sigs.append(tuple(norm(n) for n in descendants(parsed[p].root) if n.tag=='nav' and hasclass(n,component)))
  ok &= group_sigs[0]==group_sigs[1]==group_sigs[2]
 print(f"{'PASS' if ok else 'FAIL'} | {route or '/'} | EN {'PASS' if lang_ok[0] else 'FAIL'} | UZ {'PASS' if lang_ok[1] else 'FAIL'} | RU {'PASS' if lang_ok[2] else 'FAIL'}")
 if not ok: fail+=1
# Stylesheet parity and root-absolute paths on each translated route.
print('\nSTYLESHEET PARITY — all 9 routes')
for route in routes:
 ps=[langpath(l,route) for l in ('en','uz','ru')]
 sets=[];valid=True
 for p in ps:
  links=[n.attrs.get('href','') for n in descendants(parsed[p].root) if n.tag=='link' and 'stylesheet' in n.attrs.get('rel','').split()]
  sets.append(tuple(links));valid &= all(x.startswith('/') for x in links)
 ok=valid and sets[0]==sets[1]==sets[2]
 print(f"{'PASS' if ok else 'FAIL'} | {route or '/'} | identical root-absolute hrefs and cache queries")
 if not ok:fail+=1
# All public HTML checks.
print('\nSOCIAL LOGOS — all public pages')
for p,h in parsed.items():
 nodes=list(descendants(h.root)); foot=[n for n in nodes if n.tag=='nav' and hasclass(n,'footer-social')]
 menus=[n for n in nodes if n.tag=='nav' and hasclass(n,'menu-social')]
 contacts=[n for n in nodes if n.tag=='nav' and hasclass(n,'social-rows')]
 ok=True; reasons=[]
 if len(foot)!=1:ok=False;reasons.append('footer nav count')
 else:
  links=[n for n in foot[0].children if n.tag=='a']
  if len(links)!=4:ok=False;reasons.append('footer social count')
  if any('soc-btn' not in n.attrs.get('class','').split() for n in links):ok=False;reasons.append('footer soc-btn class')
  for a in links:
   if a.attrs.get('href') not in SYMBOLS.values() or a.attrs.get('target')!='_blank' or a.attrs.get('rel')!='noopener noreferrer' or not a.attrs.get('aria-label'):ok=False;reasons.append('footer link attrs')
 if len(menus)!=1 or len([n for n in menus[0].children if n.tag=='a'])!=4:ok=False;reasons.append('menu social count')
 if len(menus)==1 and any('soc-btn' not in n.attrs.get('class','').split() for n in menus[0].children if n.tag=='a'):ok=False;reasons.append('menu soc-btn class')
 for nav in menus:
  for a in (n for n in nav.children if n.tag=='a'):
   if a.attrs.get('href') not in SYMBOLS.values() or a.attrs.get('target')!='_blank' or a.attrs.get('rel')!='noopener noreferrer' or not a.attrs.get('aria-label'):ok=False;reasons.append('menu link attrs')
 for nav in foot+menus+contacts:
  for x in (x for x in descendants(nav) if x.tag=='use'):
   u=x.attrs.get('href','')
   if not u.startswith('/assets/icons/sprite.svg#') or u.rsplit('#',1)[-1] not in SYMBOLS:ok=False;reasons.append('sprite reference')
   svg=x.parent
   if svg.tag!='svg' or 'ico' not in svg.attrs.get('class','').split() or svg.attrs.get('aria-hidden')!='true' or svg.attrs.get('focusable')!='false':ok=False;reasons.append('sprite svg accessibility attrs')
 if contacts:
  c=contacts[0];rows=[n for n in c.children if n.tag=='a']
  if len(rows)!=4:ok=False;reasons.append('contact rows')
  for a in rows:
   ico=[x for x in descendants(a) if hasclass(x,'row-ico')]
   sym=[x.attrs.get('href','').rsplit('#',1)[-1] for x in descendants(a) if x.tag=='use']
   if len(ico)!=1 or len(sym)!=1 or a.attrs.get('href')!=SYMBOLS.get(sym[0]) or a.attrs.get('target')!='_blank' or a.attrs.get('rel')!='noopener noreferrer' or not a.attrs.get('aria-label'):ok=False;reasons.append('contact icon/link mapping')
 if h.symbols:ok=False;reasons.append('inline symbol definition')
 if any(u.startswith('assets/') or u.startswith('../assets/') for u in h.uses):ok=False;reasons.append('relative sprite')
 print(f"{'PASS' if ok else 'FAIL'} | /{p.relative_to(ROOT)} | {'; '.join(sorted(set(reasons))) if reasons else 'footer/menu/contact and sprite'}")
 if not ok:fail+=1
# Global sprite XML validity and expected symbol IDs.
try:
 import subprocess
 subprocess.run(['xmllint','--noout',str(ROOT/'assets/icons/sprite.svg')],check=True,capture_output=True)
 text=(ROOT/'assets/icons/sprite.svg').read_text();ids=set(re.findall(r'<symbol\s+id="([^"]+)"',text));ok=set(SYMBOLS)<=ids and all(re.search(r'<symbol\s+id="'+re.escape(i)+r'"[^>]*viewBox="[^"]+"[^>]*fill="currentColor"',text) for i in SYMBOLS)
 print(f"{'PASS' if ok else 'FAIL'} | sprite.svg XML + symbols | {', '.join(sorted(ids))}")
 if not ok:fail+=1
except Exception as e:print('FAIL | sprite.svg XML |',e);fail+=1
# Source-level forbidden rules among the shared link-row definitions.
css='\n'.join(p.read_text() for p in (ROOT/'css').glob('*.css'))
checks={
 'anywhere-wrap on shared rows': not bool(re.search(r'(?:row-copy|social-copy|route-links|next-page|\.soc)[^{}]*\{[^}]*overflow-wrap\s*:\s*anywhere',css,re.S)),
 'break-all/break-word on shared rows': not bool(re.search(r'(?:row-copy|social-copy|route-links|next-page|\.soc)[^{}]*\{[^}]*word-break\s*:\s*(?:break-all|break-word)',css,re.S)),
 'row-copy constrained width/max-width': all((prop=='width' and value.strip()=='auto') or (prop=='max-width' and value.strip()=='none') for block in re.findall(r'([^{}]*\.row-copy[^{}]*)\{([^}]*)\}',css,re.S) for prop,value in re.findall(r'(?<!-)(width|max-width)\s*:\s*([^;]+)',block[1])),
 'grid columns on shared row anchors': not bool(re.search(r'(?:route-links|next-page|\.soc|menu-links a|project-footer|project-live|technology-teaser)[^{}]*\{[^}]*grid-template-columns',css,re.S)),
 'shared rows are flex with end-pinned chips': all(x in css for x in ('.soc>a,.route-links>a,.next-page>a,.affordance-list>a{display:flex', 'margin-left:auto;width:48px;height:48px', '.project-footer{display:flex', '.menu-links a{display:flex')),
 'no absolute-positioned chips in row selectors': not bool(re.search(r'(?:route-links|next-page|\.soc|project-live|technology-teaser)[^{}]*::after[^{}]*\{[^}]*position\s*:\s*absolute',css,re.S)),
 'desktop row width and title scale': '@media(min-width:1024px){.soc>a,.route-links>a,.next-page>a,.affordance-list>a{max-width:880px}' in css and 'font-size:clamp(22px,2.2vw,30px)' in css,
 'contact/footer/menu icon dimensions': '.row-ico{flex:none;width:48px;height:48px' in css and 'width:44px;height:44px;min-width:44px;min-height:44px' in css,
 'language-specific row CSS': not bool(re.search(r'(?:html\[lang=["\'](?:uz|ru)|\.(?:uz|ru)\b)[^{}]*(?:route-links|next-page|row-copy|social-copy|\.soc)',css,re.I)),
}
print('\nCSS STATIC SCAN')
for name,ok in checks.items():print(f"{'PASS' if ok else 'FAIL'} | {name}")
fail+=sum(not x for x in checks.values())
# Narrow-screen title/action token check. The 12px-per-glyph estimate is intentionally conservative.
longest=(0,'','')
for p,h in parsed.items():
 for n in descendants(h.root):
  if n.tag=='strong' or 'row-action-label' in n.attrs.get('class','').split() or n.tag=='em':
   for word in re.findall(r'[^\W_]+',n.text,re.UNICODE):
    if len(word)>longest[0]:longest=(len(word),word,'/'+str(p.relative_to(ROOT)))
stress_ok=longest[0]*12<=198
print(f"TEXT WIDTH STRESS | {'PASS' if stress_ok else 'FAIL'} | longest token {longest[1]!r} ({longest[0]} chars ≈ {longest[0]*12}px at 12px/glyph), 198px provided budget | {longest[2]}")
fail+=not stress_ok
print(f"\nRESULT: {'PASS' if not fail else 'FAIL'} — {len(pages)} pages scanned, {fail} failures")
sys.exit(bool(fail))
