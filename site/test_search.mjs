import assert from 'node:assert/strict';
import {search,segments} from './search.mjs';
const docs=[{id:'a',title:'像素场景研究',summary:'天气与水',text:'这里讨论像素场景。雨后的水面出现倒影。',date:'2026-10-07',category:'设计'},{id:'b',title:'水面倒影',summary:'像素',text:'正文以及 <script>alert(1)</script> a.b [hi]',date:'2026-10-06',category:'研究'}];
assert.equal(search(docs,'倒影').length,2);assert.equal(search(docs,'雨后 水面')[0].doc.id,'a');assert.equal(search(docs,'像素','研究').length,1);assert.equal(search(docs,'nothing').length,0);assert.equal(search(docs,'').length,2);assert.equal(search(docs,'水面')[0].doc.id,'b');assert.deepEqual(segments('a.b axb','a.b').filter(x=>x.hit).map(x=>x.text),['a.b']);assert.equal(segments('<script>alert(1)</script>','script').filter(x=>x.hit).length,2);assert.equal(segments('中文搜索','中文')[0].text,'中文');assert.equal(search(docs,'[]').length,0);console.log('9 search assertions passed');
const tagged={id:'tag-check',title:'Sample',summary:'',text:'',date:'2026-10-07',category:'计算与系统',topic:'排序算法',tags:['特殊索引词']};
if(search([tagged],'特殊索引词').length!==1 || search([tagged],'排序算法','计算与系统').length!==1 || search([tagged],'','社会与自然').length!==0)throw Error('Topic/tag/category regression');
console.log('3 topic/tag/category assertions passed');
