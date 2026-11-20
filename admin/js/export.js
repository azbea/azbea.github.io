(() => {
 function download(name,data,type='application/json'){const blob=new Blob([typeof data==='string'?data:JSON.stringify(data,null,2)],{type}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
 function snippet(record){const title=AdminValidate.clean(record.title||record.name||record.institution||record.label,300),body=AdminValidate.clean(record.description||record.content||record.introduction,5000);return `<article class="glass-card"><h2>${AdminUI.escape(title)}</h2><p>${AdminUI.escape(body)}</p></article>`;}
 window.AdminExport={download,snippet};
})();
