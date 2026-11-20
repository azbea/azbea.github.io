(() => {
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduce)return;
  const $=s=>document.querySelector(s),hero=$('#hero'),heroIn=$('#heroIn'),orb=$('#orb'),rings=[$('#r1'),$('#r2'),$('#r3')].filter(Boolean),marquee=$('#mq'),tunnel=$('#journey'),cards=[...document.querySelectorAll('.card3d')],count=$('#count'),projects=[...document.querySelectorAll('.pc')],innerHero=document.querySelector('.inner-hero');
  let raf=0,paused=false,smoothedScroll=scrollY;
  const clamp=(x,min,max)=>Math.min(Math.max(x,min),max),smooth=x=>x*x*(3-2*x);
  function frame(){
    raf=0;if(paused||document.hidden)return;
    const currentScroll=scrollY,innerProgress=innerHero?clamp((innerHero.offsetHeight-innerHero.getBoundingClientRect().bottom)/Math.max(innerHero.offsetHeight,1),0,1):0,heroProgress=innerHero?innerProgress:clamp(currentScroll/Math.max(innerHeight,1),0,1.2),tunnelRect=tunnel?tunnel.getBoundingClientRect():null,tunnelHeight=tunnel?tunnel.offsetHeight:1,tunnelProgress=tunnel?clamp(-tunnelRect.top/Math.max(1,tunnelHeight-innerHeight),0,1):0,n=cards.length,raw=n>1?tunnelProgress*(n-1):0,fl=Math.min(Math.floor(raw),Math.max(n-2,0)),fr=raw-fl,pos=n>1?fl+(fr<.3?0:fr>.7?1:smooth((fr-.3)/.4)):0,projectRects=projects.map(el=>el.getBoundingClientRect());
    smoothedScroll+=(currentScroll-smoothedScroll)*.12;
    if(heroIn){if(innerHero){heroIn.style.transform=`translateZ(${-heroProgress*100}px) rotateX(${heroProgress*3}deg) translateY(${-heroProgress*18}px)`;heroIn.style.opacity=String(1-heroProgress*.45);}else{heroIn.style.transform=`translateZ(${-heroProgress*260}px) rotateX(${heroProgress*10}deg) translateY(${-heroProgress*60}px)`;heroIn.style.opacity=String(Math.max(0,1-heroProgress*1.15));}}
    if(orb)orb.style.transform=innerHero?`translate(-50%,calc(-50% + ${heroProgress*18}px)) scale(${1+heroProgress*.12})`:`translate(-50%,calc(-50% + ${smoothedScroll*.25}px)) scale(${1+heroProgress*.35})`;
    if(rings.length){if(innerHero){rings[0].style.transform=`translate(-50%,-50%) rotateX(${68-heroProgress*4}deg) rotateZ(${heroProgress*4}deg)`;}else{if(rings[0])rings[0].style.transform=`translate(-50%,-50%) rotateX(${68-heroProgress*20}deg) rotateZ(${smoothedScroll*.12}deg)`;if(rings[1])rings[1].style.transform=`translate(-50%,-50%) rotateX(${68+heroProgress*10}deg) rotateZ(${-smoothedScroll*.07}deg)`;if(rings[2])rings[2].style.transform=`translate(-50%,-50%) rotateX(${68-heroProgress*30}deg) rotateZ(${smoothedScroll*.2}deg)`;}}
    if(marquee)marquee.style.transform=`translateX(${-12-smoothedScroll*.03}%)`;
    if(cards.length){cards.forEach((card,i)=>{const d=i-pos,z=d>0?-d*900:-d*700,opacity=d>0?Math.max(0,1-d*.85):Math.max(0,1+d*1.4),rx=d*6,ry=d*-16,x=d*14;card.style.transform=`translate3d(${x}vw,${d*-6}vh,${z}px) rotateY(${ry}deg) rotateX(${rx}deg)`;card.style.opacity=String(opacity);card.style.filter=`blur(${Math.min(Math.abs(d)*3.5,8)}px)`;card.style.zIndex=String(10-Math.round(Math.abs(d)*10));});if(count)count.textContent=String(Math.min(n,Math.round(pos)+1)).padStart(2,'0');}
    projects.forEach((el,i)=>{const box=projectRects[i],k=clamp(1-(box.top-innerHeight*.35)/(innerHeight*.5),0,1);el.style.transform=`rotateX(${(1-k)*16}deg) rotateY(${(1-k)*-9}deg) translateZ(${-(1-k)*60}px)`;el.style.opacity=String(.25+k*.75);});
    if((heroIn||cards.length||projects.length)&&Math.abs(currentScroll-smoothedScroll)>.1)raf=requestAnimationFrame(frame);
  }
  function start(){if(!paused&&!document.hidden&&!raf)raf=requestAnimationFrame(frame);}
  function stop(){if(raf){cancelAnimationFrame(raf);raf=0;}}
  document.addEventListener('site-menu-open',()=>{paused=true;stop();});document.addEventListener('site-menu-close',()=>{paused=false;start();});document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();else start();});addEventListener('scroll',start,{passive:true});addEventListener('resize',start,{passive:true});start();
})();
