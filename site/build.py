#!/usr/bin/env python3
"""Fail-closed static export. Only explicitly selected items and declared files leave archive."""
import argparse, json, re, shutil, subprocess, hashlib
from pathlib import Path
from urllib.parse import urlsplit, unquote, quote
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parent.parent
SITE=ROOT/'site'
CATEGORIES={'reading':'阅读与社会','game-design':'游戏设计','research':'跨题研究','motion':'影像与动态','portfolio':'作品档案','game-art':'像素与场景','fiction':'小说创作','design':'平面设计'}
def category(item):
    if item.get("category"):return item["category"]
    if item.get('series') == 'research-100-20261007':
        n=int(item['series_number'])
        return '感知与设计' if n<=34 else '计算与系统' if n<=67 else '社会与自然'
    return CATEGORIES.get(item['path'].split('/')[0],'其他')

class Text(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]; self.toc=[]; self.heading=None
    def handle_starttag(self,tag,attrs):
        if re.fullmatch('h[1-6]',tag): self.heading=[dict(attrs).get('id',''),'',int(tag[1])]
    def handle_data(self,data):
        self.parts.append(data)
        if self.heading is not None:self.heading[1]+=data
    def handle_endtag(self,tag):
        if self.heading and re.fullmatch('h[1-6]',tag):self.toc.append(self.heading);self.heading=None

def inside(path):
    p=(ROOT/path).resolve()
    if not p.is_relative_to(ROOT) or not p.is_file() or p.is_symlink():raise ValueError('Invalid declared file: '+str(path))
    return p

def convert(item, allowed):
    md=inside(item['readableMarkdown']).read_text()
    # Keep historical Word bookmark targets, while dropping all other raw HTML.
    md=re.sub(r'<a id="([\w-]+)"></a>',r'[]{#\1}',md)
    ast=json.loads(subprocess.check_output(['pandoc','-f','markdown+bracketed_spans-raw_html','-t','json'],input=md.encode()))
    parent=Path(item['readableMarkdown']).parent
    def walk(x):
        if isinstance(x,list):return [walk(v) for v in x]
        if not isinstance(x,dict):return x
        if x.get('t') in ['RawInline','RawBlock']:return {'t':'Str','c':''}
        if x.get('t') in ['Link','Image']:
            attr,label,target=x['c'];url,title=target; parts=urlsplit(url); safe=None
            if x['t']=='Link' and parts.scheme in ['https','http'] and parts.netloc:safe=url
            elif x['t']=='Link' and url.startswith('#'):safe=url
            elif not parts.scheme and not parts.netloc:
                resolved=(ROOT/parent/unquote(parts.path)).resolve()
                if resolved.is_relative_to(ROOT):
                    rel=resolved.relative_to(ROOT).as_posix()
                    if rel in allowed:safe='./files/'+quote(rel,safe='/')+(('#'+parts.fragment) if parts.fragment else '')
            if safe is None:return {'t':'Span','c':[['',[],[]],walk(label)]}
            x={'t':x['t'],'c':[['',[],[]],walk(label),[safe,title]]}
        return {k:walk(v) for k,v in x.items()}
    ast=walk(ast)
    html=subprocess.check_output(['pandoc','-f','json','-t','html5','--wrap=none'],input=json.dumps(ast).encode()).decode()
    parser=Text();parser.feed(html)
    return html,' '.join(parser.parts),[{'id':i,'title':t,'level':l} for i,t,l in parser.toc if i]

def build(policy,output):
    policy=json.loads(Path(policy).read_text())
    if policy.get('schema')!=1 or not isinstance(policy.get('approved_items'),list):raise ValueError('Explicit schema 1 approved_items list required')
    selected=policy['approved_items'];items=json.loads((ROOT/'manifest.json').read_text())['items']; byid={i['path']:i for i in items}
    if len(set(selected))!=len(selected) or set(selected)-byid.keys():raise ValueError('Unknown or duplicate item IDs')
    output=Path(output).resolve()
    if output==ROOT or output==SITE or output in ROOT.parents:raise ValueError('Unsafe output directory')
    # Never silently retain stale exported content after narrowing approval.
    if output.exists():
        if not (output/'.fieldnotes-build').exists():raise ValueError('Output exists without build ownership marker')
        shutil.rmtree(output)
    output.mkdir(parents=True);(output/'.fieldnotes-build').write_text('Generated static export\n');(output/'.nojekyll').touch()
    for f in ['index.html','style.css','app.js','search.mjs','data.mjs']:shutil.copyfile(SITE/f,output/f)
    docs=[]
    for key in selected:
        item=byid[key];declared=[item['readableMarkdown']]+([item['sources']] if item.get('sources') else [])+item.get('assets',[])+[f['path'] for f in item.get('originals',[])]
        allowed=set(declared)
        for p in allowed:
            src=inside(p);dst=output/'files'/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
        body,text,toc=convert(item,allowed)
        docs.append({'id':key,'title':item['title'],'category':category(item),'topic':item.get('topic',''),'tags':item.get('tags',[]),'summary':item.get('summary',''),'status':item.get('status',''),'date':item.get('archived_at',''),'text':text,'html':body,'toc':toc,'downloads':[{'name':f['original_name'],'url':'./files/'+quote(f['path'],safe='/'),'format':Path(f['path']).suffix[1:].upper()} for f in item.get('originals',[])],'sources':'./files/'+quote(item['sources'],safe='/') if item.get('sources') else None})
    # Content-addressed, bounded JSON resources: landing pages never fetch full bodies.
    limit=180_000
    def encoded(value):return json.dumps(value,ensure_ascii=False,separators=(',',':')).encode()
    def resource(kind,value):
        data=encoded(value)
        if len(data)>limit:raise ValueError('JSON resource exceeds byte budget: '+kind)
        digest=hashlib.sha256(data).hexdigest()[:24]
        path=Path('data')/kind/(digest+'.json');target=output/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        return './'+path.as_posix()
    def packed(kind,key,entries):
        urls=[];batch=[]
        for entry in entries:
            if batch and len(encoded({key:batch+[entry]}))>limit:
                urls.append(resource(kind,{key:batch}));batch=[]
            batch.append(entry)
        if batch:urls.append(resource(kind,{key:batch}))
        return urls
    metadata=[];search_entries=[]
    for d in docs:
        parts=[resource('body',{'html':d['html'][n:n+16000]}) for n in range(0,len(d['html']),16000)]
        article=resource('articles',{'parts':parts,'toc':d['toc']})
        metadata.append({**{k:v for k,v in d.items() if k not in ['html','text','toc']},'textLength':len(d['text']),'article':article})
        search_entries.extend({'id':d['id'],'text':d['text'][n:n+16000]} for n in range(0,len(d['text']),16000))
    index={'schema':2,'item_count':len(docs),'metadata':packed('metadata','items',metadata),'search':packed('search','entries',search_entries)}
    index_data=encoded(index)
    if len(index_data)>limit:raise ValueError('Catalog index exceeds byte budget')
    (output/'catalog.json').write_bytes(index_data)
    digest=hashlib.sha256(index_data+b''.join((SITE/f).read_bytes()for f in ['app.js','data.mjs','search.mjs'])).hexdigest()[:16]
    app=(output/'app.js').read_text().replace("fetch('./catalog.json'", "fetch('./catalog.json?v="+digest+"'")
    for module in ['search.mjs','data.mjs']:
        app=app.replace("'./"+module+"'", "'./"+module+"?v="+digest+"'")
    (output/'app.js').write_text(app)
    index_html=(output/'index.html').read_text().replace('src="./app.js"','src="./app.js?v='+digest+'"')
    (output/'index.html').write_text(index_html)
    (output/'export-audit.json').write_text(json.dumps({'approved_items':selected,'item_count':len(docs)},ensure_ascii=False,indent=2))
    print(f'Built {len(docs)} explicitly selected articles → {output}')
    return docs
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--policy',default=SITE/'publication.json');p.add_argument('--output',default=SITE/'dist');a=p.parse_args();build(a.policy,a.output)
