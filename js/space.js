(() => {
  const canvas=document.getElementById('space');
  if(!canvas)return;
  const ctx=canvas.getContext('2d',{alpha:false,desynchronized:true});
  if(!ctx)return;
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  let width=0,height=0,dpr=1,stars=[],raf=0,active=!document.hidden,covered=false,lastFrame=0,scroll=0,scrollTarget=0,velocity=0;
  const lowPower=innerWidth<700||navigator.hardwareConcurrency&&navigator.hardwareConcurrency<=4;
  function resize(){dpr=Math.min(devicePixelRatio||1,lowPower?1.5:2);width=innerWidth;height=innerHeight;canvas.width=Math.round(width*dpr);canvas.height=Math.round(height*dpr);canvas.style.width=width+'px';canvas.style.height=height+'px';ctx.setTransform(dpr,0,0,dpr,0,0);}
  function seed(){const count=width<700?520:900;stars=Array.from({length:count},()=>({a:Math.random()*Math.PI*2,r:Math.pow(Math.random(),.6)*1.6+.05,z:Math.random(),ember:Math.random()<.22}));}
  function draw(time=0){ctx.clearRect(0,0,width,height);const focal=Math.min(width,height)*.9,ox=width/2,oy=height*.45,flow=scroll*.0011+(reduce?0:time*.00004),streak=reduce?0:Math.min(Math.abs(velocity)*.006,.22);for(const s of stars){let z=((s.z-flow)%1+1)%1;z=Math.max(z,.02);const radius=s.r*focal/(z*2.2+.15),x=ox+Math.cos(s.a)*radius,y=oy+Math.sin(s.a)*radius*.8,z2=Math.min(z+streak,1),radius2=s.r*focal/(z2*2.2+.15),x2=ox+Math.cos(s.a)*radius2,y2=oy+Math.sin(s.a)*radius2*.8,alpha=Math.min(1,(1-z)*1.3)*(s.ember?.95:.6),size=(1-z)*2.4+.3;ctx.strokeStyle=s.ember?`rgba(255,${150+Math.floor((1-z)*80)},70,${alpha})`:`rgba(235,235,255,${alpha*.8})`;ctx.lineWidth=size;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(x2,y2);ctx.lineTo(x,y);ctx.stroke();}}
  function tick(time){raf=0;if(!active||covered||document.hidden)return;const target=scrollTarget;velocity+=(target-scroll-velocity)*.12;scroll+=(target-scroll)*.12;window.__abbScrollVelocity=velocity;if(!reduce||!lastFrame)draw(time);lastFrame=time;if(!reduce)raf=requestAnimationFrame(tick);}
  function start(){if(active&&!covered&&!document.hidden&&!raf)raf=requestAnimationFrame(tick);}
  function stop(){if(raf){cancelAnimationFrame(raf);raf=0;}}
  function onScroll(){scrollTarget=scrollY;start();}
  function setCovered(value){covered=value;if(covered)stop();else start();}
  resize();seed();draw(0);start();addEventListener('resize',()=>{resize();seed();start();},{passive:true});addEventListener('scroll',onScroll,{passive:true});document.addEventListener('visibilitychange',()=>{active=!document.hidden;if(active)start();else stop();});document.addEventListener('site-menu-open',()=>setCovered(true));document.addEventListener('site-menu-close',()=>setCovered(false));
})();
