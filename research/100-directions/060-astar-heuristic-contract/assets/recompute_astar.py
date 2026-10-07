"""Four-node teaching example; standard library only. No performance claims."""
from heapq import heappop, heappush
from itertools import count
import json, pathlib, sys
G={'S':[('A',2),('B',1)],'A':[('G',2)],'B':[('A',.5),('G',100)],'G':[]}
H={'inconsistent':{'S':3.5,'A':0,'B':2.5,'G':0},'zero':dict.fromkeys(G,0),'consistent':{'S':1.5,'A':0,'B':.5,'G':0}}
def search(h,reopen):
 serial=count();q=[(h['S'],next(serial),'S',0,('S',))];best={'S':0};closed=set();trace=[]
 while q:
  f,_,u,g,path=heappop(q)
  if g != best[u]:continue
  if u in closed and not reopen:continue
  trace.append({'node':u,'g':g,'h':h[u],'f':f,'path':list(path)})
  if u=='G':return {'cost':g,'path':list(path),'trace':trace}
  closed.add(u)
  for v,c in G[u]:
   if v in closed and not reopen:continue
   ng=g+c
   if ng < best.get(v,float('inf')):
    best[v]=ng;heappush(q,(ng+h[v],next(serial),v,ng,path+(v,)))
 raise AssertionError('unreachable')
out={}
for name,reopen in [('inconsistent',False),('inconsistent',True),('zero',False),('consistent',False)]:out[f'{name}_reopen_{reopen}']=search(H[name],reopen)
assert [x['cost'] for x in out.values()]==[4,3.5,3.5,3.5]
assert [x['node'] for x in out['inconsistent_reopen_True']['trace']]==['S','A','B','A','G']
for u,edges in G.items():
 for v,c in edges:assert H['consistent'][u]<=c+H['consistent'][v]
# Exhaustive simple paths independently verify optimum (positive-edge finite graph).
def paths(u,path=(),cost=0):
 if u=='G':yield cost,path+(u,);return
 for v,c in G[u]:
  if v not in path:yield from paths(v,path+(u,),cost+c)
out['all_simple_paths']=[{'cost':c,'path':list(p)} for c,p in paths('S')]
assert min(x['cost'] for x in out['all_simple_paths'])==3.5
out['runtime']={'python':sys.version.split()[0],'purpose':'deterministic didactic correctness checks; not a benchmark'}
p=pathlib.Path(__file__).resolve().parent/'060-recomputed.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2));print(p);print(json.dumps(out,ensure_ascii=False,indent=2))
