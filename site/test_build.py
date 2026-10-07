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
   p=Path(temp);items=json.loads((ROOT/'manifest.json').read_text())['items'];policy=p/'p.json';policy.write_text(json.dumps({'schema':1,'approved_items':[x['path'] for x in items]}));docs=build(policy,p/'out');self.assertEqual(len(docs),13)
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
   for d in docs:
    q=Links();q.feed(d['html']);self.assertGreater(len(d['text']),200);self.assertNotIn('<script',d['html']);self.assertNotIn('javascript:',d['html']);self.assertTrue(d['toc'],d['id'])
if __name__=='__main__':unittest.main()
