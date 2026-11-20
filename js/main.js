document.documentElement.classList.remove('no-js');
document.documentElement.classList.add('js');

const revealItems=document.querySelectorAll('[data-reveal]');
if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
  const revealObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{
    if(entry.isIntersecting){entry.target.classList.add('is-visible');revealObserver.unobserve(entry.target);}
  }),{threshold:.14});
  revealItems.forEach(item=>revealObserver.observe(item));
}else revealItems.forEach(item=>item.classList.add('is-visible'));
const sampleMode=new URLSearchParams(location.search).get('samples')==='1';
if(sampleMode)document.body.classList.add('show-samples');
