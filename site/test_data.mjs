import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {LibraryData,routeGate} from './data.mjs';
import {search} from './search.mjs';
const index=JSON.parse(await readFile(new URL('../docs/catalog.json',import.meta.url)));
let active=0,peak=0,calls=0,failOnce=true;
const fake=async url=>{calls++;active++;peak=Math.max(peak,active);await new Promise(r=>setTimeout(r,url.includes('/search/')?2:1));active--;if(url===index.search[0]&&failOnce){failOnce=false;throw Error('injected network failure');}return {ok:true,json:async()=>JSON.parse(await readFile(new URL('../docs/'+url.replace(/^\.\//,''),import.meta.url)))};};
const lib=new LibraryData(index,fake);let items=await lib.metadata();assert.equal(items.length,116);assert.equal(calls,index.metadata.length);assert(items.every(d=>!d.html&&!d.toc&&d.text===''));
await assert.rejects(lib.fulltext(items,()=>{}));items=await lib.fulltext(items,()=>{});assert.equal(items.length,116);assert(peak<=4);
for(const d of items){assert(search(items,d.text.slice(0,40)).some(r=>r.doc.id===d.id),d.id);const full=await lib.article(d);assert(full.html&&full.toc.length);assert.equal(Array.from(d.text).length,d.textLength);}
const before=calls;await lib.fulltext(items,()=>{});assert.equal(calls,before);
const gate=routeGate(),first=gate.next(),second=gate.next();assert(!gate.current(first));assert(gate.current(second));
const ordered=new LibraryData({metadata:['m'],item_count:1,search:['slow','fast']},async url=>{if(url==='slow')await new Promise(r=>setTimeout(r,10));return {ok:true,json:async()=>url==='m'?{items:[{id:'x'}]}:{entries:[{id:'x',text:url==='slow'?'first':'second'}]}};});
assert.equal((await ordered.fulltext(await ordered.metadata(),()=>{}))[0].text,'firstsecond');
console.log('schema2:116 full-text searches/readers; metadata-only startup; <=4 concurrency; failure retry; cache; ordered assembly; route gate passed');
