// Chạy trong tab https://www.youtube.com/@SOLVERALOGISTICS/videos (trình duyệt trong app). Thay KNOWN bằng mảng id đã đăng trên web.
(async()=>{
const KNOWN=[/*IDS*/];
await new Promise(r=>setTimeout(r,2500)); for(let i=0;i<8;i++){window.scrollTo(0,document.documentElement.scrollHeight); await new Promise(r=>setTimeout(r,1200));}
const m=new Map(); document.querySelectorAll('a[href*="/watch?v="]').forEach(a=>{const x=a.href.match(/v=([\w-]{11})/); if(!x||KNOWN.includes(x[1])) return; const t=(a.getAttribute('title')||a.getAttribute('aria-label')||a.innerText||'').trim().replace(/\s+/g,' '); if(!m.has(x[1])||t.length>m.get(x[1]).length) m.set(x[1],t);});
let vids=[],desc=[];
for(const [id,t] of m){ const h=await (await fetch('/watch?v='+id)).text(); const s=h.match(/"shortDescription":"((?:[^"\\]|\\.)*)"/); const d=h.match(/"publishDate":"([^"]+)"/); const ti=h.match(/<meta name="title" content="([^"]*)"/); let tx=s?JSON.parse('"'+s[1]+'"'):''; let i=tx.search(/-{4,}\/\/\/|📞 Contact Us/); if(i>=0) tx=tx.slice(0,i); tx=tx.split('\n').filter(l=>!l.trim().startsWith('#')).join('\n').trim();
 vids.push(id+'|'+(ti?ti[1]:t).replace(/&amp;/g,'&').replace(/&#39;/g,"'")); desc.push('@@'+id+'|'+(d?d[1].slice(0,10):'')+'\n'+tx); }
return {n:m.size, videos:vids.join('\n'), desc:desc.join('\n')};
})()
