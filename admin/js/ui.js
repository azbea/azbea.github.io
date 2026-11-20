(() => {
 const toastEl=()=>document.getElementById('toast');let timer=0;
 function toast(message,action){const el=toastEl();if(!el)return;el.replaceChildren(document.createTextNode(message));if(action){const b=document.createElement('button');b.type='button';b.textContent=action.label;b.addEventListener('click',action.run,{once:true});el.append(' ',b);}el.classList.add('show');clearTimeout(timer);timer=setTimeout(()=>el.classList.remove('show'),8000);}
 function escape(value){return String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
 async function confirm(message,typed=false){const dialog=document.getElementById('confirm-dialog');document.getElementById('dialog-copy').textContent=message;const label=document.getElementById('typed-label'),input=document.getElementById('typed-confirm');label.hidden=!typed;input.value='';dialog.querySelector('[value="confirm"]').disabled=typed;input.oninput=()=>dialog.querySelector('[value="confirm"]').disabled=input.value!=='REPLACE';dialog.showModal();return new Promise(resolve=>{dialog.addEventListener('close',()=>resolve(dialog.returnValue==='confirm'&&(!typed||input.value==='REPLACE')),{once:true});});}
 function preview(container,content){container.replaceChildren(AdminValidate.sanitize(content));}
 window.AdminUI={toast,confirm,escape,preview};
})();
