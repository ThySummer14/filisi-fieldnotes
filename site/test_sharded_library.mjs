import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {search} from './search.mjs';
const root=path.resolve(process.argv[2]||'../docs');
const read=u=>JSON.parse(fs.readFileSync(path.join(root,u),'utf8'));
const index=read('catalog.json');
const items=index.metadata.flatMap(u=>read(u).items).map(d=>({...d,text:''}));
const byid=new Map(items.map(d=>[d.id,d]));
for(const url of index.search)for(const e of read(url).entries)byid.get(e.id).text+=e.text;
for(const d of items){
 assert.equal(d.text.length>100,true,d.id);
 const probe=d.text.slice(250,285).trim();
 assert(search(items,probe).some(r=>r.doc.id===d.id),'Full text search missed '+d.id);
 const manifest=read(d.article);
 const html=manifest.parts.map(u=>read(u).html).join('');
 assert(html.length>100&&manifest.toc.length>0,d.id);
 for(const f of d.downloads)assert(fs.existsSync(path.join(root,decodeURIComponent(f.url))),f.url);
}
console.log(`${items.length} articles: sharded full-text search probes, body assembly and downloads pass`);
