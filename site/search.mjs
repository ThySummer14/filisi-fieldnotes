export const terms=q=>q.trim().toLocaleLowerCase().split(/\s+/u).filter(Boolean).slice(0,15);
export function search(items,q,category='全部') {
 const ts=terms(q);
 return items.filter(d=>category==='全部'||d.category===category).map(d=>{
  const title=d.title.toLocaleLowerCase(),summary=d.summary.toLocaleLowerCase(),body=d.text.toLocaleLowerCase();
  const all=title+' '+summary+' '+body;
  if(!ts.every(t=>all.includes(t)))return null;
  const score=ts.reduce((n,t)=>n+(title.includes(t)?10:0)+(summary.includes(t)?4:0)+(body.includes(t)?1:0),0);
  const hit=ts.length?Math.min(...ts.map(t=>body.indexOf(t)).filter(i=>i>=0)):Infinity;
  const snippet=Number.isFinite(hit)?(hit>45?'…':'')+d.text.slice(Math.max(0,hit-45),hit+125)+'…':d.summary;
  return {doc:d,score,snippet};
 }).filter(Boolean).sort((a,b)=>b.score-a.score||b.doc.date.localeCompare(a.doc.date)||a.doc.title.localeCompare(b.doc.title,'zh'));
}
export function segments(text,q){const ts=terms(q).sort((a,b)=>b.length-a.length);if(!ts.length)return [{text,hit:false}];const re=new RegExp(ts.map(t=>t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|'),'giu');let out=[],start=0;for(const m of text.matchAll(re)){if(m.index>start)out.push({text:text.slice(start,m.index),hit:false});out.push({text:m[0],hit:true});start=m.index+m[0].length;}if(start<text.length)out.push({text:text.slice(start),hit:false});return out;}
