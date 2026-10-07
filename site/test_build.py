import json,tempfile,unittest
from pathlib import Path
from build import build,convert,ROOT
class BuildTests(unittest.TestCase):
 def test_empty_and_selected(self):
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp);policy=p/'policy.json';policy.write_text('{"schema":1,"approved_items":[]}');out=p/'out';self.assertEqual(build(policy,out),[]);self.assertFalse((out/'files').exists())
   items=json.loads((ROOT/'manifest.json').read_text())['items'];selected=items[0];policy.write_text(json.dumps({'schema':1,'approved_items':[selected['path']]}));docs=build(policy,out);self.assertEqual(len(docs),1);self.assertIn(selected['title'],docs[0]['title']);self.assertFalse((out/'files'/items[1]['path']).exists());self.assertTrue(docs[0]['toc'])
   policy.write_text('{"schema":1,"approved_items":[]}');build(policy,out);self.assertFalse((out/'files').exists())
 def test_hostile_markdown(self):
  from build import SITE
  with tempfile.TemporaryDirectory(dir=SITE) as temp:
   source=Path(temp)/'evil.md';source.write_text('# Heading\n\n<script>alert(1)</script>\n\n[x](javascript:alert) ![x](https://tracker.example/a.png) [private](../../manifest.json)\n\n<a id="safe-anchor"></a>Kept text\n')
   html,text,toc=convert({'readableMarkdown':source.relative_to(ROOT).as_posix()},set())
   self.assertNotIn('<script',html);self.assertNotIn('href="javascript:',html);self.assertNotIn('src="https:',html);self.assertNotIn('href="../../manifest',html);self.assertIn('id="safe-anchor"',html);self.assertIn('Kept text',text)
 def test_unknown_fails(self):
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp);policy=p/'p.json';policy.write_text('{"schema":1,"approved_items":["not/real"]}')
   with self.assertRaises(ValueError):build(policy,p/'out')
 def test_unowned_output_fails(self):
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp);policy=p/'p.json';policy.write_text('{"schema":1,"approved_items":[]}');out=p/'out';out.mkdir()
   with self.assertRaises(ValueError):build(policy,out)
 def test_all_article_links_and_images(self):
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp);items=json.loads((ROOT/'manifest.json').read_text())['items'];policy=p/'p.json';policy.write_text(json.dumps({'schema':1,'approved_items':[x['path'] for x in items]}));docs=build(policy,p/'out');self.assertEqual(len(docs),len(items));self.assertIn('catalog.json?v=',(p/'out/app.js').read_text());self.assertIn('app.js?v=',(p/'out/index.html').read_text())
   index=json.loads((p/'out/catalog.json').read_text());self.assertEqual(index['schema'],2);self.assertEqual(index['item_count'],len(items))
   def read(url):return json.loads((p/'out'/url.removeprefix('./')).read_text())
   metadata=[item for url in index['metadata'] for item in read(url)['items']]
   self.assertEqual(len(metadata),len(docs));texts={d['id']:'' for d in docs}
   for url in index['search']:
    for entry in read(url)['entries']:texts[entry['id']]+=entry['text']
   byid={d['id']:d for d in docs}
   for meta in metadata:
    self.assertNotIn('html',meta);self.assertNotIn('text',meta)
    original=byid[meta['id']];article=read(meta['article'])
    self.assertEqual(''.join(read(url)['html'] for url in article['parts']),original['html'])
    self.assertEqual(article['toc'],original['toc']);self.assertEqual(texts[meta['id']],original['text'])
    self.assertEqual(meta['downloads'],original['downloads']);self.assertEqual(meta['textLength'],len(original['text']))
   import hashlib
   for part in (p/'out/data').rglob('*.json'):
    self.assertLessEqual(part.stat().st_size,200000);self.assertEqual(part.stem,hashlib.sha256(part.read_bytes()).hexdigest()[:24])
   self.assertLessEqual((p/'out/catalog.json').stat().st_size,200000)
   from html.parser import HTMLParser
   from urllib.parse import unquote
   class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
     for k,v in attrs:
      if k in ['href','src']:
       self.urls.append(v)
       if v.startswith('./files/'):assert (p/'out'/unquote(v.split('#')[0])).is_file(),v
      assert not k.lower().startswith('on'),(k,v)
    urls=[]
   index=json.loads((p/'out/catalog.json').read_text());self.assertEqual(index['schema'],2)
   for f in (p/'out/data').rglob('*.json'):self.assertLessEqual(f.stat().st_size,200000)
   self.assertLessEqual((p/'out/catalog.json').stat().st_size,200000)
   metadata=[d for u in index['metadata'] for d in json.loads((p/'out'/u).read_text())['items']]
   texts={}
   for u in index['search']:
    for e in json.loads((p/'out'/u).read_text())['entries']:texts[e['id']]=texts.get(e['id'],'')+e['text']
   for d,meta in zip(docs,metadata):
    self.assertNotIn('html',meta);self.assertNotIn('text',meta)
    article=json.loads((p/'out'/meta['article']).read_text());html=''.join(json.loads((p/'out'/u).read_text())['html']for u in article['parts'])
    self.assertEqual(html,d['html']);self.assertEqual(texts[d['id']],d['text']);self.assertEqual(article['toc'],d['toc'])
   for d in docs:
    q=Links();q.feed(d['html']);self.assertGreater(len(d['text']),200);self.assertNotIn('<script',d['html']);self.assertNotIn('javascript:',d['html']);self.assertTrue(d['toc'],d['id'])
if __name__=='__main__':unittest.main()
