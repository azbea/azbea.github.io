(() => {
  const trigger=document.querySelector('[data-menu-trigger]');
  const overlay=document.querySelector('[data-menu-overlay]');
  const closeButton=document.querySelector('[data-menu-close]');
  const main=document.querySelector('main');
  const header=document.querySelector('.site-header');
  if(!trigger||!overlay||!closeButton)return;
  const labels={en:{open:'Open navigation menu',close:'Close navigation menu'},uz:{open:'Navigatsiya menyusini ochish',close:'Navigatsiya menyusini yopish'},ru:{open:'Открыть меню навигации',close:'Закрыть меню навигации'}}[document.documentElement.lang]||{open:'Open navigation menu',close:'Close navigation menu'};
  let restoreFocus=null,previousOverflow='',previousPadding='',inertWasSet=false,headerWasInert=false;
  const focusable=()=>[...overlay.querySelectorAll('a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"])')].filter(el=>!el.hidden&&el.getClientRects().length);
  function open(){
    if(overlay.classList.contains('is-open'))return;
    restoreFocus=document.activeElement;previousOverflow=document.body.style.overflow;previousPadding=document.body.style.paddingRight;
    const gap=Math.max(0,innerWidth-document.documentElement.clientWidth);
    if(gap)document.body.style.paddingRight=`${gap}px`;
    document.body.style.overflow='hidden';
    if(main){inertWasSet=main.inert;main.inert=true;}
    if(header){headerWasInert=header.inert;header.inert=true;}
    overlay.inert=false;overlay.setAttribute('aria-hidden','false');overlay.classList.add('is-open');
    trigger.setAttribute('aria-expanded','true');trigger.setAttribute('aria-label',labels.close);
    document.dispatchEvent(new Event('site-menu-open'));closeButton.focus();
  }
  function close(){
    if(!overlay.classList.contains('is-open'))return;
    overlay.classList.remove('is-open');overlay.inert=true;overlay.setAttribute('aria-hidden','true');
    trigger.setAttribute('aria-expanded','false');trigger.setAttribute('aria-label',labels.open);
    document.body.style.overflow=previousOverflow;document.body.style.paddingRight=previousPadding;
    if(main)main.inert=inertWasSet;
    if(header)header.inert=headerWasInert;
    document.dispatchEvent(new Event('site-menu-close'));
    if(restoreFocus&&typeof restoreFocus.focus==='function')restoreFocus.focus();
  }
  trigger.addEventListener('click',()=>overlay.classList.contains('is-open')?close():open());
  closeButton.addEventListener('click',close);
  overlay.querySelectorAll('a').forEach(link=>link.addEventListener('click',close));
  document.addEventListener('keydown',event=>{
    if(!overlay.classList.contains('is-open'))return;
    if(event.key==='Escape'){event.preventDefault();close();return;}
    if(event.key==='Tab'){
      const items=focusable();if(!items.length){event.preventDefault();closeButton.focus();return;}
      const first=items[0],last=items[items.length-1];
      if(event.shiftKey&&(document.activeElement===first||!overlay.contains(document.activeElement))){event.preventDefault();last.focus();}
      else if(!event.shiftKey&&(document.activeElement===last||!overlay.contains(document.activeElement))){event.preventDefault();first.focus();}
    }
  });
  overlay.addEventListener('click',event=>{if(event.target===overlay)close();});
})();
